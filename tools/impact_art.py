"""Original drop-trajectory previews, landing flares, and Isaac-inspired tears.

All artwork is local SVG. Style and tear kinds are one-based; frames start at
zero. Actual drop trajectories are drawn by native Scratch pen blocks.
"""
from math import cos, sin, pi
from visuals import svg, rect

DROP_NAMES = ['White Line', 'Neon Pulse', 'Rainbow Beam', 'Flame Trail', 'Frost Stream', 'Void Rift']
TEAR_NAMES = ['Blue', 'Blood', 'Spectral', 'Golden']
SPECTRUM = ['#ff738f', '#ffb76a', '#fff088', '#90efad', '#7bdfff', '#b19bff']
TEAR_COLORS = [('#73c8f3', '#c7f3ff', '#326eaa'), ('#d85a75', '#ffc1b7', '#853b58'),
               ('#a79ce8', '#e7deff', '#6354a4'), ('#eec76e', '#fff2bb', '#ac7a38')]


def _path(d, fill='none', stroke='none', width=1, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def _ellipse(x, y, rx, ry, fill='none', stroke='none', width=1, extra=''):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def _circle(x, y, radius, fill='none', stroke='none', width=1, extra=''):
    return _ellipse(x, y, radius, radius, fill, stroke, width, extra)


def _kind(value, count):
    return max(1, min(count, int(value)))


def _star(x, y, radius, color, opacity=1):
    return _path(f'M{x} {y-radius}L{x+.65} {y-.65}L{x+radius} {y}L{x+.65} {y+.65}L{x} {y+radius}L{x-.65} {y+.65}L{x-radius} {y}L{x-.65} {y-.65}Z', color,
                 extra=f'opacity="{opacity:.3f}"')


def drop_preview(style=1):
    """60×48 preview with a trail spanning the miniature's occupied width."""
    style = _kind(style, 6)
    colors = ['#effaff', '#78e5ff', '#b6bdff', '#ffc16b', '#b6eaff', '#bc9aff']
    color = colors[style-1]
    b = _ellipse(30, 41, 12, 2, '#8db6cf', extra='opacity=".1"')
    if style == 3:
        for i, c in enumerate(SPECTRUM):
            b += rect(22+i*16/6,14,16/6,25,c,extra='fill-opacity=".5"')
    else:
        b += rect(22,14,16,25,color,extra='fill-opacity=".16"')
        b += _path('M30 14V39', stroke=color, width=5 if style in (4,6) else 3.5, extra='opacity=".16"')
        b += _path('M30 14V39', stroke=color, width=1.6 if style in (4,6) else 1.1, extra='opacity=".95"')
        b += _path('M30 15V39', stroke='#fff', width=.45, extra='opacity=".9"')
    if style == 2:
        b += _path('M26.5 18V24M33.5 27V33', stroke='#bd9bff', width=.7)
        b += _ellipse(30, 34, 6, 2, stroke='#87e8ff', width=.65, extra='opacity=".8"')
    elif style == 4:
        b += _path('M24 39Q24 34 27 31Q25 36 29 35L31 29Q35 34 36 39Z', '#ff8b51', extra='opacity=".6"')
        b += _path('M28 39Q27 35 30 34Q33 36 32 39Z', '#ffe9a7')
    elif style == 5:
        for x,y in [(25,22),(35,30),(24,36)]:
            b += _path(f'M{x} {y-2}V{y+2}M{x-1.7} {y}H{x+1.7}', stroke='#bcefff', width=.65)
        b += _path('M27 16V27M33 24V35', stroke='#91cbf4', width=.6, extra='opacity=".6"')
    elif style == 6:
        b += _ellipse(30, 38, 8, 3, '#0d1021', '#b39cff', .7)
        b += _path('M23 36Q30 32 37 36M26 27L28 25M33 20L35 18', stroke='#b896e9', width=.65)
    else:
        b += _ellipse(30, 39, 7, 2, stroke=color, width=.7, extra='opacity=".8"')
    # The solid miniature starts above the line; the outline is its landing spot.
    for x,y in [(22,3),(27.5,3),(33,3),(27.5,8.5)]:
        b += rect(x, y, 5, 5, color, '#f4fbff', .6, extra='stroke-width=".35" fill-opacity=".84"')
        b += rect(x, y+29, 5, 5, 'none', color, .6, extra='stroke-width=".5" stroke-opacity=".6"')
    return svg(b, 60, 48)


def drop_tip(style=1, frame=0):
    """24×24, centered at (12,12), six fading landing-flare frames."""
    style = _kind(style, 6)
    f = max(0, min(5, int(frame)))
    fade = 1-f/6.5
    radius = 3+f*1.35
    b = ''
    if style == 1:
        b += _ellipse(12, 13, radius+1, 1.2+f*.25, stroke='#effbff', width=.75, extra=f'opacity="{fade:.3f}"')
        b += _star(12, 11, 4+f*.55, '#ffffff', fade*.85)
    elif style == 2:
        b += _circle(12, 12, radius, stroke='#79e9ff', width=.85, extra=f'opacity="{fade:.3f}"')
        b += _ellipse(12, 13, radius+1, radius*.34, stroke='#bc9bff', width=.7, extra=f'opacity="{fade:.3f}"')
        b += _circle(12, 12, 1.4, '#efffff', extra=f'opacity="{fade:.3f}"')
    elif style == 3:
        for i,c in enumerate(SPECTRUM):
            a = i*pi/3+f*.12
            x,y = 12+cos(a)*radius,12+sin(a)*radius
            b += _path(f'M{12+cos(a)*(radius-2):.3f} {12+sin(a)*(radius-2):.3f}L{x:.3f} {y:.3f}', stroke=c, width=1.3, extra=f'opacity="{fade:.3f}"')
        b += _star(12, 12, 3, '#fff5ef', fade)
    elif style == 4:
        lift = f*.65
        b += _path(f'M5 17Q4 {10-lift} 9 {6-lift}Q7 12 11 11L14 {3+lift}Q14 10 19 13Q21 18 16 20H9Q5 20 5 17Z', '#ff794c', extra=f'opacity="{fade*.8:.3f}"')
        b += _path('M9 17Q8 13 12 11Q12 15 15 15Q18 19 13 20Q9 21 9 17Z', '#ffe5a0', extra=f'opacity="{fade:.3f}"')
        b += _ellipse(12, 20, 7, 1, stroke='#ffb46b', width=.7, extra=f'opacity="{fade:.3f}"')
    elif style == 5:
        for i in range(6):
            a = i*pi/3
            x,y = 12+cos(a)*radius,12+sin(a)*radius
            b += _path(f'M12 12L{x:.3f} {y:.3f}', stroke='#c5f6ff', width=.8, extra=f'opacity="{fade:.3f}"')
        b += _path(f'M12 {12-radius}L{12+radius*.55} 12L12 {12+radius}L{12-radius*.55} 12Z', stroke='#90d1ef', width=.6, extra=f'opacity="{fade:.3f}"')
        b += _star(12, 12, 2.5, '#fff', fade)
    else:
        b += _ellipse(12, 12, radius+1, radius*.6, '#0c1020', '#ac91e9', .8, f'fill-opacity="{fade*.6:.3f}" stroke-opacity="{fade:.3f}"')
        b += _path(f'M{12-radius} 9Q12 {5-f*.2} {12+radius} 9M{12-radius} 15Q12 {19+f*.2} {12+radius} 15', stroke='#d2b9ff', width=.7, extra=f'opacity="{fade:.3f}"')
        b += _path('M11 6L13 10L11 14L13 18', stroke='#f2e6ff', width=.85, extra=f'opacity="{fade:.3f}"')
    return svg(b, 24, 24)


def drop_band(style=1, cells=1):
    """One seamless 16-pixel-high ribbon tile with flat, exact piece edges."""
    style = _kind(style, 6)
    w = _kind(cells, 4) * 16
    if style == 3:
        b = ''.join(rect(i*w/6,0,w/6,16,c,extra='fill-opacity=".5"')
                    for i,c in enumerate(SPECTRUM))
    else:
        c = ['#ffffff','#8ceaff','#ffffff','#ff5a2d','#90e4ff','#5e3678'][style-1]
        b = rect(0,0,w,16,c,extra='fill-opacity=".14"')
        if style == 2:
            b += rect(w*.2,0,w*.6,16,'#92dcff',extra='fill-opacity=".08"')
        elif style == 4:
            b += rect(w*.175,0,w*.65,16,'#ffb24e',extra='fill-opacity=".25"')
        elif style == 5:
            for x in [w*.05,w*.91]:
                b += rect(x,0,w*.04,16,'#bcf5ff',extra='fill-opacity=".45"')
        elif style == 6:
            b += rect(w*.225,0,w*.55,16,'#c6a1f1',extra='fill-opacity=".18"')
    return svg(b,w,16)


def tear(kind=1, frame=0):
    """12×16 animated blue, blood, spectral, or golden tear; center (6,8)."""
    kind = _kind(kind, 4)
    f = max(0, min(3, int(frame)))
    color, light, dark = TEAR_COLORS[kind-1]
    squash = [1, .97, .94, .98][f]
    b = f'<g transform="translate(6 8) scale({1+(1-squash)*.6:.3f} {squash}) translate(-6 -8)">'
    b += _path('M6 1C5 4 1.2 7 1.2 10.2C1.2 16 10.8 16 10.8 10.2C10.8 7 7 4 6 1Z', color, dark, .55, 'fill-opacity=".92"')
    b += _path('M5 6Q2.8 9 3.5 11.3', stroke=light, width=1.1, extra='opacity=".9"')
    b += _ellipse(7.2, 12.2, 1.8, .8, light, extra='opacity=".3"')
    if kind == 2:
        b += _path('M7 8Q9 10 8.2 12', stroke='#f39b9a', width=.6, extra='opacity=".7"')
    elif kind == 3:
        b += _path('M2 11Q6 7.5 10 11M3 13Q6 10 9 13', stroke='#f1eaff', width=.45, extra='opacity=".7"')
    elif kind == 4:
        b += _star(7.2, 9, 1.8, '#fff8d4', .95)
    b += '</g>'
    return svg(b, 12, 16)


def tear_splash(kind=1, frame=0):
    """32×16, centered at (16,8), six tear-impact crown/ripple frames."""
    kind = _kind(kind, 4)
    f = max(0, min(5, int(frame)))
    color, light, dark = TEAR_COLORS[kind-1]
    fade = 1-f/6.1
    spread = 4+f*1.65
    b = _ellipse(16, 11.5, spread+2, 1.1+f*.35, color, color, .6,
                 f'fill-opacity="{fade*.12:.3f}" stroke-opacity="{fade*.8:.3f}"')
    b += _ellipse(16, 11.5, spread*.6, .7+f*.2, stroke=light, width=.6, extra=f'opacity="{fade*.7:.3f}"')
    crown_y = 7.5+f*.45
    b += _path(f'M{16-spread} 11L{16-spread*.65} {crown_y:.3f}L{16-spread*.25} 9L16 {4+f*.65:.3f}L{16+spread*.25} 9L{16+spread*.65} {crown_y:.3f}L{16+spread} 11Z', color,
               extra=f'opacity="{fade*.75:.3f}"')
    for i,side in enumerate((-1,1)):
        x = 16+side*(spread+1.5)
        y = 5.6+f*.65+i*.6
        b += _ellipse(x, y, .8, 1.1-f*.08, light, extra=f'opacity="{fade:.3f}"')
        b += _ellipse(16+side*spread*.62, 3.4+f*.45, .6, .9, color, extra=f'opacity="{fade*.7:.3f}"')
    return svg(b, 32, 16)
