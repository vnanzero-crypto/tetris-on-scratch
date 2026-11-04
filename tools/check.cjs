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
 // Control Scratch's project clock so combo boundaries are tested without sleeps.
 const clock=rt.ioDevices.clock,originalTimer=clock.projectTimer;
 let testTime=10;clock.projectTimer=()=>testTime;
 function singleClear() {
  get('board').fill(0);for(let c=0;c<10;c++)if(c!==4&&c!==5)get('board')[190+c]=1;
  set('piece',4);set('x',3);set('y',18);set('rotation',0);set('last rotation',0);run('lock');
 }
 run('reset');singleClear();
 assert(Number(get('COMBO'))===1&&Number(get('combo bonus'))===0&&Number(get('SCORE'))===100,'first clear starts combo at one without an extra bonus');
 assert(Number(get('combo expires'))===14,'combo window expires four seconds after the latest clear');
 assert(Number(get('shake ticks'))===10,'line clear starts a short camera shake');
 let movedCamera=false;
 for(let frame=0;frame<11;frame++){
  run('update camera');const sx=Number(get('shake x')),sy=Number(get('shake y'));
  assert(Math.abs(sx)<=2&&Math.abs(sy)<=2,`camera shake stays within two pixels on frame ${frame}`);
  movedCamera=movedCamera||sx!==0||sy!==0;
 }
 assert(movedCamera,'clear shake produces a visible camera offset');
 assert(Number(get('shake ticks'))===0&&Number(get('shake x'))===0&&Number(get('shake y'))===0,'camera settles at the origin after the shake');
 testTime=14;run('update combo');assert(Number(get('COMBO'))===1,'combo remains active at the exact four-second boundary');
 singleClear();assert(Number(get('COMBO'))===2&&Number(get('combo bonus'))===50&&Number(get('SCORE'))===250,'second clear in the window increments combo and awards fifty bonus points');
 assert(Number(get('combo expires'))===18,'each clear refreshes the four-second combo window');
 testTime=15;get('board').fill(0);set('piece',4);set('x',3);set('y',18);set('rotation',0);set('last rotation',0);run('lock');
 assert(Number(get('COMBO'))===2&&Number(get('SCORE'))===250,'a non-clearing lock preserves the active timed combo and score');
 testTime=18.001;run('update combo');assert(Number(get('COMBO'))===0,'combo expires immediately after the four-second window');
 testTime=19;singleClear();assert(Number(get('COMBO'))===1&&Number(get('SCORE'))===350,'a clear after timeout starts a new combo without carrying the old bonus');
 testTime=20;set('LEVEL',3);const scoreBefore=Number(get('SCORE'));singleClear();
 assert(Number(get('COMBO'))===2&&Number(get('combo bonus'))===150&&Number(get('SCORE'))-scoreBefore===450,'combo bonus scales with the level and adds to normal clear points');
 run('reset');assert(Number(get('COMBO'))===0&&Number(get('shake ticks'))===0,'restart clears combo and camera shake');
 get('board').fill(0);set('piece',4);set('x',3);set('y',18);set('rotation',0);set('last rotation',0);run('lock');
 assert(Number(get('shake ticks'))===0,'a lock without a line clear does not trigger shake');
 clock.projectTimer=originalTimer;
 // Theme cycling changes the artwork, never the logical board or score.
 const stage=rt.targets.find(target=>target.isStage),costumes=t.getCostumes();
 assert(stage.getCostumes().length===5&&new Set(stage.getCostumes().map(c=>c.assetId)).size===5,'all five background themes have distinct embedded artwork');
 const paletteIds=[];
 for(let theme=1;theme<=5;theme++){
  const themed=costumes.filter(c=>c.name.startsWith(`t${theme}-`));
  assert(themed.length===14,`theme ${theme} includes all seven block colors and seven ghost skins`);
  paletteIds.push(costumes.find(c=>c.name===`t${theme}-1`).assetId);
 }
 assert(new Set(paletteIds).size===5,'the five themes include distinct block palettes');
 set('THEME',1);set('SCORE',765);get('board')[199]=2;const themeBoard=JSON.stringify(get('board'));
 for(let step=0;step<5;step++){
  run('next theme');const expected=((step+1)%5)+1;
  assert(Number(get('THEME'))===expected&&stage.getCostumes()[stage.currentCostume].name===`theme${expected}`,`theme cycle selects background ${expected}`);
  assert(Number(get('SCORE'))===765&&JSON.stringify(get('board'))===themeBoard,'theme changes preserve the board and score');
 }
 set('THEME',3);run('reset');assert(Number(get('THEME'))===3,'restarting preserves the selected visual theme');
 // Sprite size changes require a renderer; camera scale is checked by the browser suite.
 run('reset');set('COMBO',4);get('board').fill(1);run('spawn');assert(get('GAME OVER')==1,'blocked spawn ends game');
 assert(Number(get('COMBO'))===0,'game over clears the combo counter');
 console.log('Scratch VM loaded native project and completed gameplay checks.');
 vm.quit();
})().catch(e=>{console.error(e);process.exit(1)});
