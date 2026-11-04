"""Vector settings and achievement panels; live values are native Scratch stamps."""
from visuals import svg,rect,text,_back_button
from progression import ACHIEVEMENTS, EFFECT_NAMES, SKIN_NAMES, AURA_NAMES, DIFFICULTY_NAMES

def button(x,y,w,h,label):
 return rect(x,y,w,h,'#101a2c','#526881',3,extra='stroke-width=".6"')+text(x+w/2,y+h/2+3,label,8,'#d4dff2',300,extra='text-anchor="middle" letter-spacing=".5"')
def settings_panel(tab=1):
 b=[rect(0,0,480,360,'#080e1b',extra='fill-opacity=".97"'),_back_button(),button(166,16,140,26,'GENERAL'),button(316,16,140,26,'RGB COLORS'),text(24,64,'SETTINGS',22,'#edf5ff',300,extra='letter-spacing="2"')]
 if tab==1:
  b += [text(24,95,'NAME',8,'#a0b2cf'),button(126,78,330,26,'')]
  b += [text(24,132,'DIFFICULTY',8,'#a0b2cf')]
  for i,label in enumerate(DIFFICULTY_NAMES):b += [button(126+i*66,116,60,24,label.upper())]
  b += [text(24,168,'SHAKE',8,'#a0b2cf'),rect(146,162,270,4,'#354a68',r=2),button(424,153,38,22,'OFF')]
  b += [button(126,214,330,38,'COSMETICS'),text(24,205,'APPEARANCE',8,'#a0b2cf')]
 else:
  for title,y in [('GAME ACCENT RGB',90),('KEY HIGHLIGHT RGB',210)]:b += [text(24,y,title,10,'#b7d3f2',300,extra='letter-spacing="1"')]
  for row,(label,c) in enumerate([('R','#ff7b8d'),('G','#8eeab3'),('B','#83bdff')]):
   for offset in [0,120]:
    y=112+row*30+offset;b += [text(24,y+3,label,10,c),rect(142,y-2,218,4,'#283d58',r=2),rect(142,y-1,218,2,c,extra='fill-opacity=".35"')]
  b += [button(18,182,146,20,'RAINBOW ACCENT'),button(174,316,122,28,'RAINBOW KEYS'),button(18,316,146,28,'USE THEME COLORS')]
 b += [button(310,316,152,28,'SAVE PROFILE')]
 return svg(''.join(b))
def select_marker(w=100,h=24):return svg(rect(1,1,w-2,h-2,'none','#b5dfff',3,extra='stroke-width="1.3"'),w,h)
def slider_knob():return svg('<circle cx="6" cy="6" r="5" fill="#bdeaff" stroke="#fff" stroke-width=".6"/>',12,12)
def save_notice(kind='saved'):
 labels={'saved':'PROFILE SAVED','locked':'LOCKED COSMETIC','name':'NAME UPDATED'}
 return svg(text(0,12,labels.get(kind,''),8,'#9cebc6' if kind=='saved' else '#efc29c',300,extra='letter-spacing=".7"'),200,18)
def achievements_panel():
 return svg(rect(0,0,480,360,'#080d19',extra='fill-opacity=".97"')+_back_button()+text(240,64,'ACHIEVEMENTS',22,'#e9f4ff',300,extra='text-anchor="middle" letter-spacing="2"')+button(96,306,100,28,'PREVIOUS')+button(284,306,100,28,'NEXT'))
def achievement_tile(index,unlocked=False):
 name,req,reward=ACHIEVEMENTS[index-1];c='#a9f2cf' if unlocked else '#8192b2'
 b=rect(.5,.5,211,60,'#142236' if unlocked else '#0c1424',c,4,extra='stroke-width=".7"')
 b+=f'<path d="M18 14L28 24L18 34L8 24Z" fill="{c}" opacity=".65"/>'
 if unlocked:b+='<path d="M12 24l4 4 8-9" stroke="#fff" stroke-width="1.2" fill="none"/>'
 else:b+=rect(14,20,8,8,'none',c,1)+ '<path d="M15 20V17a3 3 0 0 1 6 0v3" fill="none" stroke="#8192b2"/>'
 b+=text(36,17,name,9,c)+text(36,33,req,7,'#bac7dc')+text(36,49,('UNLOCKED / ' if unlocked else 'REWARD / ')+reward,6.8,'#b2c5e1')
 return svg(b,212,61)
