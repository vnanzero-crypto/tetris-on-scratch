"""Build an original Scratch 3 falling-block game using native Scratch blocks."""
import json, zipfile, hashlib, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ZOOM=.82
from progression import CATALOG, ACHIEVEMENTS, SKIN_REQUIREMENTS, AURA_REQUIREMENTS, EFFECT_REQUIREMENTS, EFFECT_NAMES, SKIN_NAMES, AURA_NAMES, DIFFICULTY_NAMES
blocks={}; variables={}; lists={}; count=0

def uid():
 global count
 count+=1; return 'b'+str(count)
def var(n):
 variables.setdefault(n,[n,0]); return n
def lst(n):
 lists.setdefault(n,[n,[]]); return n
def B(op,inputs=None,fields=None,**extra):
 i=uid(); blocks[i]=dict(opcode=op,next=None,parent=None,inputs=inputs or {},fields=fields or {},shadow=False,topLevel=False,**extra); return i
def inp(v):
 if isinstance(v,tuple): return [3,v[0],[10,'']]
 return [1,[10,str(v)]]
def R(op,**kwargs): return (B(op,{k:inp(v) for k,v in kwargs.items()}),)
def V(n): return (B('data_variable',fields={'VARIABLE':[n,var(n)]}),)
def item(n,i): return (B('data_itemoflist',{'INDEX':inp(i)}, {'LIST':[n,lst(n)]}),)
def length(n):return (B('data_lengthoflist',fields={'LIST':[n,lst(n)]}),)
def add(a,b):return R('operator_add',NUM1=a,NUM2=b)
def sub(a,b):return R('operator_subtract',NUM1=a,NUM2=b)
def mul(a,b):return R('operator_multiply',NUM1=a,NUM2=b)
def mod(a,b):return R('operator_mod',NUM1=a,NUM2=b)
def eq(a,b):return R('operator_equals',OPERAND1=a,OPERAND2=b)
def lt(a,b):return R('operator_lt',OPERAND1=a,OPERAND2=b)
def gt(a,b):return R('operator_gt',OPERAND1=a,OPERAND2=b)
def either(a,b):return R('operator_or',OPERAND1=a,OPERAND2=b)
def both(a,b):return R('operator_and',OPERAND1=a,OPERAND2=b)
def neg(a):return R('operator_not',OPERAND=a)
def key(k):return R('sensing_keypressed',KEY_OPTION=k)
def held(k):
 aliases={'a':'left arrow','d':'right arrow','w':'up arrow','s':'down arrow'}
 return either(key(k),key(aliases[k])) if k in aliases else key(k)
def setv(n,v):return B('data_setvariableto',{'VALUE':inp(v)},{'VARIABLE':[n,var(n)]})
def change(n,v):return B('data_changevariableby',{'VALUE':inp(v)},{'VARIABLE':[n,var(n)]})
def append(n,v):return B('data_addtolist',{'ITEM':inp(v)},{'LIST':[n,lst(n)]})
def insert(n,i,v):return B('data_insertatlist',{'INDEX':inp(i),'ITEM':inp(v)},{'LIST':[n,lst(n)]})
def delete(n,i):return B('data_deleteoflist',{'INDEX':inp(i)},{'LIST':[n,lst(n)]})
def clear(n):return B('data_deletealloflist',fields={'LIST':[n,lst(n)]})
def replace(n,i,v):return B('data_replaceitemoflist',{'INDEX':inp(i),'ITEM':inp(v)},{'LIST':[n,lst(n)]})
def seq(ss):
 ss=[s for s in ss if s]
 for a,b in zip(ss,ss[1:]):blocks[a]['next']=b;blocks[b]['parent']=a
 return ss[0] if ss else None
def control(op,cond,ss,other=None):
 i=B(op,{'TIMES' if op=='control_repeat' else 'CONDITION':inp(cond)})
 for name,chain in [('SUBSTACK',ss),('SUBSTACK2',other)]:
  if chain:
   h=seq(chain);blocks[i]['inputs'][name]=[2,h];blocks[h]['parent']=i
 return i
def repeat(n,ss):return control('control_repeat',n,ss)
def If(c,ss,other=None):return control('control_if_else' if other else 'control_if',c,ss,other)
def until(c,ss):return control('control_repeat_until',c,ss)
def call(n):return B('procedures_call',mutation={'tagName':'mutation','children':[],'proccode':n,'argumentids':'[]','warp':'true'})
def proc(n,ss):
 p=B('procedures_prototype',mutation={'tagName':'mutation','children':[],'proccode':n,'argumentids':'[]','argumentnames':'[]','argumentdefaults':'[]','warp':'true'});blocks[p]['shadow']=True
 d=B('procedures_definition',{'custom_block':[1,p]});blocks[p]['parent']=d
 h=seq(ss);blocks[d]['next']=h;blocks[h]['parent']=d;blocks[d].update(topLevel=True,x=500,y=count*5)
def idx(x,y):return add(add(mul(y,10),x),1)
def cell():return R('operator_letter_of',LETTER=add(V('i'),1),STRING=V('shape'))
def shape(piece,rot):return item('shapes',add(add(mul(sub(piece,1),4),rot),1))
def floor(a):return (B('operator_mathop',{'NUM':inp(a)},{'OPERATOR':['floor',None]}),)
def coords():return [setv('cx',add(V('tx'),mod(V('i'),4))),setv('cy',add(V('ty'),floor(R('operator_divide',NUM1=V('i'),NUM2=4))))]
def join(a,b):return R('operator_join',STRING1=a,STRING2=b)
def div(a,b):return R('operator_divide',NUM1=a,NUM2=b)
def random(a,b):return R('operator_random',FROM=a,TO=b)
def position(px,py):return B('motion_gotoxy',{'X':inp(add(mul(px,ZOOM),V('shake x'))),'Y':inp(add(mul(py,ZOOM),V('shake y')))})
def raw_stamp(px,py,p):return [B('motion_gotoxy',{'X':inp(px),'Y':inp(py)}),B('looks_switchcostumeto',{'COSTUME':inp(p)}),B('pen_stamp')]
def stamp(px,py,p):return [position(px,py),B('looks_switchcostumeto',{'COSTUME':inp(p)}),B('pen_stamp')]
def block_stamp(px,py,p):return stamp(px,py,join(join(V('block prefix'),'-'),p))
def timer():return (B('sensing_timer'),)
def resize(inputs):
 # Scratch clamps scale using the current costume. Use the full-size interface
 # while sizing, so thin timer bars and tiny sparks do not enlarge later stamps.
 return repeat(1,[B('looks_switchcostumeto',{'COSTUME':inp('interface')}),B('looks_setsizeto',inputs)])
def mathop(op,n):return (B('operator_mathop',{'NUM':inp(n)},{'OPERATOR':[op,None]}),)
def effect(name,value):return B('looks_seteffectto',{'VALUE':inp(value)},{'EFFECT':[name,None]})
def out_of_bounds(x,y):return either(either(lt(V(x),0),gt(V(x),9)),either(lt(V(y),0),gt(V(y),19)))

PROFILE_FIELDS=['PLAYER NAME','SHAKE','DIFFICULTY','CLEAR EFFECT','BLOCK SKIN','AURA','game r','game g','game b','key r','key g','key b','game custom','key custom','DROP EFFECT']
DEFAULTS={'PLAYER NAME':'PLAYER','SHAKE':50,'DIFFICULTY':2,'CLEAR EFFECT':1,'BLOCK SKIN':1,'AURA':0,'game r':150,'game g':112,'game b':255,'key r':125,'key g':190,'key b':255,'game custom':0,'key custom':0,'DROP EFFECT':1}
def packed(prefix):return add(add(mul(V(prefix+' draw r'),65536),mul(V(prefix+' draw g'),256)),V(prefix+' draw b'))
def segment(x1,y1,x2,y2,color,width,world=False,transparency=None):
 move=position if world else lambda x,y:B('motion_gotoxy',{'X':inp(x),'Y':inp(y)})
 alpha=[] if transparency is None else [B('pen_setPenColorParamTo',{'COLOR_PARAM':inp('transparency'),'VALUE':inp(transparency)})]
 return [B('pen_penUp'),B('pen_setPenColorToColor',{'COLOR':inp(color)}),B('pen_setPenSizeTo',{'SIZE':inp(width)})]+alpha+[move(x1,y1),B('pen_penDown'),move(x2,y2),B('pen_penUp')]
cosmetic_guards=[]
for variable,mapping,fallback in [('BLOCK SKIN',SKIN_REQUIREMENTS,1),('AURA',AURA_REQUIREMENTS,0),('CLEAR EFFECT',EFFECT_REQUIREMENTS,1)]:
 for option,aid in mapping.items():cosmetic_guards += [If(both(eq(V(variable),option),neg(eq(item('unlocked',aid),1))),[setv(variable,fallback)])]
proc('validate cosmetics',cosmetic_guards)
clamps=[]
for name,lo,hi in [('SHAKE',0,100),('DIFFICULTY',1,5),('CLEAR EFFECT',1,10),('BLOCK SKIN',1,9),('AURA',0,7),('DROP EFFECT',1,6)]+[(p+' '+c,0,255) for p in ['game','key'] for c in ['r','g','b']]+[('game custom',0,2),('key custom',0,2)]:
 clamps += [setv(name,floor(V(name))),If(lt(V(name),lo),[setv(name,lo)]),If(gt(V(name),hi),[setv(name,hi)])]
proc('clamp settings',clamps+[call('validate cosmetics')])
proc('save profile',[call('clamp settings'),call('checkpoint run'),clear('saved profile'),append('saved profile',2)]+[append('saved profile',V(n)) for n in PROFILE_FIELDS]+[setv('profile saved',1),setv('settings notice','saved'),setv('notice until',add(timer(),2))])
proc('init profile',[If(neg(eq(V('profile ready'),1)),[setv(n,v) for n,v in DEFAULTS.items()]+[clear('unlocked'),repeat(50,[append('unlocked',0)]),setv('lifetime lines',0),setv('lifetime spins',0),setv('lifetime quads',0),setv('profile ready',1),call('save profile'),setv('settings notice','')]),
 until(neg(lt(length('unlocked'),50)),[append('unlocked',0)]),until(neg(lt(length('run difficulties'),length('run ids'))),[append('run difficulties',2)]),until(neg(gt(length('run difficulties'),length('run ids'))),[delete('run difficulties',length('run difficulties'))])])
proc('load profile',[call('init profile'),If(both(eq(length('saved profile'),15),eq(item('saved profile',1),1)),[setv(n,item('saved profile',i+2)) for i,n in enumerate(PROFILE_FIELDS[:-1])]+[setv('DROP EFFECT',1),call('clamp settings')]),If(both(eq(length('saved profile'),16),eq(item('saved profile',1),2)),[setv(n,item('saved profile',i+2)) for i,n in enumerate(PROFILE_FIELDS)]+[call('clamp settings')]),setv('settings notice','')])
# Version two adds drop style; version-one snapshots retain all prior fields.
proc('sanitize name',[setv('PLAYER NAME',''),setv('name index',1),repeat(12,[setv('name char',R('operator_letter_of',LETTER=V('name index'),STRING=V('name draft'))),
 If(both(neg(eq(V('name char'),'')),gt((B('data_itemnumoflist',{'ITEM':inp(V('name char'))},{'LIST':['name alphabet',lst('name alphabet')]}),),0)),[setv('PLAYER NAME',join(V('PLAYER NAME'),V('name char')))]),change('name index',1)]),
 If(eq(V('PLAYER NAME'),''),[setv('PLAYER NAME','PLAYER')]),setv('profile saved',0)])
color_fields=[p+' '+c for p in ['game','key'] for c in ['r','g','b']]
color_entry=[]
for i,name in enumerate(color_fields,1):color_entry += [If(eq(V('color channel'),i),[setv(name,(B('sensing_answer'),)),setv(name.split()[0]+' custom',1)])]
proc('edit color value',[B('sensing_askandwait',{'QUESTION':inp('RGB value: enter a number from 0 to 255')})]+color_entry+[call('clamp settings'),setv('profile saved',0),call('sync inputs')])
proc('edit name',[B('sensing_askandwait',{'QUESTION':inp('Name: up to 12 letters, numbers, spaces, - or _')}),setv('name draft',(B('sensing_answer'),)),call('sanitize name'),setv('settings notice','name'),setv('notice until',add(timer(),2)),call('sync inputs')])
proc('apply difficulty',[setv('gravity base',item('gravity choices',V('DIFFICULTY'))),setv('lock limit',item('lock choices',V('DIFFICULTY'))),setv('combo window',item('combo choices',V('DIFFICULTY'))),setv('run difficulty',V('DIFFICULTY'))])
# Fifty actual progress thresholds, with permanent rewards and local developer unlock.
ach=[If(gt(V('run max combo'),V('best combo')),[setv('best combo',V('run max combo'))])]
for i,(_,metric,threshold,_) in enumerate(CATALOG,1):
 ach += [If(both(gt(V(metric),threshold-1),neg(eq(item('unlocked',i),1))),[replace('unlocked',i,1),setv('achievement notice',i),setv('achievement until',add(timer(),3))])]
proc('check achievements',ach)
proc('unlock all',[call('init profile'),setv('unlock index',1),repeat(50,[replace('unlocked',V('unlock index'),1),change('unlock index',1)]),setv('achievement until',0),setv('unlock until',add(timer(),3))])
rainbow_updates=[]
for prefix in ['game','key']:
 for c,phase in [('r',0),('g',120),('b',240)]:
  rainbow_updates += [If(eq(V(prefix+' custom'),2),[setv(prefix+' draw '+c,floor(add(127.5,mul(127.5,mathop('sin',add(mul(timer(),95),phase))))))],[setv(prefix+' draw '+c,V(prefix+' '+c))])]
proc('update rainbow',rainbow_updates)
proc('draw raw text',[resize({'SIZE':inp(V('text scale'))}),setv('text index',1),repeat(R('operator_length',STRING=V('text value')),[setv('text char',R('operator_letter_of',LETTER=V('text index'),STRING=V('text value'))),
 setv('text glyph',(B('data_itemnumoflist',{'ITEM':inp(V('text char'))},{'LIST':['name alphabet',lst('name alphabet')]}),)),If(gt(V('text glyph'),0),raw_stamp(V('text x'),V('text y'),join('letter',V('text glyph')))),change('text x',mul(V('text scale'),.12)),change('text index',1)])])
# The run's difficulty sets the real-clock combo and held-effect window.
proc('update combo',[If(both(gt(V('COMBO'),0),gt(timer(),V('combo expires'))),[setv('COMBO',0),setv('combo expires',0),setv('combo animating',0),call('clear combo buffs')])])
proc('clear combo',[If(either(eq(V('COMBO'),0),gt(timer(),V('combo expires'))),[setv('COMBO',1),call('clear combo buffs')],[change('COMBO',1)]),
 setv('combo pulse',0),setv('combo animating',1),If(gt(V('COMBO'),V('run max combo')),[setv('run max combo',V('COMBO'))]),If(gt(V('COMBO'),V('best combo')),[setv('best combo',V('COMBO'))]),setv('combo expires',add(timer(),V('combo window'))),setv('combo bonus',mul(mul(sub(V('COMBO'),1),50),V('LEVEL')))])
proc('update camera',[setv('shake x',0),setv('shake y',0),If(gt(V('shake ticks'),0),[
 setv('shake amount',mul(mul(div(V('shake ticks'),10),div(V('SHAKE'),100)),8)),
 If(eq(mod(V('shake ticks'),2),0),[setv('shake x',V('shake amount'))],[setv('shake x',sub(0,V('shake amount')))]),
 If(eq(mod(V('shake ticks'),3),0),[setv('shake y',mul(V('shake amount'),-.5))],[setv('shake y',mul(V('shake amount'),.5))]),change('shake ticks',-1)])])
proc('apply theme',[B('looks_switchbackdropto',{'BACKDROP':inp(join('theme',V('THEME')))})])
proc('next theme',[setv('THEME',add(mod(V('THEME'),12),1)),call('apply theme')])

history_columns=['run ids','run scores','run lines','run combos','run themes','run status','run difficulties']
proc('checkpoint run',[If(eq(V('run record open'),1),[
 If(gt(V('COMBO'),V('run max combo')),[setv('run max combo',V('COMBO'))]),
 replace('run scores',1,V('SCORE')),replace('run lines',1,V('LINES')),replace('run combos',1,V('run max combo')),replace('run themes',1,V('THEME')),
 If(gt(V('SCORE'),V('BEST SCORE')),[setv('BEST SCORE',V('SCORE'))])])])
proc('finish run',[If(eq(V('run record open'),1),[call('checkpoint run'),replace('run status',1,V('finish reason')),setv('run record open',0)])])
proc('begin run',[change('run serial',1),setv('run max combo',0),change('lifetime runs',1),If(eq(V('run difficulty'),4),[change('expert starts',1)]),If(eq(V('run difficulty'),5),[change('nightmare starts',1)]),insert('run ids',1,V('run serial')),insert('run scores',1,0),insert('run lines',1,0),insert('run combos',1,0),insert('run themes',1,V('THEME')),insert('run status',1,'Playing'),insert('run difficulties',1,V('run difficulty')),
 If(gt(length('run ids'),20),[delete(name,21) for name in history_columns]),setv('run record open',1)])
# Decorative particles are bounded and never touch logical board/history state.
proc('init ambient',[clear('ambient x'),clear('ambient y'),clear('ambient speed'),repeat(24,[append('ambient x',random(-235,235)),append('ambient y',random(-175,175)),append('ambient speed',div(random(15,60),100))])])
proc('draw ambient',[If(neg(both(eq(length('ambient x'),24),both(eq(length('ambient y'),24),eq(length('ambient speed'),24)))),[call('init ambient')]),resize({'SIZE':inp(100)}),setv('ambient index',1),repeat(24,[
 replace('ambient y',V('ambient index'),add(item('ambient y',V('ambient index')),item('ambient speed',V('ambient index')))),
 If(gt(item('ambient y',V('ambient index')),178),[replace('ambient y',V('ambient index'),-178)]),
 setv('ambient draw x',add(item('ambient x',V('ambient index')),mul(mathop('sin',add(mul(timer(),18),mul(V('ambient index'),29))),3))),
 If(either(neg(eq(V('SCREEN'),'play')),either(gt(mathop('abs',V('ambient draw x')),74),gt(mathop('abs',item('ambient y',V('ambient index'))),144))),
 raw_stamp(V('ambient draw x'),item('ambient y',V('ambient index')),'ambient spark')),change('ambient index',1)])])
proc('test position',[
 setv('valid',1),setv('shape',shape(V('piece'),V('tr'))),setv('i',0),
 repeat(16,[If(eq(cell(),1),coords()+[
  If(out_of_bounds('cx','cy'),[setv('valid',0)],
   [If(gt(item('board',idx(V('cx'),V('cy'))),0),[setv('valid',0)])])]),change('i',1)])])
proc('move',[setv('tx',add(V('x'),V('dx'))),setv('ty',add(V('y'),V('dy'))),setv('tr',V('rotation')),call('test position'),
 If(eq(V('valid'),1),[setv('x',V('tx')),setv('y',V('ty')),If(neg(eq(V('dx'),0)),[setv('last rotation',0)])])])
proc('refill bag',[clear('pool'),repeat(7,[append('pool',add(length('pool'),1))]),repeat(7,[setv('pick',random(1,length('pool'))),append('bag',item('pool',V('pick'))),delete('pool',V('pick'))])])
proc('spawn',[If(eq(length('bag'),0),[call('refill bag')]),setv('piece',item('bag',1)),delete('bag',1),
 setv('x',3),setv('y',0),setv('rotation',0),setv('last rotation',0),setv('fall',0),setv('ground ticks',0),
 setv('tx',V('x')),setv('ty',V('y')),setv('tr',0),call('test position'),If(eq(V('valid'),0),[setv('GAME OVER',1),setv('COMBO',0),setv('combo expires',0),setv('finish reason','Game Over'),call('finish run')])])
# Compact wall and floor kick set; spin scoring uses the three-corner rule.
proc('rotate',[setv('kick',1),setv('rotated',0),repeat(7,[If(eq(V('rotated'),0),[
 setv('tx',add(V('x'),item('kick x',V('kick')))),setv('ty',add(V('y'),item('kick y',V('kick')))),setv('tr',mod(add(V('rotation'),V('turn')),4)),call('test position'),
 If(eq(V('valid'),1),[setv('x',V('tx')),setv('y',V('ty')),setv('rotation',V('tr')),setv('rotated',1),setv('last rotation',1),change('SCORE',5),change('lifetime rotations',1)])]),change('kick',1)])])
proc('detect spin',[setv('t spin',0),setv('corners',0),
 If(both(eq(V('piece'),6),eq(V('last rotation'),1)),[setv('corner',0),repeat(4,[
  setv('cx',add(V('x'),mul(mod(V('corner'),2),2))),setv('cy',add(V('y'),mul(floor(div(V('corner'),2)),2))),
  If(out_of_bounds('cx','cy'),[change('corners',1)],[If(gt(item('board',idx(V('cx'),V('cy'))),0),[change('corners',1)])]),change('corner',1)]),
  If(gt(V('corners'),2),[setv('t spin',1)])])])

# All effects are native Scratch pen stamps; their state expires after 24 frames.
proc('start clear fx',[setv('fx style',V('CLEAR EFFECT')),If(eq(V('THEME'),12),[setv('fx style',11)]),clear('clear rows'),setv('fx row',1),repeat(length('pending clear rows'),[
 append('clear rows',item('pending clear rows',V('fx row'))),change('fx row',1)]),
 setv('shake ticks',10),setv('fx active',1),setv('fx age',0),clear('particle x'),clear('particle y'),clear('particle vx'),clear('particle vy'),
 setv('fx row',1),repeat(length('clear rows'),[setv('fx y',sub(152,mul(item('clear rows',V('fx row')),16))),repeat(12,[
 append('particle x',random(-74,74)),append('particle y',V('fx y')),append('particle vx',div(random(-30,30),10)),append('particle vy',div(random(15,55),10))]),change('fx row',1)]),call('start isaac tears')])
proc('lock',[call('detect spin'),setv('shape',shape(V('piece'),V('rotation'))),setv('tx',V('x')),setv('ty',V('y')),setv('i',0),
 repeat(16,[If(eq(cell(),1),coords()+[replace('board',idx(V('cx'),V('cy')),V('piece'))]),change('i',1)]),
 setv('row',19),setv('cleared',0),clear('pending clear rows'),repeat(20,[setv('full',1),setv('col',0),repeat(10,[
 If(eq(item('board',idx(V('col'),V('row'))),0),[setv('full',0)]),change('col',1)]),
 If(eq(V('full'),1),[append('pending clear rows',sub(V('row'),V('cleared'))),repeat(10,[delete('board',add(mul(V('row'),10),1))]),
 repeat(10,[B('data_insertatlist',{'INDEX':inp(1),'ITEM':inp(0)},{'LIST':['board',lst('board')]})]),change('cleared',1)],[change('row',-1)])]),
 change('LINES',V('cleared')),change('lifetime lines',V('cleared')),If(eq(V('CLEAR EFFECT'),5),[change('rainbow lines',V('cleared'))]),If(eq(V('THEME'),11),[change('beeswarm lines',V('cleared'))]),If(eq(V('cleared'),4),[change('lifetime quads',1)]),If(eq(V('t spin'),1),[change('lifetime spins',1)]),setv('awarded',0),
 If(eq(V('t spin'),1),[setv('awarded',mul(item('spin points',add(V('cleared'),1)),V('LEVEL'))),setv('notification','tspin'),setv('flash',42)],
 [If(gt(V('cleared'),0),[setv('awarded',mul(item('points',V('cleared')),V('LEVEL'))),setv('notification',join('clear',V('cleared'))),setv('flash',36)])]),
 change('SCORE',V('awarded')),If(gt(V('cleared'),0),[call('clear combo'),change('SCORE',V('combo bonus')),call('start clear fx'),call('grant bee buff')]),
 setv('LEVEL',add(floor(div(V('LINES'),10)),1)),setv('can hold',1),call('check achievements'),call('spawn')])
proc('hold',[If(eq(V('can hold'),1),[setv('swap',V('HOLD')),setv('HOLD',V('piece')),If(eq(V('swap'),0),[call('spawn')],[
 setv('piece',V('swap')),setv('x',3),setv('y',0),setv('rotation',0),setv('last rotation',0),setv('fall',0),setv('ground ticks',0),setv('tx',3),setv('ty',0),setv('tr',0),call('test position'),
 If(eq(V('valid'),0),[setv('GAME OVER',1),setv('COMBO',0),setv('combo expires',0),setv('finish reason','Game Over'),call('finish run')])]),setv('can hold',0)])])
proc('draw piece',[setv('shape',shape(V('piece'),V('rotation'))),setv('tx',V('x')),setv('ty',V('draw y')),setv('i',0),
 repeat(16,[If(eq(cell(),1),coords()+block_stamp(add(-72,mul(V('cx'),16)),sub(152,mul(V('cy'),16)),add(V('piece'),V('draw style')))),change('i',1)])])
proc('mini',[setv('shape',shape(V('mini piece'),0)),setv('i',0),repeat(16,[If(eq(cell(),1),
 block_stamp(add(add(V('mini x'),mul(neg(either(eq(V('mini piece'),1),eq(V('mini piece'),4))),6)),mul(mod(V('i'),4),12)),sub(V('mini y'),mul(floor(div(V('i'),4)),12)),V('mini piece'))),change('i',1)])])
proc('draw number',[setv('number text',join('000000',V('number value'))),setv('digit index',sub(R('operator_length',STRING=V('number text')),V('number digits'))),repeat(V('number digits'),[
 change('digit index',1),position(V('number x'),V('number y')),
 B('looks_switchcostumeto',{'COSTUME':inp(join('digit',R('operator_letter_of',LETTER=V('digit index'),STRING=V('number text'))))}),B('pen_stamp'),change('number x',V('number spacing'))])])
proc('draw raw number',[resize({'SIZE':inp(V('number scale'))}),setv('number text',join('00000000',V('number value'))),setv('digit index',sub(R('operator_length',STRING=V('number text')),V('number digits'))),repeat(V('number digits'),[
 change('digit index',1),B('motion_gotoxy',{'X':inp(V('number x')),'Y':inp(V('number y'))}),B('looks_switchcostumeto',{'COSTUME':inp(join('digit',R('operator_letter_of',LETTER=V('digit index'),STRING=V('number text'))))}),B('pen_stamp'),change('number x',V('number spacing'))])])
proc('draw clear fx',[If(eq(V('fx active'),1),[
 call('draw isaac tears'),
 If(lt(V('fx age'),20),[If(either(eq(length('clear rows'),4),eq(V('notification'),'tspin')),[setv('fx beam','quadbeam')],[setv('fx beam','beam')]),setv('fx row',1),repeat(length('clear rows'),
 stamp(0,sub(152,mul(item('clear rows',V('fx row')),16)),join(join('element',V('fx style')),join('-',floor(div(V('fx age'),2)))))+[change('fx row',1)])]),
 effect('GHOST',mul(V('fx age'),4)),setv('particle',1),repeat(length('particle x'),[
 replace('particle x',V('particle'),add(item('particle x',V('particle')),item('particle vx',V('particle')))),
 replace('particle y',V('particle'),add(item('particle y',V('particle')),item('particle vy',V('particle')))),
 replace('particle vy',V('particle'),sub(item('particle vy',V('particle')),.28)),
 If(both(both(gt(item('particle x',V('particle')),-78),lt(item('particle x',V('particle')),78)),both(gt(item('particle y',V('particle')),-158),lt(item('particle y',V('particle')),158))),
 stamp(item('particle x',V('particle')),item('particle y',V('particle')),join('element spark',V('fx style')))),change('particle',1)]),B('looks_cleargraphiceffects'),change('fx age',1),
 If(gt(V('fx age'),23),[setv('fx active',0),call('clear isaac tears')])])])

render=[setv('block prefix',join('t',V('THEME'))),If(gt(V('BLOCK SKIN'),1),[setv('block prefix',join('skin',V('BLOCK SKIN')))]),setv('number spacing',14),call('update combo'),call('update camera'),B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(ZOOM*100)})]+stamp(0,0,'interface')+[call('draw game accent'),If(gt(V('AURA'),0),stamp(0,0,join(join('aura',V('AURA')),join('-',mod(floor(mul(timer(),8)),8))))),call('draw drop dash')]+[setv('i',1),repeat(200,[If(gt(item('board',V('i')),0),block_stamp(add(-72,mul(mod(sub(V('i'),1),10),16)),sub(152,mul(floor(div(sub(V('i'),1),10)),16)),item('board',V('i')))),change('i',1)]),
 setv('ghost',V('y')),setv('valid',1),until(eq(V('valid'),0),[setv('tx',V('x')),setv('ty',add(V('ghost'),1)),setv('tr',V('rotation')),call('test position'),If(eq(V('valid'),1),[change('ghost',1)])]),
 setv('draw style',7),setv('draw y',V('ghost')),call('draw piece'),setv('draw style',0),setv('draw y',V('y')),call('draw piece'),
 resize({'SIZE':inp(70*ZOOM)}),If(gt(V('HOLD'),0),[setv('mini piece',V('HOLD')),setv('mini x',-180),setv('mini y',38),call('mini')]),
 setv('preview',1),repeat(4,[If(lt(V('preview'),add(length('bag'),1)),[setv('mini piece',item('bag',V('preview'))),setv('mini x',144),setv('mini y',sub(113,mul(sub(V('preview'),1),31))),call('mini')]),change('preview',1)]),resize({'SIZE':inp(100*ZOOM)})]
for value,digits,xx,yy in [('SCORE',7,-217,-9),('LINES',3,-217,-60),('LEVEL',2,-217,-103)]:
 render += [setv('number value',V(value)),setv('number digits',digits),setv('number x',xx),setv('number y',yy),call('draw number')]
proc('draw combo',[
 setv('combo scale',1),If(both(gt(V('COMBO'),0),lt(V('combo pulse'),8)),[setv('combo scale',sub(1.14,mul(V('combo pulse'),.0175)))]),
 resize({'SIZE':inp(mul(100*ZOOM,V('combo scale')))}),setv('number spacing',14),setv('number value',V('COMBO')),setv('number digits',2),setv('number x',-136),setv('number y',120),call('draw number'),resize({'SIZE':inp(100*ZOOM)}),
 If(gt(V('COMBO'),0),[setv('combo title',V('COMBO')),If(gt(V('combo title'),15),[setv('combo title',15)])]+stamp(-161,100,join('title',V('combo title')))+[
 resize({'SIZE':inp(100*ZOOM)}),If(eq(V('combo animating'),1),[change('combo pulse',1),If(gt(V('combo pulse'),23),[setv('combo animating',0)])])])])
render += [call('draw clear fx'),If(gt(V('flash'),0),[change('flash',-1)]+stamp(-161,78,V('notification'))),call('draw combo'),call('draw combo timer'),call('draw companions'),call('draw bee tokens'),call('draw combo wisps'),call('draw bee buffs')]
# Optional exact RGB pen fill below the white arrow glyph, independent of theme colors.
for arrow,k,x,y in [('↑','w',160,-40),('←','a',118,-70),('↓','s',160,-70),('→','d',202,-70)]:
 render += [If(both(gt(V('key custom'),0),held(k)),segment(x-7,y,x+7,y,packed('key'),22*ZOOM,True)+stamp(x,y,'arrow glyph'+k),stamp(x,y,join('arrow'+k+'-',held(k))))]
render += [If(eq(V('GAME OVER'),1),stamp(0,0,'gameover')),resize({'SIZE':inp(100)})]+raw_stamp(-186,158,'menu button')+[resize({'SIZE':inp(100*ZOOM)})]
proc('render game',render)
proc('render menu',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)}),If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),raw_stamp(0,0,join(join('menu',V('THEME')),'-resume')),raw_stamp(0,0,join(join('menu',V('THEME')),'-play')))]+raw_stamp(125,120,'edition logo'))
proc('render themes',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('theme menu',V('THEME'))))
# Page the newest twenty run records, five rows per page.
history_render=[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,'history panel')+[
 setv('number value',V('BEST SCORE')),setv('number digits',7),setv('number scale',85),setv('number spacing',12),setv('number x',94),setv('number y',116),call('draw raw number'),
 setv('history row',0),repeat(5,[setv('history index',add(add(mul(V('history page'),5),V('history row')),1)),
 If(lt(V('history index'),add(length('run ids'),1)),[setv('history y',sub(54,mul(V('history row'),32)))]+sum([
 [setv('number value',item(name,V('history index'))),setv('number digits',digits),setv('number scale',60),setv('number spacing',8),setv('number x',x-240),setv('number y',V('history y')),call('draw raw number')]
 for name,digits,x in [('run ids',3,24),('run scores',7,70),('run lines',3,180),('run combos',2,226)]],[])+[
 resize({'SIZE':inp(100)})]+raw_stamp(42,add(V('history y'),4),join('history theme',item('run themes',V('history index'))))+raw_stamp(42,sub(V('history y'),7),join('history status',item('run status',V('history index'))))+raw_stamp(162,add(V('history y'),4),join('history difficulty',item('run difficulties',V('history index'))))),change('history row',1)]),
 If(eq(length('run ids'),0),raw_stamp(0,0,'history empty')),setv('history pages',1),If(gt(length('run ids'),0),[setv('history pages',add(floor(div(sub(length('run ids'),1),5)),1))]),
 setv('number value',add(V('history page'),1)),setv('number digits',1),setv('number scale',55),setv('number spacing',8),setv('number x',-15),setv('number y',-123),call('draw raw number'),resize({'SIZE':inp(100)})]+raw_stamp(0,-123,'history slash')+[
 setv('number value',V('history pages')),setv('number digits',1),setv('number scale',55),setv('number spacing',8),setv('number x',8),setv('number y',-123),call('draw raw number')]
proc('render history',history_render)
proc('render',[call('update hover'),If(eq(V('SCREEN'),'play'),[call('render game')],[If(eq(V('SCREEN'),'themes'),[call('render themes')],[If(eq(V('SCREEN'),'history'),[call('render history')],[call('render menu')])])]),call('draw hover')])
proc('reset',[call('init profile'),call('apply difficulty'),If(either(lt(V('THEME'),1),gt(V('THEME'),12)),[setv('THEME',1)]),call('apply theme'),call('init companions'),call('reset bee buffs'),call('clear isaac tears'),setv('dash active',0),setv('dash age',0),setv('COMBO',0),setv('combo expires',0),setv('combo bonus',0),setv('run max combo',0),setv('combo pulse',0),setv('combo animating',0),setv('shake ticks',0),setv('shake x',0),setv('shake y',0),clear('board'),repeat(200,[append('board',0)]),clear('bag'),clear('clear rows'),setv('fx active',0),setv('fx age',0),setv('flash',0),
 setv('SCORE',0),setv('LINES',0),setv('LEVEL',1),setv('HOLD',0),setv('GAME OVER',0),setv('can hold',1),setv('left ticks',0),setv('right ticks',0),
 setv('z previous',0),setv('w previous',0),setv('space previous',0),setv('c previous',0),call('spawn')])
def edge(k,prev,ss):return [If(both(held(k),eq(V(prev),0)),ss),setv(prev,held(k))]
def sideways(k,t,dx):return If(held(k),[change(t,1),If(either(eq(V(t),1),both(gt(V(t),9),eq(mod(V(t),2),0))),[setv('dx',dx),setv('dy',0),call('move')])],[setv(t,0)])
proc('capture drop start',[setv('drop style',V('DROP EFFECT')),setv('drop start row',V('y')),setv('drop local x',0),setv('drop local y',0),setv('drop min col',4),setv('drop max col',-1),setv('shape',shape(V('piece'),V('rotation'))),setv('i',0),repeat(16,[
 If(eq(cell(),1),[change('drop local x',mod(V('i'),4)),change('drop local y',floor(div(V('i'),4))),If(lt(mod(V('i'),4),V('drop min col')),[setv('drop min col',mod(V('i'),4))]),If(gt(mod(V('i'),4),V('drop max col')),[setv('drop max col',mod(V('i'),4))])]),change('i',1)]),
 setv('drop x',add(-72,mul(add(V('x'),div(V('drop local x'),4)),16))),setv('drop left',add(-80,mul(add(V('x'),V('drop min col')),16))),setv('drop right',add(-64,mul(add(V('x'),V('drop max col')),16))),setv('drop width',sub(V('drop right'),V('drop left'))),setv('drop center x',div(add(V('drop left'),V('drop right')),2)),setv('drop from y',sub(152,mul(add(V('y'),div(V('drop local y'),4)),16))),setv('drop to y',V('drop from y'))])
proc('hard drop',[call('capture drop start'),setv('dash active',1),setv('dash age',0),change('lifetime drops',1),setv('valid',1),until(eq(V('valid'),0),[setv('dx',0),setv('dy',1),call('move'),If(eq(V('valid'),1),[change('SCORE',2)])]),setv('drop rows',sub(V('y'),V('drop start row'))),setv('drop to y',sub(V('drop from y'),mul(V('drop rows'),16))),call('lock')])
active=[sideways('a','left ticks',-1),sideways('d','right ticks',1)]
active+=edge('w','w previous',[setv('turn',1),call('rotate')])+edge('z','z previous',[setv('turn',3),call('rotate')])+edge('c','c previous',[call('hold')])+edge('space','space previous',[call('hard drop')])
active += [change('fall',1),If(either(both(held('s'),eq(mod(V('fall'),2),0)),gt(V('fall'),div(V('gravity base'),V('LEVEL')))),[
 setv('dx',0),setv('dy',1),call('move'),If(eq(V('valid'),1),[If(held('s'),[change('SCORE',1)]),setv('fall',0)])]),
 setv('tx',V('x')),setv('ty',add(V('y'),1)),setv('tr',V('rotation')),call('test position'),If(eq(V('valid'),0),[change('ground ticks',1),
 If(gt(V('ground ticks'),V('lock limit')),[call('lock')])],[setv('ground ticks',0)])]
proc('sync inputs',[setv('w previous',held('w')),setv('z previous',key('z')),setv('space previous',key('space')),setv('c previous',key('c')),setv('left ticks',0),setv('right ticks',0)])
proc('open menu',[If(eq(V('SCREEN'),'play'),[call('update combo'),setv('pause started',timer()),setv('SCREEN','menu'),setv('shake ticks',0),setv('shake x',0),setv('shake y',0),If(eq(V('run record open'),1),[call('checkpoint run'),replace('run status',1,'Paused')]),call('sync inputs')])])
proc('resume game',[If(both(eq(V('SCREEN'),'menu'),both(eq(V('has game'),1),eq(V('GAME OVER'),0))),[
 If(gt(V('COMBO'),0),[change('combo expires',sub(timer(),V('pause started')))]),setv('SCREEN','play'),If(eq(V('run record open'),1),[replace('run status',1,'Playing')]),call('sync inputs')])])
proc('start game',[setv('finish reason','Restarted'),call('finish run'),call('reset'),setv('has game',1),setv('SCREEN','play'),call('begin run'),call('sync inputs')])
def mouse_x():return (B('sensing_mousex'),)
def mouse_y():return (B('sensing_mousey'),)
def hit(x1,y1,x2,y2):
 # Input bounds are canvas coordinates with origin at the upper-left.
 return both(both(gt(mouse_x(),x1-240),lt(mouse_x(),x2-240)),both(gt(mouse_y(),180-y2),lt(mouse_y(),180-y1)))
proc('show themes',[setv('SCREEN','themes')])
proc('show history',[setv('history page',0),setv('SCREEN','history')])
menu_keys=edge('t','t previous',[call('show themes')])+edge('h','h previous',[call('show history')])
menu_keys+=edge('space','space previous',[If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),[call('resume game')],[call('choose difficulty')])])+edge('n','n previous',[call('choose difficulty')])
theme_keys=edge('t','t previous',[call('next theme')])
for theme in range(1,13):
 theme_keys+=edge(str(theme%10) if theme<11 else ('b' if theme==11 else 'i'),'theme key '+str(theme),[setv('THEME',theme),call('apply theme')])
menu_clicks=[If(hit(32,112,246,150),[If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),[call('resume game')],[call('choose difficulty')])]),If(hit(32,162,246,192),[call('choose difficulty')]),If(hit(32,204,246,234),[call('show themes')]),If(hit(32,246,246,276),[call('show history')])]
theme_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')])]
for theme in range(1,13):
 col=(theme-1)%4;row=(theme-1)//4;left=12+col*116;top=86+row*70
 theme_clicks += [If(hit(left,top,left+106,top+62),[setv('THEME',theme),call('apply theme')])]
history_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')]),If(both(hit(96,288,196,316),gt(V('history page'),0)),[change('history page',-1)]),If(both(hit(284,288,384,316),lt(mul(add(V('history page'),1),5),length('run ids'))),[change('history page',1)])]
# Hover lookup uses the same hitboxes as click routing and does not select items.
hover_menu=[]
for kind,box in [(1,(32,112,246,150)),(2,(32,162,246,192)),(3,(32,204,246,234)),(4,(32,246,246,276))]:
 hover_menu += [If(hit(*box),[setv('hover object',kind)])]
hover_themes=[If(hit(16,16,100,42),[setv('hover object',5)])]
for theme in range(1,13):
 left=12+((theme-1)%4)*116;top=86+((theme-1)//4)*70
 hover_themes += [If(hit(left,top,left+106,top+62),[setv('hover object',theme+10)])]
hover_history=[If(hit(16,16,100,42),[setv('hover object',5)]),If(hit(96,288,196,316),[setv('hover object',6)]),If(hit(284,288,384,316),[setv('hover object',7)])]
proc('update hover',[setv('hover object',0),If(eq(V('SCREEN'),'menu'),hover_menu,[If(eq(V('SCREEN'),'themes'),hover_themes,[If(eq(V('SCREEN'),'history'),hover_history)])])])
proc('draw hover',[If(gt(V('hover object'),0),[
 setv('hover frame',mod(floor(mul(timer(),8)),8)),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('outline',V('hover object')))+[
 setv('hover x',125),setv('hover y',-5),setv('hover size',100),
 If(eq(V('SCREEN'),'themes'),[setv('hover x',188),setv('hover y',-144),setv('hover size',40)]),
 If(eq(V('SCREEN'),'history'),[setv('hover x',20),setv('hover y',120),setv('hover size',50)]),
 resize({'SIZE':inp(V('hover size'))})]+raw_stamp(V('hover x'),add(V('hover y'),mul(mathop('sin',mul(timer(),80)),3)),join(join('object',V('hover object')),join('-',V('hover frame')))))])
clicks=[If(eq(V('SCREEN'),'menu'),menu_clicks,[If(eq(V('SCREEN'),'themes'),theme_clicks,[If(eq(V('SCREEN'),'history'),history_clicks,[If(hit(8,10,100,34),[call('open menu')])])])])]
loop=edge('u','u previous',[call('unlock all')])+edge('m','m previous',[If(eq(V('SCREEN'),'play'),[call('open menu')],[If(eq(V('SCREEN'),'menu'),[call('resume game')],[setv('SCREEN','menu')])])])
loop += [If(both((B('sensing_mousedown'),),eq(V('mouse previous'),0)),clicks),setv('mouse previous',(B('sensing_mousedown'),)),
 If(eq(V('SCREEN'),'menu'),menu_keys,[If(eq(V('SCREEN'),'themes'),theme_keys,[If(both(eq(V('SCREEN'),'play'),eq(V('GAME OVER'),0)),[If(key('r'),[call('choose difficulty')])]+active)])]),call('checkpoint run'),call('check achievements'),call('render'),B('control_wait',{'DURATION':inp(.02)})]
forever=B('control_forever');h=seq(loop);blocks[forever]['inputs']['SUBSTACK']=[2,h];blocks[h]['parent']=forever
hat=B('event_whenflagclicked');h=seq([B('looks_hide'),call('init profile'),setv('finish reason','Stopped'),call('finish run'),call('load profile'),call('reset'),setv('has game',0),setv('SCREEN','menu'),call('init ambient'),setv('m previous',0),setv('mouse previous',0),setv('n previous',0),call('sync inputs'),forever]);blocks[hat]['next']=h;blocks[h]['parent']=hat;blocks[hat].update(topLevel=True,x=20,y=20)
# RGB accents and settings overlay are native pen blocks, not external extensions.
accent=[]
for x1,y1,x2,y2 in [(-81,161,81,161),(81,161,81,-161),(81,-161,-81,-161),(-81,-161,-81,161)]:
 accent+=segment(x1,y1,x2,y2,packed('game'),1.8,True)
proc('draw game accent',[If(gt(V('game custom'),0),accent)])
def raw_number(value,digits,x,y,scale=60,spacing=8):
 return [setv('number value',value),setv('number digits',digits),setv('number scale',scale),setv('number spacing',spacing),setv('number x',x-240),setv('number y',180-y),call('draw raw number')]
def raw_text(value,x,y,scale=65):
 return [setv('text value',value),setv('text x',x-240),setv('text y',180-y),setv('text scale',scale),call('draw raw text')]
settings_general=raw_text(V('PLAYER NAME'),140,91)+raw_number(V('SHAKE'),3,101,164)+[resize({'SIZE':inp(100)})]+raw_stamp(add(-94,mul(div(V('SHAKE'),100),270)),16,'slider knob')
settings_general += [resize({'SIZE':inp(100)})]+raw_stamp(sub(add(126,mul(sub(V('DIFFICULTY'),1),66)),210),52,'marker60x24')
settings_rgb=[]
for prefix,offset in [('game',0),('key',120)]:
 for ci,c in enumerate(['r','g','b']):
  yy=112+ci*30+offset;settings_rgb += raw_number(V(prefix+' '+c),3,385,yy)+[resize({'SIZE':inp(100)})]+raw_stamp(add(-98,mul(div(V(prefix+' '+c),255),218)),180-yy,'slider knob')
 settings_rgb += segment(194,38-offset,206,38-offset,packed(prefix),16)
proc('render settings',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('settings panel',V('settings tab')))+raw_stamp(add(-4,mul(sub(V('settings tab'),1),150)),151,'marker140x26')+[If(eq(V('settings tab'),1),settings_general,settings_rgb),If(gt(V('notice until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(-220,-172,join('notice',V('settings notice'))))])
ach_render=[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,'achievements panel')
for slot in range(6):
 x=18+(slot%2)*232;y=80+(slot//2)*70
 ach_render += [setv('achievement index',add(mul(V('achievement page'),6),slot+1)),If(lt(V('achievement index'),51),raw_stamp(x+106-240,180-(y+30.5),join(join(join('achievement',V('achievement index')),'-'),item('unlocked',V('achievement index')))))]
ach_render += raw_number(add(V('achievement page'),1),1,225,319,55)+[resize({'SIZE':inp(100)})]+raw_stamp(0,-139,'history slash')+raw_number(9,1,248,319,55)
proc('render achievements',ach_render)
proc('show settings',[setv('settings return','menu'),setv('hover object',0),setv('SCREEN','settings'),setv('settings tab',1),setv('settings notice','')])
proc('show achievements',[setv('achievement page',0),setv('hover object',0),call('check achievements'),setv('SCREEN','achievements')])
# Route extra pages before the ordinary render dispatcher, retaining its existing branches.
render_def=next(k for k,b in blocks.items() if b['opcode']=='procedures_prototype' and b['mutation']['proccode']=='render')
render_def=blocks[render_def]['parent'];old=blocks[render_def]['next']
wrapper=seq([call('update rainbow'),If(eq(V('SCREEN'),'settings'),[call('render settings')],[If(eq(V('SCREEN'),'achievements'),[call('render achievements')],[If(eq(V('SCREEN'),'cosmetics'),[call('render cosmetics')],[If(eq(V('SCREEN'),'difficulty'),[call('render difficulty')],[old])])])]),call('draw button hover'),
 If(either(eq(V('SCREEN'),'menu'),eq(V('SCREEN'),'history')),raw_text(V('PLAYER NAME'),120 if False else 32,350,60)),
 If(both(eq(item('unlocked',5),1),eq(V('SCREEN'),'menu')),[resize({'SIZE':inp(100)})]+raw_stamp(-58,-170,'spin title')),
 # Each page reserves a different gap for notices, clear of buttons and play cells.
 setv('toast y',-164),
 If(eq(V('SCREEN'),'cosmetics'),[setv('toast y',91)]),
 If(eq(V('SCREEN'),'achievements'),[setv('toast y',-113)]),
 If(eq(V('SCREEN'),'settings'),[setv('toast y',-100),If(eq(V('settings tab'),2),[setv('toast y',-126)])]),
 If(eq(V('SCREEN'),'themes'),[setv('toast y',105)]),
 If(eq(V('SCREEN'),'history'),[setv('toast y',92)]),
 If(eq(V('SCREEN'),'difficulty'),[setv('toast y',91)]),
 If(gt(V('unlock until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(0,V('toast y'),'unlock all toast'),
 [If(gt(V('achievement until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(0,V('toast y'),join('achievement toast',V('achievement notice'))))])])
blocks[render_def]['next']=wrapper;blocks[wrapper]['parent']=render_def
# Settings mouse controls. All drafts preview immediately, Save Profile commits them.
settings_clicks=[If(hit(16,16,100,42),[setv('SCREEN',V('settings return'))]),If(hit(166,16,306,42),[setv('settings tab',1)]),If(hit(316,16,456,42),[setv('settings tab',2)]),If(hit(310,316,462,344),[call('save profile')])]
general_clicks=[If(hit(126,78,456,104),[call('edit name')]),If(hit(424,153,462,175),[setv('SHAKE',0),setv('profile saved',0)])]
for n in range(1,6):general_clicks += [If(hit(126+(n-1)*66,116,186+(n-1)*66,140),[setv('DIFFICULTY',n),setv('profile saved',0)])]
general_clicks += [If(hit(126,214,456,252),[call('show cosmetics')])]
rgb_clicks=[If(hit(18,182,164,202),[setv('game custom',2),setv('profile saved',0)]),If(hit(174,316,296,344),[setv('key custom',2),setv('profile saved',0)]),If(hit(18,316,164,344),[setv('game custom',0),setv('key custom',0),setv('profile saved',0)])]
for ci,yy in enumerate([112,142,172,232,262,292],1):rgb_clicks += [If(hit(376,yy-10,418,yy+10),[setv('color channel',ci),call('edit color value')])]
settings_clicks += [If(eq(V('settings tab'),1),general_clicks,rgb_clicks)]
settings_drags=[If(both(eq(V('settings tab'),1),hit(140,153,420,175)),[setv('SHAKE',floor(mul(div(add(mouse_x(),94),270),100))),call('clamp settings'),setv('profile saved',0)])]
for prefix,offset in [('game',0),('key',120)]:
 for ci,c in enumerate(['r','g','b']):
  yy=112+ci*30+offset
  settings_drags += [If(both(eq(V('settings tab'),2),hit(136,yy-7,366,yy+7)),[setv(prefix+' '+c,floor(mul(div(add(mouse_x(),98),218),255))),setv(prefix+' custom',1),call('clamp settings'),setv('profile saved',0)])]
extra_clicks=[If(eq(V('SCREEN'),'settings'),settings_clicks,[If(eq(V('SCREEN'),'achievements'),[If(hit(16,16,100,42),[setv('SCREEN','menu')]),If(both(hit(96,306,196,334),gt(V('achievement page'),0)),[change('achievement page',-1)]),If(both(hit(284,306,384,334),lt(V('achievement page'),8)),[change('achievement page',1)])],[If(eq(V('SCREEN'),'cosmetics'),[call('cosmetics click')],[If(eq(V('SCREEN'),'difficulty'),[call('difficulty click')],clicks)])])])]
# Replace the click substack only, keeping its edge-trigger guard and original navigation.
for k,b in list(blocks.items()):
 if b['opcode']=='control_if' and b['inputs'].get('SUBSTACK',[None,None])[1]==seq(clicks):
  h=seq(extra_clicks);b['inputs']['SUBSTACK']=[2,h];blocks[h]['parent']=k;break
# Add main-menu buttons after its existing actions (same main-menu branch).
menu_extra=[If(hit(270,266,468,290),[call('show cosmetics')]),If(hit(270,300,358,328),[call('show settings')]),If(hit(364,300,468,328),[call('show achievements')])]
end=menu_clicks[0]
while blocks[end]['next']:end=blocks[end]['next']
h=seq(menu_extra);blocks[end]['next']=h;blocks[h]['parent']=end
# Dragging is continuous; a button click remains edge-triggered.
waitblock=loop[-1];previous=next(k for k,b in blocks.items() if b.get('next')==waitblock)
h=seq([If(both(eq(V('SCREEN'),'settings'),(B('sensing_mousedown'),)),settings_drags)])
blocks[previous]['next']=h;blocks[h]['parent']=previous;blocks[h]['next']=waitblock;blocks[waitblock]['parent']=h

proc('choose difficulty',[If(eq(V('SCREEN'),'play'),[call('open menu')]),setv('hover object',0),setv('SCREEN','difficulty')])
proc('render difficulty',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,'difficulty panel'))
diff_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')])]
for mode in range(1,6):diff_clicks += [If(hit(32,98+(mode-1)*44,448,132+(mode-1)*44),[setv('DIFFICULTY',mode),call('start game')])]
proc('difficulty click',diff_clicks)
proc('show cosmetics',[setv('SCREEN','cosmetics'),setv('cosmetics tab',1),setv('hover object',0),setv('settings notice','')])
cosm_render=[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('cosmetics panel',V('cosmetics tab')))
cosm_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')]),If(hit(18,316,164,344),[call('show settings'),setv('settings tab',2),setv('settings return','cosmetics')]),If(hit(310,316,462,344),[call('save profile')])]
for tab in range(1,5):cosm_clicks += [If(hit(112+(tab-1)*90,16,198+(tab-1)*90,42),[setv('cosmetics tab',tab)])]
for tab,options,variable,requirements,offset in [(1,10,'CLEAR EFFECT',EFFECT_REQUIREMENTS,0),(2,9,'BLOCK SKIN',SKIN_REQUIREMENTS,0),(3,8,'AURA',AURA_REQUIREMENTS,-1),(4,6,'DROP EFFECT',{},0)]:
 draw=[];click=[]
 for index in range(1,options+1):
  x=12+((index-1)%5)*94;y=100+((index-1)//5)*100;choice=index+offset;aid=requirements.get(choice)
  draw += [setv('cosmetic state',0),If(eq(V(variable),choice),[setv('cosmetic state',1)])]
  if aid:draw += [If(neg(eq(item('unlocked',aid),1)),[setv('cosmetic state',2)])]
  draw += raw_stamp(x+41-240,180-(y+41),join('card'+str(tab)+'-'+str(index)+'-',V('cosmetic state')))
  equip=[setv(variable,choice),setv('profile saved',0)]
  if aid:equip=[If(eq(item('unlocked',aid),1),equip,[setv('settings notice','locked'),setv('notice until',add(timer(),2))])]
  click += [If(hit(x,y,x+82,y+82),equip)]
 cosm_render += [If(eq(V('cosmetics tab'),tab),draw)]
 cosm_clicks += [If(eq(V('cosmetics tab'),tab),click)]
cosm_render += [If(gt(V('notice until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(-220,-172,join('notice',V('settings notice'))))]
proc('render cosmetics',cosm_render);proc('cosmetics click',cosm_clicks)
proc('draw combo timer',[If(gt(V('COMBO'),0),segment(-110,145,110,145,0x28344a,7)+segment(-110,145,add(-110,mul(div(sub(V('combo expires'),timer()),V('combo window')),220)),145,0xacecff,6)+[resize({'SIZE':inp(100)})]+raw_stamp(0,164,'combo timer caption'))])
# Independent random walks use the outer stage and the corridors above/below
# the well. The protected rectangle includes max shake and the full sprite size.
COMPANION_FIELDS=['companion '+field for field in ['x','y','vx','vy','turn']]
def random_velocity():return mul(sub(mul(random(0,1),2),1),div(random(6,18),10))
proc('init companions',[clear(name) for name in COMPANION_FIELDS]+[repeat(10,[
 append('companion x',mul(sub(mul(random(0,1),2),1),random(104,218))),append('companion y',random(-162,162)),
 append('companion vx',random_velocity()),append('companion vy',random_velocity()),append('companion turn',random(18,70))])])
def protected(x,y):return both(lt(mathop('abs',x),96),lt(mathop('abs',y),150))
step=[setv('flight x',item('companion x',V('companion index'))),setv('flight y',item('companion y',V('companion index'))),
 If(either(either(gt(mathop('abs',V('flight x')),222),gt(mathop('abs',V('flight y')),164)),protected(V('flight x'),V('flight y'))),[
 setv('flight x',mul(sub(mul(random(0,1),2),1),random(104,218))),setv('flight y',random(-162,162))]),
 replace('companion turn',V('companion index'),sub(item('companion turn',V('companion index')),1)),
 If(lt(item('companion turn',V('companion index')),1),[replace('companion vx',V('companion index'),random_velocity()),replace('companion vy',V('companion index'),random_velocity()),replace('companion turn',V('companion index'),random(18,70))]),
 setv('flight next',add(V('flight x'),item('companion vx',V('companion index')))),
 If(either(gt(mathop('abs',V('flight next')),222),protected(V('flight next'),V('flight y'))),[replace('companion vx',V('companion index'),sub(0,item('companion vx',V('companion index'))))],[setv('flight x',V('flight next'))]),
 setv('flight next',add(V('flight y'),item('companion vy',V('companion index')))),
 If(either(gt(mathop('abs',V('flight next')),164),protected(V('flight x'),V('flight next'))),[replace('companion vy',V('companion index'),sub(0,item('companion vy',V('companion index'))))],[setv('flight y',V('flight next'))]),
 replace('companion x',V('companion index'),V('flight x')),replace('companion y',V('companion index'),V('flight y'))]
proc('step companion',step)
companion_loop=[call('step companion'),setv('bee x',V('flight x')),setv('bee y',V('flight y'))]+raw_stamp(V('flight x'),V('flight y'),join(join(V('companion prefix'),V('companion index')),join('-',mod(floor(add(mul(timer(),12),mul(V('companion index'),3))),4))))+[change('companion index',1)]
valid_flock=eq(length(COMPANION_FIELDS[0]),10)
for name in COMPANION_FIELDS[1:]:valid_flock=both(valid_flock,eq(length(name),10))
scene=[If(neg(valid_flock),[call('init companions')]),setv('companion count',V('LINES')),
 If(gt(V('companion count'),10),[setv('companion count',10)]),If(lt(V('companion count'),0),[setv('companion count',0)]),
 setv('companion prefix','bee'),If(eq(V('THEME'),11),[setv('bee count',V('companion count')),If(gt(V('bee count'),V('max bees')),[setv('max bees',V('bee count'))])],[setv('companion prefix','familiar'),setv('familiar count',V('companion count'))]),
 resize({'SIZE':inp(60)}),setv('companion index',1),repeat(V('companion count'),companion_loop),resize({'SIZE':inp(100*ZOOM)})]
proc('draw companions',[setv('bee count',0),setv('familiar count',0),If(either(eq(V('THEME'),11),eq(V('THEME'),12)),scene)])
proc('draw bees',[call('draw companions')])
bee_tokens=[resize({'SIZE':inp(70)}),effect('GHOST',mul(V('fx age'),3))]
for token,bx,by in [(1,-208,-140),(3,208,-140),(4,208,140)]:
 bee_tokens+=raw_stamp(bx,by,join('bee token'+str(token)+'-',mod(floor(mul(timer(),12)),4)))
bee_tokens += [B('looks_cleargraphiceffects'),resize({'SIZE':inp(100*ZOOM)})]
proc('draw bee tokens',[If(both(eq(V('THEME'),11),eq(V('fx active'),1)),bee_tokens)])
# Timed first-clear buffs and combo-held buffs share badges, never game modifiers.
proc('clear combo buffs',[clear('combo buff stacks'),repeat(12,[append('combo buff stacks',0)]),setv('combo buffs active',0)])
proc('reset bee buffs',[clear('buff stacks'),clear('buff life'),repeat(12,[append('buff stacks',0),append('buff life',0)]),call('clear combo buffs')])
def ensure_buffs():return If(neg(both(eq(length('buff stacks'),12),both(eq(length('buff life'),12),eq(length('combo buff stacks'),12)))),[call('reset bee buffs')])
proc('grant combo buffs',[If(both(eq(V('THEME'),11),gt(V('COMBO'),1)),[ensure_buffs(),clear('buff pool'),repeat(12,[append('buff pool',add(length('buff pool'),1))]),repeat(5,[
 setv('buff pick',random(1,length('buff pool'))),setv('buff choice',item('buff pool',V('buff pick'))),delete('buff pool',V('buff pick')),
 replace('combo buff stacks',V('buff choice'),add(item('combo buff stacks',V('buff choice')),1)),If(gt(item('combo buff stacks',V('buff choice')),99),[replace('combo buff stacks',V('buff choice'),99)])]),setv('combo buffs active',1)])])
proc('grant bee buff',[If(eq(V('THEME'),11),[ensure_buffs(),If(gt(V('COMBO'),1),[call('grant combo buffs')],[setv('buff choice',random(1,12)),
 replace('buff stacks',V('buff choice'),add(item('buff stacks',V('buff choice')),1)),If(gt(item('buff stacks',V('buff choice')),99),[replace('buff stacks',V('buff choice'),99)]),replace('buff life',V('buff choice'),240)])])])
buff_draw=[setv('buff y',sub(124,mul(V('buff slot'),24))),resize({'SIZE':inp(100)}),
 If(both(eq(item('combo buff stacks',V('buff index')),0),lt(item('buff life',V('buff index')),60)),[effect('GHOST',mul(sub(60,item('buff life',V('buff index'))),1.5))]),
 If(gt(item('combo buff stacks',V('buff index')),0),raw_stamp(-220,V('buff y'),'combo buff badge'),raw_stamp(-220,V('buff y'),'buff badge')),
 resize({'SIZE':inp(70)})]+raw_stamp(-228,V('buff y'),join('buff icon',V('buff index')))+[
 resize({'SIZE':inp(100)})]+raw_stamp(-217.5,sub(V('buff y'),1),'buff multiplier')+[
 setv('number value',V('buff total')),setv('number digits',1),If(gt(V('buff total'),9),[setv('number digits',2)]),setv('number scale',40),setv('number spacing',4.5),setv('number x',-214),setv('number y',sub(V('buff y'),3)),call('draw raw number'),B('looks_cleargraphiceffects'),
 If(both(both(gt(mouse_x(),-237),lt(mouse_x(),-203)),both(gt(mouse_y(),sub(V('buff y'),11)),lt(mouse_y(),add(V('buff y'),11)))),[resize({'SIZE':inp(100)})]+raw_stamp(-150,139,join('buff label',V('buff index')))),change('buff slot',1)]
buff_loop=[If(gt(item('buff life',V('buff index')),0),[
 replace('buff life',V('buff index'),sub(item('buff life',V('buff index')),1)),If(eq(item('buff life',V('buff index')),0),[replace('buff stacks',V('buff index'),0)])]),
 setv('buff total',add(item('buff stacks',V('buff index')),item('combo buff stacks',V('buff index')))),If(gt(V('buff total'),99),[setv('buff total',99)]),If(gt(V('buff total'),0),buff_draw),change('buff index',1)]
proc('draw bee buffs',[If(both(eq(V('COMBO'),0),eq(V('combo buffs active'),1)),[call('clear combo buffs')]),If(eq(V('THEME'),11),[ensure_buffs(),setv('buff index',1),setv('buff slot',0),repeat(12,buff_loop),resize({'SIZE':inp(100*ZOOM)})])])
wisp_loop=[setv('wisp x',mul(sub(mul(mod(add(V('wisp kind'),V('wisp index')),2),2),1),add(108,mod(add(add(mul(V('wisp kind'),13),mul(V('wisp index'),29)),mul(mathop('sin',mul(timer(),60)),10)),105)))),
 setv('wisp y',sub(mod(add(add(mul(timer(),40),mul(V('wisp kind'),37)),mul(V('wisp index'),101)),280),140))]+raw_stamp(V('wisp x'),V('wisp y'),join(join('buff wisp',V('wisp kind')),join('-',mod(floor(mul(timer(),8)),4))))+[change('wisp index',1)]
proc('draw combo wisps',[If(both(eq(V('THEME'),11),gt(V('COMBO'),1)),[ensure_buffs(),resize({'SIZE':inp(65)}),setv('wisp kind',1),repeat(12,[
 setv('wisp count',item('combo buff stacks',V('wisp kind'))),If(gt(V('wisp count'),4),[setv('wisp count',4)]),setv('wisp index',1),repeat(V('wisp count'),wisp_loop),change('wisp kind',1)]),resize({'SIZE':inp(100*ZOOM)})])])
# A Space edge records the actual piece center and landing before lock/spawn.
# Each ribbon spans the rotated piece's occupied columns; every layer stays
# inside those edges. Its vertical endpoints still follow the actual drop.
def trail_stroke(color,width,offset=0,base_alpha=0):
 return segment(add(V('drop center x'),mul(V('drop width'),offset)),V('drop from y'),add(V('drop center x'),mul(V('drop width'),offset)),V('drop to y'),color,mul(V('drop width'),width*ZOOM),True,add(base_alpha,mul(V('dash age'),(95-base_alpha)/20)))
drop_styles={
 1:trail_stroke(0xffffff,.08),
 2:trail_stroke(packed('game'),.12)+trail_stroke(0xffffff,.04),
 3:trail_stroke(0xffffff,.04),
 4:trail_stroke(0xfff1bf,.12),
 5:trail_stroke(0xe9ffff,.1)+trail_stroke(0x9ddcff,.04,-.43)+trail_stroke(0x9ddcff,.04,.43),
 6:trail_stroke(0xf6e2ff,.06)}
drop_draw=[]
for style,strokes in drop_styles.items():drop_draw += [If(eq(V('drop style'),style),strokes)]
drop_tiles=stamp(V('drop center x'),sub(sub(V('drop from y'),8),mul(V('drop tile'),16)),join(join('drop band',V('drop style')),join('-',div(V('drop width'),16))))+[change('drop tile',1)]
proc('draw drop dash',[If(eq(V('dash active'),1),[resize({'SIZE':inp(100*ZOOM)}),effect('GHOST',mul(V('dash age'),4)),setv('drop tile',0),repeat(V('drop rows'),drop_tiles),B('looks_cleargraphiceffects')]+drop_draw+[resize({'SIZE':inp(mul(div(V('drop width'),24),100*ZOOM))}),effect('GHOST',mul(V('dash age'),4))]+stamp(V('drop center x'),V('drop to y'),join(join('drop tip',V('drop style')),join('-',floor(div(mul(V('dash age'),6),20)))))+[
 B('looks_cleargraphiceffects'),resize({'SIZE':inp(100*ZOOM)}),change('dash age',1),If(gt(V('dash age'),19),[setv('dash active',0)])])])
TEAR_FIELDS=['tear '+field for field in ['x','y','vx','vy','kind']]
proc('clear isaac tears',[clear(name) for name in TEAR_FIELDS])
proc('start isaac tears',[call('clear isaac tears'),If(eq(V('fx style'),11),[setv('tear row',1),repeat(length('clear rows'),[
 setv('tear origin y',sub(152,mul(item('clear rows',V('tear row')),16))),setv('tear spawn',0),repeat(8,[append('tear x',random(-68,68)),append('tear y',V('tear origin y')),append('tear vx',div(random(-18,18),10)),append('tear vy',div(random(32,64),10)),append('tear kind',add(mod(V('tear spawn'),4),1)),change('tear spawn',1)]),change('tear row',1)])])])
tear_loop=[replace('tear x',V('tear index'),add(item('tear x',V('tear index')),item('tear vx',V('tear index')))),
 replace('tear y',V('tear index'),add(item('tear y',V('tear index')),item('tear vy',V('tear index')))),replace('tear vy',V('tear index'),sub(item('tear vy',V('tear index')),.3)),
 If(both(lt(mathop('abs',item('tear x',V('tear index'))),73),lt(mathop('abs',item('tear y',V('tear index'))),150)),stamp(item('tear x',V('tear index')),item('tear y',V('tear index')),join(join('isaac tear',item('tear kind',V('tear index'))),join('-',mod(floor(div(V('fx age'),2)),4))))),change('tear index',1)]
tear_splashes=[]
for i,xx in enumerate([-48,0,48]):tear_splashes+=stamp(xx,sub(152,mul(item('clear rows',V('tear row')),16)),join('tear splash'+str(i+1)+'-',floor(div(V('fx age'),4))))
proc('draw isaac tears',[If(both(eq(V('fx active'),1),eq(V('fx style'),11)),[resize({'SIZE':inp(100*ZOOM)}),effect('GHOST',mul(V('fx age'),3)),setv('tear row',1),repeat(length('clear rows'),tear_splashes+[change('tear row',1)]),setv('tear index',1),repeat(length('tear x'),tear_loop),B('looks_cleargraphiceffects')])])
# Button lighting shares one layout catalogue with the generated SVGs.
from interface import BUTTONS,button_glow
button_lookup=[]
for screen in dict.fromkeys(button[0] for button in BUTTONS):
 options=[]
 for button_id,(button_screen,tab,box,label) in enumerate(BUTTONS,1):
  if button_screen!=screen:continue
  match=hit(*box)
  if tab:match=both(eq(V('settings tab' if screen=='settings' else 'cosmetics tab'),tab),match)
  options += [If(match,[setv('button hovered',button_id)])]
 button_lookup += [If(eq(V('SCREEN'),screen),options)]
proc('update button hover',[setv('button hovered',0)]+button_lookup)
proc('draw button hover',[call('update button hover'),If(gt(V('button hovered'),0),[resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('button glow',V('button hovered')))+[
 If(eq(V('SCREEN'),'play'),[resize({'SIZE':inp(100*ZOOM)})])])])
# establish parent pointers for reporter input blocks
for k,b in list(blocks.items()):
 for v in b['inputs'].values():
  if len(v)>1 and isinstance(v[1],str) and v[1] in blocks:blocks[v[1]]['parent']=k
assets={}
def costume(name,svg,cx,cy):
 data=svg.encode();md=hashlib.md5(data).hexdigest();assets[md+'.svg']=data
 return dict(name=name,assetId=md,dataFormat='svg',md5ext=md+'.svg',rotationCenterX=cx,rotationCenterY=cy)
from visuals import COLORS, THEME_NAMES, THEME_PALETTES, landscape, block, arena, digit, gameover, badge, clear_beam, particle, svg, text, rect, menu, menu_button, keycap, combo_banner, theme_menu, history_panel, arrow_keycap, combo_title, COMBO_NAMES, hover_outline, hover_object, ambient_spark
from settings_art import settings_panel, select_marker, slider_knob, save_notice, achievements_panel, achievement_tile, ACHIEVEMENTS
from effects_art import elemental_beam, particle_skin, cosmetic_block, aura
from expansion_art import bee,bee_token,logo,menu_cosmetics,difficulty_panel,BEE_NAMES
from cosmetics_art import card
from scene_art import familiar,FAMILIAR_NAMES,brimstone_beam,brimstone_spark,buff_icon,buff_label,buff_wisp,BUFF_NAMES
from impact_art import DROP_NAMES,drop_tip,drop_band,tear,tear_splash
costumes=[]
for theme,palette in enumerate(THEME_PALETTES,1):
 costumes += [costume('t'+str(theme)+'-'+str(i+1),block(c,theme=theme),8,8) for i,c in enumerate(palette)]
 costumes += [costume('t'+str(theme)+'-'+str(i+8),block(c,True,theme=theme),8,8) for i,c in enumerate(palette)]
costumes += [costume('digit'+str(i),digit(i),0,13) for i in range(10)]
costumes += [costume('gameover',gameover(),80,160)]
costumes += [costume('clear'+str(i),badge(i),60,7) for i in range(1,5)]
costumes += [costume('beam'+str(i),clear_beam(i),80,8) for i in range(10)]
costumes += [costume('quadbeam'+str(i),clear_beam(i,True),80,8) for i in range(10)]
costumes += [costume('spark',particle('#cceeff'),3,3)]
costumes += [costume('tspin',svg(text(60,10,'T-SPIN',8.5,'#d4a5ff',300,extra='text-anchor="middle" letter-spacing="2"'),120,14),60,7)]
costumes += [costume('interface',arena(),240,180)]
costumes += [costume('combo timer',svg(rect(0,0,110,2,'#b8eeff'),110,2),0,1)]
costumes += [costume('menu button',menu_button(),46,12)]
for theme in range(1,13):
 for resume in [False,True]:
  costumes += [costume('menu'+str(theme)+('-resume' if resume else '-play'),menu(theme,resume),240,180)]
 costumes += [costume('theme menu'+str(theme),theme_menu(theme),240,180)]
 costumes += [costume('history theme'+str(theme),svg(text(0,10,THEME_NAMES[theme-1].upper(),9,'#d5d8eb',300),170,14),0,7)]
for arrow,k in [('↑','w'),('←','a'),('↓','s'),('→','d')]:
 for pressed in [False,True]:
  costumes += [costume('arrow'+k+'-'+str(pressed).lower(),arrow_keycap(arrow,pressed),20,13)]
for n in range(1,16):costumes += [costume('title'+str(n),combo_title(n),60,7)]
costumes += [costume('history panel',history_panel(),240,180)]
for status in ['Playing','Paused','Stopped','Restarted','Game Over']:
 costumes += [costume('history status'+status,svg(text(0,10,status.upper(),6.5,'#959fba',300),170,14),0,7)]
costumes += [costume('history empty',svg(text(150,16,'NO RUNS YET',12,'#aab3cc',300,extra='text-anchor="middle"'),300,24),150,12)]
costumes += [costume('history slash',svg(text(5,11,'/',11,'#aab3cc',300,extra='text-anchor="middle"'),10,16),5,8)]
costumes += [costume('ambient spark',ambient_spark(),3,3)]
for kind in list(range(1,8))+list(range(11,23)):
 costumes += [costume('outline'+str(kind),hover_outline(kind),240,180)]
 for frame in range(8):costumes += [costume('object'+str(kind)+'-'+str(frame),hover_object(kind,frame),60,60)]
for kind in range(1,11):
 costumes += [costume('element'+str(kind)+'-'+str(f),elemental_beam(kind,f),80,16 if kind==5 else 8) for f in range(10)]
 costumes += [costume('element spark'+str(kind),particle_skin(kind),6 if kind==5 else 4,6 if kind==5 else 4)]
for style in range(2,10):
 for i,c in enumerate(THEME_PALETTES[0],1):
  costumes += [costume('skin'+str(style)+'-'+str(i),cosmetic_block(c,style),8,8),costume('skin'+str(style)+'-'+str(i+7),cosmetic_block(c,style,True),8,8)]
for style in range(1,8):costumes += [costume('aura'+str(style)+'-'+str(f),aura(style,f),84,164) for f in range(8)]
for tab in [1,2]:costumes += [costume('settings panel'+str(tab),settings_panel(tab),240,180)]
for w,h in [(60,24),(100,24),(84,28),(106,24),(100,16),(140,26)]:costumes += [costume('marker'+str(w)+'x'+str(h),select_marker(w,h),w/2,h/2)]
costumes += [costume('slider knob',slider_knob(),6,6)]
for kind in ['saved','locked','name']:costumes += [costume('notice'+kind,save_notice(kind),0,9)]
costumes += [costume('small lock',svg(rect(3,5,7,6,'#8799b6',r=1)+'<path d="M4 5V3a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="#bed1ea"/>',12,12),6,6)]
costumes += [costume('achievements panel',achievements_panel(),240,180)]
for i in range(1,51):
 for unlocked in [0,1]:costumes += [costume('achievement'+str(i)+'-'+str(unlocked),achievement_tile(i,bool(unlocked)),106,30.5)]
 costumes += [costume('achievement toast'+str(i),svg(rect(.5,.5,189,17,'#0a1821','#5e9d87',3,extra='stroke-width=".5"')+text(95,12,'UNLOCKED / '+ACHIEVEMENTS[i-1][2].upper(),8,'#b9f5d7',300,extra='text-anchor="middle"'),190,18),95,9)]
costumes += [costume('spin title',svg(text(0,10,'SPIN ARTIST',6.5,'#d5bcff',300,extra='letter-spacing="1"'),100,14),0,7)]
for arrow,k in [('↑','w'),('←','a'),('↓','s'),('→','d')]:costumes += [costume('arrow glyph'+k,svg(text(20,18,arrow,16,'#fff',300,extra='text-anchor="middle"'),40,26),20,13)]
for i,label in enumerate(['EASY','NORMAL','HARD','EXPERT','NIGHTMARE'],1):costumes += [costume('history difficulty'+str(i),svg(text(0,10,label,6.5,'#b3d9ef',300),65,14),0,7)]
NAME_ALPHABET=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -_')
for i,c in enumerate(NAME_ALPHABET,1):costumes += [costume('letter'+str(i),svg(text(0,16,c,17,'#ecf5ff',300),12,20),0,10)]
lists['name alphabet']=['name alphabet',NAME_ALPHABET]
lists['gravity choices']=['gravity choices',[60,35,15,8,3]];lists['lock choices']=['lock choices',[35,25,12,8,5]];lists['combo choices']=['combo choices',[12,10,7,5,4]]
for tab,options in [(1,10),(2,9),(3,8),(4,6)]:
 costumes += [costume('cosmetics panel'+str(tab),menu_cosmetics(tab),240,180)]
 for option in range(1,options+1):
  for state in range(3):costumes += [costume('card'+str(tab)+'-'+str(option)+'-'+str(state),card(tab,option,state),41,41)]
costumes += [costume('difficulty panel',difficulty_panel(),240,180),costume('edition logo',logo(),80,30)]
costumes += [costume('combo timer caption',svg(text(110,10,'COMBO WINDOW',6.5,'#b2ccdf',300,extra='text-anchor="middle" letter-spacing="1.5"'),220,14),110,7)]
costumes += [costume('unlock all toast',svg(rect(.5,.5,239,17,'#0a1821','#5e9d87',3,extra='stroke-width=".5"')+text(120,12,'ALL COSMETICS UNLOCKED',9,'#c5f5d8',300,extra='text-anchor="middle"'),240,18),120,9)]
for i in range(1,11):
 for frame in range(4):costumes += [costume('bee'+str(i)+'-'+str(frame),bee(i,frame),24,18)]
for i in [1,2,3,4]:
 for frame in range(4):costumes += [costume('bee token'+str(i)+'-'+str(frame),bee_token(i,frame),16,16)]
for i in range(1,11):
 for frame in range(4):costumes += [costume('familiar'+str(i)+'-'+str(frame),familiar(i,frame),24,20)]
for frame in range(10):
 costumes += [costume('element11-'+str(frame),brimstone_beam(frame),80,14)]
costumes += [costume('element spark11',brimstone_spark(),6,6),costume('buff badge',svg(rect(.5,.5,33,21,'#0d1c24','#d7c56d',4,extra='stroke-width=".6"'),34,22),17,11),costume('combo buff badge',svg(rect(.5,.5,33,21,'#10262c','#9ef9df',4,extra='stroke-width=".9"')+rect(1,4,1,14,'#baffea',r=.5),34,22),17,11)]
costumes += [costume('buff multiplier',svg(text(3,6.5,'×',7,'#dff8ec',300,extra='text-anchor="middle"'),6,8),3,4)]
for i in range(1,13):
 costumes += [costume('buff icon'+str(i),buff_icon(i),10,10),costume('buff label'+str(i),buff_label(i),30,6)]
 for frame in range(4):costumes += [costume('buff wisp'+str(i)+'-'+str(frame),buff_wisp(i,frame),12,12)]
for i in range(1,7):
 for frame in range(6):costumes += [costume('drop tip'+str(i)+'-'+str(frame),drop_tip(i,frame),12,12)]
 for cells in range(1,5):costumes += [costume('drop band'+str(i)+'-'+str(cells),drop_band(i,cells),cells*8,8)]
for i in range(1,5):
 for frame in range(4):costumes += [costume('isaac tear'+str(i)+'-'+str(frame),tear(i,frame),6,8)]
 for frame in range(6):costumes += [costume('tear splash'+str(i)+'-'+str(frame),tear_splash(i,frame),16,8)]
for i,(_,_,box,_) in enumerate(BUTTONS,1):costumes += [costume('button glow'+str(i),button_glow(box),240,180)]
lists['achievement names']=['achievement names',[a[0] for a in ACHIEVEMENTS]]
lists['bee names']=['bee names',[n+' Bee' for n in BEE_NAMES]]
lists['familiar names']=['familiar names',FAMILIAR_NAMES]
lists['buff names']=['buff names',BUFF_NAMES]
lists['drop names']=['drop names',DROP_NAMES]
lists['button labels']=['button labels',[button[3] for button in BUTTONS]]
backdrops=[costume('theme'+str(i),landscape(i),240,180) for i in range(1,13)]
# Matrix order: I J L O S T Z. Rotation around SRS centers.
bases=[[(0,1),(1,1),(2,1),(3,1)],[(0,0),(0,1),(1,1),(2,1)],[(2,0),(0,1),(1,1),(2,1)],[(1,0),(2,0),(1,1),(2,1)],[(1,0),(2,0),(0,1),(1,1)],[(1,0),(0,1),(1,1),(2,1)],[(0,0),(1,0),(1,1),(2,1)]]
matrices=[]
for p,base in enumerate(bases):
 cells=base
 for rot in range(4):
  matrices.append(''.join('1' if (x,y) in cells else '0' for y in range(4) for x in range(4)))
  if p!=3:
   center=1.5 if p==0 else 1
   cells=[(int(center-(y-center)),int(center+(x-center))) for x,y in cells]
lists['shapes']=['shapes',matrices];lists['kick x']=['kick x',[0,-1,1,-2,2,0,0]];lists['kick y']=['kick y',[0,0,0,0,0,-1,-2]];lists['points']=['points',[100,300,500,800]];lists['spin points']=['spin points',[400,800,1200,1600]]
lists['combo names']=['combo names',COMBO_NAMES]
for n in ['ground ticks','BEST SCORE','run serial','run record open']:var(n)
monitors=[]
stage=dict(isStage=True,name='Stage',variables={},lists={},broadcasts={},blocks={},comments={},currentCostume=0,costumes=backdrops,sounds=[],volume=100,layerOrder=0,tempo=60,videoTransparency=50,videoState='on',textToSpeechLanguage=None)
sprite=dict(isStage=False,name='Engine',variables=variables,lists=lists,broadcasts={},blocks=blocks,comments={},currentCostume=0,costumes=costumes,sounds=[],volume=100,layerOrder=1,visible=False,x=0,y=0,size=100,direction=90,draggable=False,rotationStyle='all around')
project=dict(targets=[stage,sprite],monitors=monitors,extensions=['pen'],meta={'semver':'3.0.0','vm':'5.0.300','agent':'Tetris Vnanzero Edition builder'})
ROOT.joinpath('dist').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT/'dist/stack-flow.sb3','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('project.json',json.dumps(project))
 for path,data in assets.items():z.writestr(path,data)
print(f'Built {len(blocks)} blocks, {len(assets)} assets → dist/stack-flow.sb3')

(ROOT/'dist/tetris-vnanzero-edition.sb3').write_bytes((ROOT/'dist/stack-flow.sb3').read_bytes())
