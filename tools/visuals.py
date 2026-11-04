"""Original vector artwork for Stack / Flow's competitive Scratch layout."""
from html import escape

# Familiar competitive falling-block colors, with distinct identities at 16px.
COLORS = ['#41cfe8', '#5685e8', '#efa54a', '#e9cf51', '#70c864', '#a777d8', '#df637b']


def svg(body, w=480, h=360):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


def text(x, y, s, size=10, color='#eeeeef', weight=500, extra=''):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans Condensed,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(s)}</text>'


def rect(x, y, w, h, fill, stroke='none', r=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def block(c, ghost=False):
    """16px sharp, flat minos; the ghost is a fine hollow wireframe."""
    if ghost:
        return svg(rect(.8, .8, 14.4, 14.4, c, c, extra='fill-opacity=".035" stroke-opacity=".6" stroke-width=".8"'), 16, 16)
    return svg(
        rect(.3, .3, 15.4, 15.4, c)
        + '<path d="M.3 15.7H15.7V.3" stroke="#000" stroke-opacity=".28" stroke-width=".8" fill="none"/>'
        + '<path d="M.5 15V.5H15" stroke="#fff" stroke-opacity=".24" stroke-width=".6" fill="none"/>'
        + rect(1.4, 1.4, 13.2, 13.2, 'none', '#fff', extra='stroke-opacity=".065" stroke-width=".5"'),
        16, 16,
    )


def arena():
    b = [
        '<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#161619"/><stop offset=".52" stop-color="#0e0e11"/><stop offset="1" stop-color="#1b1821"/></linearGradient></defs>',
        rect(0, 0, 480, 360, 'url(#bg)'),
        '<path d="M0 222L153 29V360H0Z" fill="#fff" opacity=".014"/>',
        '<path d="M480 0L328 178V0Z M480 235L381 360H480Z" fill="#fff" opacity=".016"/>',
        '<path d="M0 270L145 87 M348 357L480 191" fill="none" stroke="#fff" stroke-opacity=".035" stroke-width=".6"/>',
        # The exact 10x20 playfield remains at (160,20)..(320,340).
        rect(160, 20, 160, 320, '#070709'),
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
        text(24, 49, 'MARATHON', 9, '#8c879c', 700, 'letter-spacing="2.5"'),
        text(134, 101, 'HOLD', 11, '#f0eff5', 800, 'text-anchor="end" letter-spacing="1.2"'),
        text(24, 101, '[ C ]', 7, '#7f7b89', 600),
        '<path d="M24 108H135" stroke="#fff" stroke-opacity=".15" stroke-width=".6"/>',
    ]
    for label, y in [('SCORE', 170), ('LINES', 222), ('LEVEL', 265)]:
        b += [
            text(24, y, label, 9, '#9894a3', 800, 'letter-spacing="1.9"'),
            f'<path d="M24 {y+34}H133" stroke="#fff" stroke-opacity=".08" stroke-width=".6"/>',
        ]
    b += [
        text(24, 311, 'A / D', 7.5, '#e2dfe9', 800), text(71, 311, 'MOVE', 7, '#918b9d', 600),
        text(24, 323, 'W / Z', 7.5, '#e2dfe9', 800), text(71, 323, 'ROTATE', 7, '#918b9d', 600),
        text(24, 335, 'S / SPACE', 7.1, '#e2dfe9', 800), text(81, 335, 'DROP', 7, '#918b9d', 600),
        text(348, 35, 'NEXT', 12, '#f1eff6', 900, 'letter-spacing="1.8"'),
        '<path d="M347 43H452" stroke="#fff" stroke-opacity=".15" stroke-width=".6"/>',
        # A subtle bracket, rather than six separate rounded cards.
        '<path d="M349 52H345V285H349" stroke="#fff" stroke-opacity=".10" stroke-width=".7" fill="none"/>',
        text(348, 310, 'ENDLESS', 10, '#d4cede', 800, 'letter-spacing="1.7"'),
        text(348, 324, '7-BAG RANDOMIZER', 6.8, '#77717f', 600, 'letter-spacing=".5"'),
        text(348, 337, 'R  RESTART', 7.2, '#aaa4b6', 700, 'letter-spacing=".8"'),
    ]
    return svg(''.join(b))


def digit(d):
    """16x26 cells: condensed white numerals sit on the fixed HUD positions."""
    return svg(text(0, 21, str(d), 24, '#f5f3fa', 800, 'textLength="14" lengthAdjust="spacingAndGlyphs"'), 16, 26)


def gameover():
    return svg(
        rect(0, 0, 160, 320, '#09070f', extra='fill-opacity=".9"')
        + '<path d="M0 106H160 M0 213H160" stroke="#b693ef" stroke-opacity=".55" stroke-width=".7"/>'
        + rect(0, 107, 160, 105, '#19131f', extra='fill-opacity=".94"')
        + text(80, 128, 'STACK / FLOW', 7, '#a198b6', 800, 'text-anchor="middle" letter-spacing="2"')
        + text(80, 151, 'GAME', 23, '#f9f6ff', 900, 'text-anchor="middle" letter-spacing="1"')
        + text(80, 175, 'OVER', 23, '#f9f6ff', 900, 'text-anchor="middle" letter-spacing="1"')
        + text(80, 198, '[ R ]  PLAY AGAIN', 8, '#cdb6ed', 800, 'text-anchor="middle" letter-spacing=".6"'),
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
