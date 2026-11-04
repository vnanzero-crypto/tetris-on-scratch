"""Original SVG art for the Vnanzero edition expansion.

All artwork is drawn locally.  Bee designs are original blocky fan art inspired
by the named Bee Swarm Simulator bees, rather than copied game assets.
"""
from html import escape
import math

from visuals import rect, svg, text


BEE_NAMES = [
    'Basic', 'Bomb', 'Cool', 'Rascal', 'Bubble', 'Rage', 'Commander',
    'Music', 'Diamond', 'Tabby',
]
TOKEN_NAMES = ['Honey', 'Pollen', 'Bomb', 'Bubble']


def _named(value, choices, default=0):
    """Accept a one-based costume number or a case-insensitive display name."""
    if isinstance(value, (int, float)):
        return choices[(int(value) - 1) % len(choices)]
    name = str(value).lower().replace(' bee', '').replace('_', '').replace(' ', '')
    if name in ('bomber', 'bombbee'):
        name = 'bomb'
    for choice in choices:
        if name == choice.lower().replace(' ', ''):
            return choice
    return choices[default]


def _path(d, fill='none', stroke='none', width=1, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def _circle(x, y, radius, fill, stroke='none', width=1, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def bee(kind='Basic', frame=0):
    """48 x 36 bee costume, with a stable rotation center at (24, 18)."""
    kind = _named(kind, BEE_NAMES)
    frame = int(frame)
    flap = (frame % 4) in (1, 2)
    palettes = {
        'Basic': ('#f8d047', '#ffe68b', '#ca8c25'),
        'Bomb': ('#3d4754', '#6b7785', '#202a36'),
        'Cool': ('#a3dcf4', '#dcf7ff', '#5593bb'),
        'Rascal': ('#e66454', '#ff9982', '#993b3c'),
        'Bubble': ('#6edcdd', '#bcffff', '#3c9fbd'),
        'Rage': ('#e75252', '#ff8a6e', '#a52d40'),
        'Commander': ('#93ac70', '#c1d49a', '#5b714c'),
        'Music': ('#b49ae7', '#e2ceff', '#7755b1'),
        'Diamond': ('#a4e7fa', '#e3fbff', '#579abd'),
        'Tabby': ('#e4a15a', '#ffd39a', '#b46d36'),
    }
    base, light, shade = palettes[kind]
    b = '<ellipse cx="24" cy="31" rx="13" ry="2.3" fill="#070d1c" opacity=".16"/>'
    if flap:
        b += _path('M14 15C4 17 3 8 9 7C14 7 17 10 18 14Z', '#e4faff', '#7caabb', .7, 'fill-opacity=".88"')
        b += _path('M32 14C33 7 38 4 42 7C47 12 41 17 34 17Z', '#e4faff', '#7caabb', .7, 'fill-opacity=".88"')
        b += _path('M7 8L4 5M42 6L45 3', stroke='#caf5ff', width=.7, extra='opacity=".6"')
    else:
        b += _path('M15 16C5 13 2 18 6 22C10 26 16 22 18 18Z', '#d9f5ff', '#7caabb', .7, 'fill-opacity=".78"')
        b += _path('M32 17C39 12 46 15 43 21C40 26 34 22 31 19Z', '#d9f5ff', '#7caabb', .7, 'fill-opacity=".78"')
    # A cube silhouette, black legs and a tiny stinger establish the bee shape.
    b += _path('M17 27L15 30M24 28L24 31M32 27L34 30', stroke='#25303f', width=1.3)
    b += _path('M34 23L39 24L35 26Z', '#25303f')
    b += _path('M12 12L17 8H35L37 12V27L32 30H12Z', shade, '#263040', .8)
    b += _path('M12 12L17 8H35L31 12Z', light)
    b += _path('M31 12L35 8L37 12V27L31 30Z', shade)
    b += rect(12, 12, 19, 18, base)
    b += rect(12, 12, 19, 2, light, extra='opacity=".44"')
    b += _path('M14 10L13 6L10 5M29 10L30 5L33 4', stroke='#263040', width=1.25)
    b += _circle(10, 5, 1, '#263040') + _circle(33, 4, 1, '#263040')
    b += _path('M33 13V18M33 22V28M35 12V17M35 21V26', stroke='#273240', width=1.7, extra='opacity=".85"')
    if kind == 'Basic':
        b += _circle(17, 20, 1.55, '#263040') + _circle(26, 20, 1.55, '#263040')
        b += _path('M19 25Q22 27 25 24', stroke='#6a4b20', width=1)
        b += _circle(14.5, 23, 1.1, '#ed9d52', extra='opacity=".6"')
    elif kind == 'Bomb':
        b += rect(14.5, 16, 14.5, 10, '#e6edf1', r=1)
        b += rect(17, 19, 2, 3, '#27313c') + rect(25, 19, 2, 3, '#27313c')
        b += _path('M20 25H25', stroke='#27313c', width=1)
        b += _circle(24, 9.2, 3.2, '#202c3a')
        b += _path('M25 6L26 3L29 3', stroke='#eab352', width=1.2)
        b += _path('M30 1V4M28.5 2.5H31.5', stroke='#ffeaa6', width=.8)
    elif kind == 'Cool':
        b += _path('M13 17H30M14 18L15 23H20L22 19L24 23H29L30 18Z', '#1b3048')
        b += _path('M15 18L18 18M25 18L28 18', stroke='#94e8ff', width=.8)
        b += _path('M20 26L25 25', stroke='#366e8d', width=1)
    elif kind == 'Rascal':
        b += _path('M13 17L18 16L22 18L26 16L31 17L29 23L24 23L22 21L20 23H14Z', '#563944')
        b += _circle(17, 20, 1.1, '#ffe6a9') + _circle(27, 20, 1.1, '#ffe6a9')
        b += _path('M19 26Q23 23 26 25', stroke='#643640', width=1)
        b += _path('M14 10L17 6L20 10M25 10L28 6L31 10', '#d95045')
    elif kind == 'Bubble':
        b += _circle(17, 20, 1.4, '#235e7b') + _circle(26, 20, 1.4, '#235e7b')
        b += _path('M19 25Q22 27 25 25', stroke='#287e95', width=1)
        b += _circle(28, 12, 4.2, '#b8f7ff', '#f0ffff', .7, 'fill-opacity=".5"')
        b += _circle(29, 10.5, 1, '#f5ffff')
        b += _circle(8, 11 if flap else 17, 2.2, '#b8f7ff', '#f0ffff', .6, 'fill-opacity=".4"')
    elif kind == 'Rage':
        b += _path('M13 10L16 5L20 8L24 4L27 8L31 6L33 10Z', '#b72b3e')
        b += _path('M14 17L20 19M25 19L30 16', stroke='#622437', width=2)
        b += rect(16, 20, 3, 2, '#fff1d2') + rect(26, 20, 3, 2, '#fff1d2')
        b += _path('M19 27L22 24L26 27', stroke='#6f2935', width=1.2)
    elif kind == 'Commander':
        b += _path('M11 13L14 7H30L33 13Z', '#657a51', '#344539', .6)
        b += rect(12, 12, 21, 3, '#405847')
        b += _path('M22 8L23 10L25 10L23.5 11.5L24 13L22 12L20 13L20.5 11.5L19 10H21Z', '#f1db8d')
        b += rect(14, 18, 16, 5, '#2a3e40', r=.6)
        b += _path('M16 19H28', stroke='#afd0a5', width=.7)
        b += _path('M20 26H25', stroke='#425c40', width=1)
    elif kind == 'Music':
        b += _path('M12 17V24M31 17V24M12 17Q21 5 31 17', stroke='#66508d', width=2.4)
        b += rect(11, 18, 3.5, 7, '#493e6d', r=1) + rect(29, 18, 3.5, 7, '#493e6d', r=1)
        b += _circle(18, 20, 1.3, '#453658') + _circle(26, 20, 1.3, '#453658')
        b += _path('M20 25Q23 27 25 25', stroke='#65507e', width=1)
        b += _path('M35 4V10M35 4L40 3V9', stroke='#d9bdff', width=1.2)
        b += _circle(33.7, 10.5, 1.6, '#d9bdff') + _circle(38.7, 9.5, 1.6, '#d9bdff')
    elif kind == 'Diamond':
        b += _path('M18 8L21 3H27L30 8L24 13Z', '#e3fbff', '#78bdd6', .6)
        b += _path('M18 8H30M21 3L24 13L27 3', stroke='#75bdd7', width=.6)
        b += _path('M12 19L18 14L22 21L31 14L25 28L18 26Z', '#d8f8ff', extra='opacity=".32"')
        b += _circle(17, 20, 1.3, '#326b91') + _circle(27, 20, 1.3, '#326b91')
        b += _path('M20 25H25', stroke='#4a84a3', width=1)
        b += _path('M39 8V13M36.5 10.5H41.5', stroke='#e7fbff', width=1)
    else:  # Tabby: cat ears, forehead stripes, whiskers, and a curled tail.
        b += _path('M13 13L13 5L20 10M24 10L31 5V14', base, '#9c6037', .7)
        b += _path('M14.5 11V8L17.5 10M26.5 10L29.5 8V11', '#e7aa9c', width=.6)
        b += _path('M19 13L20 17M23 13V16M27 13L26 17', stroke='#9f6338', width=1.6)
        b += _path('M15 20L18 21L20 20M24 20L26 21L29 20', stroke='#5a4c39', width=1.1)
        b += _path('M21 23L23 23L22 24Z', '#ac685e')
        b += _path('M22 24L20 26M22 24L24 26M18 24L11 23M18 26L11 27M26 24L32 23M26 26L32 27', stroke='#805b3c', width=.7)
        b += _path('M36 26C45 27 46 18 41 18C38 18 40 22 42 21', stroke='#c78a4c', width=2.2)
    return svg(b, 48, 36)


def bee_token(kind='Honey', frame=0):
    """32 x 32 rotating token bursts for honey, pollen, bombs and bubbles."""
    kind = _named(kind, TOKEN_NAMES)
    frame = int(frame) % 6
    spin = (1, .82, .5, .72, 1, .86)[frame]
    b = ''
    colors = {'Honey': '#f7c856', 'Pollen': '#f6e99e', 'Bomb': '#a7b1c2', 'Bubble': '#85edff'}
    color = colors[kind]
    for i in range(5):
        angle = math.radians(i * 72 + frame * 9)
        x, y = 16 + math.cos(angle) * 13, 16 + math.sin(angle) * 13
        b += _circle(round(x, 2), round(y, 2), .7 if i % 2 else 1, color, extra='opacity=".7"')
    b += f'<g transform="translate(16 16) scale({spin} 1) translate(-16 -16)">'
    if kind == 'Bubble':
        b += _circle(16, 16, 10.8, '#83e4fa', '#c9fbff', 1.1, 'fill-opacity=".2"')
        b += _circle(16, 16, 8, 'none', '#8accf5', .6, 'stroke-opacity=".7"')
        b += _path('M9 14Q10 9 15 8', stroke='#f0ffff', width=2)
        b += _circle(21, 22, 1.5, '#d4fcff', extra='opacity=".8"')
    elif kind == 'Bomb':
        b += _circle(16, 17, 10, '#344054', '#8a9ab6', 1)
        b += _circle(13, 13, 3, '#64778f', extra='opacity=".55"')
        b += rect(14, 5, 5, 4, '#4f5e75', r=1)
        b += _path('M17 5L19 2L22 3', stroke='#f6ca62', width=1.4)
        b += _path('M24 1V6M21.5 3.5H26.5', stroke='#fff0af', width=1)
        b += _path('M12 19L15 22L21 14', stroke='#b8c5d7', width=1.3)
    else:
        b += _path('M16 4L26.4 10V22L16 28L5.6 22V10Z', '#e9a836' if kind == 'Honey' else '#e2c663', '#ffe8a0', 1)
        b += _path('M16 7L24 11.5V20.5L16 25L8 20.5V11.5Z', color, '#b47f25', .6)
        if kind == 'Honey':
            b += _path('M16 9C15 13 11 15 11 19C11 25 22 25 22 19C22 15 18 13 16 9Z', '#bd8122')
            b += _path('M14 18Q12 21 15 22', stroke='#ffe8a0', width=1.1)
        else:
            for i in range(5):
                a = math.radians(i * 72 - 90)
                b += _circle(round(16 + math.cos(a) * 4, 2), round(16 + math.sin(a) * 4, 2), 3, '#fff2b3', '#bf9b35', .5)
            b += _circle(16, 16, 2.7, '#bd8c28')
    b += '</g>'
    return svg(b, 32, 32)


def _hexagon(x, y, radius, fill='none', stroke='#6d6130', opacity=1):
    points = ' '.join(f'{x + radius * math.cos(math.radians(i * 60)):.2f},{y + radius * math.sin(math.radians(i * 60)):.2f}' for i in range(6))
    return f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width=".7" opacity="{opacity}"/>'


def beeswarm_landscape():
    """480 x 360 nocturnal flower field, kept subdued through the playfield."""
    b = '<defs><linearGradient id="beeNight" x2="0" y2="1"><stop stop-color="#091223"/><stop offset=".62" stop-color="#142b32"/><stop offset="1" stop-color="#203b30"/></linearGradient><radialGradient id="beeMoon"><stop stop-color="#fee5a1" stop-opacity=".2"/><stop offset="1" stop-color="#fee5a1" stop-opacity="0"/></radialGradient></defs>'
    b += rect(0, 0, 480, 360, 'url(#beeNight)')
    b += _circle(396, 64, 85, 'url(#beeMoon)') + _circle(396, 64, 18, '#f3de9e', extra='opacity=".68"')
    b += _path('M399 47C384 57 386 77 402 80C379 87 369 54 391 47Z', '#142a31')
    for i in range(34):
        x = (i * 97 + 17) % 480
        y = (i * 37 + 9) % 180
        b += _circle(x, y, .5 + (i % 3) * .15, '#d5e8c3', extra=f'opacity="{.25 + (i % 4) * .1}"')
    b += _path('M0 245Q50 209 94 235T184 239T291 231T387 224T480 231V360H0Z', '#1a3433')
    b += _path('M0 273Q69 235 127 266T254 265T377 251T480 268V360H0Z', '#203c32')
    # Hive and blue flower silhouettes anchor opposite edges, outside gameplay.
    b += _path('M20 210Q20 176 45 170Q70 177 70 210V250H20Z', '#584a2a', '#a48a45', .6)
    b += _path('M22 190H67M20 204H70M20 218H70M20 232H70', stroke='#86703c', width=1.2)
    b += _path('M36 250V236Q45 225 54 236V250Z', '#142329')
    b += _hexagon(46, 188, 7, '#aa8b3f', '#c0a45a', .65)
    b += _hexagon(38, 204, 6, 'none', '#aa8b3f', .6) + _hexagon(55, 217, 6, 'none', '#aa8b3f', .6)
    # Deterministic flower beds provide variety while the board area stays calm.
    flower_colors = ['#7f95bd', '#b3bba0', '#bd8878', '#af9b67', '#8a9c8b']
    for i in range(68):
        x = (i * 61 + 8) % 480
        if 150 < x < 330:
            continue
        y = 264 + (i * 29) % 91
        size = 2.3 + (i % 3) * .7
        color = flower_colors[i % len(flower_colors)]
        b += _path(f'M{x} {y + 9}L{x} {y}', stroke='#416644', width=.9)
        for petal in range(4):
            a = math.radians(petal * 90 + 45)
            b += _circle(round(x + math.cos(a) * size, 2), round(y + math.sin(a) * size, 2), size * .75, color, extra='opacity=".68"')
        b += _circle(x, y, size * .55, '#e8c470', extra='opacity=".8"')
    for i, (x, y) in enumerate([(88, 92), (438, 174), (111, 235), (392, 302), (31, 308)]):
        b += _hexagon(x, y, 5 + i % 2, '#d7b25b', '#ead18e', .24)
        b += _circle(x - 1, y - 1, 1, '#f6e1a0', extra='opacity=".38"')
    b += rect(155, 0, 170, 360, '#071222', extra='opacity=".2"')
    return svg(b)


def logo():
    """160 x 60 lockup with an original interlocking V tetromino icon."""
    b = '<defs><linearGradient id="vnLogo" x2="1" y2="1"><stop stop-color="#74f2ed"/><stop offset=".5" stop-color="#8ca6ff"/><stop offset="1" stop-color="#dca0ff"/></linearGradient></defs>'
    b += _path('M6 7H41L49 15V46L40 54H6L1 48V13Z', '#101a31', '#54638b', .9)
    b += _path('M7 14H17V24H27V34H37V14H47V34H37V44H27V54H17V44H7Z', 'url(#vnLogo)')
    for x, y in [(7, 14), (17, 24), (27, 34), (37, 14), (37, 24), (17, 44)]:
        b += rect(x + 1, y + 1, 8, 8, 'none', '#e3faff', extra='stroke-opacity=".36" stroke-width=".7"')
    b += text(57, 21, 'TETRIS', 17, '#e8efff', 350, 'letter-spacing="2.1"')
    b += text(58, 38, 'VNANZERO', 11, '#a7beee', 350, 'letter-spacing="1"')
    b += text(59, 51, 'EDITION', 8, '#93a0be', 300, 'letter-spacing="3"')
    return svg(b, 160, 60)


def _back_button():
    return (rect(16, 16, 84, 26, '#121d34', '#354466', r=4)
            + _path('M29 24L25 29L29 34M25 29H36', stroke='#adbedf', width=1.2)
            + text(46, 33, 'BACK', 10, '#c1cde4', extra='letter-spacing="1.2"'))


def _menu_background():
    b = '<defs><linearGradient id="expansionPanel" x2="1" y2="1"><stop stop-color="#0b1326"/><stop offset="1" stop-color="#151830"/></linearGradient></defs>'
    b += rect(0, 0, 480, 360, 'url(#expansionPanel)')
    b += _path('M0 74H480M0 316H480', stroke='#2b3551', width=.7)
    b += _path('M0 346L92 254M413 360L480 293', stroke='#2a3355', width=.7, extra='opacity=".55"')
    b += _circle(449, 79, 63, 'none', '#657296', .5, 'opacity=".12"')
    return b


def menu_cosmetics(tab='Clear'):
    """Cosmetics shell with 82 x 82 cards at (12+94c,100+100r).

    Labels, equipped markers and item previews are drawn by the Scratch UI.
    """
    tab = _named(tab, ['Clear', 'Blocks', 'Auras', 'Drops'])
    b = _menu_background() + _back_button()
    for index, label in enumerate(['Clear', 'Blocks', 'Auras', 'Drops']):
        x = 112 + index * 90
        selected = tab == label
        b += rect(x, 16, 86, 26, '#273755' if selected else '#121b31', '#8297ce' if selected else '#303c59', r=4)
        b += text(x + 43, 33, label.upper(), 9, '#e1eaff' if selected else '#9faeca', extra='text-anchor="middle" letter-spacing="1.2"')
        if selected:
            b += rect(x + 16, 40, 54, 2, '#a9bfff', r=1)
    b += text(16, 69, 'COSMETICS', 19, '#edf2ff', 300, 'letter-spacing="3.5"')
    b += text(468, 67, tab.upper(), 9, '#8192b9', extra='text-anchor="end" letter-spacing="2"')
    for index in range({'Clear':10, 'Blocks':9, 'Auras':8, 'Drops':6}[tab]):
        x, y = 12 + 94 * (index % 5), 100 + 100 * (index // 5)
        b += rect(x, y, 82, 82, '#111d33', '#354460', r=6)
        b += rect(x + 3, y + 3, 76, 53, '#17223a', r=4)
        b += _path(f'M{x + 9} {y + 60}H{x + 73}', stroke='#34405b', width=.6)
    b += rect(18, 316, 146, 28, '#21314c', '#657cb0', r=4)
    b += text(91, 334, 'RGB / RAINBOW', 10, '#c5d4ff', extra='text-anchor="middle" letter-spacing="1"')
    b += rect(310, 316, 152, 28, '#21314c', '#657cb0', r=4)
    b += text(386, 334, 'SAVE PROFILE', 10, '#c5d4ff', extra='text-anchor="middle" letter-spacing="1"')
    return svg(b)


def difficulty_panel():
    """Five difficulty buttons; hitboxes x32..448, y98+44i, height34."""
    b = _menu_background() + _back_button()
    b += text(240, 72, 'DIFFICULTY', 22, '#e4edff', 300, 'text-anchor="middle" letter-spacing="4"')
    colors = ['#9cdbc4', '#96bfff', '#d6a273', '#ce8cbd', '#f07889']
    names = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'NIGHTMARE']
    for i, (name, color) in enumerate(zip(names, colors)):
        y = 98 + 44 * i
        b += rect(32, y, 416, 34, '#111e34', '#34435f', r=5)
        b += rect(32, y + 7, 3, 20, color, r=1)
        for step in range(5):
            b += rect(52 + step * 7, y + 22 - step * 2.5, 4, 5 + step * 2.5, color if step <= i else '#2d3a53', r=.6)
        b += text(101, y + 22, name, 12, color, 300, 'letter-spacing="1.8"')
        b += text(405, y + 21, f'{[12, 10, 7, 5, 4][i]} SEC COMBO', 7.5, '#9baecb', 300, 'text-anchor="end" letter-spacing=".7"')
        b += _path(f'M{425} {y + 12}L{430} {y + 17}L{425} {y + 22}', stroke=color, width=1.2)
    return svg(b)
