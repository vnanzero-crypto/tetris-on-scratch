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
        text(134, 101, 'HOLD', 11, '#f0eff5', 800, 'text-anchor="end" letter-spacing="1.2"'),
        text(24, 65, 'COMBO', 9, '#aaa7bb', 300, 'letter-spacing="1.8"'),
        rect(24, 89, 110, 2, '#77708c', extra='fill-opacity=".28"'),
        '<path d="M24 108H135" stroke="#fff" stroke-opacity=".15" stroke-width=".6"/>',
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
    name = ['SINGLE', 'DOUBLE', 'TRIPLE', 'QUAD'][n-1]
    c = '#faf6ff' if n < 4 else '#cdb1ff'
    return svg(
        rect(0, 0, 130, 30, '#111015', extra='fill-opacity=".88"')
        + '<path d="M0 0H130 M0 30H130" stroke="#b19bd0" stroke-opacity=".55" stroke-width=".5"/>'
        + text(65, 21, name, 17, c, 900, 'text-anchor="middle" letter-spacing="2.5"'),
        130, 30,
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
    """Full-stage menu overlay with dedicated theme and run-history pages."""
    theme = max(1, min(10, int(theme)))
    accent = THEME_PALETTES[theme-1][5]
    b = [rect(0, 0, 480, 360, '#060a14', extra='fill-opacity=".62"'),
         rect(104, 26, 272, 185, '#080d19', accent, 4, extra='fill-opacity=".76" stroke-opacity=".24" stroke-width=".6"'),
         text(240, 65, 'STACK / FLOW', 28, '#f5f3ff', 200, 'text-anchor="middle" letter-spacing="3.2"'),
         text(240, 88, 'A LITTLE FOCUS. A LITTLE FLOW.', 7.2, '#aeb5ce', 300, 'text-anchor="middle" letter-spacing="1.9"'),
         text(240, 112, 'YOUR RUN IS PAUSED' if resume else 'READY WHEN YOU ARE', 7.5, accent, 300, 'text-anchor="middle" letter-spacing="1.6"'),
         rect(140, 130, 200, 38, 'none', accent, 3, extra='stroke-opacity=".15" stroke-width="3"'),
         rect(142, 132, 196, 34, '#15192a', accent, 2, extra='fill-opacity=".94" stroke-opacity=".85" stroke-width=".8"'),
         text(240, 154, 'RESUME' if resume else 'PLAY', 15, '#f8f7ff', 300, 'text-anchor="middle" letter-spacing="4"'),
         rect(142, 174, 196, 26, '#0c111e', '#58627a', 2, extra='fill-opacity=".8" stroke-width=".6"'),
         text(240, 191, 'NEW RUN', 10, '#b4bed5', 300, 'text-anchor="middle" letter-spacing="2.8"')]
    for x,label in [(72,'THEMES'),(248,'RUN HISTORY')]:
        b += [rect(x,224,160,30,'#0c1322','#626780',3,extra='fill-opacity=".94" stroke-opacity=".7" stroke-width=".6"'),
              text(x+80,243,label,10,'#d4d9e8',300,'text-anchor="middle" letter-spacing="1.7"')]
    b += [text(240,288,THEME_NAMES[theme-1].upper(),8.5,accent,300,'text-anchor="middle" letter-spacing="2.5"'),
          text(240,325,'YOUR NEXT PERSONAL BEST STARTS HERE.',7,'#8c96b0',300,'text-anchor="middle" letter-spacing="1.3"')]
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
    b += [text(240,274,'SELECTED  /  '+THEME_NAMES[theme-1].upper(),10,THEME_PALETTES[theme-1][5],300,
               'text-anchor="middle" letter-spacing="1.8"'),
          text(240,300,'DISTINCT BLOCKS. DISTINCT ATMOSPHERES.',7,'#7d8da9',300,
               'text-anchor="middle" letter-spacing="1"')]
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
