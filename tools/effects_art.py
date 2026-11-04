"""Original selectable clear effects and earned cosmetic skins."""
from visuals import svg,rect,block
from math import sin,cos,pi

def elemental_beam(kind,frame):
 f=max(0,min(9,int(frame)));p=f/9;opacity=1-p*.85;b=[]
 colors=['#8be6ff','#ff7b38','#57d5ff','#d5f6ff','#f9a1ff'];c=colors[kind-1]
 b += [rect(0,5,160,6,c,extra=f'fill-opacity="{.8*(1-p):.3f}"'),rect(0,7,160,2,'#fff',extra=f'fill-opacity="{1-p:.3f}"')]
 for i in range(16):
  x=(i*13+f*5)%160
  if kind==2:
   h=4+((i*7+f*3)%10);b.append(f'<path d="M{x-5} 15Q{x+3} {12-h} {x} {2-h*.15}Q{x+9} 8 {x+6} 15Z" fill="{["#ff5637","#ffab42","#fff099"][i%3]}" opacity="{opacity:.3f}"/>')
  elif kind==3:
   y=8+sin((i+f)*.9)*4;b.append(f'<path d="M{x-6} {y}Q{x} {y-7} {x+7} {y}" fill="none" stroke="#7ce9ff" stroke-width="1.4" opacity="{opacity:.3f}"/><circle cx="{x+3}" cy="{max(1,y-4)}" r="1.2" fill="#e1ffff"/>')
  elif kind==4:
   h=3+(i*7+f)%9;b.append(f'<path d="M{x-5} 13L{x-1} {13-h}L{x+4} 2L{x+7} 13Z" fill="#b6e9ff" stroke="#f4ffff" stroke-width=".5" opacity="{opacity:.3f}"/>')
  elif kind==5:
   color=['#ff657f','#ffa355','#ffe867','#70f2b3','#65d9ff','#a58bff'][i%6];b += [rect(i*10,2+(f+i)%7,12,4,color,extra=f'fill-opacity="{opacity:.3f}"')]
  else:b.append(f'<path d="M{x} 2V14 M{x-3} 8H{x+3}" stroke="#c2eeff" opacity="{opacity*.6:.3f}" stroke-width=".6"/>')
 return svg(''.join(b),160,16)

def particle_skin(kind):
 if kind==2:b='<path d="M4 0Q2 4 1 5Q0 9 6 7Q9 4 5 2Q6 5 4 5Z" fill="#ff8241"/><path d="M4 4L6 7H2Z" fill="#fff5b7"/>'
 elif kind==3:b='<path d="M4 0Q10 7 4 8Q-2 7 4 0Z" fill="#65dfff"/><path d="M3 3L2 5" stroke="#fff" stroke-width="1"/>'
 elif kind==4:b='<path d="M4 0V8 M0 4H8 M1 1L7 7 M7 1L1 7" stroke="#d8fbff" stroke-width=".9"/>'
 elif kind==5:b='<path d="M4 0L8 4L4 8L0 4Z" fill="#d6a0ff"/><path d="M0 4H8M4 0V8" stroke="#8df6fa" stroke-width="1"/>'
 else:b='<path d="M4 0L8 4L4 8L0 4Z" fill="#e3f6ff"/>'
 return svg(b,8,8)

def cosmetic_block(c,style=2,ghost=False):
 if ghost:return block(c,True)
 b=rect(.5,.5,15,15,c,r=1)
 if style==2:b+='<path d="M1 15L5 8L7 12L10 3L15 15Z" fill="#fff1b1" opacity=".42"/><path d="M2 2H14" stroke="#fff" opacity=".75"/>'
 elif style==3:b+='<path d="M1 1L8 8L15 1 M1 15L8 8L15 15 M1 1L15 15 M1 15L15 1" stroke="#e7ffff" opacity=".65" stroke-width=".6"/><path d="M8 2L11 8L8 14L5 8Z" fill="#fff" opacity=".25"/>'
 else:
  b+='<path d="M1 1H15V15H1Z" fill="none" stroke="#f9dcff" stroke-width="1"/><path d="M2 12L12 2M6 14L14 6" stroke="#9dffff" opacity=".65"/>'
 return svg(b,16,16)

def aura(style,frame):
 c='#ffd57d' if style==1 else ['#ff799c','#ffb55e','#f9ed84','#7df4c0','#74dfff','#b89bff','#e4a3ff','#ff93bf'][frame%8]
 b=rect(2,2,164,324,'none',c,3,extra='stroke-width=".8" stroke-opacity=".55"')+rect(4,4,160,320,'none',c,2,extra='stroke-width="1.4" stroke-opacity=".65"')
 for i in range(12):
  y=(i*31+frame*7)%320+4;b+=f'<circle cx="{3 if i%2 else 165}" cy="{y}" r="1.3" fill="{c}"/>'
 return svg(b,168,328)
