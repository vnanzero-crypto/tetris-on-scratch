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
 set('SCREEN','play');for(let frame=0;frame<24;frame++)run('render');
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
 // Sidebar combo animation restarts on a clear, finishes, and stops on expiry.
 testTime=20;run('reset');singleClear();
 assert(Number(get('combo pulse'))===0&&Number(get('combo animating'))===1,'a clear starts the sidebar combo animation from frame zero');
 for(let frame=0;frame<24;frame++)run('draw combo');
 assert(Number(get('combo animating'))===0&&Number(get('combo pulse'))===24,'sidebar combo animation completes after twenty-four frames');
 assert(Number(get('COMBO'))===1,'finishing the combo animation does not erase the active combo count');
 testTime=21;singleClear();
 assert(Number(get('COMBO'))===2&&Number(get('combo pulse'))===0&&Number(get('combo animating'))===1,'another combo clear restarts the pulse with the incremented count');
 testTime=25.001;run('update combo');
 assert(Number(get('COMBO'))===0&&Number(get('combo animating'))===0,'combo timeout removes the count and its sidebar animation');
 // Opening the menu pauses an existing run without discarding its board or timer.
 testTime=20;run('start game');set('THEME',4);run('apply theme');singleClear();
 set('piece',6);set('x',3);set('y',5);set('rotation',2);set('SCORE',2345);
 const pausedState=JSON.stringify({board:get('board'),bag:get('bag'),piece:get('piece'),x:get('x'),y:get('y'),rotation:get('rotation'),score:get('SCORE'),theme:get('THEME')});
 assert(get('SCREEN')==='play'&&Number(get('has game'))===1,'starting a run enters play with an active game');
 testTime=21;run('open menu');
 assert(get('SCREEN')==='menu'&&Number(get('pause started'))===21,'menu records the real-clock pause time');
 assert(JSON.stringify({board:get('board'),bag:get('bag'),piece:get('piece'),x:get('x'),y:get('y'),rotation:get('rotation'),score:get('SCORE'),theme:get('THEME')})===pausedState,'opening the menu preserves the entire current run');
 assert(Number(get('combo expires'))===24&&Number(get('COMBO'))===1,'opening the menu preserves the current combo remaining time');
 testTime=24;run('open menu');assert(Number(get('pause started'))===21,'opening an already open menu does not replace the pause timestamp');
 testTime=31;run('resume game');
 assert(get('SCREEN')==='play'&&Number(get('has game'))===1,'resume returns an existing run to play');
 assert(Number(get('combo expires'))===34&&Number(get('COMBO'))===1,'resume shifts combo expiry by the paused duration');
 assert(JSON.stringify({board:get('board'),bag:get('bag'),piece:get('piece'),x:get('x'),y:get('y'),rotation:get('rotation'),score:get('SCORE'),theme:get('THEME')})===pausedState,'resuming restores the board, score, piece and selected theme');
 testTime=32;run('resume game');assert(Number(get('combo expires'))===34,'resuming an already playing run cannot extend the combo timer');
 testTime=34;run('update combo');assert(Number(get('COMBO'))===1,'resumed combo stays valid at its shifted exact deadline');
 testTime=34.001;run('update combo');assert(Number(get('COMBO'))===0,'resumed combo expires after its shifted deadline');
 run('open menu');set('THEME',5);run('start game');
 assert(get('SCREEN')==='play'&&Number(get('has game'))===1&&Number(get('SCORE'))===0&&Number(get('COMBO'))===0,'new run from the menu resets score and combo then starts play');
 assert(get('board').length===200&&get('board').every(x=>Number(x)===0)&&Number(get('THEME'))===5,'new run clears the board and retains the chosen menu theme');
 set('GAME OVER',1);run('open menu');run('resume game');
 assert(get('SCREEN')==='menu','a game-over run cannot be resumed from the main menu');
 set('has game',0);set('GAME OVER',0);run('resume game');
 assert(get('SCREEN')==='menu','resume cannot start a nonexistent run');
 clock.projectTimer=originalTimer;
 // Theme cycling changes the artwork, never the logical board or score.
 const stage=rt.targets.find(target=>target.isStage),costumes=t.getCostumes();
 assert(stage.getCostumes().length===10&&new Set(stage.getCostumes().map(c=>c.assetId)).size===10,'all ten background themes have distinct embedded artwork');
 const paletteIds=[];
 for(let theme=1;theme<=10;theme++){
  const themed=costumes.filter(c=>c.name.startsWith(`t${theme}-`));
  assert(themed.length===14,`theme ${theme} includes all seven block colors and seven ghost skins`);
  paletteIds.push(costumes.find(c=>c.name===`t${theme}-1`).assetId);
 }
 assert(new Set(paletteIds).size===10,'the ten themes include distinct block palettes');
 set('THEME',1);set('SCORE',765);get('board')[199]=2;const themeBoard=JSON.stringify(get('board'));
 for(let step=0;step<10;step++){
  run('next theme');const expected=((step+1)%10)+1;
  assert(Number(get('THEME'))===expected&&stage.getCostumes()[stage.currentCostume].name===`theme${expected}`,`theme cycle selects background ${expected}`);
  assert(Number(get('SCORE'))===765&&JSON.stringify(get('board'))===themeBoard,'theme changes preserve the board and score');
 }
 set('THEME',3);run('reset');assert(Number(get('THEME'))===3,'restarting preserves the selected visual theme');
 // Sprite size changes require a renderer; camera scale is checked by the browser suite.
 run('reset');set('COMBO',4);get('board').fill(1);run('spawn');assert(get('GAME OVER')==1,'blocked spawn ends game');
 assert(Number(get('COMBO'))===0,'game over clears the combo counter');

 // Every sidebar combo level through fifteen has an explicit named callout.
 const comboNames=get('combo names');
 assert(comboNames.length===15&&new Set(comboNames.map(String)).size===15,'all fifteen combo counts have distinct names');
 function comboName(n){return String(comboNames[n-1]).toUpperCase().replace(/\s+/g,' ')}
 assert(comboName(3)==='NICE!'&&comboName(5)==='GREAT!'&&comboName(7)==='CRAZY!','requested combo milestones are Nice, Great and Crazy');
 assert(comboName(15)==='BEYOND LIMITS!','fifteenth combo has the final milestone name');
 // History lives in ordinary Scratch lists, independent of transient board resets.
 const historyLists=['run ids','run scores','run lines','run combos','run themes','run status'];
 for(const name of historyLists)set(name,[]);
 set('run record open',0);set('run serial',0);set('BEST SCORE',0);set('has game',0);
 run('start game');set('THEME',7);set('SCORE',1234);set('LINES',12);set('run max combo',5);run('checkpoint run');
 assert(historyLists.every(name=>get(name).length===1),'starting a run creates one aligned row across every history list');
 assert(Number(get('run ids')[0])===1&&Number(get('run scores')[0])===1234&&Number(get('run lines')[0])===12&&Number(get('run combos')[0])===5&&Number(get('run themes')[0])===7,'live checkpoint saves score, lines, max combo and theme for the current run');
 assert(Number(get('BEST SCORE'))===1234,'checkpoint records the personal best score');
 run('open menu');assert(get('run status')[0]==='Paused'&&Number(get('run scores')[0])===1234,'pausing marks and checkpoints the live history row');
 run('resume game');assert(get('run status')[0]==='Playing','resuming updates the existing history row rather than adding a run');
 run('start game');
 assert(Number(get('run ids')[0])===2&&get('run status')[1]==='Restarted'&&Number(get('run scores')[1])===1234,'a new run archives the previous score and inserts a new latest row');
 assert(Number(get('BEST SCORE'))===1234&&Number(get('run scores')[0])===0,'a zero-score new run cannot erase a personal best');
 set('SCORE',2400);set('LINES',18);set('run max combo',7);run('checkpoint run');
 assert(Number(get('BEST SCORE'))===2400,'a higher score updates the personal best');
 set('finish reason','Ended');run('finish run');const finishedRows=JSON.stringify(historyLists.map(name=>get(name)));
 run('finish run');assert(Number(get('run record open'))===0&&JSON.stringify(historyLists.map(name=>get(name)))===finishedRows,'finishing an already archived run is idempotent');
 run('reset');assert(Number(get('BEST SCORE'))===2400&&JSON.stringify(historyLists.map(name=>get(name)))===finishedRows,'resetting board state never clears saved history or best score');
 // Maximum combo survives the four-second chain ending, then starts fresh per run.
 run('start game');set('COMBO',6);set('combo expires',999999);run('clear combo');run('checkpoint run');
 assert(Number(get('run max combo'))===7&&Number(get('run combos')[0])===7,'new combo milestones update the current run peak and its saved checkpoint');
 set('combo expires',-1);run('update combo');run('checkpoint run');
 assert(Number(get('COMBO'))===0&&Number(get('run max combo'))===7&&Number(get('run combos')[0])===7,'combo expiry preserves the run maximum for comparison');
 // Keep the newest twenty records with all columns still describing the same run.
 for(let i=0;i<25;i++){
  run('start game');set('SCORE',500+i*11);set('LINES',i);set('run max combo',i%15);set('THEME',1+i%10);run('checkpoint run');
 }
 assert(historyLists.every(name=>get(name).length===20),'history is capped at twenty equally sized lists');
 const ids=get('run ids').map(Number);
 assert(new Set(ids).size===20&&ids.every((id,i)=>i===0||id===ids[i-1]-1),'saved run identifiers remain unique and newest first after pruning');
 assert(Number(get('run scores')[0])===764&&Number(get('run lines')[0])===24&&Number(get('run combos')[0])===9&&Number(get('run themes')[0])===5,'latest retained history columns remain aligned');
 assert(Number(get('run scores')[19])===555&&Number(get('run lines')[19])===5&&Number(get('run combos')[19])===5&&Number(get('run themes')[19])===6,'oldest retained history columns remain aligned after pruning');
 assert(Number(get('BEST SCORE'))===2400,'pruning lower-score runs never lowers the lifetime best');
 run('start game');set('SCORE',4321);set('LINES',22);set('run max combo',8);get('board').fill(1);run('spawn');
 assert(get('GAME OVER')==1&&get('run status')[0]==='Game Over'&&Number(get('run scores')[0])===4321&&Number(get('run record open'))===0,'topping out saves the latest run once as Game Over');
 // Stop preserves the last live checkpoint; green flag archives it without duplication.
 run('start game');set('SCORE',5432);set('LINES',25);set('run max combo',9);run('checkpoint run');
 const stopId=Number(get('run ids')[0]),stopCount=get('run ids').length;
 vm.stopAll();
 assert(Number(get('run scores')[0])===5432&&Number(get('BEST SCORE'))===5432,'the Stop action retains the live score and personal best');
 vm.greenFlag();
 for(let step=0;step<100;step++){
  rt.redrawRequested=false;rt.sequencer.stepThreads();
  if(get('SCREEN')==='menu'&&Number(get('has game'))===0&&Number(get('run record open'))===0)break;
 }
 vm.stopAll();
 assert(get('SCREEN')==='menu'&&Number(get('run scores')[0])===5432&&Number(get('run ids')[0])===stopId&&get('run ids').length===stopCount,'green-flag startup preserves the stopped run without adding a duplicate');
 assert(get('run status')[0]==='Stopped'&&Number(get('BEST SCORE'))===5432,'green-flag startup labels the interrupted run Stopped and preserves the lifetime best');

 // Saving the .sb3 must carry personal history into a fresh Scratch VM as well.
 const exportedProject=await vm.saveProjectSb3();
 const restoredVm=new VM();restoredVm.attachStorage(new ScratchStorage());
 await restoredVm.loadProject(Buffer.from(await exportedProject.arrayBuffer()));
 const restored=restoredVm.runtime.targets.find(target=>target.sprite.name==='Engine');
 assert(historyLists.every(name=>JSON.stringify(restored.variables[name].value)===JSON.stringify(get(name))),'saving and reloading the Scratch project preserves every run-history column');
 assert(Number(restored.variables['BEST SCORE'].value)===5432&&Number(restored.variables['run serial'].value)===Number(get('run serial')),'saved project reload preserves the lifetime best and next-run identifier');
 restoredVm.quit();
 console.log('Scratch VM loaded native project and completed gameplay checks.');
 vm.quit();
})().catch(e=>{console.error(e);process.exit(1)});
