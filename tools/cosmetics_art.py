"""Equipable cosmetic collection cards."""
from visuals import svg,rect,text,block,THEME_PALETTES
from effects_art import elemental_beam,cosmetic_block,aura
from progression import EFFECT_NAMES,SKIN_NAMES,AURA_NAMES
from impact_art import DROP_NAMES,drop_preview

def card(tab,index,state=0):
 names=[EFFECT_NAMES,SKIN_NAMES,AURA_NAMES,DROP_NAMES][tab-1];name=names[index-1]
 b=rect(.5,.5,81,81,'#142438' if state==1 else '#0a1322','#b8e4ff' if state==1 else '#40516e',4,extra='stroke-width="1"')
 if tab==1:
  art=elemental_beam(index,3);inside=art[art.index('>')+1:art.rfind('</svg>')];b+=f'<g transform="translate(7 23) scale(.42)">{inside}</g>'
 elif tab==2:
  for k,(x,y) in enumerate([(24,14),(10,28),(24,28),(38,28)]):
   art=block(THEME_PALETTES[0][5]) if index==1 else cosmetic_block(THEME_PALETTES[0][k%7],index)
   inside=art[art.index('>')+1:art.rfind('</svg>')];b+=f'<g transform="translate({x} {y})">{inside}</g>'
 elif tab==4:
  art=drop_preview(index);inside=art[art.index('>')+1:art.rfind('</svg>')];b+=f'<g transform="translate(11 3)">{inside}</g>'
 elif index==1:b+='<circle cx="41" cy="28" r="17" fill="none" stroke="#8194b4"/><path d="M28 41L54 15" stroke="#8194b4"/>'
 else:
  art=aura(index-1,3);inside=art[art.index('>')+1:art.rfind('</svg>')];b+=f'<g transform="translate(29 4) scale(.15)">{inside}</g>'
 b+=text(41,65,name.upper(),6.5,'#dce8fa',300,'text-anchor="middle"')
 if state==2:b+=rect(3,3,76,49,'#050a13',r=3,extra='fill-opacity=".7"')+'<path d="M35 27v-5a6 6 0 0 1 12 0v5" stroke="#d4dded" fill="none"/>'+rect(33,27,16,13,'#657b9a',r=2)
 if state==1:b+='<path d="M63 10l4 4 8-9" fill="none" stroke="#bdf7d8" stroke-width="1.4"/>'
 return svg(b,82,82)
