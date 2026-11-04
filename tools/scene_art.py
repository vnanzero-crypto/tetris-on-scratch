"""Original roaming familiar art, cosmetic bee buffs, and animated clear trails.

These locally drawn fan designs use no extracted or downloaded game artwork.
Familiar and buff kinds are one-based; animation frames start at zero.
"""
from math import sin
from visuals import svg, rect, text

FAMILIAR_NAMES = [
    'Brother Bobby', 'Sister Maggy', 'Little Steven', 'Little Brimstone',
    'Demon Baby', 'Ghost Baby', 'Rotten Baby', 'Seraphim',
    'Guardian Angel', 'Incubus',
]
BUFF_NAMES = [
    'Bomb Honey', 'Flower Honey', 'Bubble Pollen', 'Blue Haste',
    'Red Boost', 'Blue Boost', 'White Boost', 'Focus',
    'Melody', 'Inspire', 'Rage', 'Baby Love',
]
BUFF_COLORS = [
    '#ffb35d', '#ffe384', '#87e2f0', '#a7cfff',
    '#ff8794', '#7ebcff', '#f3f5dc', '#b5e8b4',
    '#ddacff', '#fff2a1', '#ff785d', '#ffa9cf',
]


def _path(d, fill='none', stroke='none', width=1, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def _circle(x, y, r, fill, stroke='none', width=1, extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def _ellipse(x, y, rx, ry, fill, stroke='none', width=1, extra=''):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def _index(kind, choices):
    if isinstance(kind, str):
        for i, name in enumerate(choices):
            if kind.lower().replace(' ', '') == name.lower().replace(' ', ''):
                return i + 1
        return 1
    return max(1, min(len(choices), int(kind)))


def familiar(kind=1, frame=0):
    """48×40 familiar, centered at (24,20), with four flutter frames."""
    kind = _index(kind, FAMILIAR_NAMES)
    f = int(frame) % 4
    flap = [0, -2, 0, 2][f]
    palettes = [
        ('#8aaee7', '#c3dbff', '#344f86'),
        ('#e985a4', '#ffc1d0', '#9e456b'),
        ('#343643', '#737489', '#121622'),
        ('#8b384a', '#d76a70', '#391d32'),
        ('#554a75', '#9382b5', '#211d3c'),
        ('#bddce5', '#effaff', '#6f9caf'),
        ('#89a979', '#c6d6a2', '#415541'),
        ('#e0cc99', '#fff5ce', '#8e7457'),
        ('#9bb8c9', '#dff3ff', '#496778'),
        ('#68588e', '#ad91cd', '#2b224c'),
    ]
    base, light, shade = palettes[kind-1]
    b = _ellipse(24, 36.5, 11, 1.2, '#070a16', extra='opacity=".14"')
    b += f'<g transform="translate(0 {[0, -.35, .1, .35][f]})">'
    # Tiny bat or feather wings keep each familiar readable at the sideband scale.
    if kind in (4, 5, 10):
        b += _path(f'M16 22Q7 {12+flap} 3 {15+flap}L7 {23+flap}L11 22L14 27Z', shade, light, .7)
        b += _path(f'M32 22Q41 {12-flap} 45 {15-flap}L41 {23-flap}L37 22L34 27Z', shade, light, .7)
    elif kind in (8, 9):
        b += _path(f'M17 24Q6 {10+flap} 2 {15+flap}Q4 {23+flap} 15 29L18 27Z', '#e5eff8', '#93b0c4', .65)
        b += _path(f'M31 24Q42 {10-flap} 46 {15-flap}Q44 {23-flap} 33 29L30 27Z', '#e5eff8', '#93b0c4', .65)
        for side in (-1, 1):
            b += _path(f'M{24+side*17} {19+side*flap}L{24+side*11} 26M{24+side*19} {17+side*flap}L{24+side*12} 23', stroke='#b4cad9', width=.6)
    if kind == 6:
        b += _path('M17 22Q12 27 13 34L18 32L21 36L25 33L30 36L35 33Q34 25 31 22Z', base, shade, .8, 'fill-opacity=".88"')
    else:
        b += _ellipse(24, 28, 7.5, 7.5, base, shade, .9)
        b += _path('M19 33L18 36M29 33L30 36', stroke=shade, width=2)
        b += _path('M17 25L14 29M31 25L34 29', stroke=shade, width=2)
    b += _ellipse(24, 17, 11, 10.5, base, shade, 1)
    b += _path('M16 14Q18 8 25 9', stroke=light, width=1.4, extra='opacity=".6"')
    # The ten companions retain distinct recognizable motifs.
    if kind == 1:  # Blue baby and twin tear marks.
        b += _ellipse(19.5, 17, 1.6, 2.3, '#0c172a') + _ellipse(28.5, 17, 1.6, 2.3, '#0c172a')
        b += _path('M18 20L19 25L21 21M27 21L29 25L30 20', '#8fe3ff')
        b += _path('M22 23Q24 21 26 23', stroke=shade, width=.9)
    elif kind == 2:  # Pink baby, little bow and red tears.
        b += _path('M22 9L15 6L15 12L22 10M24 9L31 6L31 12L24 10', '#d93f75', '#783352', .5)
        b += _circle(23, 9, 1.8, '#ffd2df')
        b += _circle(19.5, 17, 1.8, '#3a2136') + _circle(28.5, 17, 1.8, '#3a2136')
        b += _path('M18.5 19L19 24M28.5 19L29 24', stroke='#c34064', width=1.4)
        b += _path('M22 23H26', stroke=shade, width=1)
    elif kind == 3:  # Little shadow companion with bright smiling face.
        b += _ellipse(19.5, 16.5, 2.2, 2.8, '#f7f0d0') + _ellipse(28.5, 16.5, 2.2, 2.8, '#f7f0d0')
        b += _circle(20, 16, .8, '#191b29') + _circle(28, 16, .8, '#191b29')
        b += _path('M18 23Q24 28 30 23L28 26H21Z', '#f5edcf')
    elif kind == 4:  # Small horned brimstone demon, glowing red mouth.
        b += _path('M16 11L12 3L20 8M28 8L36 3L32 12', shade, '#ca6d76', .7)
        b += _path('M17 16L21 18M27 18L31 16', stroke='#ffe49f', width=2)
        b += _ellipse(24, 23, 4.2, 3.4, '#2c101c', '#ff4b4f', .8)
        b += _ellipse(24, 23, 1.6, 2.1, '#ffe0b3')
    elif kind == 5:  # Purple demon, horn nubs and pinprick eyes.
        b += _path('M15 11L15 5L20 8M29 8L34 5L33 12', shade, light, .6)
        b += _circle(19, 17, 2, '#d75d67') + _circle(29, 17, 2, '#d75d67')
        b += _path('M20 24L22 22L24 24L26 22L28 24', stroke='#ded5e8', width=.8)
    elif kind == 6:  # Pale ghost's open mouth and trailing wisps.
        b += _ellipse(19, 16.5, 1.7, 2.6, '#37596d') + _ellipse(29, 16.5, 1.7, 2.6, '#37596d')
        b += _ellipse(24, 23, 2.5, 3, '#557788')
        b += _path(f'M7 {26+flap}Q3 24 5 21M40 {27-flap}Q45 24 43 21', stroke='#d0f1fc', width=1, extra='opacity=".6"')
    elif kind == 7:  # Green fly keeper with stitched eye.
        b += _path('M16 16L21 20M21 16L16 20', stroke='#263b2b', width=1.3)
        b += _ellipse(29, 17, 1.8, 2.1, '#233126')
        b += _path('M20 24Q24 21 28 24', stroke=shade, width=1)
        b += _circle(12, 9, 1.6, '#17222b') + _ellipse(10.7, 7.8, 1.8, 1, '#bccfd4', extra='opacity=".8"') + _ellipse(13.7, 7.8, 1.8, 1, '#bccfd4', extra='opacity=".8"')
    elif kind == 8:  # Gold angel, crown-like halo and closed gentle eyes.
        b += _ellipse(24, 4.6, 8, 2.5, 'none', '#ffe9a3', 1.3)
        b += _path('M17 17Q19 19 21 17M27 17Q29 19 31 17', stroke='#765840', width=1)
        b += _path('M22 23Q24 25 26 23', stroke=shade, width=.8)
        b += _path('M24 28V33M21.5 30H26.5', stroke='#fff5c8', width=1)
    elif kind == 9:  # Silver guardian's helmet, shield and halo.
        b += _ellipse(24, 4.8, 8, 2.3, 'none', '#d7f1ff', 1.2)
        b += _path('M14 15Q24 3 34 15L32 19H16Z', '#688da4', light, .7)
        b += _path('M18 17H21M27 17H30', stroke='#203a4a', width=1.5)
        b += _path('M27 25L35 24L38 28L35 34L31 37L27 33Z', '#6c95ab', '#dff5ff', .8)
        b += _path('M32 26V33M29 29H35', stroke='#cce8f4', width=.8)
    else:  # Incubus, asymmetrical sweep and dark tear trails.
        b += _path('M15 11L10 5L20 8M29 8L38 4L33 13', shade, light, .7)
        b += _path('M17 16L21 17M27 17L31 16', stroke='#f5b9dc', width=1.6)
        b += _path('M19 20L18 25M29 20L30 25', stroke='#24172f', width=1.7)
        b += _path('M22 24Q24 22 26 24', stroke='#d59ebd', width=.8)
    return svg(b + '</g>', 48, 40)


def brimstone_beam(frame=0):
    """160×28 horizontal laser, ten frames, centered at (80,14)."""
    f = max(0, min(9, int(frame)))
    fade = 1 - f / 11
    pulse = 1.4 + sin(f * 1.7) * .6
    b = '<defs><linearGradient id="brimstoneCore" x2="0" y2="1"><stop stop-color="#ff9380"/><stop offset=".5" stop-color="#fff1d7"/><stop offset="1" stop-color="#ff413c"/></linearGradient></defs>'
    b += f'<g opacity="{fade:.3f}">'
    b += rect(0, 2, 160, 24, '#1b060e', r=3, extra='opacity=".72"')
    b += _path('M0 14H160', stroke='#9a122e', width=18, extra='opacity=".5"')
    b += _path('M0 14H160', stroke='#ff243e', width=10 + pulse)
    b += _path('M0 14H160', stroke='#ff8b67', width=5.8 + pulse*.5)
    b += rect(0, 12, 160, 4, 'url(#brimstoneCore)')
    b += _path('M0 14H160', stroke='#fff5cf', width=1.6)
    for i in range(10):
        x = 8 + i*16
        dy = (i*7 + f*3) % 5
        b += _path(f'M{x-5} {8-dy}L{x-2} {3+dy*.4}L{x+1} {8-dy}M{x-2} {4+dy*.4}V10M{x+4} {20+dy}L{x+6} {24-dy*.4}L{x+8} {20+dy}', stroke='#ffb788', width=.7, extra='opacity=".8"')
        b += _path(f'M{x-7} 11L{x-3} {9-dy*.3}L{x+2} 11L{x+6} {10+dy*.3}', stroke='#320410', width=.7, extra='opacity=".6"')
    for i in range(14):
        x = (i*31 + f*11) % 160
        y = 2 + (i*7 + f*5) % 25
        b += _path(f'M{x-1.7} {y}H{x+1.7}M{x} {y-1.7}V{y+1.7}', stroke='#ffe1a4', width=.7)
        b += _circle((x+6)%160, 27-y, .6, '#ff4751')
    b += '</g>'
    return svg(b, 160, 28)


def brimstone_spark():
    """12×12 red-white impact spark, center (6,6)."""
    return svg(_path('M6 0L7.8 4.2L12 6L7.8 7.8L6 12L4.2 7.8L0 6L4.2 4.2Z', '#ff344b') + _path('M6 2L7 5L10 6L7 7L6 10L5 7L2 6L5 5Z', '#ffd5a7') + _path('M6 4V8M4 6H8', stroke='#fff9df', width=1), 12, 12)


def buff_icon(kind=1):
    """20×20 badge for one of twelve purely cosmetic Bee Swarm-style buffs."""
    kind = _index(kind, BUFF_NAMES)
    c = BUFF_COLORS[kind-1]
    b = rect(.5,.5,19,19,'#111d2b',c,4,extra='stroke-width=".7" fill-opacity=".94"')
    if kind == 1:
        b += _circle(10, 12, 5.5, '#3b4856', '#cad6dc', .65)
        b += rect(9, 5, 3, 2.5, '#9aa5ad', r=.5)
        b += _path('M11 5Q12 1 15 4M15 2V6M13 4H17', stroke='#ffd477', width=.9)
        b += _path('M8 12L10 10L11 13L13 12', stroke='#ffc15d', width=1)
    elif kind == 2:
        for x,y in [(10,5),(5.5,8),(7,13.5),(13,13.5),(14.5,8)]:b += _circle(x,y,2.7,'#fff0b9','#e9b94f',.45)
        b += _circle(10,9.5,3,'#e5a83f','#fff0a0',.5)
        b += _path('M10 13V18M10 16Q5 17 5 14M10 15Q15 15 15 12', stroke='#8bce87', width=1.1)
    elif kind == 3:
        b += _circle(9,10,5.6,'#328daa','#b3f7ff',.8,'fill-opacity=".25"')
        b += _circle(14.5,5.5,2.2,'#66cbdf','#c5ffff',.7,'fill-opacity=".3"')
        b += _path('M5.5 9Q6 6 8.5 6M7 16H13', stroke='#eaffff', width=1)
        b += _circle(13,13.5,.8,'#d8ffff')
    elif kind == 4:
        b += _path('M11 3L5 11H9L7 18L15 8H11L14 3Z','#a2ceff','#e4f5ff',.7)
        b += _path('M3 6H6M14 15H17M3 15H5',stroke='#6e9de0',width=.8)
    elif kind in (5, 6, 7):
        # Three pollen flowers carry distinct red, blue and ivory boost marks.
        dark = ['#8a3b50', '#365789', '#8e916c'][kind-5]
        for x,y in [(10,5.1),(5.3,8.6),(7.1,14.1),(12.9,14.1),(14.7,8.6)]:
            b += _ellipse(x,y,2.5,3,c,dark,.55)
        b += _circle(10,9.6,3.1,dark,c,.6)
        b += _path('M10 7.6V11.6M8 9.6H12',stroke='#fffceb',width=1)
        b += _path('M5 17H15M6 15.5L4 17L6 18.5M14 15.5L16 17L14 18.5',stroke=c,width=.65)
    elif kind == 8:
        b += _path('M3 10Q10 2 17 10Q10 18 3 10Z','#243f34',c,.8)
        b += _circle(10,10,3.7,'none','#efffda',.7)+_circle(10,10,1.6,c)
        b += _path('M10 2V4M10 16V18M2 10H4M16 10H18',stroke='#f3ffdc',width=.8)
    elif kind == 9:
        b += _path('M8 14V5L15 3V12M8 6L15 4',stroke=c,width=1.4)
        b += _ellipse(5.8,14.5,2.8,2,'#ca88ef','#f5d8ff',.55)
        b += _ellipse(12.8,12.5,2.8,2,'#ca88ef','#f5d8ff',.55)
        b += _path('M3 6L4 4L5 6L4 8Z','#f8eaff')
    elif kind == 10:
        b += _path('M10 2.6L12.2 7.3L17.4 8L13.6 11.6L14.5 16.8L10 14.3L5.5 16.8L6.4 11.6L2.6 8L7.8 7.3Z',c,'#fffbd8',.65)
        b += _path('M10 6L11 9L14 9.3L11.5 11L12 13.5L10 12.3L8 13.5L8.5 11L6 9.3L9 9Z','#dcad4c')
    elif kind == 11:
        b += _path('M10 2L12 7L16 5L14 11L17 14L12 17L8 17L3 14L6 11L4 5L8 7Z','#bd3f43',c,.75)
        b += _path('M5.5 9L8.5 10.3M11.5 10.3L14.5 9',stroke='#fff0bd',width=1.2)
        b += _path('M7 14L9 12.6L10 14L11 12.6L13 14',stroke='#ffe6ad',width=.9)
    else:
        b += _path('M10 16.5C7 14.5 3.1 11.4 3.1 7.7C3.1 3 8.2 2.8 10 6C11.8 2.8 16.9 3 16.9 7.7C16.9 11.4 13 14.5 10 16.5Z','#e987b6','#ffe6ed',.7)
        b += _path('M6 7Q6 5.5 7.5 5.5',stroke='#fff2f2',width=1.1)
        b += _path('M7.5 10Q8.3 10.8 9.1 10M10.9 10Q11.7 10.8 12.5 10M9 12Q10 13 11 12',stroke='#873e68',width=.65)
    return svg(b, 20, 20)


def buff_label(kind=1):
    """60×12 slim buff label, centered at (30,6)."""
    kind = _index(kind, BUFF_NAMES)
    return svg(text(0, 8.7, BUFF_NAMES[kind-1].upper(), 5.6, '#d8e8f2', 300), 60, 12)


def buff_wisp(kind=1, frame=0):
    """24×24 transparent buff mote, four looping frames, center at (12,12).

    The engine can layer several types at once in the outer stage corridors.
    Each animation retains its own recognizable pollen, music, star or heart
    motif instead of tinting one generic spark for every active effect.
    """
    kind = _index(kind, BUFF_NAMES)
    f = int(frame) % 4
    c = BUFF_COLORS[kind-1]
    pulse = [1, 1.12, 1.04, .92][f]
    drift = [0, -.7, 0, .7][f]
    b = f'<g transform="translate(12 {12+drift}) scale({pulse}) translate(-12 -12)" opacity="{[.72,.9,.78,.62][f]}">'
    if kind == 1:
        r = 4.5 + f*.8
        b += _circle(12,12,r,'none',c,.65,'opacity=".65"')
        b += _path('M12 4L13.6 9.2L19 8L15.6 12L19 16L13.5 14.8L12 20L10.5 14.8L5 16L8.4 12L5 8L10.4 9.2Z',c,extra='opacity=".35"')
        b += _circle(12,12,2.5,'#ffead0')
        b += _path(f'M{3+f} 4L{5+f} 6M{21-f} 18L{19-f} 16',stroke=c,width=.8)
    elif kind == 2:
        b += f'<g transform="rotate({f*18} 12 12)">'
        for x,y in [(12,5),(5.4,9.8),(7.9,17.5),(16.1,17.5),(18.6,9.8)]:
            b += _ellipse(x,y,3.2,3.7,c,extra='opacity=".55"')
        b += _circle(12,12,3.6,'#fff6c0')+'</g>'
        b += _circle(3+f,3.5,1,c)+_circle(21-f,20.5,.8,'#ffeaae')
    elif kind == 3:
        b += _circle(10,12,5.6+f*.25,c,'#d0fcff',.6,'fill-opacity=".12"')
        b += _circle(18-f*.6,5+f*.6,2.2,'none','#b8ffff',.55)
        b += _path('M6.2 10Q7 7.4 10 7M13 16L14.5 14.5',stroke='#eaffff',width=.8)
        b += _circle(4+f*.4,20-f*.5,1,c,extra='opacity=".7"')
    elif kind == 4:
        b += _path('M13 3L6 13H11L9 21L18 10H13L16 3Z',c,'#d9f1ff',.5)
        b += _path(f'M{3+f*.3} 6H8M2 10H6M{3+f*.4} 17H7',stroke=c,width=.8,extra='opacity=".45"')
    elif kind in (5,6,7):
        # Distinct pollen boosts: rising ribbons and a bright flower center.
        turn = (f*19 + (kind-5)*30)
        b += f'<g transform="rotate({turn} 12 12)">'
        b += _path('M4 13Q4 4 12 4Q20 4 20 12M20 11L18 14L16 10M20 12Q20 20 12 20Q4 20 4 14M4 15L6 12L8 16',stroke=c,width=.9,extra='opacity=".65"')
        for x,y in [(12,8),(8.2,10.8),(9.6,15.3),(14.4,15.3),(15.8,10.8)]:
            b += _circle(x,y,2,c,extra='opacity=".45"')
        b += _circle(12,12,2.1,'#fffdf1')+'</g>'
        if kind==5:b += _path('M2 3L4 5M20 19L22 21',stroke='#ffc6b9',width=.8)
        elif kind==6:b += _circle(3,4+f*.2,1.2,'#d2eaff')+_circle(21,20-f*.2,.9,'#a7d8ff')
        else:b += _path('M3 3V7M1 5H5M21 17V21M19 19H23',stroke='#ffffdf',width=.75)
    elif kind == 8:
        r = 6 + f*.45
        b += _circle(12,12,r,'none',c,.6,'opacity=".55"')
        b += _path('M3 12Q12 4 21 12Q12 20 3 12Z','none',c,.75)
        b += _circle(12,12,2.6,'#efffe4',c,.5)
        b += _path('M12 1V5M12 19V23M1 12H5M19 12H23',stroke=c,width=.75,extra='opacity=".7"')
    elif kind == 9:
        b += _path('M10 16V6L18 4V14M10 8L18 6',stroke=c,width=1.2)
        b += _ellipse(7.8,16.5,2.9,2,c,'#f4d9ff',.45)
        b += _ellipse(15.8,14.5,2.9,2,c,'#f4d9ff',.45)
        b += _path(f'M{3+f*.25} 4Q1 7 3 10M{21-f*.25} 17Q23 14 21 11',stroke='#e8c7ff',width=.65,extra='opacity=".5"')
    elif kind == 10:
        b += f'<g transform="rotate({f*12} 12 12)">'
        b += _path('M12 3L14.6 9L21 9.6L16.1 13.8L17.5 20L12 16.7L6.5 20L7.9 13.8L3 9.6L9.4 9Z',c,'#fffad6',.6)
        b += _path('M12 7L13 11L17 11.2L14 13.3L14.7 16.8L12 15L9.3 16.8L10 13.3L7 11.2L11 11Z','#fffef3',extra='opacity=".7"')+'</g>'
        b += _circle(3,3,.8,c)+_circle(21,21,1,c)
    elif kind == 11:
        b += _path('M12 2L15 9L20 6L17 14L21 18L14 22L10 22L3 18L7 14L4 6L9 9Z',c,extra='opacity=".45"')
        b += _path('M6 10L10 12M14 12L18 10',stroke='#fff2bc',width=1.4)
        b += _path('M9 17L11 15L12 17L13 15L15 17',stroke='#fff0c1',width=.9)
        b += _path(f'M{2+f*.3} 2L4 6M{22-f*.3} 2L20 6',stroke='#ffb6a2',width=.9)
    else:
        b += _path('M12 21C8.8 18.4 4 14.7 4 10.1C4 4.9 9.7 4.5 12 8C14.3 4.5 20 4.9 20 10.1C20 14.7 15.2 18.4 12 21Z',c,'#ffe0ec',.6, 'fill-opacity=".55"')
        b += _path('M7 10Q7 7.8 9 7.8',stroke='#fff4f4',width=1)
        b += _path(f'M{3+f*.3} 3V7M{1+f*.3} 5H{5+f*.3}M20 1V5M18 3H22',stroke='#ffd8ed',width=.6)
    return svg(b+'</g>',24,24)


def hard_drop_dash(frame=0):
    """160×320 transparent full-board dash overlay, ten descending frames.

    Thin separated lines leave the board and active blocks readable.  Root logic
    can briefly flash this overlay on an actual Space/hard-drop key edge.
    """
    f = max(0, min(9, int(frame)))
    fade = 1 - f / 11
    b = []
    for lane in range(10):
        x = lane*16 + 8
        for i in range(4):
            y = (lane*31 + i*83 + f*19) % 306
            length = 5 + ((lane*7+i*3)%9)
            opacity = fade * (.25 + ((lane+i)%3)*.09)
            b += [_path(f'M{x} {y}V{min(319,y+length)}', stroke='#afefff', width=.65, extra=f'opacity="{opacity:.3f}"')]
            if (lane+i)%3 == 0:
                b += [_path(f'M{x-1.5} {min(318,y+length-1)}L{x} {min(319,y+length+1)}L{x+1.5} {min(318,y+length-1)}', stroke='#ddffff', width=.55, extra=f'opacity="{opacity*.8:.3f}"')]
    return svg(''.join(b), 160, 320)
