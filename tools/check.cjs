const VM=require('scratch-vm');
const fs=require('fs');
(async()=>{
 const vm=new VM();
 const {ScratchStorage}=require('scratch-storage'); vm.attachStorage(new ScratchStorage());
 await vm.loadProject(fs.readFileSync(require('path').join(__dirname,'../dist/stack-flow.sb3')));
 const rt=vm.runtime; rt.currentStepTime=33; rt.turboMode=true; const t=rt.targets.find(t=>t.sprite.name=='Engine');
 const get=n=>t.variables[n].value;
 const set=(n,v)=>t.variables[n].value=v;
 function run(name){
  const b=Object.values(t.blocks._blocks).find(b=>b.opcode=='procedures_call'&&b.mutation.proccode==name);
  if(!b)throw Error('no call '+name);
  const id='test-'+name; t.blocks.createBlock({id,opcode:'procedures_call',next:null,parent:null,inputs:{},fields:{},topLevel:true,shadow:false,mutation:b.mutation});
  const th=rt._pushThread(id,t);
  let steps=0;
  while(th.status!==4 && steps++<10000)rt.sequencer.stepThreads();
  rt.threads=[];t.blocks.deleteBlock(id);
  if(steps>=10000)throw Error('procedure stuck '+name);
 }
 function assert(b,msg){if(!b)throw Error(msg);console.log('PASS',msg)}
 run('reset');
 assert(get('board').length==200,'200-cell board');
 assert(get('GAME OVER')==0,'spawn is legal');
 assert(new Set([get('piece'),...get('bag')]).size==7,'seven-bag contains every piece exactly once');
 const x=get('x');set('dx',-1);set('dy',0);run('move');assert(get('x')==x-1,'left input moves active piece');
 set('piece',2);set('rotation',0);set('y',0);set('x',0);set('dx',-1);run('move');assert(get('x')==0,'wall collision blocks movement');
 const p=get('piece');run('hold');assert(get('HOLD')==p&&get('can hold')==0,'hold swaps and prevents repeat hold');
 set('turn',1);run('rotate');assert(get('rotation')==1,'clockwise rotation');
 assert(get('SCORE')==5&&get('last rotation')==1,'successful rotation awards five points and records rotation');
 set('piece',4);set('x',3);set('y',18);set('rotation',0);run('lock');
 assert(get('board').filter(x=>Number(x)!==0).length==4,'locking writes four cells');
 assert(get('can hold')==1,'locking re-enables hold');
 run('reset');const board=get('board');for(let c=0;c<10;c++)board[190+c]=c==4||c==5?0:1;
 set('piece',4);set('x',3);set('y',18);set('rotation',0);run('lock');
 assert(get('LINES')==1&&get('SCORE')==100,'full row clears and scores');
 assert(get('board').length==200&&get('board').filter(x=>Number(x)!==0).length==2,'row clear preserves board and shifts remaining cells');
 // A completely blocked candidate must not award points or record a rotation.
 run('reset');set('piece',6);set('rotation',0);get('board').fill(1);set('turn',1);run('rotate');
 assert(get('SCORE')==0&&get('rotation')==0&&get('last rotation')==0,'failed rotation awards no points');
 // Vertical drops preserve the last rotation for a T-spin; lateral movement cancels it.
 run('reset');set('piece',6);set('x',3);set('y',4);set('turn',1);run('rotate');
 set('dx',0);set('dy',1);run('move');assert(get('last rotation')==1,'vertical drop preserves T-spin eligibility');
 set('dx',1);set('dy',0);run('move');assert(get('last rotation')==0,'successful lateral move cancels T-spin eligibility');
 set('last rotation',1);run('hold');assert(get('last rotation')==0,'hold clears rotation state');
 // A T at the floor has two blocked bottom corners. One upper corner makes three.
 function floorT({rotated=true,corner=true,level=1,single=false}={}) {
  run('reset');set('piece',6);set('x',3);set('y',18);set('rotation',0);set('last rotation',rotated?1:0);set('LEVEL',level);
  if(corner)get('board')[183]=1;
  if(single)for(let c=0;c<10;c++)if(c<3||c>5)get('board')[190+c]=1;
  run('lock');
 }
 floorT();assert(get('SCORE')==400&&get('LINES')==0,'three-corner rotated T lock awards a zero-line T-spin bonus');
 floorT({rotated:false});assert(get('SCORE')==0,'three occupied corners without a rotation do not score a T-spin');
 floorT({corner:false});assert(get('SCORE')==0,'two occupied corners do not score a T-spin');
 floorT({level:2});assert(get('SCORE')==800,'T-spin bonus scales with level');
 floorT({single:true});assert(get('SCORE')==800&&get('LINES')==1,'T-spin single awards its bonus instead of ordinary line-clear points');
 // A vertical I fills four bottom-row holes; all four original rows must animate.
 run('reset');for(let y=16;y<20;y++)for(let c=0;c<10;c++)get('board')[y*10+c]=c==4?0:1;
 set('piece',1);set('x',2);set('y',16);set('rotation',1);run('lock');
 assert(get('LINES')==4&&get('SCORE')==800,'four-line clear scores correctly');
 assert(get('board').length==200&&get('board').every(x=>Number(x)===0),'four-line clear leaves an empty 200-cell board');
 assert(JSON.stringify(get('clear rows').map(Number))==='[19,18,17,16]','clear effect records all four original row positions');
 assert(Number(get('fx active'))===1&&Number(get('fx age'))===0,'line clear starts animation from frame zero');
 for(let frame=0;frame<24;frame++)run('render');
 assert(Number(get('fx active'))===0,'line-clear animation finishes and cannot remain stuck');
 run('reset');get('board').fill(1);run('spawn');assert(get('GAME OVER')==1,'blocked spawn ends game');
 console.log('Scratch VM loaded native project and completed gameplay checks.');
 vm.quit();
})().catch(e=>{console.error(e);process.exit(1)});
