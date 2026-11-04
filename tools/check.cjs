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
 const rotationsBefore=Number(get('lifetime rotations'));
 set('turn',1);run('rotate');assert(get('rotation')==1,'clockwise rotation');
 assert(get('SCORE')==5&&get('last rotation')==1,'successful rotation awards five points and records rotation');
 assert(Number(get('lifetime rotations'))===rotationsBefore+1,'successful rotations advance lifetime achievement progress');
 set('piece',4);set('x',3);set('y',18);set('rotation',0);run('lock');
 assert(get('board').filter(x=>Number(x)!==0).length==4,'locking writes four cells');
 assert(get('can hold')==1,'locking re-enables hold');
 run('reset');const board=get('board');for(let c=0;c<10;c++)board[190+c]=c==4||c==5?0:1;
 set('piece',4);set('x',3);set('y',18);set('rotation',0);run('lock');
 assert(get('LINES')==1&&get('SCORE')==100,'full row clears and scores');
 assert(get('board').length==200&&get('board').filter(x=>Number(x)!==0).length==2,'row clear preserves board and shifts remaining cells');
 // A completely blocked candidate must not award points or record a rotation.
 run('reset');set('piece',6);set('rotation',0);get('board').fill(1);set('turn',1);const blockedRotations=Number(get('lifetime rotations'));run('rotate');
 assert(get('SCORE')==0&&get('rotation')==0&&get('last rotation')==0,'failed rotation awards no points');
 assert(Number(get('lifetime rotations'))===blockedRotations,'blocked rotations do not fabricate achievement progress');
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
 set('SHAKE',20);let movedCamera=false;
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
 assert(stage.getCostumes().length===11&&new Set(stage.getCostumes().map(c=>c.assetId)).size===11,'all eleven background themes have distinct embedded artwork');
 const paletteIds=[];
 for(let theme=1;theme<=11;theme++){
  const themed=costumes.filter(c=>c.name.startsWith(`t${theme}-`));
  assert(themed.length===14,`theme ${theme} includes all seven block colors and seven ghost skins`);
  paletteIds.push(costumes.find(c=>c.name===`t${theme}-1`).assetId);
 }
 assert(new Set(paletteIds).size===11,'the eleven themes include distinct block palettes');
 set('THEME',1);set('SCORE',765);get('board')[199]=2;const themeBoard=JSON.stringify(get('board'));
 for(let step=0;step<11;step++){
  run('next theme');const expected=((step+1)%11)+1;
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
 const historyLists=['run ids','run scores','run lines','run combos','run themes','run status','run difficulties'];
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

 // Ambient effects and hover previews are presentation state: they must never
 // move a piece, consume the bag, award points or change a saved run.
 const presentationGuardNames=['board','bag','piece','x','y','rotation','HOLD','can hold','last rotation','SCORE','LINES','LEVEL','COMBO','combo expires','THEME','history page','has game','GAME OVER','run record open','run serial','run max combo','BEST SCORE',...historyLists];
 const presentationState=()=>JSON.stringify(presentationGuardNames.map(name=>get(name)));
 const beforePresentation=presentationState();
 const ambientNames=['ambient x','ambient y','ambient speed'];
 run('init ambient');
 assert(ambientNames.every(name=>get(name).length===24),'ambient initialization creates exactly twenty-four aligned particles');
 assert(get('ambient x').every(value=>Number.isFinite(Number(value))&&Number(value)>=-235&&Number(value)<=235)&&get('ambient y').every(value=>Number.isFinite(Number(value))&&Number(value)>=-175&&Number(value)<=175),'ambient particles start within the visible stage');
 assert(get('ambient speed').every(value=>Number.isFinite(Number(value))&&Number(value)>=0.15&&Number(value)<=0.6),'ambient particles have slow positive floating speeds');
 run('init ambient');run('init ambient');
 assert(ambientNames.every(name=>get(name).length===24),'reinitializing ambient particles replaces the field without accumulating clones');
 set('ambient x',Array.from({length:24},(_,i)=>-200+i*17));
 set('ambient y',Array(24).fill(0));set('ambient speed',Array(24).fill(0.5));
 get('ambient y')[0]=177.75;get('ambient y')[1]=-178;set('SCREEN','play');
 run('draw ambient');
 assert(Number(get('ambient y')[0])===-178,'ambient particles crossing the top wrap to the bottom');
 assert(Math.abs(Number(get('ambient y')[1])+177.5)<0.000001&&Math.abs(Number(get('ambient y')[2])-0.5)<0.000001,'ambient particles float upward at their own speed');
 assert(ambientNames.every(name=>get(name).length===24)&&get('ambient y').every(value=>Number(value)>=-178&&Number(value)<=178),'ambient animation retains a bounded, fixed-size particle field');
 for(const name of ambientNames){
  set(name,[]);run('draw ambient');
  assert(ambientNames.every(particleList=>get(particleList).length===24),'drawing repairs a missing '+name+' list after a restart');
 }
 assert(presentationState()===beforePresentation,'ambient initialization and animation preserve gameplay and saved history');

 const mouse=rt.ioDevices.mouse;
 function hoverAt(screen,canvasX,canvasY,expected,label){
  set('SCREEN',screen);mouse._scratchX=canvasX-240;mouse._scratchY=180-canvasY;
  run('update hover');
  assert(Number(get('hover object'))===expected,label);
  run('draw hover');
  assert(get('SCREEN')===screen,'hover preview keeps the '+screen+' screen open');
 }
 hoverAt('menu',120,130,1,'Play has a matching menu hover object');
 hoverAt('menu',120,177,2,'New Run has a matching menu hover object');
 hoverAt('menu',120,219,3,'Themes has a matching menu hover object');
 hoverAt('menu',120,261,4,'Run History has a matching menu hover object');
 hoverAt('menu',12,130,0,'moving away from menu actions clears the hover object');
 hoverAt('menu',120,155,0,'the gap between menu actions has no stale hover object');
 for(let theme=0;theme<11;theme++){
  hoverAt('themes',65+116*(theme%4),117+70*Math.floor(theme/4),11+theme,'theme '+(theme+1)+' has its own hover preview');
 }
 hoverAt('themes',50,28,5,'theme gallery Back has a navigation hover object');
 hoverAt('themes',123,117,0,'theme card gaps clear the previous theme preview');
 hoverAt('history',50,28,5,'history Back has a navigation hover object');
 hoverAt('history',146,302,6,'history Previous has a navigation hover object');
 hoverAt('history',334,302,7,'history Next has a navigation hover object');
 hoverAt('history',240,302,0,'the history pagination gap has no stale preview');
 hoverAt('play',120,130,0,'gameplay never shows a menu hover object');
 assert(presentationState()===beforePresentation,'hover detection and animated previews preserve the board, bag, score, combos and saved runs');
 set('SCREEN','menu');

 // Choosing a difficulty and browsing cosmetics must leave a paused run intact.
 const chooserState=presentationState();
 run('choose difficulty');
 assert(get('SCREEN')==='difficulty'&&presentationState()===chooserState,'Play opens the difficulty chooser without resetting a run or adding history');
 run('show cosmetics');
 assert(get('SCREEN')==='cosmetics'&&presentationState()===chooserState,'the dedicated Cosmetics menu preserves the current run and saved history');
 const startsBefore=[get('lifetime runs'),get('expert starts'),get('nightmare starts')].map(Number);
 for(const [difficulty,gravity,lock] of [[1,60,35],[2,35,25],[3,15,12],[4,8,8],[5,3,5]]){
  set('DIFFICULTY',difficulty);run('start game');
  assert(get('SCREEN')==='play'&&Number(get('gravity base'))===gravity&&Number(get('lock limit'))===lock&&Number(get('run difficulties')[0])===difficulty,'difficulty '+difficulty+' starts with its own timing and history label');
 }
 assert(Number(get('lifetime runs'))===startsBefore[0]+5&&Number(get('expert starts'))===startsBefore[1]+1&&Number(get('nightmare starts'))===startsBefore[2]+1,'confirmed runs advance lifetime and advanced-difficulty achievement progress');

 // Bee Swarm companions stay at the stage edge and never alter game state.
 const beeGuardNames=['board','bag','piece','x','y','rotation','SCORE','LINES','COMBO','run serial',...historyLists];
 const beeState=()=>JSON.stringify(beeGuardNames.map(name=>get(name)));
 set('THEME',11);
 for(const lines of [0,1,5,10,40]){
  set('LINES',lines);const before=beeState();run('draw bees');
  assert(Number(get('bee count'))===Math.min(lines,10),'Bee Swarm shows '+Math.min(lines,10)+' companions after '+lines+' lines');
  assert(beeState()===before,'bee animation preserves the board, score and history');
  if(lines>0)assert(Number.isFinite(Number(get('bee x')))&&Math.abs(Number(get('bee x')))>=200,'bee companions fly beyond the gameplay area');
 }
 set('THEME',1);const otherThemeBeeState=beeState();run('draw bees');
 assert(Number(get('bee count'))===0&&beeState()===otherThemeBeeState,'other themes hide bees without changing gameplay');
 set('COMBO',5);set('combo expires',clock.projectTimer()+4);const timerState=beeState();run('draw combo timer');
 assert(beeState()===timerState,'the large combo timer is presentation only');

 // Settings and progression are independent from per-run resets.
 run('init profile');
 set('SHAKE',0);set('shake ticks',10);run('update camera');assert(Number(get('shake x'))===0&&Number(get('shake y'))===0,'shake Off produces no camera offset');
 set('SHAKE',100);set('shake ticks',10);run('update camera');assert(Math.abs(Number(get('shake x')))===8&&Math.abs(Number(get('shake y')))<=4,'maximum shake is stronger and bounded at eight pixels');
 set('DIFFICULTY',1);run('apply difficulty');assert(Number(get('gravity base'))===60&&Number(get('lock limit'))===35,'Easy uses slower gravity and longer lock delay');
 set('DIFFICULTY',2);run('apply difficulty');assert(Number(get('gravity base'))===35&&Number(get('lock limit'))===25,'Normal preserves familiar timing');
 set('DIFFICULTY',3);run('apply difficulty');assert(Number(get('gravity base'))===15&&Number(get('lock limit'))===12,'Hard uses faster gravity and shorter lock delay');
 set('unlocked',Array(50).fill(0));set('BLOCK SKIN',4);set('AURA',2);run('validate cosmetics');assert(Number(get('BLOCK SKIN'))===1&&Number(get('AURA'))===0,'locked cosmetics cannot be equipped');
 const progressNames=['lifetime lines','lifetime quads','lifetime spins','run max combo','BEST SCORE','best combo','lifetime rotations','lifetime drops','lifetime runs','max bees','expert starts','nightmare starts','rainbow lines','beeswarm lines'];
 for(const name of progressNames)set(name,0);
 run('check achievements');
 assert(get('unlocked').length===50&&get('unlocked').every(x=>Number(x)===0),'all fifty achievements start locked when there is no progress');
 assert(get('achievement names').length===50&&new Set(get('achievement names').map(String)).size===50,'all fifty achievements have unique names');
 set('lifetime lines',1);run('check achievements');assert(Number(get('unlocked')[0])===1,'first line unlocks Ember blocks');
 set('lifetime lines',10);run('check achievements');assert(Number(get('unlocked')[1])===1,'ten lifetime lines unlock Frost blocks');
 set('run max combo',5);run('check achievements');assert(Number(get('unlocked')[2])===1,'five combo unlocks Prism blocks');
 set('lifetime quads',1);run('check achievements');assert(Number(get('unlocked')[3])===1,'a four-line clear unlocks Gold aura');
 set('lifetime spins',1);run('check achievements');assert(Number(get('unlocked')[4])===1,'a T-spin unlocks the Spin Artist title');
 set('BEST SCORE',5000);run('check achievements');assert(Number(get('unlocked')[5])===1,'five thousand points unlocks Rainbow aura');
 set('run max combo',0);set('lifetime lines',0);run('check achievements');assert(get('unlocked').slice(0,6).every(x=>Number(x)===1)&&Number(get('best combo'))===5,'earned achievements and lifetime peak combo survive run resets');
 set('BLOCK SKIN',4);set('AURA',2);run('validate cosmetics');assert(Number(get('BLOCK SKIN'))===4&&Number(get('AURA'))===2,'earned cosmetics can be equipped');
 for(const [choice,invalidValue,fallback] of [['CLEAR EFFECT',10,1],['BLOCK SKIN',9,1],['AURA',7,0]]){
  set(choice,invalidValue);run('validate cosmetics');assert(Number(get(choice))===fallback,'new locked '+choice.toLowerCase()+' cannot be equipped');
 }
 const unlockGuardNames=['SCORE','LINES','COMBO','THEME','CLEAR EFFECT','BLOCK SKIN','AURA',...progressNames,...historyLists];
 const beforeUnlock=JSON.stringify(unlockGuardNames.map(name=>get(name)));run('unlock all');
 assert(get('unlocked').length===50&&get('unlocked').every(x=>Number(x)===1),'U unlock procedure grants all fifty achievements');
 assert(JSON.stringify(unlockGuardNames.map(name=>get(name)))===beforeUnlock,'unlocking all cosmetics does not award points, fabricate history or change the selected cosmetics');
 for(const [choice,values] of [['CLEAR EFFECT',Array.from({length:10},(_,i)=>i+1)],['BLOCK SKIN',Array.from({length:9},(_,i)=>i+1)],['AURA',Array.from({length:8},(_,i)=>i)]]){
  for(const value of values){set(choice,value);run('validate cosmetics');assert(Number(get(choice))===value,'unlocked '+choice.toLowerCase()+' '+value+' can be selected');}
 }
 set('BLOCK SKIN',4);set('AURA',2);
 set('SHAKE',999);set('game r',-4);set('game g',999);set('key b',51.9);run('clamp settings');assert(Number(get('SHAKE'))===100&&Number(get('game r'))===0&&Number(get('game g'))===255&&Number(get('key b'))===51,'slider values are safely clamped to valid integer ranges');
 set('name draft','Nova_12!✨');run('sanitize name');assert(get('PLAYER NAME')==='Nova_12','name entry keeps supported letters and numbers');
 set('name draft','abcdefghijklmnop');run('sanitize name');assert(get('PLAYER NAME').length===12,'names are limited to twelve displayable characters');
 set('name draft','!!!');run('sanitize name');assert(get('PLAYER NAME')==='PLAYER','empty or unsupported names use a visible default');
 const colorNames=['game r','game g','game b','key r','key g','key b'];
 [12,90,210,255,42,90].forEach((value,index)=>set(colorNames[index],value));
 set('game custom',1);set('key custom',1);run('update rainbow');
 const drawnColorNames=['game draw r','game draw g','game draw b','key draw r','key draw g','key draw b'];
 assert(drawnColorNames.every((name,index)=>Number(get(name))===Number(get(colorNames[index]))),'solid accent and key colors use the exact chosen RGB values');
 const storedColors=JSON.stringify(colorNames.map(name=>get(name)));
 set('game custom',2);set('key custom',2);clock.projectTimer=()=>0;run('update rainbow');
 const rainbowStart=JSON.stringify(drawnColorNames.map(name=>get(name)));
 clock.projectTimer=()=>0.731;run('update rainbow');
 assert(JSON.stringify(drawnColorNames.map(name=>get(name)))!==rainbowStart&&drawnColorNames.every(name=>Number.isFinite(Number(get(name)))&&Number(get(name))>=0&&Number(get(name))<=255),'rainbow accent and key colors animate within valid RGB channels');
 assert(JSON.stringify(colorNames.map(name=>get(name)))===storedColors,'rainbow animation preserves the player’s saved solid RGB colors');
 clock.projectTimer=originalTimer;
 set('name draft','Nova_12');run('sanitize name');set('SHAKE',75);set('DIFFICULTY',5);set('CLEAR EFFECT',10);set('BEST SCORE',5432);
 run('checkpoint run');const profileHistory=JSON.stringify(historyLists.map(name=>get(name)));run('save profile');
 assert(get('saved profile').length===15&&Number(get('profile saved'))===1&&get('settings notice')==='saved','Save Profile commits a versioned snapshot and shows confirmation');
 const profileSnapshot=JSON.stringify(get('saved profile'));set('PLAYER NAME','Changed');set('SHAKE',0);set('DIFFICULTY',1);set('game r',0);set('BLOCK SKIN',1);run('load profile');
 assert(get('PLAYER NAME')==='Nova_12'&&Number(get('SHAKE'))===75&&Number(get('DIFFICULTY'))===5&&Number(get('CLEAR EFFECT'))===10,'Load Profile restores the saved name, Nightmare difficulty and expanded effect choice');
 assert(Number(get('game r'))===12&&Number(get('key r'))===255&&Number(get('game custom'))===2&&Number(get('key custom'))===2&&Number(get('BLOCK SKIN'))===4,'Load Profile restores stored RGB, rainbow modes and earned cosmetic choices');
 assert(JSON.stringify(historyLists.map(name=>get(name)))===profileHistory&&get('unlocked').every(x=>Number(x)===1),'loading settings preserves score history and unlocked rewards');
 set('key custom',1);run('update rainbow');set('settings tab',2);run('render settings');const rgbPen=t.getCustomState('Scratch.pen').penAttributes.color4f.slice(0,3).map(x=>Math.round(x*255));set('key custom',2);
 // Scratch converts RGB through HSV and can truncate a channel by one unit.
 assert(rgbPen.every((v,i)=>Math.abs(v-[255,42,90][i])<=1),'rendered RGB matches selected key channels within Scratch rounding');
 assert(costumes.filter(c=>c.name.startsWith('element')&&!c.name.startsWith('element spark')).length===100,'ten selectable clear effects each include ten animation frames');
 assert(costumes.filter(c=>c.name.startsWith('skin')).length===112,'eight earned skins include every block and ghost color');
 assert(costumes.filter(c=>c.name.startsWith('aura')).length===56,'seven earned auras include eight animation frames each');
 assert(costumes.filter(c=>/^achievement\d+-[01]$/.test(c.name)).length===100,'all fifty achievement cards include distinct locked and unlocked states');
 const beam=costumes.find(c=>c.name==='element5-0');
 assert(Boolean(beam)&&beam.rotationCenterX===80&&beam.rotationCenterY===16,'the expanded rainbow beam is centered on a full row and twice the normal height');
 const beamSvg=beam?Buffer.from(beam.asset.data).toString('utf8'):'';
 assert(/\bwidth=["']160["']/.test(beamSvg)&&/\bheight=["']32["']/.test(beamSvg),'rainbow clear artwork spans the complete 160-pixel row with a 32-pixel burst');
 for(let tab=1;tab<=3;tab++){
  set('cosmetics tab',tab);set('SCREEN','cosmetics');const before=beeState();run('render cosmetics');
  assert(get('SCREEN')==='cosmetics'&&Number(get('cosmetics tab'))===tab&&beeState()===before,'Cosmetics tab '+tab+' renders without affecting gameplay or history');
 }
 for(let page=0;page<=8;page++){
  set('achievement page',page);set('SCREEN','achievements');const before=beeState();run('render achievements');
  assert(Number(get('achievement page'))===page&&beeState()===before,'achievement page '+(page+1)+' renders without changing the current run');
 }
 // Saving the .sb3 must carry personal history into a fresh Scratch VM as well.
 const exportedProject=await vm.saveProjectSb3();
 const restoredVm=new VM();restoredVm.attachStorage(new ScratchStorage());
 await restoredVm.loadProject(Buffer.from(await exportedProject.arrayBuffer()));
 const restored=restoredVm.runtime.targets.find(target=>target.sprite.name==='Engine');
 assert(historyLists.every(name=>JSON.stringify(restored.variables[name].value)===JSON.stringify(get(name))),'saving and reloading the Scratch project preserves every run-history column');
 assert(Number(restored.variables['BEST SCORE'].value)===5432&&Number(restored.variables['run serial'].value)===Number(get('run serial')),'saved project reload preserves the lifetime best and next-run identifier');
 assert(JSON.stringify(restored.variables['saved profile'].value)===profileSnapshot&&restored.variables['PLAYER NAME'].value==='Nova_12','saved profile and typed name survive exporting and reopening the project');
 assert(restored.variables.unlocked.value.every(x=>Number(x)===1),'unlocked cosmetic achievements survive exporting and reopening the project');
 restoredVm.quit();
 console.log('Scratch VM loaded native project and completed gameplay checks.');
 vm.quit();
})().catch(e=>{console.error(e);process.exit(1)});
