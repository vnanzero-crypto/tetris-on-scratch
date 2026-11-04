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
  const b=Object.values(t.blocks._blocks).find(b=>b.opcode=='procedures_call'&&b.mutation.proccode==name)
   ||Object.values(t.blocks._blocks).find(b=>b.opcode=='procedures_prototype'&&b.mutation.proccode==name);
  if(!b)throw Error('no call '+name);
  const id='test-'+name; t.blocks.createBlock({id,opcode:'procedures_call',next:null,parent:null,inputs:{},fields:{},topLevel:true,shadow:false,mutation:b.mutation});
  const th=rt._pushThread(id,t);
  let steps=0;
  while(th.status!==4 && steps++<10000)rt.sequencer.stepThreads();
  rt.threads=[];t.blocks.deleteBlock(id);
  if(steps>=10000)throw Error('procedure stuck '+name);
 }
 function assert(b,msg){if(!b)throw Error(msg);console.log('PASS',msg)}
 const total=list=>list.reduce((sum,value)=>sum+Number(value),0);
 const near=(actual,expected)=>Math.abs(Number(actual)-expected)<1e-6;
 function capturePen(draw){
  const segments=[],setXY=t.setXY;
  t.setXY=function(x,y,...args){
   const pen=this.getCustomState('Scratch.pen');
   if(pen?.penDown)segments.push({from:[this.x,this.y],to:[x,y],color:pen.penAttributes.color4f.slice(),diameter:pen.penAttributes.diameter});
   return setXY.call(this,x,y,...args);
  };
  try{draw()}finally{t.setXY=setXY}
  return segments;
 }
 function captureStamps(draw){
  const stamps=[],stamp=rt._primitives.pen_stamp;
  rt._primitives.pen_stamp=(args,util)=>{
   const target=util.target;
   stamps.push({name:target.getCostumes()[target.currentCostume].name,x:target.x,y:target.y,size:target.size});
   return stamp(args,util);
  };
  try{draw()}finally{rt._primitives.pen_stamp=stamp}
  return stamps;
 }
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
 assert(stage.getCostumes().length===12&&new Set(stage.getCostumes().map(c=>c.assetId)).size===12,'all twelve background themes have distinct embedded artwork');
 const paletteIds=[];
 for(let theme=1;theme<=12;theme++){
  const themed=costumes.filter(c=>c.name.startsWith(`t${theme}-`));
  assert(themed.length===14,`theme ${theme} includes all seven block colors and seven ghost skins`);
  paletteIds.push(costumes.find(c=>c.name===`t${theme}-1`).assetId);
 }
 assert(new Set(paletteIds).size===12,'the twelve themes include distinct block palettes');
 set('THEME',1);set('SCORE',765);get('board')[199]=2;const themeBoard=JSON.stringify(get('board'));
 for(let step=0;step<12;step++){
  run('next theme');const expected=((step+1)%12)+1;
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
 for(let theme=0;theme<12;theme++){
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
 // Compare the actual hover art with the new four-column layout. Checking the
 // pixels encoded in each SVG catches the old five-column outline regression.
 function firstRect(svg){
  const tag=svg.match(/<rect\b[^>]*>/)?.[0];
  return tag?['x','y','width','height'].map(n=>Number(tag.match(new RegExp('\\b'+n+'="([^"]+)"'))?.[1])):[];
 }
 for(let theme=0;theme<12;theme++){
  const c=costumes.find(c=>c.name==='outline'+(11+theme));
  const rect=c?firstRect(Buffer.from(c.asset.data).toString('utf8')):[];
  const expected=[11+116*(theme%4),85+70*Math.floor(theme/4),108,64];
  assert(JSON.stringify(rect)===JSON.stringify(expected),'theme '+(theme+1)+' hover outline follows its current gallery card');
 }
 // Expected visible controls, independent of the builder's hover catalogue.
 const buttons=[],button=(screen,tab,box,label)=>buttons.push([screen,tab,box,label]);
 for(const [box,label] of [
  [[32,112,246,150],'Play / Resume'],[[32,162,246,192],'New Run'],[[32,204,246,234],'Themes'],[[32,246,246,276],'Run History'],
  [[270,266,468,290],'Cosmetics'],[[270,300,358,328],'Settings'],[[364,300,468,328],'Achievements']])button('menu',0,box,label);
 button('play',0,[8,10,100,34],'Menu');button('themes',0,[16,16,100,42],'Back');
 const themeNames=['Galaxy','Mountains','Ocean','Sunset','Neon City','Black','Sakura','Volcano','Aurora','Blueprint','Beeswarm Sim Theme','Binding of Isaac'];
 themeNames.forEach((name,i)=>{const x=12+116*(i%4),y=86+70*Math.floor(i/4);button('themes',0,[x,y,x+106,y+62],name)});
 for(const [screen,y1,y2] of [['history',288,316],['achievements',306,334]]){
  button(screen,0,[16,16,100,42],'Back');button(screen,0,[96,y1,196,y2],'Previous');button(screen,0,[284,y1,384,y2],'Next');
 }
 const modes=['Easy','Normal','Hard','Expert','Nightmare'];
 button('difficulty',0,[16,16,100,42],'Back');modes.forEach((name,i)=>button('difficulty',0,[32,98+i*44,448,132+i*44],name));
 for(const [box,label] of [
  [[16,16,100,42],'Back'],[[112,16,198,42],'Clear tab'],[[202,16,288,42],'Blocks tab'],[[292,16,378,42],'Auras tab'],[[382,16,468,42],'Drops tab'],
  [[18,316,164,344],'RGB / Rainbow'],[[310,316,462,344],'Save Profile']])button('cosmetics',0,box,label);
 const dropNames=['White Line','Neon Pulse','Rainbow Beam','Flame Trail','Frost Stream','Void Rift'];
 const cosmeticNames=[['Normal','Fire','Water','Ice','Rainbow','Lightning','Void','Confetti','Honey','Galaxy'],['Classic','Ember','Frost','Prism','Neon Wire','Obsidian','Honeycomb','Plasma','Marble'],['None','Gold','Rainbow','Inferno','Tidal','Glacial','Nebula','Hive'],dropNames];
 cosmeticNames.forEach((names,tab)=>names.forEach((name,i)=>{const x=12+94*(i%5),y=100+100*Math.floor(i/5);button('cosmetics',tab+1,[x,y,x+82,y+82],name)}));
 for(const [box,label] of [[[16,16,100,42],'Back'],[[166,16,306,42],'General tab'],[[316,16,456,42],'RGB Colors tab'],[[310,316,462,344],'Save Profile']])button('settings',0,box,label);
 button('settings',1,[126,78,456,104],'Player name');modes.forEach((name,i)=>button('settings',1,[126+66*i,116,186+66*i,140],name));
 button('settings',1,[140,153,420,175],'Shake intensity');button('settings',1,[424,153,462,175],'Shake Off');button('settings',1,[126,214,456,252],'Cosmetics');
 for(const [title,offset] of [['Game accent',0],['Key highlight',120]])['R','G','B'].forEach((channel,i)=>{
  const y=112+30*i+offset;button('settings',2,[136,y-7,366,y+7],title+' '+channel+' slider');button('settings',2,[376,y-10,418,y+10],title+' '+channel+' value');
 });
 for(const [box,label] of [[[18,182,164,202],'Rainbow Accent'],[[174,316,296,344],'Rainbow Keys'],[[18,316,164,344],'Use Theme Colors']])button('settings',2,box,label);
 assert(buttons.length===101&&get('button labels').length===buttons.length,'all 101 interface controls have a native hover target');
 const buttonState=presentationState();
 for(let index=0;index<buttons.length;index++){
  const [screen,tab,[x1,y1,x2,y2],label]=buttons[index];
  set('SCREEN',screen);if(tab)set(screen==='settings'?'settings tab':'cosmetics tab',tab);
  mouse._scratchX=(x1+x2)/2-240;mouse._scratchY=180-(y1+y2)/2;
  run('update button hover');run('draw button hover');
  const glow=costumes.find(c=>c.name==='button glow'+(index+1));
  const rect=glow?firstRect(Buffer.from(glow.asset.data).toString('utf8')):[];
  assert(Number(get('button hovered'))===index+1&&String(get('button labels')[index])===label&&JSON.stringify(rect)===JSON.stringify([x1+.5,y1+.5,x2-x1-1,y2-y1-1]),screen+' / '+label+' lights up in its visible button bounds');
 }
 set('SCREEN','cosmetics');set('cosmetics tab',3);mouse._scratchX=429-240;mouse._scratchY=180-241;run('update button hover');
 assert(Number(get('button hovered'))===0,'hidden cosmetic cards do not retain the previous tab hover');
 set('SCREEN','settings');set('settings tab',1);mouse._scratchX=251-240;mouse._scratchY=180-112;run('update button hover');
 assert(Number(get('button hovered'))===0,'RGB slider hover targets are inactive on the General tab');
 set('SCREEN','themes');mouse._scratchX=123-240;mouse._scratchY=180-117;run('update button hover');
 assert(Number(get('button hovered'))===0,'gaps between theme cards clear button lighting');
 assert(presentationState()===buttonState,'lighting every interface control preserves gameplay, progression and run history');
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

 // Roaming companion counts and decorative rendering never alter game state.
 const beeGuardNames=['board','bag','piece','x','y','rotation','HOLD','can hold','last rotation','fall','ground ticks','gravity base','lock limit','LEVEL','SCORE','LINES','COMBO','combo expires','run max combo','run serial','BEST SCORE','unlocked','lifetime lines','lifetime spins','lifetime quads','lifetime rotations','lifetime drops','lifetime runs','rainbow lines','beeswarm lines',...historyLists];
 const beeState=()=>JSON.stringify(beeGuardNames.map(name=>get(name)));
 const safeCompanion=(x,y)=>Number.isFinite(Number(x))&&Number.isFinite(Number(y))&&Math.abs(Number(x))<=222&&Math.abs(Number(y))<=164&&(Math.abs(Number(x))>=96||Math.abs(Number(y))>=150);
 set('THEME',11);
 for(const lines of [0,1,5,10,40]){
  set('LINES',lines);const before=beeState();run('draw bees');
  assert(Number(get('bee count'))===Math.min(lines,10),'Bee Swarm shows '+Math.min(lines,10)+' companions after '+lines+' lines');
  assert(beeState()===before,'bee animation preserves the board, score and history');
  if(lines>0)assert(get('companion x').every((x,i)=>safeCompanion(x,get('companion y')[i])),'bee companions remain outside the protected gameplay rectangle');
 }
 set('THEME',1);const otherThemeBeeState=beeState();run('draw bees');
 assert(Number(get('bee count'))===0&&beeState()===otherThemeBeeState,'other themes hide bees without changing gameplay');
 set('THEME',12);
 for(const lines of [0,1,6,10,40]){
  set('LINES',lines);const before=beeState();run('draw companions');
  assert(Number(get('familiar count'))===Math.min(lines,10)&&Number(get('bee count'))===0,'Isaac theme shows '+Math.min(lines,10)+' familiars after '+lines+' lines');
  assert(beeState()===before,'familiar animation preserves board, score and history');
 }
 const companionLists=['companion x','companion y','companion vx','companion vy','companion turn'];
 run('init companions');
 assert(companionLists.every(n=>get(n).length===10)&&get('companion x').every((x,i)=>safeCompanion(x,get('companion y')[i])),'random flight initializes ten aligned companions outside gameplay');
 const initialPositions=get('companion x').map((x,i)=>[Number(x),Number(get('companion y')[i])]);
 const flightGuard=beeState();let safeFlight=true,roamedInward=false;const movedCompanions=new Set();
 for(let frame=0;frame<400;frame++)for(let index=1;index<=10;index++){
  set('companion index',index);run('step companion');
  const x=Number(get('companion x')[index-1]),y=Number(get('companion y')[index-1]);
  safeFlight&&=safeCompanion(x,y);roamedInward||=Math.abs(x)<190;
  if(Math.hypot(x-initialPositions[index-1][0],y-initialPositions[index-1][1])>1)movedCompanions.add(index);
 }
 assert(safeFlight,'four thousand flight steps remain on stage and avoid the protected gameplay rectangle');
 assert(roamedInward&&movedCompanions.size===10,'companions roam individually beyond the old fixed edge formation');
 assert(new Set(get('companion vx').map((x,i)=>x+','+get('companion vy')[i])).size>1,'different companions maintain different flight directions');
 assert(beeState()===flightGuard,'random flight never changes a piece, score, combo or saved run');
 function flightFixture(x,y,vx,vy){
  for(const [name,value] of [['companion x',x],['companion y',y],['companion vx',vx],['companion vy',vy],['companion turn',100]])get(name)[0]=value;
  set('companion index',1);run('step companion');
  return [Number(get('companion x')[0]),Number(get('companion y')[0])];
 }
 let flight=flightFixture(97,0,-2,0);
 assert(safeCompanion(...flight)&&flight[0]>=96,'sideways flight reflects before entering gameplay');
 flight=flightFixture(0,151,0,-2);
 assert(safeCompanion(...flight)&&flight[1]>=150,'vertical flight reflects before entering gameplay');
 flight=flightFixture(97,152,-2,0);
 assert(safeCompanion(...flight)&&flight[0]<96,'companions can cross above the board instead of staying in side lanes');
 flight=flightFixture(221,163,2,2);
 assert(safeCompanion(...flight),'corner flight reflects within the visible stage');

 // Ordinary Bee buffs retain their short lifetime. Chained clears add five
 // different held effects, which persist together for the entire combo.
 set('THEME',1);set('COMBO',0);run('reset bee buffs');run('grant bee buff');
 assert(get('buff stacks').length===12&&get('buff life').length===12&&get('combo buff stacks').length===12&&total(get('buff stacks'))===0&&total(get('combo buff stacks'))===0,'ordinary themes never receive the twelve Bee Swarm buffs');
 set('THEME',11);const buffGuard=beeState();run('grant bee buff');
 assert(total(get('buff stacks'))===1&&get('buff life').filter(x=>Number(x)===240).length===1&&total(get('combo buff stacks'))===0,'a first clear grants one random timed cosmetic buff');
 for(let i=0;i<1000;i++)run('grant bee buff');
 assert(get('buff stacks').every(x=>Number(x)>0&&Number(x)<=99)&&get('buff life').every(x=>Number(x)===240),'random drops can stack all twelve buff types within display limits');
 assert(beeState()===buffGuard,'gaining and stacking buffs never changes board, scoring, combo or history');
 set('buff stacks',[3,4,2,...Array(9).fill(0)]);set('buff life',[2,1,61,...Array(9).fill(0)]);run('draw bee buffs');
 assert(JSON.stringify(get('buff life').map(Number))===JSON.stringify([1,0,60,...Array(9).fill(0)])&&JSON.stringify(get('buff stacks').map(Number))===JSON.stringify([3,0,2,...Array(9).fill(0)]),'timed badges decay, fade and remove only their expired stacks');
 set('buff stacks',Array(12).fill(3));set('buff life',Array(12).fill(240));for(let frame=0;frame<240;frame++)run('draw bee buffs');
 assert(total(get('buff life'))===0&&total(get('buff stacks'))===0,'ordinary cosmetic badges disappear after their lifetime');
 clock.projectTimer=()=>testTime;testTime=100;run('reset');set('SCREEN','play');set('has game',1);singleClear();
 assert(Number(get('SCORE'))===100&&Number(get('LINES'))===1&&total(get('buff stacks'))===1&&total(get('combo buff stacks'))===0,'an actual first Bee Swarm clear grants one ordinary buff without changing scoring');
 const timedBeforeChain=JSON.stringify(get('buff stacks'));testTime=101;singleClear();
 assert(Number(get('COMBO'))===2&&total(get('combo buff stacks'))===5&&get('combo buff stacks').filter(x=>Number(x)===1).length===5,'the second clear grants exactly five distinct simultaneous combo effects');
 assert(JSON.stringify(get('buff stacks'))===timedBeforeChain,'a combo bundle adds held effects independently of the ordinary timed badge');
 const activeBuffKinds=get('combo buff stacks').flatMap((count,index)=>Number(count)>0?[index+1]:[]);
 const wisps=captureStamps(()=>run('draw combo wisps')).filter(stamp=>/^buff wisp\d+-/.test(stamp.name));
 const wispKinds=[...new Set(wisps.map(stamp=>Number(stamp.name.match(/^buff wisp(\d+)-/)[1])))].sort((a,b)=>a-b);
 assert(JSON.stringify(wispKinds)===JSON.stringify(activeBuffKinds)&&wisps.every(stamp=>Math.abs(stamp.x)>=108&&Math.abs(stamp.x)<214&&Math.abs(stamp.y)<=140),'five different combo effects render together around the protected playfield');
 const heldBeforeFrames=JSON.stringify(get('combo buff stacks')),heldGuard=beeState();
 for(let frame=0;frame<260;frame++)run('draw bee buffs');
 assert(JSON.stringify(get('combo buff stacks'))===heldBeforeFrames&&total(get('buff stacks'))===0,'combo effects outlive ordinary badge timers and stay active while the combo lives');
 assert(beeState()===heldGuard,'simultaneous held effects remain purely cosmetic');
 for(const at of [102,103]){testTime=at;singleClear()}
 assert(Number(get('COMBO'))===4&&total(get('combo buff stacks'))===15&&get('combo buff stacks').some(x=>Number(x)>1),'later chained clears add five effects each and stack repeated rolls');
 const beforeNoClear=JSON.stringify(get('combo buff stacks'));
 get('board').fill(0);set('piece',4);set('x',3);set('y',18);set('rotation',0);run('lock');
 assert(JSON.stringify(get('combo buff stacks'))===beforeNoClear,'a non-clearing placement grants no combo effects');
 testTime=104;run('open menu');const heldPaused=JSON.stringify(get('combo buff stacks'));
 testTime=120;run('render');
 assert(Number(get('COMBO'))===4&&JSON.stringify(get('combo buff stacks'))===heldPaused,'menu time leaves held combo effects intact');
 run('resume game');const heldDeadline=Number(get('combo expires'));
 assert(heldDeadline===123,'resuming shifts the held-effects deadline by the paused duration');
 testTime=heldDeadline;run('update combo');
 assert(Number(get('COMBO'))===4&&JSON.stringify(get('combo buff stacks'))===heldPaused,'held effects survive the exact combo deadline');
 testTime=heldDeadline+.001;run('update combo');
 assert(Number(get('COMBO'))===0&&total(get('combo buff stacks'))===0,'combo expiry removes all held effects together');
 assert(captureStamps(()=>run('draw combo wisps')).length===0,'no held-effect wisps render after the combo disappears');
 set('COMBO',2);set('combo expires',200);run('grant combo buffs');get('board').fill(1);run('spawn');run('draw bee buffs');
 assert(Number(get('GAME OVER'))===1&&total(get('combo buff stacks'))===0,'topping out clears held combo effects');
 run('reset');
 assert(total(get('buff stacks'))===0&&total(get('buff life'))===0&&total(get('combo buff stacks'))===0,'new runs clear both timed and held cosmetic effects');
 set('THEME',1);set('COMBO',2);run('grant combo buffs');
 assert(total(get('combo buff stacks'))===0,'other themes cannot receive Bee Swarm combo bundles');
 clock.projectTimer=originalTimer;

 set('THEME',12);set('CLEAR EFFECT',5);run('reset');singleClear();
 assert(Number(get('fx style'))===11&&Number(get('fx active'))===1&&get('clear rows').map(Number).join(',')==='19','Isaac clears select the full-row brimstone animation');
 assert(Number(get('SCORE'))===100&&Number(get('LINES'))===1&&get('unlocked').length===50,'brimstone clears retain ordinary scoring and the fifty-achievement catalogue');
 const tearFields=['tear x','tear y','tear vx','tear vy','tear kind'];
 assert(tearFields.every(name=>get(name).length===8)&&[1,2,3,4].every(kind=>get('tear kind').filter(value=>Number(value)===kind).length===2),'each Isaac cleared row launches eight tears across all four tear styles');
 const tearStart=get('tear y').map(Number),tearSpeed=get('tear vy').map(Number),brimstoneGuard=beeState();set('shake x',0);set('shake y',0);
 const tearStamps=captureStamps(()=>run('draw clear fx')).filter(stamp=>/^isaac tear\d+-/.test(stamp.name));
 assert(get('tear y').every((value,index)=>near(value,tearStart[index]+tearSpeed[index]))&&get('tear vy').every((value,index)=>near(value,tearSpeed[index]-.3)),'Isaac tears follow upward arcs with gravity after a clear');
 assert(tearStamps.length===8&&tearStamps.every(stamp=>Math.abs(stamp.x)<73*.82&&Math.abs(stamp.y)<150*.82),'all four tear styles render inside the well clipping bounds');
 for(let frame=1;frame<24;frame++)run('draw clear fx');
 assert(Number(get('fx active'))===0&&tearFields.every(name=>get(name).length===0)&&beeState()===brimstoneGuard,'brimstone and tears expire together without changing gameplay');
 assert(captureStamps(()=>run('draw isaac tears')).length===0,'expired Isaac clears leave no tear or splash stamps behind');
 run('reset');for(let row=16;row<20;row++)for(let col=0;col<10;col++)get('board')[row*10+col]=col===4?0:1;
 set('piece',1);set('rotation',1);set('x',2);set('y',16);run('lock');
 assert(Number(get('LINES'))===4&&tearFields.every(name=>get(name).length===32),'four-row Isaac clears cap the tear field at thirty-two aligned particles');
 const quadTearGuard=beeState();for(let frame=0;frame<24;frame++)run('draw clear fx');
 assert(tearFields.every(name=>get(name).length===0)&&beeState()===quadTearGuard,'the largest tear burst remains bounded and cleans up without awarding extra points');
 set('THEME',1);run('reset');singleClear();
 assert(tearFields.every(name=>get(name).length===0),'ordinary themes do not launch Isaac tears');
 // The default trail follows the dropped piece, rather than unrelated dashes
 // covering the board. Check every tetromino orientation against its cells.
 set('THEME',1);set('DROP EFFECT',1);
 for(let piece=1;piece<=7;piece++)for(let rotation=0;rotation<4;rotation++){
  run('reset');set('piece',piece);set('rotation',rotation);set('x',3);set('y',2);set('DROP EFFECT',1);
  const cells=[...String(get('shapes')[(piece-1)*4+rotation])].flatMap((cell,index)=>cell==='1'?[[index%4,Math.floor(index/4)]]:[]);
  const meanX=total(cells.map(c=>c[0]))/4,meanY=total(cells.map(c=>c[1]))/4,landing=19-Math.max(...cells.map(c=>c[1]));
  const expectedX=-72+(3+meanX)*16,expectedFrom=152-(2+meanY)*16,expectedTo=152-(landing+meanY)*16;
  run('hard drop');set('shake x',0);set('shake y',0);
  const segments=capturePen(()=>run('draw drop dash'));
  const white=segments.find(s=>s.color.slice(0,3).every(c=>near(c,1))&&near(s.from[0],expectedX*.82)&&near(s.to[0],expectedX*.82)&&near(s.from[1],expectedFrom*.82)&&near(s.to[1],expectedTo*.82));
  assert(near(get('drop x'),expectedX)&&near(get('drop from y'),expectedFrom)&&near(get('drop to y'),expectedTo)&&Boolean(white),'piece '+piece+' rotation '+rotation+' draws a straight white trail from its actual center to its landing');
 }
 run('reset');set('piece',4);set('rotation',0);set('x',3);set('y',2);get('board')[104]=1;run('hard drop');
 assert(near(get('drop from y'),112)&&near(get('drop to y'),16)&&Number(get('SCORE'))===12,'drop trails stop at an occupied landing surface and preserve hard-drop scoring');
 for(let style=1;style<=6;style++){
  run('reset');set('DROP EFFECT',style);const dropsBeforeDash=Number(get('lifetime drops'));run('hard drop');
  assert(Number(get('dash active'))===1&&Number(get('dash age'))===0&&Number(get('drop style'))===style&&Number(get('lifetime drops'))===dropsBeforeDash+1,'drop style '+style+' starts exactly once with a snapshot of the equipped effect');
  set('DROP EFFECT',style===6?1:style+1);const dashGuard=beeState();
  const segments=capturePen(()=>{for(let frame=0;frame<20;frame++)run('draw drop dash')});
  assert(Number(get('dash active'))===0&&Number(get('drop style'))===style&&segments.length>0&&beeState()===dashGuard,'drop style '+style+' fades after twenty frames without changing gameplay or switching mid-trail');
 }
 run('hard drop');run('reset');assert(Number(get('dash active'))===0,'new runs clear unfinished placement trails');
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
 for(const [draft,expected] of [[0,1],[999,6],[3.9,3]]){
  set('DROP EFFECT',draft);run('clamp settings');assert(Number(get('DROP EFFECT'))===expected,'drop style '+draft+' clamps to a selectable style');
 }
 set('SCREEN','cosmetics');set('cosmetics tab',4);const dropSelectionGuard=beeState();
 for(let style=1;style<=6;style++){
  mouse._scratchX=53+94*((style-1)%5)-240;mouse._scratchY=180-(141+100*Math.floor((style-1)/5));run('cosmetics click');
  assert(Number(get('DROP EFFECT'))===style&&Number(get('profile saved'))===0,'the Drops tab equips '+dropNames[style-1]);
 }
 assert(beeState()===dropSelectionGuard,'equipping every placement style preserves the active run and saved history');
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
 set('name draft','Nova_12');run('sanitize name');set('SHAKE',75);set('DIFFICULTY',5);set('CLEAR EFFECT',10);set('DROP EFFECT',6);set('BEST SCORE',5432);
 run('checkpoint run');const profileHistory=JSON.stringify(historyLists.map(name=>get(name)));run('save profile');
 assert(get('saved profile').length===16&&Number(get('saved profile')[0])===2&&Number(get('saved profile')[15])===6&&Number(get('profile saved'))===1&&get('settings notice')==='saved','Save Profile commits a version-two snapshot including the selected drop style');
 const legacyProfile=[1,...get('saved profile').slice(1,15)],migrationUnlocks=JSON.stringify(get('unlocked'));
 set('saved profile',legacyProfile);set('PLAYER NAME','Changed');set('DROP EFFECT',4);run('load profile');
 assert(get('PLAYER NAME')==='Nova_12'&&Number(get('SHAKE'))===75&&Number(get('DIFFICULTY'))===5&&Number(get('CLEAR EFFECT'))===10&&Number(get('game custom'))===2&&Number(get('key custom'))===2&&Number(get('DROP EFFECT'))===1,'version-one profiles restore every legacy setting and default to White Line');
 assert(JSON.stringify(get('saved profile'))===JSON.stringify(legacyProfile)&&JSON.stringify(historyLists.map(name=>get(name)))===profileHistory&&JSON.stringify(get('unlocked'))===migrationUnlocks,'loading a legacy profile preserves its snapshot, history and unlocks');
 run('save profile');
 assert(get('saved profile').length===16&&Number(get('saved profile')[0])===2&&Number(get('saved profile')[15])===1,'saving a loaded legacy profile upgrades it to version two');
 set('DROP EFFECT',6);run('save profile');
 const profileSnapshot=JSON.stringify(get('saved profile'));set('PLAYER NAME','Changed');set('SHAKE',0);set('DIFFICULTY',1);set('game r',0);set('BLOCK SKIN',1);set('DROP EFFECT',3);run('load profile');
 assert(get('PLAYER NAME')==='Nova_12'&&Number(get('SHAKE'))===75&&Number(get('DIFFICULTY'))===5&&Number(get('CLEAR EFFECT'))===10&&Number(get('DROP EFFECT'))===6,'Load Profile restores the name, difficulty, clear effect and equipped placement style');
 assert(Number(get('game r'))===12&&Number(get('key r'))===255&&Number(get('game custom'))===2&&Number(get('key custom'))===2&&Number(get('BLOCK SKIN'))===4,'Load Profile restores stored RGB, rainbow modes and earned cosmetic choices');
 assert(JSON.stringify(historyLists.map(name=>get(name)))===profileHistory&&get('unlocked').every(x=>Number(x)===1),'loading settings preserves score history and unlocked rewards');
 set('key custom',1);run('update rainbow');set('settings tab',2);run('render settings');const rgbPen=t.getCustomState('Scratch.pen').penAttributes.color4f.slice(0,3).map(x=>Math.round(x*255));set('key custom',2);
 // Scratch converts RGB through HSV and can truncate a channel by one unit.
 assert(rgbPen.every((v,i)=>Math.abs(v-[255,42,90][i])<=1),'rendered RGB matches selected key channels within Scratch rounding');
 assert(costumes.filter(c=>/^element(?:[1-9]|10)-/.test(c.name)).length===100,'ten selectable clear effects each include ten animation frames');
 assert(costumes.filter(c=>/^element11-/.test(c.name)).length===10&&Boolean(costumes.find(c=>c.name==='element spark11')),'Isaac includes ten brimstone clear frames and a matching spark');
 assert(costumes.filter(c=>/^familiar\d+-[0-3]$/.test(c.name)).length===40&&get('familiar names').length===10&&new Set(get('familiar names').map(String)).size===10,'ten distinct familiars each include four animation frames');
 assert(costumes.filter(c=>/^drop tip[1-6]-[0-5]$/.test(c.name)).length===36&&JSON.stringify(get('drop names'))===JSON.stringify(dropNames),'all six selectable placement styles include six landing-flare frames');
 assert(!costumes.some(c=>/^drop dash\d$/.test(c.name)),'unrelated full-board falling dashes are removed');
 assert(costumes.filter(c=>/^buff icon(?:[1-9]|1[0-2])$/.test(c.name)).length===12&&get('buff names').length===12&&new Set(get('buff names').map(String)).size===12,'all twelve Bee Swarm buffs have distinct readable icons and names');
 assert(costumes.filter(c=>/^buff wisp(?:[1-9]|1[0-2])-[0-3]$/.test(c.name)).length===48,'all twelve held effects include four animated wisp frames');
 assert(costumes.filter(c=>/^isaac tear[1-4]-[0-3]$/.test(c.name)).length===16&&costumes.filter(c=>/^tear splash[1-4]-[0-5]$/.test(c.name)).length===24,'Isaac includes four animated tear kinds and their splash frames');
 const brimstone=costumes.find(c=>c.name==='element11-0');
 assert(Boolean(brimstone)&&brimstone.rotationCenterX===80&&brimstone.rotationCenterY===14&&/\bwidth="160"/.test(Buffer.from(brimstone.asset.data).toString('utf8')),'brimstone clears align with the complete ten-column row');
 assert(costumes.filter(c=>c.name.startsWith('skin')).length===112,'eight earned skins include every block and ghost color');
 assert(costumes.filter(c=>c.name.startsWith('aura')).length===56,'seven earned auras include eight animation frames each');
 assert(costumes.filter(c=>/^achievement\d+-[01]$/.test(c.name)).length===100,'all fifty achievement cards include distinct locked and unlocked states');
 const beam=costumes.find(c=>c.name==='element5-0');
 assert(Boolean(beam)&&beam.rotationCenterX===80&&beam.rotationCenterY===16,'the expanded rainbow beam is centered on a full row and twice the normal height');
 const beamSvg=beam?Buffer.from(beam.asset.data).toString('utf8'):'';
 assert(/\bwidth=["']160["']/.test(beamSvg)&&/\bheight=["']32["']/.test(beamSvg),'rainbow clear artwork spans the complete 160-pixel row with a 32-pixel burst');
 for(let tab=1;tab<=4;tab++){
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
 assert(Number(restored.variables['DROP EFFECT'].value)===6&&Number(restored.variables['saved profile'].value[0])===2,'the equipped placement style survives an actual exported project reload');
 assert(restored.variables.unlocked.value.every(x=>Number(x)===1),'unlocked cosmetic achievements survive exporting and reopening the project');
 restoredVm.quit();
 console.log('Scratch VM loaded native project and completed gameplay checks.');
 vm.quit();
})().catch(e=>{console.error(e);process.exit(1)});
