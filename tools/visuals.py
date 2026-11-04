"""Original vector artwork for Stack / Flow's competitive Scratch layout."""
from html import escape

THEME_NAMES = ['Galaxy', 'Mountains', 'Ocean', 'Sunset', 'Neon City', 'Black', 'Sakura', 'Volcano', 'Aurora', 'Blueprint']
THEME_PALETTES = [
    ['#65e5ff', '#738aff', '#ffb56d', '#f5df8a', '#78ecc7', '#c49bff', '#ff8db9'],
    ['#9ae7f2', '#7ea1ec', '#e1b08c', '#ebdfa4', '#89cbb3', '#b9a2d8', '#e5a2b3'],
    ['#42ddf2', '#4398e5', '#ffa777', '#f4e38b', '#56dba5', '#a291eb', '#f486b1'],
    ['#7ed8f6', '#8d99ff', '#ffb164', '#ffde70', '#b3db9b', '#d38dcb', '#ff839d'],
    ['#24e9ff', '#557dff', '#ff962d', '#f7f953', '#7bff82', '#c36bff', '#ff54b8'],
]
THEME_PALETTES += [
    ['#f5f5f5', '#c6c6c6', '#a6a6a6', '#ffffff', '#b6b6b6', '#e2e2e2', '#d2d2d2'],
    ['#a9e4eb', '#a6abd9', '#efb5a2', '#f9e1b0', '#bddab8', '#d8a3db', '#f18fb5'],
    ['#ffbf49', '#db6e3b', '#ff913c', '#ffdc71', '#c44f45', '#bf668b', '#f65b4b'],
    ['#75f0d7', '#729fe9', '#b9d8a1', '#ecedaf', '#65d5a6', '#bf9fe7', '#e5a3d4'],
    ['#b0edff', '#7ab8ef', '#d0e4f6', '#f5fcff', '#7cd4e9', '#a4bde7', '#a0d9dc'],
]
COLORS = THEME_PALETTES[0]


def svg(body, w=480, h=360):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


def text(x, y, s, size=10, color='#eeeeef', weight=300, extra=''):
    # Keep UI lettering slender on Scratch's portable browser font stack.
    weight = min(int(weight), 400)
    return f'<text x="{x}" y="{y}" font-family="Segoe UI Light,DejaVu Sans,Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(s)}</text>'


def rect(x, y, w, h, fill, stroke='none', r=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def block(c, ghost=False, theme=1):
    """Theme-tinted 16px minos retain distinct shapes and readable wireframe ghosts."""
    if ghost:
        return svg(rect(.8, .8, 14.4, 14.4, c, c, extra='fill-opacity=".035" stroke-opacity=".72" stroke-width=".8"'), 16, 16)
    theme = int(theme)
    if theme == 6:
        body = rect(.5, .5, 15, 15, '#050505', c, extra='stroke-width=".8"')
        body += rect(2, 2, 12, 12, c, extra='fill-opacity=".88"')
    elif theme == 10:
        body = rect(.5, .5, 15, 15, '#0b2844', c, extra='stroke-width=".9"')
        body += f'<path d="M4 1V15 M8 1V15 M12 1V15 M1 4H15 M1 8H15 M1 12H15" stroke="{c}" opacity=".28" stroke-width=".4"/><circle cx="8" cy="8" r="2.8" stroke="{c}" fill="none" stroke-width=".55"/>'
    elif theme == 5:
        body = rect(.5, .5, 15, 15, '#101427', c, extra='stroke-width="1"') + rect(2, 2, 12, 12, c, extra='fill-opacity=".6"')
        body += f'<path d="M3 4H12 M3 11V4" stroke="{c}" stroke-width=".8" fill="none"/>'
    else:
        body = rect(.3, .3, 15.4, 15.4, c)
        body += '<path d="M.3 15.7H15.7V.3" stroke="#000" stroke-opacity=".28" stroke-width=".8" fill="none"/><path d="M.5 15V.5H15" stroke="#fff" stroke-opacity=".3" stroke-width=".6" fill="none"/>'
        if theme == 1:
            body += '<path d="M2 12L13 2H15L4 14H2Z" fill="#fff" opacity=".10"/><path d="M11 3V7 M9 5H13" stroke="#fff" stroke-width=".6" opacity=".7"/>'
        elif theme == 2:
            body += '<path d="M1 15L7 2L15 15Z" fill="#fff" opacity=".15"/><path d="M7 2L8 7L10 6L9 9L7 8L5 9Z" fill="#fff" opacity=".35"/>'
        elif theme == 3:
            body += '<path d="M1 6Q4 3 8 6T15 6 M1 11Q4 8 8 11T15 11" stroke="#fff" stroke-opacity=".22" fill="none" stroke-width=".8"/>'
        elif theme == 4:
            body += '<path d="M2 4H14 M2 7H14 M2 10H14 M2 13H14" stroke="#fff" stroke-opacity=".14" stroke-width=".8"/>'
        elif theme == 7:
            body += '<path d="M8 8Q3 8 4 4Q8 3 8 8Q8 3 12 4Q13 8 8 8Q13 8 12 12Q8 13 8 8Q8 13 4 12Q3 8 8 8Z" fill="#fff" opacity=".22"/><circle cx="8" cy="8" r=".7" fill="#fff" opacity=".65"/>'
        elif theme == 8:
            body += '<path d="M1 12L5 9L4 5L9 3L11 1 M5 9L10 10L13 14 M9 3L14 6" fill="none" stroke="#3f1721" stroke-width="1.2" opacity=".5"/><path d="M1 12L5 9L4 5L9 3L11 1" fill="none" stroke="#fff0a0" stroke-width=".4" opacity=".7"/>'
        elif theme == 9:
            body += '<path d="M1 11Q4 2 8 8T15 4 M1 14Q4 5 8 11T15 7" fill="none" stroke="#fff" opacity=".28" stroke-width="1.1"/>'
    return svg(body, 16, 16)


def arena():
    b = [
        # This artwork is a transparent world-space overlay. The renderer shrinks
        # and shakes it together with the blocks, while landscapes stay still.
        rect(14, 15, 132, 330, '#070b14', extra='fill-opacity=".64"'),
        rect(338, 15, 126, 330, '#070b14', extra='fill-opacity=".64"'),
        rect(160, 20, 160, 320, '#050911', extra='fill-opacity=".96"'),
    ]
    for x in range(1, 10):
        b.append(f'<path d="M{160+x*16} 20V340" stroke="#fff" opacity=".035" stroke-width=".5"/>')
    for y in range(1, 20):
        b.append(f'<path d="M160 {20+y*16}H320" stroke="#fff" opacity=".035" stroke-width=".5"/>')
    b += [
        '<path d="M159 19V341H321V19" stroke="#e0e0e5" stroke-width="1.25" fill="none"/>',
        '<path d="M160 20H320" stroke="#fff" stroke-opacity=".15" stroke-width=".5"/>',
        '<path d="M156 332V344H169 M311 344H324V332" fill="none" stroke="#a998d1" stroke-width=".7" stroke-opacity=".6"/>',
        text(24, 34, 'STACK / FLOW', 14, '#f3f3f5', 900, 'letter-spacing="1" textLength="112" lengthAdjust="spacingAndGlyphs"'),
        text(24, 49, 'MARATHON', 9, '#aaa7bb', 700, 'letter-spacing="2.5"'),
        text(134, 121, 'HOLD', 11, '#f0eff5', 800, 'text-anchor="end" letter-spacing="1.2"'),
        text(24, 65, 'COMBO', 9, '#aaa7bb', 300, 'letter-spacing="1.8"'),
        rect(24, 89, 110, 2, '#77708c', extra='fill-opacity=".28"'),
        '<path d="M24 128H135" stroke="#fff" stroke-opacity=".15" stroke-width=".6"/>',
    ]
    for label, y in [('SCORE', 170), ('LINES', 222), ('LEVEL', 265)]:
        b += [
            text(24, y, label, 9, '#9894a3', 800, 'letter-spacing="1.9"'),
            f'<path d="M24 {y+34}H133" stroke="#fff" stroke-opacity=".08" stroke-width=".6"/>',
        ]
    b += [
        text(348, 35, 'NEXT', 12, '#f1eff6', 900, 'letter-spacing="1.8"'),
        '<path d="M347 43H452" stroke="#fff" stroke-opacity=".15" stroke-width=".6"/>',
        # Four previews leave a live input display underneath.
        '<path d="M349 52H345V184H349" stroke="#fff" stroke-opacity=".10" stroke-width=".7" fill="none"/>',
        text(348, 310, 'ENDLESS', 10, '#d4cede', 800, 'letter-spacing="1.7"'),
        text(348, 324, '7-BAG RANDOMIZER', 6.8, '#77717f', 600, 'letter-spacing=".5"'),
    ]
    return svg(''.join(b))


def digit(d):
    """16x26 cells: condensed white numerals sit on the fixed HUD positions."""
    return svg(text(0, 21, str(d), 24, '#f5f3fa', 300, 'textLength="13" lengthAdjust="spacingAndGlyphs"'), 16, 26)


def gameover():
    return svg(
        rect(0, 0, 160, 320, '#09070f', extra='fill-opacity=".9"')
        + '<path d="M0 106H160 M0 213H160" stroke="#b693ef" stroke-opacity=".55" stroke-width=".7"/>'
        + rect(0, 107, 160, 105, '#19131f', extra='fill-opacity=".94"')
        + text(80, 128, 'STACK / FLOW', 7, '#a198b6', 800, 'text-anchor="middle" letter-spacing="2"')
        + text(80, 151, 'GAME', 23, '#f9f6ff', 900, 'text-anchor="middle" letter-spacing="1"')
        + text(80, 175, 'OVER', 23, '#f9f6ff', 900, 'text-anchor="middle" letter-spacing="1"')
        + text(80, 198, 'RUN SAVED', 8, '#cdb6ed', 300, 'text-anchor="middle" letter-spacing=".6"'),
        160, 320,
    )


def badge(n):
    """120x14 sidebar clear caption, centered at (60,7)."""
    name = ['SINGLE', 'DOUBLE', 'TRIPLE', 'QUAD'][n-1]
    c = '#faf6ff' if n < 4 else '#cdb1ff'
    return svg(
        '<path d="M6 7H23 M97 7H114" stroke="#b19bd0" stroke-opacity=".5" stroke-width=".6"/>'
        + text(60, 10, name, 8, c, 300, 'text-anchor="middle" letter-spacing="1.8"'),
        120, 14,
    )


def clear_beam(frame, quad=False):
    """160x16 row-clear animation, frames 0..9; center is (80,8).

    Early frames flash the cleared row; later frames split into outward-moving
    light ribbons and deterministic spark diamonds. No SVG filters required.
    """
    f = max(0, min(9, int(frame)))
    progress = f / 9
    c = '#bc90ff' if quad else '#74e8ff'
    opacity = max(0, 1-progress)
    body = [f'<g opacity="{opacity:.3f}">']
    if f < 3:
        body += [rect(0, 0, 160, 16, c, extra=f'fill-opacity="{.48-f*.1:.2f}"'), rect(0, 4+f, 160, 8-f*2, '#fff')]
    # Several rails make the bloom bright while keeping the graphic pixel sharp.
    width = max(3, 78-f*6)
    for side in (-1, 1):
        mid = 80 + side*(f*8)
        body += [rect(mid-width/2, 3, width, 10, c, extra='fill-opacity=".18"'), rect(mid-width/2, 6, width, 4, c, extra='fill-opacity=".8"'), rect(mid-width/2, 7, width, 2, '#fff')]
    for k in range(13):
        x = (k*37 + 11 + (f*7 if k%2 else -f*7)) % 160
        y = 2 + (k*11+f*3)%12
        size = 1.1 + (k%3)*.45
        body.append(f'<path d="M{x} {y-size}L{x+size*2} {y}L{x} {y+size}L{x-size*2} {y}Z" fill="{c if k%3 else "#fff"}"/>')
    body.append('</g>')
    return svg(''.join(body), 160, 16)


def particle(color='#c8a9ff'):
    """6x6 glowing diamond, centered at (3,3), for moving particle stamps."""
    return svg(f'<path d="M3 0L6 3L3 6L0 3Z" fill="{color}" opacity=".3"/><path d="M3 1L5 3L3 5L1 3Z" fill="#fff"/>', 6, 6)


def _sky(top, bottom):
    return '<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="' + top + '"/><stop offset="1" stop-color="' + bottom + '"/></linearGradient></defs>' + rect(0, 0, 480, 360, 'url(#sky)')


def _stars(seed=0, count=75, dim=False):
    b = []
    for i in range(count):
        x = (i*113 + seed*53 + 17) % 480
        y = (i*i*17 + i*13 + seed*37 + 9) % 350
        r = [.45, .55, .75, 1.05][i % 4]
        opacity = .22+(i % 6)*.1
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d8e7ff" opacity="{opacity if not dim else opacity*.5:.2f}"/>')
        if i % 17 == 0:
            b.append(f'<path d="M{x-3} {y}H{x+3} M{x} {y-3}V{y+3}" stroke="#d1d9ff" stroke-width=".5" opacity=".45"/>')
    return ''.join(b)


def _pine(x, y, scale=1, color='#0b2330'):
    return f'<g transform="translate({x} {y}) scale({scale})"><path d="M0 0L-8 14H-4L-12 26H-6L-15 39H15L6 26H12L4 14H8Z" fill="{color}"/><path d="M-1 37H1V45H-1Z" fill="{color}"/></g>'


def landscape(theme=1):
    """Full-stage 480x360 original landscape, selected independently of camera shake."""
    theme = max(1, min(10, int(theme)))
    if theme == 1:
        b = [_sky('#050919', '#1c1238')]
        b += ['<defs><radialGradient id="nebula"><stop stop-color="#813ca7" stop-opacity=".34"/><stop offset="1" stop-color="#4a2676" stop-opacity="0"/></radialGradient><radialGradient id="blue"><stop stop-color="#2d76b9" stop-opacity=".32"/><stop offset="1" stop-color="#184666" stop-opacity="0"/></radialGradient><linearGradient id="planet" x2="1" y2="1"><stop stop-color="#8667bb"/><stop offset=".5" stop-color="#34436c"/><stop offset="1" stop-color="#121a35"/></linearGradient></defs>', '<ellipse cx="95" cy="198" rx="225" ry="96" fill="url(#nebula)" transform="rotate(-30 95 198)"/><ellipse cx="367" cy="202" rx="166" ry="91" fill="url(#blue)" transform="rotate(-30 367 202)"/>', _stars(1, 112)]
        b += ['<ellipse cx="424" cy="78" rx="48" ry="12" fill="none" stroke="#ac9ce6" stroke-width="4" opacity=".16" transform="rotate(-25 424 78)"/><circle cx="424" cy="78" r="27" fill="url(#planet)" stroke="#9aa4de" stroke-opacity=".32" stroke-width=".5"/><path d="M382 96Q423 99 465 58" fill="none" stroke="#a5a9dc" stroke-width="2.5" opacity=".4"/>', '<circle cx="48" cy="274" r="11" fill="#334564"/><path d="M43 264Q54 267 57 276" stroke="#8c97bb" stroke-width=".8" opacity=".3" fill="none"/>', '<path d="M12 65L72 46" stroke="#a1caff" stroke-width=".6" opacity=".4"/><path d="M439 297L475 283" stroke="#aa8ddc" stroke-width=".6" opacity=".45"/>']
    elif theme == 2:
        b = [_sky('#17223d', '#8c919e')]
        b += ['<defs><linearGradient id="moon"><stop stop-color="#d1dfdf"/><stop offset="1" stop-color="#8da6bf"/></linearGradient></defs>', '<circle cx="61" cy="55" r="19" fill="url(#moon)" opacity=".85"/>', _stars(2, 22, True), '<path d="M0 201L58 101L118 179L191 72L270 184L350 88L425 157L480 115V360H0Z" fill="#50647d"/><path d="M25 156L58 101L86 138L70 132L58 140L48 130Z M155 124L191 72L227 123L204 115L194 127L181 111L170 122Z M326 120L350 88L380 124L357 116L347 125L341 113Z" fill="#b9ced6" opacity=".85"/>', '<path d="M0 229L66 161L121 215L173 147L246 215L311 157L370 220L436 154L480 202V360H0Z" fill="#2b485c"/><path d="M0 268Q60 221 129 252T248 248T377 249T480 225V360H0Z" fill="#193849"/>', '<path d="M0 298Q96 285 173 305T337 298T480 306V360H0Z" fill="#173543"/><path d="M0 319Q115 300 218 322T480 315" fill="none" stroke="#658d98" stroke-width=".8" opacity=".35"/>']
        for i in range(20):
            x = i*27-10
            b.append(_pine(x, 266+(i*19)%32, .7+(i%3)*.16, '#102a36'))
        for x,y,size in [(6,220,1.9),(467,212,2.15),(38,277,1.2),(438,283,1.4)]:
            b.append(_pine(x,y,size,'#0b202d'))
    elif theme == 3:
        b = [_sky('#032c46', '#031928')]
        b += ['<defs><linearGradient id="water" x2="0" y2="1"><stop stop-color="#4097a1" stop-opacity=".35"/><stop offset="1" stop-color="#194658" stop-opacity="0"/></linearGradient></defs>', '<path d="M0 29Q40 19 87 28T180 27T275 28T369 26T480 26V44Q418 35 365 42T270 41T180 42T88 40T0 43Z" fill="#78c7c9" opacity=".5"/><path d="M0 31Q40 21 87 30T180 29T275 30T369 28T480 28" fill="none" stroke="#a8eaec" stroke-width="1" opacity=".7"/>', '<path d="M53 37L0 330H64L109 35Z M144 36L96 330H140L189 35Z M351 36L351 330H412L397 36Z M426 37L456 330H480L470 36Z" fill="url(#water)" opacity=".65"/>', '<path d="M0 310Q87 284 160 310T320 312T480 291V360H0Z" fill="#0a3b45"/><path d="M0 328Q78 305 152 327T319 331T480 313V360H0Z" fill="#072d37"/>']
        for i in range(25):
            x = (i*67+17)%480;y=(i*41+66)%300;r=1+(i%4)*.75
            b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#97e7e7" stroke-width=".6" opacity=".18"/>')
        for x,y,s in [(19,305,1),(452,298,1.3),(30,333,.8),(425,336,.8)]:
            b.append(f'<path d="M{x} 360Q{x-9*s} {y+25} {x} {y} M{x} {y+30}Q{x+15*s} {y+9} {x+14*s} {y-3} M{x} {y+40}Q{x-18*s} {y+21} {x-14*s} {y+7}" stroke="#3c8c79" stroke-width="{4*s}" fill="none" stroke-linecap="round" opacity=".8"/>')
        for x,y,d in [(43,111,1),(434,149,-1),(30,225,1),(458,90,-1)]:
            b.append(f'<g transform="translate({x} {y}) scale({d} 1)" fill="#58a2ae" opacity=".45"><path d="M-9 0Q0-6 8 0Q0 6-9 0L-14 5V-5Z"/><circle cx="5" cy="-1" r=".6" fill="#e8f4ec"/></g>')
        b.append('<path d="M443 343Q444 331 451 337Q460 326 463 341Q472 339 471 352H442Z" fill="#a46c86" opacity=".55"/>')
    elif theme == 4:
        b = [_sky('#311934', '#b6665b')]
        b += ['<defs><linearGradient id="sun" x2="0" y2="1"><stop stop-color="#f8d6a3"/><stop offset="1" stop-color="#d57d70"/></linearGradient></defs>', '<circle cx="421" cy="102" r="43" fill="url(#sun)" opacity=".88"/>', '<path d="M377 109H465 M379 119H463 M387 130H455 M399 141H443" stroke="#a25c64" stroke-width="2.3"/>', '<path d="M0 124Q49 113 116 122 M301 57Q353 43 401 52 M15 81Q71 72 139 82" stroke="#f1bba1" stroke-width="1" opacity=".25" fill="none"/>', '<path d="M0 231Q74 169 149 204T287 211T480 185V360H0Z" fill="#754458"/><path d="M0 270Q74 211 158 251T318 239T480 236V360H0Z" fill="#4b3049"/><path d="M0 309Q83 259 182 295T353 293T480 271V360H0Z" fill="#2b233a"/>', '<path d="M0 337Q90 299 181 322T369 320T480 308V360H0Z" fill="#211e30"/>']
        # Wind-sculpted dune ridges; vegetation frames the outer margins.
        b += ['<path d="M0 271Q80 217 159 251 M279 305Q387 275 480 275" stroke="#be7b7d" stroke-width=".8" opacity=".24" fill="none"/>', '<path d="M25 359Q38 312 28 271 M28 282Q5 263 0 277 M28 282Q46 257 67 273 M29 282Q49 278 56 293 M28 281Q15 266 9 252" stroke="#1c1b2b" stroke-width="4" fill="none" stroke-linecap="round"/>', '<path d="M474 360Q459 318 465 285 M465 296Q451 278 433 289 M465 296Q477 278 489 282" stroke="#211d30" stroke-width="4" fill="none" stroke-linecap="round"/>']
        for x,y in [(41,65),(75,55),(443,204)]:
            b.append(f'<path d="M{x-5} {y}Q{x-2} {y-3} {x} {y}Q{x+3} {y-3} {x+6} {y}" stroke="#382742" stroke-width=".8" fill="none" opacity=".8"/>')
    elif theme == 5:
        b = [_sky('#090b25', '#271436'), _stars(4, 40, True)]
        b += ['<circle cx="414" cy="61" r="25" fill="#b446ab" opacity=".2"/><circle cx="414" cy="61" r="17" fill="none" stroke="#e364d8" stroke-width="1" opacity=".6"/>', '<path d="M400 61H428 M414 47V75" stroke="#eea3eb" stroke-width=".6" opacity=".4"/>']
        # Back skyline and bright foreground towers use deterministic windows.
        for i in range(18):
            x=i*29-6;h=37+(i*47)%95
            b += [rect(x,280-h,24,h,'#17192f'),rect(x+3,280-h,1,h,'#58316b',extra='fill-opacity=".4"')]
        for i in range(12):
            x=i*45-12;w=29+(i%3)*5;h=45+(i*53)%138;y=302-h
            b += [rect(x,y,w,h,'#0c1227'),f'<path d="M{x} 302V{y}H{x+w}" stroke="{["#a643a2","#287692","#6251b4"][i%3]}" stroke-width=".8" opacity=".75"/>']
            for row in range(max(0,(h-12)//11)):
                for col in range(2):
                    if (row+i+col)%4!=0:
                        b.append(rect(x+6+col*10,y+8+row*11,4,2,'#6ed3df' if (i+row)%3 else '#dc6ab8',extra='fill-opacity=".45"'))
            if i%3==0:
                b.append(f'<path d="M{x+w/2} {y}V{y-9}" stroke="#d867c6" stroke-width=".7"/><circle cx="{x+w/2}" cy="{y-10}" r="1" fill="#fba2e9"/>')
        b += [rect(0,302,480,58,'#0b1022'),'<path d="M0 311H480 M0 326H480 M0 346H480" stroke="#6d326e" opacity=".4" stroke-width=".7"/>']
        for x in range(-200,701,60):
            b.append(f'<path d="M240 302L{x} 360" stroke="#39567e" stroke-width=".7" opacity=".42"/>')
        b += [rect(5,225,27,9,'#793b82',extra='fill-opacity=".6"'),text(18.5,232,'NIGHT',5,'#e3a8e5',800,'text-anchor="middle" letter-spacing=".4"'),rect(445,238,29,14,'#16516b',extra='fill-opacity=".7"'),text(459.5,248,'PLAY',7,'#98ebf4',800,'text-anchor="middle" letter-spacing=".5"')]
    elif theme == 6:
        return svg(rect(0, 0, 480, 360, '#000000'))
    elif theme == 7:
        b = [_sky('#171324', '#674459')]
        b += ['<circle cx="406" cy="72" r="30" fill="#efbbc9" opacity=".65"/>',
              '<path d="M0 287Q62 251 117 274T234 268T351 275T480 261V360H0Z" fill="#352537"/><path d="M0 316Q81 279 151 306T319 298T480 309V360H0Z" fill="#201e2f"/>',
              '<path d="M6 360Q39 245 25 102 M25 158Q67 102 114 88 M24 179Q5 127 0 111 M29 245Q73 201 113 207 M27 133Q60 69 94 53" fill="none" stroke="#211a2b" stroke-width="9" stroke-linecap="round"/>',
              '<path d="M474 360Q452 286 462 174 M462 218Q430 181 398 184 M462 193Q477 162 489 149" fill="none" stroke="#241c2c" stroke-width="7" stroke-linecap="round"/>']
        for i in range(57):
            x = (i*47+21)%144 if i<38 else 389+(i*29)%90
            y = 42+(i*37)%182 if i<38 else 160+(i*31)%99
            r = 2+(i%4)*.7
            b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{["#e9a9c7","#f6c6d7","#c583ae"][i%3]}" opacity=".65"/>')
        for i in range(20):
            x=(i*73+38)%480;y=(i*41+66)%348
            b.append(f'<path d="M{x} {y}q5-3 5 1q-2 5-5-1Z" fill="#f6bfda" opacity=".5" transform="rotate({i*29} {x} {y})"/>')
        b.append('<path d="M355 317H418 M359 307V325 M412 307V325 M362 307H409" stroke="#836078" stroke-width="2" opacity=".5"/>')
    elif theme == 8:
        b = [_sky('#1b101b', '#65302c')]
        b += ['<defs><radialGradient id="lavaGlow"><stop stop-color="#ff873c" stop-opacity=".6"/><stop offset="1" stop-color="#9c2c29" stop-opacity="0"/></radialGradient></defs>',
              '<ellipse cx="390" cy="202" rx="152" ry="99" fill="url(#lavaGlow)"/>',
              '<path d="M0 263L72 189L153 258L215 180L283 259L386 111L480 247V360H0Z" fill="#342029"/><path d="M304 230L382 117L399 128L473 230L423 204L398 182L382 190L362 175L351 208Z" fill="#4b252b"/>',
              '<path d="M373 130L383 117L397 129L389 138L382 132Z" fill="#ffc76b"/><path d="M382 133L372 166L388 181L382 206L406 225L400 256L432 284L425 313L457 360" fill="none" stroke="#a52f29" stroke-width="14"/><path d="M382 133L372 166L388 181L382 206L406 225L400 256L432 284L425 313L457 360" fill="none" stroke="#ff933d" stroke-width="5"/><path d="M382 133L372 166L388 181L382 206L406 225L400 256L432 284L425 313L457 360" fill="none" stroke="#ffe090" stroke-width="1.1"/>',
              '<path d="M0 286L55 251L124 291L167 272L225 307L290 273L347 296L404 278L480 316V360H0Z" fill="#191825"/>',
              '<path d="M0 330L57 320L77 337L118 327L135 350L185 342 M248 360L276 334L300 344L338 327L362 348" stroke="#a23e32" stroke-width="1.2" fill="none"/>']
        for i in range(33):
            x=(i*89+11)%480;y=(i*47+27)%320;r=.5+(i%3)*.35
            b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffc46a" opacity="{.25+(i%4)*.13:.2f}"/>')
        b += ['<path d="M381 113Q365 83 388 61T384 9" fill="none" stroke="#2b1925" stroke-width="23" opacity=".7"/>']
    elif theme == 9:
        b = [_sky('#061820', '#16423e'), _stars(7, 62, True)]
        b += ['<defs><linearGradient id="aurora" x2="0" y2="1"><stop stop-color="#65e3c2" stop-opacity="0"/><stop offset=".65" stop-color="#78e8b9" stop-opacity=".5"/><stop offset="1" stop-color="#a08ce6" stop-opacity=".1"/></linearGradient></defs>',
              '<path d="M-20 30Q73 94 137 44T278 49T499 35V124Q377 156 299 101T135 112T-20 84Z" fill="url(#aurora)"/>',
              '<path d="M-20 90Q57 132 145 89T296 105T500 89" stroke="#8beebf" stroke-width="1.5" opacity=".37" fill="none"/>',
              '<path d="M-10 107Q83 146 158 108T296 121T493 107" stroke="#b2a0e7" stroke-width="12" opacity=".12" fill="none"/>',
              '<path d="M0 282Q95 257 174 279T330 274T480 267V360H0Z" fill="#24464b"/><path d="M0 312Q92 286 168 312T326 302T480 301V360H0Z" fill="#18333d"/><path d="M0 333Q102 315 190 336T366 328T480 332V360H0Z" fill="#112834"/>',
              '<path d="M0 314Q92 288 168 314T326 304T480 303 M36 336L123 326 M360 330L454 324" fill="none" stroke="#82abae" stroke-width=".8" opacity=".45"/>',
              '<path d="M422 271l-4-17h-21l-5 16h6l4-12h12l3 13Z" fill="#152934"/><path d="M406 254v-18m0 4l-11-9m11 12l10-12" stroke="#152934" stroke-width="2" fill="none"/>']
        for i in range(15):
            x=(i*41+3)%480;y=300+(i*17)%57
            b.append(f'<path d="M{x} {y}h{4+i%5}" stroke="#7caaa8" stroke-width=".5" opacity=".3"/>')
    else:
        b = [rect(0, 0, 480, 360, '#071e36')]
        for x in range(0,481,16):b.append(f'<path d="M{x} 0V360" stroke="#70b2d5" opacity="{.19 if x%80==0 else .075}" stroke-width=".5"/>')
        for y in range(0,361,16):b.append(f'<path d="M0 {y}H480" stroke="#70b2d5" opacity="{.19 if y%80==0 else .075}" stroke-width=".5"/>')
        b += ['<g fill="none" stroke="#9bd8ec" stroke-width=".65" opacity=".45"><circle cx="76" cy="116" r="46"/><circle cx="76" cy="116" r="35"/><path d="M17 116H135 M76 57V175 M39 79L113 153 M39 153L113 79"/><path d="M382 55h64v93h-64z M390 63h48v77h-48z M382 80h64 M414 55v93 M374 55v93 M370 55h8 M370 148h8 M382 156h64 M382 152v8 M446 152v8"/><path d="M18 264h102v62H18z M28 274h82v42H28z M18 294h102 M52 264v62 M18 256h102 M18 252v8 M120 252v8"/><path d="M376 256l33-39 49 33-22 54-60-9z M376 256l60 48 M409 217l-6 70 M458 250l-82 45"/></g>',
              '<g fill="#b1e4f1" opacity=".58">'+''.join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x,y in [(76,70),(76,162),(30,116),(122,116),(382,55),(446,148),(18,264),(120,326),(376,256),(409,217),(436,304)])+'</g>',
              text(360, 334, 'FLOW / 010', 7, '#9bd0e2', 300, 'letter-spacing="2"')]
    return svg(''.join(b))



def menu(theme=1, resume=False):
    """Asymmetric flight-console menu; the engine stamps the hover object at right."""
    theme = max(1, min(10, int(theme)))
    accent = THEME_PALETTES[theme-1][5]
    b = [
        '<defs><linearGradient id="menu-veil"><stop stop-color="#060912" stop-opacity=".98"/><stop offset=".62" stop-color="#080c17" stop-opacity=".86"/><stop offset="1" stop-color="#080c17" stop-opacity=".18"/></linearGradient></defs>',
        rect(0, 0, 480, 360, '#040810', extra='fill-opacity=".36"'),
        rect(0, 0, 305, 360, 'url(#menu-veil)'),
        '<path d="M16 31V15H53 M427 15H464V51 M16 319V345H53 M427 345H464V309" fill="none" stroke="#c4d3e9" stroke-opacity=".26" stroke-width=".6"/>',
        text(32, 59, 'STACK', 34, '#f3f4ff', 200, 'letter-spacing="4"'),
        text(34, 86, '/ FLOW', 22, '#acb6ce', 200, 'letter-spacing="5.7"'),
        f'<path d="M195 43H244 M211 50H244 M228 57H244" stroke="{accent}" opacity=".48" stroke-width=".7"/>',
        '<path d="M32 98H246 M21 119V268" stroke="#a7b8d4" stroke-opacity=".2" stroke-width=".6"/>',
    ]
    for kind, y, h, label in [(1,112,38,'RESUME' if resume else 'PLAY'),
                               (2,162,30,'NEW RUN'),(3,204,30,'THEMES'),(4,246,30,'RUN HISTORY')]:
        primary = kind == 1
        edge = accent if primary else '#8495b4'
        b += [f'<path d="M32 {y}H237L246 {y+9}V{y+h}H32Z" fill="{accent if primary else "#10182a"}" fill-opacity="{.14 if primary else .74}" stroke="{edge}" stroke-opacity="{.7 if primary else .22}" stroke-width=".65"/>',
              text(44,y+h/2+2.5,f'0{kind}',6.4,accent if primary else '#697d9e',300,'letter-spacing=".8"'),
              text(72,y+h/2+4,label,13 if primary else 9.8,'#f7f6ff' if primary else '#c6d1e7',300,'letter-spacing="2.1"'),
              f'<path d="M225 {y+h/2-3}l3 3-3 3" fill="none" stroke="{edge}" stroke-width=".8" opacity=".7"/>',
              rect(19,y+h/2-1,4,2,edge,extra='fill-opacity=".7"')]
    # The open orbital field frames the engine's 120px floating preview object.
    b += [
        f'<ellipse cx="365" cy="185" rx="84" ry="84" fill="none" stroke="{accent}" stroke-opacity=".1" stroke-width=".6"/>',
        '<ellipse cx="365" cy="185" rx="96" ry="43" fill="none" stroke="#a6cbe2" stroke-opacity=".17" stroke-width=".55" transform="rotate(-36 365 185)"/>',
        f'<path d="M365 101A84 84 0 0 1 438 143 M292 227A84 84 0 0 0 365 269" fill="none" stroke="{accent}" stroke-opacity=".7" stroke-width="1"/>',
        '<path d="M365 89V96 M365 274V281 M269 185H276 M454 185H461" stroke="#a9bed9" stroke-opacity=".5" stroke-width=".6"/>',
        '<circle cx="432" cy="134" r="2" fill="#c7e7f5" opacity=".85"/><circle cx="298" cy="236" r="1.5" fill="#c7e7f5" opacity=".55"/>',
        '<path d="M326 294H404" stroke="#b1bfd8" stroke-opacity=".2" stroke-width=".6"/>',
        '<path d="M356 300H374 M362 304H368" stroke="#b1bfd8" stroke-opacity=".35" stroke-width=".6"/>',
        text(32,326,THEME_NAMES[theme-1].upper(),9.4,accent,300,'letter-spacing="1.8"'),
        f'<circle cx="236" cy="321" r="3" fill="{accent}" opacity=".8"/>',
    ]
    return svg(''.join(b))


def menu_button():
    """92x24 fixed screen-space menu button, centered at (46,12)."""
    return svg(rect(.5, .5, 91, 23, '#0b1120', '#91a1c2', 3, extra='fill-opacity=".9" stroke-opacity=".55" stroke-width=".7"')
               + text(46, 15.5, '[ M ]  MENU', 8.3, '#e1e7f8', 300, 'text-anchor="middle" letter-spacing="1"'), 92, 24)


def keycap(label, pressed=False):
    """54x20 action-key indicator, centered at (27,10)."""
    fill = '#604c88' if pressed else '#0c1220'
    edge = '#d9c2ff' if pressed else '#65708b'
    fg = '#ffffff' if pressed else '#a8b3cd'
    b = [rect(.5, .5, 53, 19, fill, edge, 2, extra=f'fill-opacity="{.95 if pressed else .8}" stroke-opacity="{1 if pressed else .4}" stroke-width=".7"')]
    if pressed:
        b += [rect(2, 2, 50, 16, 'none', '#eadfff', 1, extra='stroke-opacity=".25" stroke-width=".5"'),
              '<path d="M5 17H49" stroke="#d6efff" stroke-width=".8" stroke-opacity=".65"/>']
    b.append(text(27, 13.6, str(label), 7.7 if len(str(label))<7 else 6.4, fg, 300,
                  'text-anchor="middle" letter-spacing=".4"'))
    return svg(''.join(b), 54, 20)


def combo_banner(frame):
    """160x60 combo pulse, 12 frames; the numeric count is drawn by the engine."""
    f = max(0, min(11, int(frame)))
    p = f/11
    alpha = .9-(p*.35)
    cx, cy = 80, 30
    b = [rect(0, 0, 160, 60, '#0a1020', extra='fill-opacity=".78"')]
    # Expanding diamond and split rails suggest a kinetic burst without filters.
    radius = 12+f*2.2
    b += [f'<path d="M{cx} {cy-radius}L{cx+radius*2} {cy}L{cx} {cy+radius}L{cx-radius*2} {cy}Z" fill="none" stroke="#b48aff" stroke-width=".8" opacity="{(1-p)*.5:.3f}"/>']
    reach = 20+f*4
    for side in (-1, 1):
        x1 = cx+side*18
        x2 = cx+side*reach
        b += [f'<path d="M{x1} 6H{x2} M{x1} 54H{x2}" stroke="#b9edff" stroke-width=".7" opacity="{alpha:.3f}"/>']
    for i in range(6):
        x = 14+i*25
        y = 8 if i%2 else 51
        drift = (f*.65)*(1 if i%2 else -1)
        b.append(f'<path d="M{x+drift-1.4} {y}L{x+drift} {y-2}L{x+drift+1.4} {y}L{x+drift} {y+2}Z" fill="#d5b8ff" opacity="{(1-p)*.7:.3f}"/>')
    b += [text(80, 16, 'COMBO', 11.5, '#dcc9ff', 300, 'text-anchor="middle" letter-spacing="5"')]
    return svg(''.join(b), 160, 60)


COMBO_NAMES = [
    'START!', 'KEEP IT UP!', 'NICE!', 'SMOOTH!', 'GREAT!',
    'ON FIRE!', 'CRAZY!', 'WILD!', 'UNREAL!', 'INSANE!',
    'PHENOMENAL!', 'UNSTOPPABLE!', 'LEGENDARY!', 'GODLIKE!', 'BEYOND LIMITS!',
]


def combo_title(n):
    """120x14 milestone caption; center at (60,7), slim baseline at y10."""
    n = max(1, min(15, int(n)))
    c = '#b7dbec' if n < 5 else '#d8bdff' if n < 10 else '#ffcf9b'
    return svg(text(60, 10, COMBO_NAMES[n-1], 7.8, c, 300,
                    'text-anchor="middle" letter-spacing="1"'), 120, 14)


def arrow_keycap(arrow, pressed=False):
    """40x26 arrow-only key; center (20,13), for a keyboard-shaped cluster."""
    c = '#e4d4ff' if pressed else '#8493b4'
    b = [rect(.5,.5,39,25,'#634b89' if pressed else '#0a1020',c,2,
              extra=f'fill-opacity="{.95 if pressed else .82}" stroke-opacity="{1 if pressed else .45}" stroke-width=".7"')]
    if pressed:
        b += [rect(2,2,36,22,'none','#e0cdff',1,extra='stroke-opacity=".25" stroke-width=".6"'),
              '<path d="M5 22H35" stroke="#d6efff" opacity=".65" stroke-width=".7"/>']
    b += [text(20,18,str(arrow),16,'#ffffff' if pressed else '#a5b2cc',300,'text-anchor="middle"')]
    return svg(''.join(b),40,26)


def _back_button():
    return rect(16,16,84,26,'#0d1424','#7b87a1',3,extra='fill-opacity=".95" stroke-opacity=".6" stroke-width=".6"') + text(58,33,'BACK',9,'#d4dce9',300,'text-anchor="middle" letter-spacing="1.6"')


def theme_menu(theme=1):
    """Ten independently illustrated cards in two rows; root owns selection input."""
    theme = max(1,min(10,int(theme)))
    b = [rect(0,0,480,360,'#070b16',extra='fill-opacity=".93"'),_back_button(),
         text(240,64,'CHOOSE YOUR WORLD',22,'#f2f3fc',200,'text-anchor="middle" letter-spacing="2.3"')]
    for i,name in enumerate(THEME_NAMES,1):
        x=12+((i-1)%5)*94;y=96+((i-1)//5)*74
        accent=THEME_PALETTES[i-1][5]
        selected=i==theme
        b += [rect(x-1,y-1,82,64,'#171728' if selected else '#0e1420',accent if selected else '#424c63',3,
                   extra=f'stroke-opacity="{.95 if selected else .65}" stroke-width="{1.1 if selected else .55}"')]
        art=landscape(i);art=art[art.index('>')+1:art.rfind('</svg>')]
        # Each miniature has a private SVG definition namespace.
        art=art.replace('id="','id="thumb'+str(i)+'-').replace('url(#','url(#thumb'+str(i)+'-')
        b += [f'<defs><clipPath id="clip{i}"><rect x="{x}" y="{y}" width="80" height="40" rx="2"/></clipPath></defs>',
              f'<g clip-path="url(#clip{i})"><g transform="translate({x} {y}) scale(.1666666667 .1111111111)">{art}</g></g>',
              text(x+40,y+51,name.upper(),6.9,'#ffffff' if selected else '#b6c0d4',300,'text-anchor="middle" letter-spacing=".25"')]
        for j,c in enumerate(THEME_PALETTES[i-1]):
            b += [rect(x+7+j*9.6,y+56,8.3,2,c)]
        if selected:
            b += [rect(x+66,y+3,10,10,'#0c1320',accent,2,extra='stroke-width=".5"'),
                  f'<path d="M{x+68} {y+8}l2 2 4-5" fill="none" stroke="{accent}" stroke-width="1"/>']
    accent=THEME_PALETTES[theme-1][5]
    b += ['<path d="M24 258H345 M24 333H345" stroke="#a6b7d5" opacity=".13" stroke-width=".6"/>',
          text(24,286,'SELECTED THEME',6.7,'#7d8da9',300,'letter-spacing="1.9"'),
          text(24,310,THEME_NAMES[theme-1].upper(),16,accent,200,'letter-spacing="2"'),
          '<ellipse cx="410" cy="298" rx="49" ry="29" fill="none" stroke="#bed2e8" stroke-opacity=".17" stroke-width=".6" transform="rotate(-32 410 298)"/>',
          f'<path d="M410 247A51 51 0 0 1 455 274 M365 322A51 51 0 0 0 410 349" stroke="{accent}" stroke-opacity=".35" stroke-width=".7" fill="none"/>']
    return svg(''.join(b))


def history_panel():
    """Five-row history shell; scores, run data and page number are stamped live."""
    b=[rect(0,0,480,360,'#060b15',extra='fill-opacity=".94"'),_back_button(),
       text(24,76,'RUN HISTORY',24,'#f0f2fa',200,'letter-spacing="2.4"'),
       text(334,44,'PERSONAL BEST',7.5,'#c7b9e4',300,'letter-spacing="1.5"')]
    for x,label in [(24,'RUN'),(70,'SCORE'),(180,'LINES'),(226,'COMBO'),(282,'THEME / STATUS')]:
        b+=[text(x,101,label,7.4,'#8998b6',300,'letter-spacing=".5"')]
    for row in range(5):
        y=107+row*32
        b+=[rect(18,y,444,28,'#121a2b' if row%2==0 else '#0c1423',r=2,extra='fill-opacity=".8"'),
            f'<path d="M18 {y+29}H462" stroke="#53617e" opacity=".16" stroke-width=".5"/>']
    for x,label in [(96,'PREVIOUS'),(284,'NEXT')]:
        b += [rect(x,288,100,28,'#10192c','#657390',3,extra='stroke-opacity=".55" stroke-width=".6"'),
              text(x+50,306,label,8,'#bfcae0',300,'text-anchor="middle" letter-spacing="1.3"')]
    b += [text(240,338,'STOP KEEPS RUNS · SAVE PROJECT TO KEEP AFTER CLOSING',6.5,'#8e9bb5',300,
               'text-anchor="middle" letter-spacing=".45"')]
    return svg(''.join(b))


def ambient_spark():
    """6x6 soft ambient mote, centered at (3,3); no opaque background."""
    return svg('<circle cx="3" cy="3" r="3" fill="#afd8ff" opacity=".055"/>'
               '<circle cx="3" cy="3" r="1.9" fill="#c5dcff" opacity=".17"/>'
               '<circle cx="3" cy="3" r=".8" fill="#f2f4ff" opacity=".8"/>',6,6)


def hover_outline(kind):
    """Full-stage transparent hover frame. All coordinates match live hitboxes."""
    kind=int(kind)
    c='#d3c4ff'
    if 1 <= kind <= 4:
        y,h=[(112,38),(162,30),(204,30),(246,30)][kind-1]
        b=(f'<path d="M32 {y}H237L246 {y+9}V{y+h}H32Z" fill="{c}" fill-opacity=".07" stroke="{c}" stroke-opacity=".95" stroke-width="1"/>'
           +rect(32,y+5,1.5,h-10,c)
           +f'<path d="M254 {y+h/2-4}l4 4-4 4" stroke="{c}" stroke-width="1" fill="none"/>')
    else:
        if kind==5:
            x,y,w,h=16,16,84,26
        elif kind in (6,7):
            x,y,w,h=(96 if kind==6 else 284),288,100,28
        elif 11<=kind<=20:
            i=kind-11
            x,y,w,h=10+(i%5)*94,94+(i//5)*74,84,66
            c=THEME_PALETTES[i][5]
        else:
            return svg('')
        b=(rect(x,y,w,h,c,c,2,extra='fill-opacity=".06" stroke-opacity=".95" stroke-width="1"')
           +f'<path d="M{x-3} {y+8}V{y-3}H{x+8} M{x+w-8} {y+h+3}H{x+w+3}V{y+h-8}" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width=".7"/>')
    return svg(b)


def _object_cube(x,y,s,top='#cfb6ff',left='#7455b1',right='#3d386f'):
    """Small hand-projected solid; y is the top diamond's horizontal axis."""
    return (f'<path d="M{x} {y-s*.56}L{x+s} {y}L{x} {y+s*.56}L{x-s} {y}Z" fill="{top}" stroke="#edebff" stroke-opacity=".45" stroke-width=".5"/>'
            f'<path d="M{x-s} {y}L{x} {y+s*.56}V{y+s*1.6}L{x-s} {y+s*1.04}Z" fill="{left}" stroke="#d9d6ff" stroke-opacity=".28" stroke-width=".5"/>'
            f'<path d="M{x} {y+s*.56}L{x+s} {y}V{y+s*1.04}L{x} {y+s*1.6}Z" fill="{right}" stroke="#d9d6ff" stroke-opacity=".28" stroke-width=".5"/>'
            f'<path d="M{x-s+2} {y+1}L{x-2} {y+s*.56}V{y+s*1.6-3}" fill="none" stroke="#fff" opacity=".16" stroke-width=".6"/>')


def _object_glint(x,y,s=4,c='#fff4d5'):
    return (f'<path d="M{x-s} {y}H{x+s} M{x} {y-s}V{y+s}" stroke="{c}" stroke-width=".65" opacity=".85"/>'
            f'<circle cx="{x}" cy="{y}" r="1" fill="#fff"/>')


def hover_object(kind,frame=0):
    """Original 120px floating menu sculptures, with eight subtle orbit frames.

    The transparent art is centered at (60,60). Camera movement belongs to the
    Scratch renderer; these frames move a satellite and gently turn each object.
    """
    from math import cos,sin,pi
    kind=int(kind)
    frame=int(frame)%8
    angle=frame*pi/4
    turn=sin(angle)*2
    defs='''<defs>
      <linearGradient id="obj-violet" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#eee4ff"/><stop offset=".4" stop-color="#a38bdd"/><stop offset="1" stop-color="#34245d"/></linearGradient>
      <linearGradient id="obj-blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ccf8ff"/><stop offset=".42" stop-color="#5eb9dc"/><stop offset="1" stop-color="#153d79"/></linearGradient>
      <linearGradient id="obj-gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff2c0"/><stop offset=".45" stop-color="#e5ae5b"/><stop offset="1" stop-color="#8f4e38"/></linearGradient>
      <linearGradient id="obj-pink" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff0ed"/><stop offset=".5" stop-color="#f3a6c9"/><stop offset="1" stop-color="#a1508d"/></linearGradient>
      <linearGradient id="obj-lava" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff3b6"/><stop offset=".45" stop-color="#ffab48"/><stop offset="1" stop-color="#b6433a"/></linearGradient>
      <linearGradient id="obj-aurora" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#8aeed0" stop-opacity=".08"/><stop offset=".28" stop-color="#94ffe1"/><stop offset=".65" stop-color="#a1aeff" stop-opacity=".75"/><stop offset="1" stop-color="#dfb4fa" stop-opacity=".08"/></linearGradient>
      <radialGradient id="obj-sphere" cx=".3" cy=".22" r=".8"><stop stop-color="#c4d2ef"/><stop offset=".36" stop-color="#667aa9"/><stop offset=".8" stop-color="#2b355d"/><stop offset="1" stop-color="#10182f"/></radialGradient>
    </defs>'''
    b=[]
    if kind==1:
        # A four-mino T sculpture, built from individual translucent-looking faces.
        for col,row in [(-1,0),(0,0),(1,0),(0,1)]:
            b.append(_object_cube(66+(col-row)*16,42+(col+row)*9,16))
        b += ['<circle cx="90" cy="84" r="13" fill="#0c1729" stroke="#a7e7f4" stroke-width=".7"/>',
              '<path d="M87 78L97 84L87 90Z" fill="#d5f7ff"/>',_object_glint(28,29,4,'#c7c3fb')]
    elif kind==2:
        b += [_object_cube(60,42,26,'#f8e9be','#aa8054','#6f5265'),
              '<path d="M60 26V54L84 42 M60 54L36 42" stroke="#fff5d4" stroke-width=".7" fill="none" opacity=".8"/>',
              '<path d="M24 26L31 32 M89 27L83 33 M17 59H26 M94 59H103 M39 91L34 99 M81 91L86 99" stroke="#d9c7ab" stroke-width=".7" opacity=".7"/>',
              _object_glint(87,27,6),_object_glint(24,82,3,'#c7dcff')]
    elif kind==3:
        b += ['<ellipse cx="60" cy="60" rx="47" ry="18" transform="rotate(-27 60 60)" fill="none" stroke="#7a709a" stroke-width="1"/>',
              '<circle cx="60" cy="57" r="28" fill="url(#obj-sphere)" stroke="#d5d7f3" stroke-opacity=".7" stroke-width=".6"/>',
              '<path d="M38 42Q59 26 79 42 M33 53Q61 34 85 52 M34 67Q60 48 87 61 M42 78Q64 60 84 71" fill="none" stroke="#d2c2f2" stroke-opacity=".22" stroke-width="1"/>',
              '<path d="M17 78Q56 97 104 40" stroke="#aeb3d9" stroke-width="1" fill="none"/>']
        for x,y,c in [(20,72,'#a593ff'),(36,82,'#f29fc9'),(59,80,'#ffd57b'),(80,68,'#a5e4ae'),(96,49,'#83dce9')]:
            b += [f'<circle cx="{x}" cy="{y}" r="5" fill="{c}" stroke="#fff" stroke-opacity=".45" stroke-width=".6"/>',f'<circle cx="{x-1.5}" cy="{y-1.5}" r="1.2" fill="#fff" opacity=".65"/>']
        b.append(_object_glint(92,24,3,'#c7dcff'))
    elif kind==4:
        b += ['<path d="M40 34H28Q26 59 46 61 M80 34H92Q94 59 74 61" fill="none" stroke="#b98449" stroke-width="7"/>',
              '<path d="M39 33H30Q29 53 43 56 M81 33H90Q91 53 77 56" fill="none" stroke="#ffe6a5" stroke-width="1.5"/>',
              '<path d="M37 29H83L78 57Q75 68 60 70Q45 68 42 57Z" fill="url(#obj-gold)" stroke="#f0ce87" stroke-width=".7"/>',
              '<ellipse cx="60" cy="29" rx="23" ry="6" fill="#5f443d" stroke="#ffe5a3" stroke-width="1"/>',
              '<ellipse cx="60" cy="29" rx="18" ry="3.5" fill="#b98a50"/>',
              '<path d="M46 36L49 55Q50 61 56 63" fill="none" stroke="#fff0ba" stroke-width="2" opacity=".6"/>',
              '<path d="M55 69H65V84H55Z" fill="url(#obj-gold)"/>',
              '<path d="M43 83L60 78L77 83V92L60 98L43 92Z" fill="#815a45"/>',
              '<path d="M43 83L60 78L77 83L60 89Z" fill="#e0bc79"/>',
              '<path d="M60 89L77 83V92L60 98Z" fill="#5d4350"/>',
              '<path d="M60 39L62 45L68 45L63 49L65 55L60 51L55 55L57 49L52 45H58Z" fill="#fff2c2" opacity=".9"/>',
              _object_glint(89,22,4)]
    elif kind==5:
        arrow='M23 54L47 31V45H69Q94 45 94 70V84H79V70Q79 60 68 60H47V75Z'
        b += [f'<path d="{arrow}" transform="translate(0 6)" fill="#203657" stroke="#516d92" stroke-width=".5"/>',
              f'<path d="{arrow}" fill="url(#obj-blue)" stroke="#c3e9f9" stroke-width=".7"/>',
              '<path d="M27 54L44 38 M52 49H70Q87 49 89 65" fill="none" stroke="#e0f6ff" stroke-opacity=".6" stroke-width=".9"/>',
              _object_glint(31,90,3,'#c8d9f2')]
    elif kind in (6,7):
        b += ['<path d="M35 22L86 29L90 91L38 84Z" fill="#243650" stroke="#7092b6" stroke-width=".6"/>',
              '<path d="M29 29L81 23L86 88L35 96Z" fill="#415474" stroke="#88a8c4" stroke-width=".6"/>',
              '<path d="M29 31L68 27L84 40L85 92L32 98Z" fill="url(#obj-blue)" stroke="#c4e3ef" stroke-width=".8"/>',
              '<path d="M68 27L69 43L84 40Z" fill="#e5faff" stroke="#8cb4cf" stroke-width=".6"/>',
              '<path d="M40 44L59 42 M40 49L63 46 M39 85L74 81" stroke="#e4f7ff" stroke-opacity=".4" stroke-width=".8"/>']
        direction=-1 if kind==6 else 1
        b += [f'<g transform="translate(59 66) scale({direction} 1)"><path d="M-14-4H2V-12L16 0L2 12V4H-14Z" fill="#f3faff" stroke="#fff" stroke-width=".5"/></g>',_object_glint(96,27,3,'#bde6ed')]
    elif kind==11:
        b += ['<ellipse cx="59" cy="58" rx="49" ry="15" fill="none" stroke="#a7a2d5" stroke-opacity=".55" stroke-width="2.4" transform="rotate(-28 59 58)"/>',
              '<circle cx="59" cy="56" r="28" fill="url(#obj-sphere)" stroke="#b4b9e4" stroke-width=".6"/>',
              '<path d="M37 40Q51 34 73 48 M32 51Q59 41 81 58 M38 69Q57 61 78 71" fill="none" stroke="#a18ec7" stroke-width="4" opacity=".22"/>',
              '<path d="M15 80Q52 93 104 35" stroke="#b9b0e4" stroke-width="2.1" fill="none"/>',
              '<path d="M17 83Q57 95 106 38" stroke="#6d81af" stroke-width=".6" fill="none"/>',
              '<circle cx="94" cy="84" r="7" fill="url(#obj-violet)" stroke="#c1c9e8" stroke-width=".5"/>',
              _object_glint(29,22,4,'#cbc8f7'),_object_glint(95,21,2,'#bde3ff')]
    elif kind==12:
        b += ['<path d="M12 84L60 62L107 85L60 106Z" fill="#1d3544" stroke="#658b97" stroke-width=".6"/>',
              '<path d="M12 84L60 95L107 85L60 106Z" fill="#0b2431"/>',
              '<path d="M20 80L49 34L77 86Z" fill="#7391a5"/>',
              '<path d="M49 34L48 85L77 86Z" fill="#375769"/>',
              '<path d="M39 51L49 34L61 57L51 52L46 55L44 49Z" fill="#d7e8ea"/>',
              '<path d="M43 90L75 20L105 84L79 95Z" fill="#9bb8c6" stroke="#bcd6dd" stroke-width=".6"/>',
              '<path d="M75 20L79 95L105 84Z" fill="#3c637b"/>',
              '<path d="M61 51L75 20L90 53L80 45L76 51L71 40L65 51Z" fill="#eff5f0"/>',
              '<path d="M75 20L76 51L80 45L90 53Z" fill="#accbd6"/>',
              '<path d="M58 77L64 64 M84 78L81 63" stroke="#d7e8ea" stroke-opacity=".35" stroke-width=".6"/>',
              '<circle cx="27" cy="28" r="6" fill="#e4eee8" opacity=".8"/>']
    elif kind==13:
        b += ['<path d="M12 82Q29 82 38 53Q49 18 82 30Q104 39 98 57Q85 44 73 49Q64 53 69 65Q82 79 107 80L98 95Q64 108 29 94Z" fill="#1f6c9a" stroke="#89e2e9" stroke-width=".7"/>',
              '<path d="M15 84Q35 83 43 56Q52 30 76 33Q95 34 98 56Q88 43 75 44Q54 45 59 66Q63 79 83 84Q56 91 35 89Z" fill="url(#obj-blue)"/>',
              '<path d="M42 57Q51 26 78 31Q100 35 98 56L91 49L84 50L79 45L71 49L66 47L61 54L55 56L50 66" fill="none" stroke="#e2fbf5" stroke-width="3.2" stroke-linejoin="round"/>',
              '<path d="M20 86Q42 94 61 84 M32 96Q62 102 92 91 M47 71Q50 85 67 88" fill="none" stroke="#9ae7e7" stroke-width=".8" opacity=".7"/>',
              '<circle cx="38" cy="39" r="2.5" fill="#b9eeec"/><circle cx="52" cy="23" r="1.5" fill="#b9eeec"/><circle cx="91" cy="25" r="2" fill="#b9eeec"/>']
    elif kind==14:
        b += ['<circle cx="60" cy="54" r="32" fill="#eba794" opacity=".08"/>',
              '<circle cx="60" cy="54" r="27" fill="url(#obj-gold)" stroke="#ffe0b6" stroke-width=".5"/>',
              '<path d="M34 59H86 M36 65H84 M40 71H80 M47 77H73" stroke="#b96570" stroke-width="2"/>',
              '<path d="M12 86Q35 63 60 82Q81 66 107 84L104 92L61 104L16 93Z" fill="#79516c"/>',
              '<path d="M13 86Q41 73 61 91Q83 80 107 84L89 98L61 104L33 99Z" fill="#382d50" stroke="#c08d9e" stroke-opacity=".6" stroke-width=".5"/>',
              '<path d="M30 90Q58 80 83 90 M42 97Q61 91 80 97" fill="none" stroke="#d9a0a8" stroke-opacity=".45" stroke-width=".6"/>',
              '<path d="M22 44H31 M89 44H98 M60 13V21 M31 22L37 28 M83 28L89 22" stroke="#ecc7ac" stroke-width=".7" opacity=".6"/>']
    elif kind==15:
        b += ['<path d="M15 88L59 65L106 88L61 109Z" fill="#171c37" stroke="#8763a7" stroke-width=".6"/>',
              '<path d="M61 109V101L106 81V88Z" fill="#0c1027"/>',
              '<path d="M24 62L38 55L52 62V90L38 97L24 90Z" fill="#1d2942" stroke="#64769c" stroke-width=".5"/>',
              '<path d="M70 47L85 40L99 47V86L85 93L70 86Z" fill="#252443" stroke="#7e70a3" stroke-width=".5"/>',
              '<path d="M43 27L60 18L77 27V87L60 96L43 87Z" fill="#1a233d" stroke="#7bd1e7" stroke-width=".7"/>',
              '<path d="M43 27L60 36L77 27 M60 36V96 M60 18V9" stroke="#97e8f4" stroke-width=".7" fill="none"/>',
              '<path d="M43 87V27L60 18 M77 87V27" stroke="#d392e2" stroke-width="1.2" fill="none" opacity=".8"/>',
              '<circle cx="60" cy="8" r="1.8" fill="#ffc3ed"/>']
        for row in range(5):
            y=37+row*10
            b += [f'<path d="M48 {y}l7 4 M66 {y+4}l6-3" stroke="{["#8be1eb","#d7a2e6"][row%2]}" stroke-width="2.6" opacity=".85"/>']
        for x,y in [(29,71),(29,80),(84,55),(84,65),(84,75)]:
            b.append(f'<path d="M{x} {y}l5 2" stroke="#dd95dc" stroke-width="1.5"/>')
    elif kind==16:
        b += ['<ellipse cx="60" cy="60" rx="47" ry="17" fill="none" stroke="#fff" stroke-width=".55" opacity=".3" transform="rotate(-25 60 60)"/>',
              '<circle cx="60" cy="58" r="30" fill="#000" stroke="#fff" stroke-width=".7"/>',
              '<circle cx="60" cy="58" r="32.5" fill="none" stroke="#fff" stroke-width=".4" stroke-opacity=".25"/>',
              '<path d="M17 78Q53 96 104 36" stroke="#fff" stroke-width="1.2" fill="none"/>',
              '<path d="M20 82Q65 93 102 43 M32 29Q60 12 86 38" stroke="#fff" stroke-opacity=".4" stroke-width=".5" fill="none"/>',
              '<path d="M29 42A35 35 0 0 1 52 25" stroke="#fff" stroke-width="1.2" fill="none"/>',
              _object_glint(97,85,2,'#fff'),'<circle cx="23" cy="24" r="1" fill="#fff"/>']
    elif kind==17:
        b += ['<path d="M25 98Q66 79 78 34 M47 82Q36 65 24 63 M64 62Q79 64 94 53" fill="none" stroke="#72596b" stroke-width="3.5" stroke-linecap="round"/>',
              '<path d="M72 68Q89 70 94 61Q81 56 72 68 M42 80Q33 66 24 70Q25 82 42 80" fill="#8bbaa7" stroke="#bdd4bd" stroke-width=".5"/>']
        for rot in range(0,360,72):
            b.append(f'<path d="M60 57C45 53 38 33 49 25Q56 20 60 31Q64 20 71 25C82 33 75 53 60 57Z" fill="url(#obj-pink)" stroke="#f4cfdf" stroke-width=".6" transform="rotate({rot} 60 57)"/>')
        b += ['<circle cx="60" cy="57" r="7" fill="#f5cfb8"/>']
        for i in range(5):
            x=60+cos(i*2*pi/5)*10;y=57+sin(i*2*pi/5)*10
            b += [f'<path d="M60 57L{x:.2f} {y:.2f}" stroke="#b57995" stroke-width=".6"/><circle cx="{x:.2f}" cy="{y:.2f}" r="1.2" fill="#f6e4b4"/>']
        b.append('<path d="M90 88Q99 76 105 84Q102 93 90 88Z" fill="#e8adcf" stroke="#f2cddf" stroke-width=".5"/>')
    elif kind==18:
        b += ['<path d="M11 86L58 68L107 87L60 105Z" fill="#331c28" stroke="#8b4b4b" stroke-width=".6"/>',
              '<path d="M22 84L47 35L72 31L101 86L61 99Z" fill="#593b43" stroke="#b17160" stroke-width=".6"/>',
              '<path d="M72 31L61 99L101 86Z" fill="#302737"/>',
              '<path d="M47 35L59 30L72 31L68 42L58 45L49 41Z" fill="#ffbe66"/>',
              '<ellipse cx="59" cy="36" rx="11" ry="3.5" fill="#8d3d38" stroke="#ffd397" stroke-width=".7"/>',
              '<path d="M55 42L59 54L51 65L60 76L56 94 M67 42L72 56L69 66L80 81L85 89" fill="none" stroke="#e87b44" stroke-width="5"/>',
              '<path d="M55 42L59 54L51 65L60 76L56 94 M67 42L72 56L69 66L80 81L85 89" fill="none" stroke="#ffe299" stroke-width="1.4"/>',
              '<path d="M48 27Q36 18 48 12 M61 24Q75 18 65 8 M74 25Q87 19 83 11" stroke="#ceaaa5" stroke-opacity=".45" stroke-width="4" fill="none" stroke-linecap="round"/>',
              '<circle cx="35" cy="37" r="1.5" fill="#f8bf77"/><circle cx="86" cy="35" r="1.2" fill="#f8bf77"/>']
    elif kind==19:
        b += ['<path d="M16 85L59 67L105 85L61 105Z" fill="#152e42" stroke="#7faec0" stroke-width=".6"/>',
              '<path d="M27 81L45 59L59 82L74 66L94 87L61 98Z" fill="#355069"/>',
              '<path d="M39 67L45 59L52 70L46 67L43 70Z M68 73L74 66L81 77L73 73Z" fill="#bbd4d9"/>',
              '<path d="M18 32Q36 7 58 34T103 29L99 67Q78 78 57 50T23 70Z" fill="url(#obj-aurora)" opacity=".62"/>',
              '<path d="M18 32Q36 7 58 34T103 29 M21 42Q38 16 59 44T102 39" fill="none" stroke="#b3f8d8" stroke-width="1" opacity=".8"/>']
        for x in range(25,98,7):
            y=24+((x*7)%23)
            b.append(f'<path d="M{x} {y}l-2 27" stroke="#c7f2e8" stroke-opacity=".16" stroke-width=".8"/>')
        b += [_object_glint(31,18,3,'#d6e9ee'),'<circle cx="91" cy="14" r="1.2" fill="#d6e9ee"/>']
    elif kind==20:
        b += ['<path d="M14 85L59 65L106 86L61 108Z" fill="#11334d" fill-opacity=".5" stroke="#90c9e5" stroke-opacity=".4" stroke-width=".6"/>',
              '<path d="M60 18L94 37V78L60 98L26 78V37Z" fill="#174263" fill-opacity=".25" stroke="#a9e1f2" stroke-width="1"/>',
              '<path d="M26 37L60 57L94 37 M60 57V98" fill="none" stroke="#c8effc" stroke-width="1"/>',
              '<path d="M60 18V59L26 78 M60 59L94 78" fill="none" stroke="#75aeca" stroke-width=".65" stroke-dasharray="3 3"/>',
              '<path d="M43 28L77 48V88 M77 28L43 48V88 M26 57L60 77L94 57" fill="none" stroke="#9dd5ed" stroke-opacity=".45" stroke-width=".55"/>',
              '<path d="M20 35L15 32 M60 11V5 M101 80L107 83 M26 84L21 87" stroke="#a3d8ea" stroke-width=".65"/>']
        for x,y in [(60,18),(94,37),(94,78),(60,98),(26,78),(26,37),(60,57)]:
            b.append(f'<circle cx="{x}" cy="{y}" r="1.9" fill="#d9f5ff"/>')
    else:
        return svg('',120,120)
    # A tiny orbiting pin gives all eight costumes a visible, restrained motion.
    pinx=60+cos(angle)*49
    piny=60+sin(angle)*39
    pin='#ffffff' if kind==16 else '#d5e9f8'
    b.append(f'<circle cx="{pinx:.2f}" cy="{piny:.2f}" r="1.1" fill="{pin}" opacity=".65"/>')
    return svg(defs+f'<g transform="rotate({turn:.3f} 60 60)">'+''.join(b)+'</g>',120,120)
