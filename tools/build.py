"""Build an original Scratch 3 falling-block game using native Scratch blocks."""
import json, zipfile, hashlib, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
ZOOM=.82
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

PROFILE_FIELDS=['PLAYER NAME','SHAKE','DIFFICULTY','CLEAR EFFECT','BLOCK SKIN','AURA','game r','game g','game b','key r','key g','key b','game custom','key custom']
DEFAULTS={'PLAYER NAME':'PLAYER','SHAKE':50,'DIFFICULTY':2,'CLEAR EFFECT':1,'BLOCK SKIN':1,'AURA':0,'game r':150,'game g':112,'game b':255,'key r':125,'key g':190,'key b':255,'game custom':0,'key custom':0}
def packed(prefix):return add(add(mul(V(prefix+' r'),65536),mul(V(prefix+' g'),256)),V(prefix+' b'))
def segment(x1,y1,x2,y2,color,width,world=False):
 move=position if world else lambda x,y:B('motion_gotoxy',{'X':inp(x),'Y':inp(y)})
 return [B('pen_penUp'),B('pen_setPenColorToColor',{'COLOR':inp(color)}),B('pen_setPenSizeTo',{'SIZE':inp(width)}),move(x1,y1),B('pen_penDown'),move(x2,y2),B('pen_penUp')]
proc('validate cosmetics',[
 If(both(eq(V('BLOCK SKIN'),2),neg(eq(item('unlocked',1),1))),[setv('BLOCK SKIN',1)]),
 If(both(eq(V('BLOCK SKIN'),3),neg(eq(item('unlocked',2),1))),[setv('BLOCK SKIN',1)]),
 If(both(eq(V('BLOCK SKIN'),4),neg(eq(item('unlocked',3),1))),[setv('BLOCK SKIN',1)]),
 If(both(eq(V('AURA'),1),neg(eq(item('unlocked',4),1))),[setv('AURA',0)]),
 If(both(eq(V('AURA'),2),neg(eq(item('unlocked',6),1))),[setv('AURA',0)])])
clamps=[]
for name,lo,hi in [('SHAKE',0,100),('DIFFICULTY',1,3),('CLEAR EFFECT',1,5),('BLOCK SKIN',1,4),('AURA',0,2)]+[(p+' '+c,0,255) for p in ['game','key'] for c in ['r','g','b']]+[('game custom',0,1),('key custom',0,1)]:
 clamps += [setv(name,floor(V(name))),If(lt(V(name),lo),[setv(name,lo)]),If(gt(V(name),hi),[setv(name,hi)])]
proc('clamp settings',clamps+[call('validate cosmetics')])
proc('save profile',[call('clamp settings'),call('checkpoint run'),clear('saved profile'),append('saved profile',1)]+[append('saved profile',V(n)) for n in PROFILE_FIELDS]+[setv('profile saved',1),setv('settings notice','saved'),setv('notice until',add(timer(),2))])
proc('init profile',[If(neg(eq(V('profile ready'),1)),[setv(n,v) for n,v in DEFAULTS.items()]+[clear('unlocked'),repeat(6,[append('unlocked',0)]),setv('lifetime lines',0),setv('lifetime spins',0),setv('lifetime quads',0),setv('profile ready',1),call('save profile'),setv('settings notice','')]),
 until(neg(lt(length('unlocked'),6)),[append('unlocked',0)]),until(neg(lt(length('run difficulties'),length('run ids'))),[append('run difficulties',2)]),until(neg(gt(length('run difficulties'),length('run ids'))),[delete('run difficulties',length('run difficulties'))])])
proc('load profile',[call('init profile'),If(both(eq(length('saved profile'),15),eq(item('saved profile',1),1)),[setv(n,item('saved profile',i+2)) for i,n in enumerate(PROFILE_FIELDS)]+[call('clamp settings')]),setv('settings notice','')])
# Saved profile is version plus fourteen fields, deliberately separate from live progress.
proc('sanitize name',[setv('PLAYER NAME',''),setv('name index',1),repeat(12,[setv('name char',R('operator_letter_of',LETTER=V('name index'),STRING=V('name draft'))),
 If(both(neg(eq(V('name char'),'')),gt((B('data_itemnumoflist',{'ITEM':inp(V('name char'))},{'LIST':['name alphabet',lst('name alphabet')]}),),0)),[setv('PLAYER NAME',join(V('PLAYER NAME'),V('name char')))]),change('name index',1)]),
 If(eq(V('PLAYER NAME'),''),[setv('PLAYER NAME','PLAYER')]),setv('profile saved',0)])
color_fields=[p+' '+c for p in ['game','key'] for c in ['r','g','b']]
color_entry=[]
for i,name in enumerate(color_fields,1):color_entry += [If(eq(V('color channel'),i),[setv(name,(B('sensing_answer'),)),setv(name.split()[0]+' custom',1)])]
proc('edit color value',[B('sensing_askandwait',{'QUESTION':inp('RGB value: enter a number from 0 to 255')})]+color_entry+[call('clamp settings'),setv('profile saved',0),call('sync inputs')])
proc('edit name',[B('sensing_askandwait',{'QUESTION':inp('Name: up to 12 letters, numbers, spaces, - or _')}),setv('name draft',(B('sensing_answer'),)),call('sanitize name'),setv('settings notice','name'),setv('notice until',add(timer(),2)),call('sync inputs')])
proc('apply difficulty',[setv('gravity base',item('gravity choices',V('DIFFICULTY'))),setv('lock limit',item('lock choices',V('DIFFICULTY'))),setv('run difficulty',V('DIFFICULTY'))])
ach_conditions=[gt(V('lifetime lines'),0),gt(V('lifetime lines'),9),gt(V('run max combo'),4),gt(V('lifetime quads'),0),gt(V('lifetime spins'),0),gt(V('BEST SCORE'),4999)]
ach=[]
for i,c in enumerate(ach_conditions,1):
 ach += [If(both(c,neg(eq(item('unlocked',i),1))),[replace('unlocked',i,1),setv('achievement notice',i),setv('achievement until',add(timer(),3))])]
proc('check achievements',ach)
proc('draw raw text',[resize({'SIZE':inp(V('text scale'))}),setv('text index',1),repeat(R('operator_length',STRING=V('text value')),[setv('text char',R('operator_letter_of',LETTER=V('text index'),STRING=V('text value'))),
 setv('text glyph',(B('data_itemnumoflist',{'ITEM':inp(V('text char'))},{'LIST':['name alphabet',lst('name alphabet')]}),)),If(gt(V('text glyph'),0),raw_stamp(V('text x'),V('text y'),join('letter',V('text glyph')))),change('text x',mul(V('text scale'),.12)),change('text index',1)])])
# Four-second rolling combo window uses Scratch's real clock, not frame counts.
proc('update combo',[If(both(gt(V('COMBO'),0),gt(timer(),V('combo expires'))),[setv('COMBO',0),setv('combo expires',0),setv('combo animating',0)])])
proc('clear combo',[If(either(eq(V('COMBO'),0),gt(timer(),V('combo expires'))),[setv('COMBO',1)],[change('COMBO',1)]),
 setv('combo pulse',0),setv('combo animating',1),If(gt(V('COMBO'),V('run max combo')),[setv('run max combo',V('COMBO'))]),setv('combo expires',add(timer(),4)),setv('combo bonus',mul(mul(sub(V('COMBO'),1),50),V('LEVEL')))])
proc('update camera',[setv('shake x',0),setv('shake y',0),If(gt(V('shake ticks'),0),[
 setv('shake amount',mul(mul(div(V('shake ticks'),10),div(V('SHAKE'),100)),8)),
 If(eq(mod(V('shake ticks'),2),0),[setv('shake x',V('shake amount'))],[setv('shake x',sub(0,V('shake amount')))]),
 If(eq(mod(V('shake ticks'),3),0),[setv('shake y',mul(V('shake amount'),-.5))],[setv('shake y',mul(V('shake amount'),.5))]),change('shake ticks',-1)])])
proc('apply theme',[B('looks_switchbackdropto',{'BACKDROP':inp(join('theme',V('THEME')))})])
proc('next theme',[setv('THEME',add(mod(V('THEME'),10),1)),call('apply theme')])

history_columns=['run ids','run scores','run lines','run combos','run themes','run status','run difficulties']
proc('checkpoint run',[If(eq(V('run record open'),1),[
 If(gt(V('COMBO'),V('run max combo')),[setv('run max combo',V('COMBO'))]),
 replace('run scores',1,V('SCORE')),replace('run lines',1,V('LINES')),replace('run combos',1,V('run max combo')),replace('run themes',1,V('THEME')),
 If(gt(V('SCORE'),V('BEST SCORE')),[setv('BEST SCORE',V('SCORE'))])])])
proc('finish run',[If(eq(V('run record open'),1),[call('checkpoint run'),replace('run status',1,V('finish reason')),setv('run record open',0)])])
proc('begin run',[change('run serial',1),setv('run max combo',0),insert('run ids',1,V('run serial')),insert('run scores',1,0),insert('run lines',1,0),insert('run combos',1,0),insert('run themes',1,V('THEME')),insert('run status',1,'Playing'),insert('run difficulties',1,V('run difficulty')),
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
 If(eq(V('valid'),1),[setv('x',V('tx')),setv('y',V('ty')),setv('rotation',V('tr')),setv('rotated',1),setv('last rotation',1),change('SCORE',5)])]),change('kick',1)])])
proc('detect spin',[setv('t spin',0),setv('corners',0),
 If(both(eq(V('piece'),6),eq(V('last rotation'),1)),[setv('corner',0),repeat(4,[
  setv('cx',add(V('x'),mul(mod(V('corner'),2),2))),setv('cy',add(V('y'),mul(floor(div(V('corner'),2)),2))),
  If(out_of_bounds('cx','cy'),[change('corners',1)],[If(gt(item('board',idx(V('cx'),V('cy'))),0),[change('corners',1)])]),change('corner',1)]),
  If(gt(V('corners'),2),[setv('t spin',1)])])])

# All effects are native Scratch pen stamps; their state expires after 24 frames.
proc('start clear fx',[clear('clear rows'),setv('fx row',1),repeat(length('pending clear rows'),[
 append('clear rows',item('pending clear rows',V('fx row'))),change('fx row',1)]),
 setv('shake ticks',10),setv('fx active',1),setv('fx age',0),clear('particle x'),clear('particle y'),clear('particle vx'),clear('particle vy'),
 setv('fx row',1),repeat(length('clear rows'),[setv('fx y',sub(152,mul(item('clear rows',V('fx row')),16))),repeat(12,[
 append('particle x',random(-74,74)),append('particle y',V('fx y')),append('particle vx',div(random(-30,30),10)),append('particle vy',div(random(15,55),10))]),change('fx row',1)])])
proc('lock',[call('detect spin'),setv('shape',shape(V('piece'),V('rotation'))),setv('tx',V('x')),setv('ty',V('y')),setv('i',0),
 repeat(16,[If(eq(cell(),1),coords()+[replace('board',idx(V('cx'),V('cy')),V('piece'))]),change('i',1)]),
 setv('row',19),setv('cleared',0),clear('pending clear rows'),repeat(20,[setv('full',1),setv('col',0),repeat(10,[
 If(eq(item('board',idx(V('col'),V('row'))),0),[setv('full',0)]),change('col',1)]),
 If(eq(V('full'),1),[append('pending clear rows',sub(V('row'),V('cleared'))),repeat(10,[delete('board',add(mul(V('row'),10),1))]),
 repeat(10,[B('data_insertatlist',{'INDEX':inp(1),'ITEM':inp(0)},{'LIST':['board',lst('board')]})]),change('cleared',1)],[change('row',-1)])]),
 change('LINES',V('cleared')),change('lifetime lines',V('cleared')),If(eq(V('cleared'),4),[change('lifetime quads',1)]),If(eq(V('t spin'),1),[change('lifetime spins',1)]),setv('awarded',0),
 If(eq(V('t spin'),1),[setv('awarded',mul(item('spin points',add(V('cleared'),1)),V('LEVEL'))),setv('notification','tspin'),setv('flash',42)],
 [If(gt(V('cleared'),0),[setv('awarded',mul(item('points',V('cleared')),V('LEVEL'))),setv('notification',join('clear',V('cleared'))),setv('flash',36)])]),
 change('SCORE',V('awarded')),If(gt(V('cleared'),0),[call('clear combo'),change('SCORE',V('combo bonus')),call('start clear fx')]),
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
 If(lt(V('fx age'),20),[If(either(eq(length('clear rows'),4),eq(V('notification'),'tspin')),[setv('fx beam','quadbeam')],[setv('fx beam','beam')]),setv('fx row',1),repeat(length('clear rows'),
 stamp(0,sub(152,mul(item('clear rows',V('fx row')),16)),join(join('element',V('CLEAR EFFECT')),join('-',floor(div(V('fx age'),2)))))+[change('fx row',1)])]),
 effect('GHOST',mul(V('fx age'),4)),setv('particle',1),repeat(length('particle x'),[
 replace('particle x',V('particle'),add(item('particle x',V('particle')),item('particle vx',V('particle')))),
 replace('particle y',V('particle'),add(item('particle y',V('particle')),item('particle vy',V('particle')))),
 replace('particle vy',V('particle'),sub(item('particle vy',V('particle')),.28)),
 If(both(both(gt(item('particle x',V('particle')),-78),lt(item('particle x',V('particle')),78)),both(gt(item('particle y',V('particle')),-158),lt(item('particle y',V('particle')),158))),
 stamp(item('particle x',V('particle')),item('particle y',V('particle')),join('element spark',V('CLEAR EFFECT')))),change('particle',1)]),B('looks_cleargraphiceffects'),change('fx age',1),
 If(gt(V('fx age'),23),[setv('fx active',0)])])])

render=[setv('block prefix',join('t',V('THEME'))),If(gt(V('BLOCK SKIN'),1),[setv('block prefix',join('skin',V('BLOCK SKIN')))]),setv('number spacing',14),call('update combo'),call('update camera'),B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(ZOOM*100)})]+stamp(0,0,'interface')+[call('draw game accent'),If(gt(V('AURA'),0),stamp(0,0,join(join('aura',V('AURA')),join('-',mod(floor(mul(timer(),8)),8)))))]+[setv('i',1),repeat(200,[If(gt(item('board',V('i')),0),block_stamp(add(-72,mul(mod(sub(V('i'),1),10),16)),sub(152,mul(floor(div(sub(V('i'),1),10)),16)),item('board',V('i')))),change('i',1)]),
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
 resize({'SIZE':inp(mul(mul(div(sub(V('combo expires'),timer()),4),100),ZOOM))})]+stamp(-216,91,'combo timer')+[
 resize({'SIZE':inp(100*ZOOM)}),If(eq(V('combo animating'),1),[change('combo pulse',1),If(gt(V('combo pulse'),23),[setv('combo animating',0)])])])])
render += [call('draw clear fx'),If(gt(V('flash'),0),[change('flash',-1)]+stamp(-161,78,V('notification'))),call('draw combo')]
# Optional exact RGB pen fill below the white arrow glyph, independent of theme colors.
for arrow,k,x,y in [('↑','w',160,-40),('←','a',118,-70),('↓','s',160,-70),('→','d',202,-70)]:
 render += [If(both(eq(V('key custom'),1),held(k)),segment(x-7,y,x+7,y,packed('key'),22*ZOOM,True)+stamp(x,y,'arrow glyph'+k),stamp(x,y,join('arrow'+k+'-',held(k))))]
render += [If(eq(V('GAME OVER'),1),stamp(0,0,'gameover')),resize({'SIZE':inp(100)})]+raw_stamp(-186,158,'menu button')+[resize({'SIZE':inp(100*ZOOM)})]
proc('render game',render)
proc('render menu',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)}),If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),raw_stamp(0,0,join(join('menu',V('THEME')),'-resume')),raw_stamp(0,0,join(join('menu',V('THEME')),'-play')))])
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
proc('reset',[call('init profile'),call('apply difficulty'),If(either(lt(V('THEME'),1),gt(V('THEME'),10)),[setv('THEME',1)]),call('apply theme'),setv('COMBO',0),setv('combo expires',0),setv('combo bonus',0),setv('run max combo',0),setv('combo pulse',0),setv('combo animating',0),setv('shake ticks',0),setv('shake x',0),setv('shake y',0),clear('board'),repeat(200,[append('board',0)]),clear('bag'),clear('clear rows'),setv('fx active',0),setv('fx age',0),setv('flash',0),
 setv('SCORE',0),setv('LINES',0),setv('LEVEL',1),setv('HOLD',0),setv('GAME OVER',0),setv('can hold',1),setv('left ticks',0),setv('right ticks',0),
 setv('z previous',0),setv('w previous',0),setv('space previous',0),setv('c previous',0),call('spawn')])
def edge(k,prev,ss):return [If(both(held(k),eq(V(prev),0)),ss),setv(prev,held(k))]
def sideways(k,t,dx):return If(held(k),[change(t,1),If(either(eq(V(t),1),both(gt(V(t),9),eq(mod(V(t),2),0))),[setv('dx',dx),setv('dy',0),call('move')])],[setv(t,0)])
proc('hard drop',[setv('valid',1),until(eq(V('valid'),0),[setv('dx',0),setv('dy',1),call('move'),If(eq(V('valid'),1),[change('SCORE',2)])]),call('lock')])
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
menu_keys+=edge('space','space previous',[If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),[call('resume game')],[call('start game')])])+edge('n','n previous',[call('start game')])
theme_keys=edge('t','t previous',[call('next theme')])
for theme in range(1,11):
 theme_keys+=edge(str(theme%10),'theme key '+str(theme),[setv('THEME',theme),call('apply theme')])
menu_clicks=[If(hit(32,112,246,150),[If(both(eq(V('has game'),1),eq(V('GAME OVER'),0)),[call('resume game')],[call('start game')])]),If(hit(32,162,246,192),[call('start game')]),If(hit(32,204,246,234),[call('show themes')]),If(hit(32,246,246,276),[call('show history')])]
theme_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')])]
for theme in range(1,11):
 col=(theme-1)%5;row=(theme-1)//5;left=12+col*94;top=96+row*74
 theme_clicks += [If(hit(left,top,left+80,top+62),[setv('THEME',theme),call('apply theme')])]
history_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')]),If(both(hit(96,288,196,316),gt(V('history page'),0)),[change('history page',-1)]),If(both(hit(284,288,384,316),lt(mul(add(V('history page'),1),5),length('run ids'))),[change('history page',1)])]
# Hover lookup uses the same hitboxes as click routing and does not select items.
hover_menu=[]
for kind,box in [(1,(32,112,246,150)),(2,(32,162,246,192)),(3,(32,204,246,234)),(4,(32,246,246,276))]:
 hover_menu += [If(hit(*box),[setv('hover object',kind)])]
hover_themes=[If(hit(16,16,100,42),[setv('hover object',5)])]
for theme in range(1,11):
 left=12+((theme-1)%5)*94;top=96+((theme-1)//5)*74
 hover_themes += [If(hit(left,top,left+80,top+62),[setv('hover object',theme+10)])]
hover_history=[If(hit(16,16,100,42),[setv('hover object',5)]),If(hit(96,288,196,316),[setv('hover object',6)]),If(hit(284,288,384,316),[setv('hover object',7)])]
proc('update hover',[setv('hover object',0),If(eq(V('SCREEN'),'menu'),hover_menu,[If(eq(V('SCREEN'),'themes'),hover_themes,[If(eq(V('SCREEN'),'history'),hover_history)])])])
proc('draw hover',[If(gt(V('hover object'),0),[
 setv('hover frame',mod(floor(mul(timer(),8)),8)),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('outline',V('hover object')))+[
 setv('hover x',125),setv('hover y',-5),setv('hover size',100),
 If(eq(V('SCREEN'),'themes'),[setv('hover x',170),setv('hover y',-118),setv('hover size',65)]),
 If(eq(V('SCREEN'),'history'),[setv('hover x',20),setv('hover y',120),setv('hover size',50)]),
 resize({'SIZE':inp(V('hover size'))})]+raw_stamp(V('hover x'),add(V('hover y'),mul(mathop('sin',mul(timer(),80)),3)),join(join('object',V('hover object')),join('-',V('hover frame')))))])
clicks=[If(eq(V('SCREEN'),'menu'),menu_clicks,[If(eq(V('SCREEN'),'themes'),theme_clicks,[If(eq(V('SCREEN'),'history'),history_clicks,[If(hit(8,10,100,34),[call('open menu')])])])])]
loop=edge('m','m previous',[If(eq(V('SCREEN'),'play'),[call('open menu')],[If(eq(V('SCREEN'),'menu'),[call('resume game')],[setv('SCREEN','menu')])])])
loop += [If(both((B('sensing_mousedown'),),eq(V('mouse previous'),0)),clicks),setv('mouse previous',(B('sensing_mousedown'),)),
 If(eq(V('SCREEN'),'menu'),menu_keys,[If(eq(V('SCREEN'),'themes'),theme_keys,[If(eq(V('SCREEN'),'play'),[If(key('r'),[call('start game')])]+active)])]),call('checkpoint run'),call('check achievements'),call('render'),B('control_wait',{'DURATION':inp(.02)})]
forever=B('control_forever');h=seq(loop);blocks[forever]['inputs']['SUBSTACK']=[2,h];blocks[h]['parent']=forever
hat=B('event_whenflagclicked');h=seq([B('looks_hide'),call('init profile'),setv('finish reason','Stopped'),call('finish run'),call('load profile'),call('reset'),setv('has game',0),setv('SCREEN','menu'),call('init ambient'),setv('m previous',0),setv('mouse previous',0),setv('n previous',0),call('sync inputs'),forever]);blocks[hat]['next']=h;blocks[h]['parent']=hat;blocks[hat].update(topLevel=True,x=20,y=20)
# RGB accents and settings overlay are native pen blocks, not external extensions.
accent=[]
for x1,y1,x2,y2 in [(-81,161,81,161),(81,161,81,-161),(81,-161,-81,-161),(-81,-161,-81,161)]:
 accent+=segment(x1,y1,x2,y2,packed('game'),1.8,True)
proc('draw game accent',[If(eq(V('game custom'),1),accent)])
def raw_number(value,digits,x,y,scale=60,spacing=8):
 return [setv('number value',value),setv('number digits',digits),setv('number scale',scale),setv('number spacing',spacing),setv('number x',x-240),setv('number y',180-y),call('draw raw number')]
def raw_text(value,x,y,scale=65):
 return [setv('text value',value),setv('text x',x-240),setv('text y',180-y),setv('text scale',scale),call('draw raw text')]
settings_general=raw_text(V('PLAYER NAME'),140,91)+raw_number(V('SHAKE'),3,101,164)+[resize({'SIZE':inp(100)})]+raw_stamp(add(-94,mul(div(V('SHAKE'),100),270)),16,'slider knob')
for varname,option_count,start,stride,yy,width,height in [('DIFFICULTY',3,126,110,128,100,24),('CLEAR EFFECT',5,18,92,218,84,28),('BLOCK SKIN',4,18,115,278,106,24),('AURA',3,126,110,302,100,16)]:
 settings_general += [resize({'SIZE':inp(100)})]+raw_stamp(sub(add(start,mul(sub(V(varname),0 if varname=='AURA' else 1),stride)),240-width/2),180-yy,'marker'+str(width)+'x'+str(height))
for flag,x,y in [(1,229,278),(2,344,278),(3,459,278),(4,326,302),(6,436,302)]:
 settings_general += [If(neg(eq(item('unlocked',flag),1)),[resize({'SIZE':inp(100)})]+raw_stamp(x-240,180-y,'small lock'))]
settings_rgb=[]
for prefix,offset in [('game',0),('key',120)]:
 for ci,c in enumerate(['r','g','b']):
  yy=112+ci*30+offset;settings_rgb += raw_number(V(prefix+' '+c),3,385,yy)+[resize({'SIZE':inp(100)})]+raw_stamp(add(-98,mul(div(V(prefix+' '+c),255),218)),180-yy,'slider knob')
 settings_rgb += segment(194,38-offset,206,38-offset,packed(prefix),16)
proc('render settings',[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,join('settings panel',V('settings tab')))+raw_stamp(add(-4,mul(sub(V('settings tab'),1),150)),151,'marker140x26')+[If(eq(V('settings tab'),1),settings_general,settings_rgb),If(gt(V('notice until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(-220,-172,join('notice',V('settings notice'))))])
ach_render=[B('pen_clear'),call('draw ambient'),resize({'SIZE':inp(100)})]+raw_stamp(0,0,'achievements panel')
for i in range(1,7):
 x=18+((i-1)%2)*232;y=80+((i-1)//2)*70
 ach_render += raw_stamp(x+106-240,180-(y+30.5),join(join('achievement'+str(i)+'-',item('unlocked',i)),''))
proc('render achievements',ach_render)
proc('show settings',[setv('hover object',0),setv('SCREEN','settings'),setv('settings tab',1),setv('settings notice','')])
proc('show achievements',[setv('hover object',0),call('check achievements'),setv('SCREEN','achievements')])
# Route extra pages before the ordinary render dispatcher, retaining its existing branches.
render_def=next(k for k,b in blocks.items() if b['opcode']=='procedures_prototype' and b['mutation']['proccode']=='render')
render_def=blocks[render_def]['parent'];old=blocks[render_def]['next']
wrapper=seq([If(eq(V('SCREEN'),'settings'),[call('render settings')],[If(eq(V('SCREEN'),'achievements'),[call('render achievements')],[old])]),
 If(either(eq(V('SCREEN'),'menu'),eq(V('SCREEN'),'history')),raw_text(V('PLAYER NAME'),120 if False else 32,350,60)),
 If(both(eq(item('unlocked',5),1),eq(V('SCREEN'),'menu')),[resize({'SIZE':inp(100)})]+raw_stamp(-58,-170,'spin title')),
 If(gt(V('achievement until'),timer()),[resize({'SIZE':inp(100)})]+raw_stamp(90,164,join('achievement toast',V('achievement notice'))))])
blocks[render_def]['next']=wrapper;blocks[wrapper]['parent']=render_def
# Settings mouse controls. All drafts preview immediately, Save Profile commits them.
settings_clicks=[If(hit(16,16,100,42),[setv('SCREEN','menu')]),If(hit(166,16,306,42),[setv('settings tab',1)]),If(hit(316,16,456,42),[setv('settings tab',2)]),If(hit(310,316,462,344),[call('save profile')])]
general_clicks=[If(hit(126,78,456,104),[call('edit name')]),If(hit(424,153,462,175),[setv('SHAKE',0),setv('profile saved',0)])]
for n in range(1,4):general_clicks += [If(hit(126+(n-1)*110,116,226+(n-1)*110,140),[setv('DIFFICULTY',n),setv('profile saved',0)])]
for n in range(1,6):general_clicks += [If(hit(18+(n-1)*92,204,102+(n-1)*92,232),[setv('CLEAR EFFECT',n),setv('profile saved',0)])]
for n,flag in [(1,0),(2,1),(3,2),(4,3)]:
 choice=[setv('BLOCK SKIN',n),setv('profile saved',0)]
 if flag:choice=[If(eq(item('unlocked',flag),1),choice,[setv('settings notice','locked'),setv('notice until',add(timer(),2))])]
 general_clicks += [If(hit(18+(n-1)*115,266,124+(n-1)*115,290),choice)]
for n,flag in [(0,0),(1,4),(2,6)]:
 choice=[setv('AURA',n),setv('profile saved',0)]
 if flag:choice=[If(eq(item('unlocked',flag),1),choice,[setv('settings notice','locked'),setv('notice until',add(timer(),2))])]
 general_clicks += [If(hit(126+n*110,294,226+n*110,310),choice)]
rgb_clicks=[If(hit(18,316,164,344),[setv('game custom',0),setv('key custom',0),setv('profile saved',0)])]
for ci,yy in enumerate([112,142,172,232,262,292],1):rgb_clicks += [If(hit(376,yy-10,418,yy+10),[setv('color channel',ci),call('edit color value')])]
settings_clicks += [If(eq(V('settings tab'),1),general_clicks,rgb_clicks)]
settings_drags=[If(both(eq(V('settings tab'),1),hit(140,153,420,175)),[setv('SHAKE',floor(mul(div(add(mouse_x(),94),270),100))),call('clamp settings'),setv('profile saved',0)])]
for prefix,offset in [('game',0),('key',120)]:
 for ci,c in enumerate(['r','g','b']):
  yy=112+ci*30+offset
  settings_drags += [If(both(eq(V('settings tab'),2),hit(136,yy-7,366,yy+7)),[setv(prefix+' '+c,floor(mul(div(add(mouse_x(),98),218),255))),setv(prefix+' custom',1),call('clamp settings'),setv('profile saved',0)])]
extra_clicks=[If(eq(V('SCREEN'),'settings'),settings_clicks,[If(eq(V('SCREEN'),'achievements'),[If(hit(16,16,100,42),[setv('SCREEN','menu')])],clicks)])]
# Replace the click substack only, keeping its edge-trigger guard and original navigation.
for k,b in list(blocks.items()):
 if b['opcode']=='control_if' and b['inputs'].get('SUBSTACK',[None,None])[1]==seq(clicks):
  h=seq(extra_clicks);b['inputs']['SUBSTACK']=[2,h];blocks[h]['parent']=k;break
# Add main-menu buttons after its existing actions (same main-menu branch).
menu_extra=[If(hit(270,300,358,328),[call('show settings')]),If(hit(364,300,468,328),[call('show achievements')])]
end=menu_clicks[0]
while blocks[end]['next']:end=blocks[end]['next']
h=seq(menu_extra);blocks[end]['next']=h;blocks[h]['parent']=end
# Dragging is continuous; a button click remains edge-triggered.
waitblock=loop[-1];previous=next(k for k,b in blocks.items() if b.get('next')==waitblock)
h=seq([If(both(eq(V('SCREEN'),'settings'),(B('sensing_mousedown'),)),settings_drags)])
blocks[previous]['next']=h;blocks[h]['parent']=previous;blocks[h]['next']=waitblock;blocks[waitblock]['parent']=h

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
for theme in range(1,11):
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
for kind in list(range(1,8))+list(range(11,21)):
 costumes += [costume('outline'+str(kind),hover_outline(kind),240,180)]
 for frame in range(8):costumes += [costume('object'+str(kind)+'-'+str(frame),hover_object(kind,frame),60,60)]
for kind in range(1,6):
 costumes += [costume('element'+str(kind)+'-'+str(f),elemental_beam(kind,f),80,8) for f in range(10)]
 costumes += [costume('element spark'+str(kind),particle_skin(kind),4,4)]
for style in range(2,5):
 for i,c in enumerate(THEME_PALETTES[0],1):
  costumes += [costume('skin'+str(style)+'-'+str(i),cosmetic_block(c,style),8,8),costume('skin'+str(style)+'-'+str(i+7),cosmetic_block(c,style,True),8,8)]
for style in [1,2]:costumes += [costume('aura'+str(style)+'-'+str(f),aura(style,f),84,164) for f in range(8)]
for tab in [1,2]:costumes += [costume('settings panel'+str(tab),settings_panel(tab),240,180)]
for w,h in [(100,24),(84,28),(106,24),(100,16),(140,26)]:costumes += [costume('marker'+str(w)+'x'+str(h),select_marker(w,h),w/2,h/2)]
costumes += [costume('slider knob',slider_knob(),6,6)]
for kind in ['saved','locked','name']:costumes += [costume('notice'+kind,save_notice(kind),0,9)]
costumes += [costume('small lock',svg(rect(3,5,7,6,'#8799b6',r=1)+'<path d="M4 5V3a2.5 2.5 0 0 1 5 0v2" fill="none" stroke="#bed1ea"/>',12,12),6,6)]
costumes += [costume('achievements panel',achievements_panel(),240,180)]
for i in range(1,7):
 for unlocked in [0,1]:costumes += [costume('achievement'+str(i)+'-'+str(unlocked),achievement_tile(i,bool(unlocked)),106,30.5)]
 costumes += [costume('achievement toast'+str(i),svg(text(95,12,'UNLOCKED / '+ACHIEVEMENTS[i-1][2].upper(),8,'#b9f5d7',300,extra='text-anchor="middle"'),190,18),95,9)]
costumes += [costume('spin title',svg(text(0,10,'SPIN ARTIST',6.5,'#d5bcff',300,extra='letter-spacing="1"'),100,14),0,7)]
for arrow,k in [('↑','w'),('←','a'),('↓','s'),('→','d')]:costumes += [costume('arrow glyph'+k,svg(text(20,18,arrow,16,'#fff',300,extra='text-anchor="middle"'),40,26),20,13)]
for i,label in enumerate(['EASY','NORMAL','HARD'],1):costumes += [costume('history difficulty'+str(i),svg(text(0,10,label,6.5,'#b3d9ef',300),65,14),0,7)]
NAME_ALPHABET=list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 -_')
for i,c in enumerate(NAME_ALPHABET,1):costumes += [costume('letter'+str(i),svg(text(0,16,c,17,'#ecf5ff',300),12,20),0,10)]
lists['name alphabet']=['name alphabet',NAME_ALPHABET]
lists['gravity choices']=['gravity choices',[60,35,15]];lists['lock choices']=['lock choices',[35,25,12]]
backdrops=[costume('theme'+str(i),landscape(i),240,180) for i in range(1,11)]
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
project=dict(targets=[stage,sprite],monitors=monitors,extensions=['pen'],meta={'semver':'3.0.0','vm':'5.0.300','agent':'Stack Flow builder'})
ROOT.joinpath('dist').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT/'dist/stack-flow.sb3','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('project.json',json.dumps(project))
 for path,data in assets.items():z.writestr(path,data)
print(f'Built {len(blocks)} blocks, {len(assets)} assets → dist/stack-flow.sb3')
