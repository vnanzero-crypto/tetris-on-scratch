"""Original SVG clear effects, block finishes, and animated board auras."""
from visuals import svg, rect, block
from math import sin

RAINBOW = ['#ff587a', '#ffac48', '#fff369', '#7dffb5', '#5ae6ff', '#a58aff']


def elemental_beam(kind, frame):
    """Ten frames; rainbow is 160x32, all other clear rows are 160x16."""
    f = max(0, min(9, int(frame)))
    p = f / 9
    opacity = 1 - p * .85
    colors = ['#8be6ff', '#ff7b38', '#57d5ff', '#d5f6ff', '#f9a1ff',
              '#b4caff', '#ac6fff', '#ff84be', '#ffc84e', '#b693ff']
    c = colors[max(0, min(9, int(kind) - 1))]
    b = []
    if kind == 5:
        stops = ''.join(f'<stop offset="{i*20}%" stop-color="{color}"/>'
                        for i, color in enumerate(RAINBOW))
        b.append(f'<defs><linearGradient id="rainbow">{stops}</linearGradient></defs>')
        # Ten 16px cells fill the exact board width. Light extends vertically.
        b += [rect(0, 3, 160, 26, 'url(#rainbow)', extra=f'opacity="{opacity*.18:.3f}"'),
              rect(0, 8, 160, 16, 'url(#rainbow)', extra=f'opacity="{opacity:.3f}"'),
              rect(0, 14, 160, 4, '#fff', extra=f'opacity="{opacity*.85:.3f}"')]
        for i in range(10):
            x = i * 16
            color = RAINBOW[(i + f // 2) % 6]
            b.append(rect(x, 8, 16, 16, 'none', '#fff', extra=f'stroke-width=".65" opacity="{opacity*.6:.3f}"'))
            y = 3 + (i + f) % 3
            b.append(f'<path d="M{x+8} {y-3}L{x+10} {y}L{x+8} {y+3}L{x+6} {y}Z M{x+8} {29-y}L{x+10} {32-y}L{x+8} {35-y}L{x+6} {32-y}Z" fill="{color}" opacity="{opacity:.3f}"/>')
        return svg(''.join(b), 160, 32)
    b += [rect(0, 5, 160, 6, c, extra=f'fill-opacity="{.8*(1-p):.3f}"'),
          rect(0, 7, 160, 2, '#fff', extra=f'fill-opacity="{1-p:.3f}"')]
    for i in range(16):
        x = (i * 13 + f * 5) % 160
        if kind == 2:
            h = 4 + ((i * 7 + f * 3) % 10)
            b.append(f'<path d="M{x-5} 15Q{x+3} {12-h} {x} {2-h*.15}Q{x+9} 8 {x+6} 15Z" fill="{["#ff5637", "#ffab42", "#fff099"][i%3]}" opacity="{opacity:.3f}"/>')
        elif kind == 3:
            y = 8 + sin((i + f) * .9) * 4
            b.append(f'<path d="M{x-6} {y}Q{x} {y-7} {x+7} {y}" fill="none" stroke="#7ce9ff" stroke-width="1.4" opacity="{opacity:.3f}"/><circle cx="{x+3}" cy="{max(1,y-4)}" r="1.2" fill="#e1ffff"/>')
        elif kind == 4:
            h = 3 + (i * 7 + f) % 9
            b.append(f'<path d="M{x-5} 13L{x-1} {13-h}L{x+4} 2L{x+7} 13Z" fill="#b6e9ff" stroke="#f4ffff" stroke-width=".5" opacity="{opacity:.3f}"/>')
        elif kind == 6:
            y = 4 + (i * 3 + f) % 7
            path = f'M{x-7} {y}L{x-2} {y-3}L{x-3} {y+2}L{x+4} {y-1}L{x+2} {y+5}L{x+8} {y+1}'
            b.append(f'<path d="{path}" fill="none" stroke="#738aff" stroke-width="3" opacity="{opacity*.65:.3f}"/><path d="{path}" fill="none" stroke="#edffff" stroke-width="1" opacity="{opacity:.3f}"/>')
        elif kind == 7:
            r = 2 + (i + f) % 4
            b.append(f'<ellipse cx="{x}" cy="8" rx="{r+3}" ry="{r}" fill="#16092b" stroke="#b378ff" stroke-width=".8" opacity="{opacity:.3f}"/><path d="M{x-6} 5Q{x} 0 {x+6} 8Q{x} 16 {x-6} 11" fill="none" stroke="#dbbeff" stroke-width=".5" opacity="{opacity:.3f}"/>')
        elif kind == 8:
            y = 2 + (i * 7 + f * 3) % 12
            color = RAINBOW[i % 6]
            b.append(f'<g transform="rotate({i*37+f*19} {x} {y})" opacity="{opacity:.3f}"><rect x="{x-2}" y="{y-1}" width="4" height="2" fill="{color}"/><path d="M{x+3} {y-4}L{x+5} {y-1}L{x+3} {y+1}" fill="none" stroke="{color}" stroke-width="1"/></g>')
        elif kind == 9:
            y = 4 + (i % 2) * 7
            b.append(f'<path d="M{x-5} {y}L{x-2.5} {y-4}H{x+2.5}L{x+5} {y}L{x+2.5} {y+4}H{x-2.5}Z" fill="#ffb62b" stroke="#fff2a0" stroke-width=".8" opacity="{opacity:.3f}"/><path d="M{x-1} {y-2}H{x+2}" stroke="#fffbd2" stroke-width="1" opacity="{opacity:.3f}"/>')
        elif kind == 10:
            y = 2 + (i * 7 + f * 2) % 12
            b.append(f'<ellipse cx="{x}" cy="8" rx="9" ry="3" fill="{["#8667ff", "#e171d4", "#6fc8ff"][i%3]}" opacity="{opacity*.22:.3f}"/><path d="M{x-2} {y}H{x+2}M{x} {y-2}V{y+2}" stroke="#fff4ff" stroke-width=".7" opacity="{opacity:.3f}"/><circle cx="{x+5}" cy="{16-y}" r=".6" fill="#b9d9ff" opacity="{opacity:.3f}"/>')
        else:
            b.append(f'<path d="M{x} 2V14 M{x-3} 8H{x+3}" stroke="#c2eeff" opacity="{opacity*.6:.3f}" stroke-width=".6"/>')
    return svg(''.join(b), 160, 16)


def particle_skin(kind):
    if kind == 2:
        b = '<path d="M4 0Q2 4 1 5Q0 9 6 7Q9 4 5 2Q6 5 4 5Z" fill="#ff8241"/><path d="M4 4L6 7H2Z" fill="#fff5b7"/>'
    elif kind == 3:
        b = '<path d="M4 0Q10 7 4 8Q-2 7 4 0Z" fill="#65dfff"/><path d="M3 3L2 5" stroke="#fff" stroke-width="1"/>'
    elif kind == 4:
        b = '<path d="M4 0V8 M0 4H8 M1 1L7 7 M7 1L1 7" stroke="#d8fbff" stroke-width=".9"/>'
    elif kind == 5:
        stops = ''.join(f'<stop offset="{i*20}%" stop-color="{c}"/>' for i, c in enumerate(RAINBOW))
        b = f'<defs><linearGradient id="spectrum">{stops}</linearGradient></defs><path d="M6 0L8 4L12 6L8 8L6 12L4 8L0 6L4 4Z" fill="url(#spectrum)"/><path d="M6 3V9M3 6H9" stroke="#fff" stroke-width="1"/>'
        return svg(b, 12, 12)
    elif kind == 6:
        b = '<path d="M4 0L1 4H3L2 8L7 3H5L7 0Z" fill="#d3e5ff" stroke="#8396ff" stroke-width=".5"/>'
    elif kind == 7:
        b = '<circle cx="4" cy="4" r="2.7" fill="#170d2c" stroke="#c58aff" stroke-width="1"/><path d="M0 5Q3 0 8 3M0 5Q5 8 8 3" fill="none" stroke="#e5caff" stroke-width=".6"/>'
    elif kind == 8:
        b = '<path d="M1 0L4 1L2 5L0 4Z" fill="#ff86b4"/><path d="M6 2L8 4L5 5Z" fill="#fff16b"/><path d="M4 6L7 5L8 7L5 8Z" fill="#74edff"/>'
    elif kind == 9:
        b = '<path d="M2 1H6L8 4L6 7H2L0 4Z" fill="#ffbd37" stroke="#fff0aa" stroke-width=".7"/><path d="M2 3L4 2H6" fill="none" stroke="#fff8c9" stroke-width=".8"/>'
    elif kind == 10:
        b = '<circle cx="4" cy="4" r="2.3" fill="#b687ff" opacity=".45"/><path d="M4 0L5 3L8 4L5 5L4 8L3 5L0 4L3 3Z" fill="#f4dfff"/><circle cx="7" cy="1" r=".7" fill="#79ddff"/>'
    else:
        b = '<path d="M4 0L8 4L4 8L0 4Z" fill="#e3f6ff"/>'
    return svg(b, 8, 8)


def cosmetic_block(c, style=2, ghost=False):
    if ghost:
        return block(c, True)
    if style == 1:
        return block(c)
    b = rect(.5, .5, 15, 15, c, r=1)
    if style == 2:
        b += '<path d="M1 15L5 8L7 12L10 3L15 15Z" fill="#fff1b1" opacity=".42"/><path d="M2 2H14" stroke="#fff" opacity=".75"/>'
    elif style == 3:
        b += '<path d="M1 1L8 8L15 1 M1 15L8 8L15 15 M1 1L15 15 M1 15L15 1" stroke="#e7ffff" opacity=".65" stroke-width=".6"/><path d="M8 2L11 8L8 14L5 8Z" fill="#fff" opacity=".25"/>'
    elif style == 4:
        b += '<path d="M1 1H15V15H1Z" fill="none" stroke="#f9dcff" stroke-width="1"/><path d="M2 12L12 2M6 14L14 6" stroke="#9dffff" opacity=".65"/>'
    elif style == 5:
        b = rect(.5, .5, 15, 15, '#0a1021', c, 1, 'stroke-width="1"')
        b += f'<path d="M3 12V4H12M5 10V6H10M11 13H13V10" fill="none" stroke="{c}" stroke-width=".9"/><path d="M1 5V1H5M11 15H15V11" fill="none" stroke="#fff" stroke-width=".7" opacity=".8"/><circle cx="12" cy="4" r="1" fill="#fff"/>'
    elif style == 6:
        b += '<path d="M1 1H15V15H1Z" fill="#0a0b15" opacity=".78"/><path d="M1 1L9 3L6 8L1 11Z" fill="#b8b5d1" opacity=".23"/><path d="M9 3L15 1L13 10L6 8Z" fill="#fff" opacity=".12"/><path d="M1 11L6 8L13 10L15 15H1Z" fill="#000" opacity=".45"/>'
        b += f'<path d="M1 11L6 8L9 3M6 8L13 10L15 15" fill="none" stroke="{c}" stroke-width=".7" opacity=".85"/>'
    elif style == 7:
        b += '<path d="M1 1H15V15H1Z" fill="#57360c" opacity=".3"/>'
        for x, y in ((5, 4), (12, 8), (5, 12)):
            b += f'<path d="M{x-4} {y}L{x-2} {y-3.5}H{x+2}L{x+4} {y}L{x+2} {y+3.5}H{x-2}Z" fill="none" stroke="#fff0aa" stroke-width=".8"/>'
        b += '<path d="M2 2H6" stroke="#fff" opacity=".75" stroke-width="1"/>'
    elif style == 8:
        b += '<path d="M1 1H15V15H1Z" fill="#1b0739" opacity=".45"/><path d="M1 11Q4 1 9 5T15 3M1 14Q6 5 10 10T15 6" fill="none" stroke="#f0b1ff" stroke-width="1.3"/><path d="M3 1Q12 4 10 10T15 14" fill="none" stroke="#c8ffff" stroke-width=".7"/><circle cx="9" cy="6" r="2" fill="#fff" opacity=".65"/>'
    elif style == 9:
        b += '<path d="M1 1H15V15H1Z" fill="#fff" opacity=".42"/><path d="M1 5Q6 2 8 7T15 10M3 1Q7 5 4 9T7 15M1 13Q8 10 12 15M9 1Q10 4 15 5" fill="none" stroke="#252a43" stroke-width=".7" opacity=".55"/><path d="M1 4Q6 1 9 6T15 9M3 1Q8 6 5 10" fill="none" stroke="#fff" stroke-width=".8" opacity=".9"/>'
    return svg(b, 16, 16)


def aura(style, frame):
    """Eight-frame, 168x328 border artwork with an empty playfield center."""
    f = int(frame) % 8
    aura_rainbow = ['#ff799c', '#ffb55e', '#f9ed84', '#7df4c0', '#74dfff', '#b89bff', '#e4a3ff', '#ff93bf']
    colors = ['#ffd57d', aura_rainbow[f], '#ff874a', '#73e5ff', '#cbf7ff', '#bb8bff', '#ffd15c']
    c = colors[max(0, min(6, int(style) - 1))]
    b = [rect(2, 2, 164, 324, 'none', c, 3, 'stroke-width=".8" stroke-opacity=".55"'),
         rect(4, 4, 160, 320, 'none', c, 2, 'stroke-width="1.4" stroke-opacity=".65"')]
    if style in (1, 2):
        for i in range(12):
            y = (i * 31 + f * 7) % 320 + 4
            b.append(f'<circle cx="{3 if i%2 else 165}" cy="{y}" r="1.3" fill="{c}"/>')
    elif style == 3:
        for side in (0, 1):
            for i in range(18):
                y = 9 + (i * 19 + f * 5) % 310
                x, d = (1, 1) if side == 0 else (167, -1)
                b.append(f'<path d="M{x} {y+5}Q{x+d*4} {y+1} {x+d} {y-6}Q{x-d} {y-2} {x} {y+5}Z" fill="{["#ff6b35", "#ffbd54", "#fff1b1"][i%3]}" opacity=".85"/>')
    elif style == 4:
        for side in (2, 166):
            points = ' '.join(f'{side+sin((y+f*9)*.1)*1.25:.2f},{y}' for y in range(7, 322, 4))
            b.append(f'<polyline points="{points}" fill="none" stroke="#bdffff" stroke-width="1.2"/>')
            for i in range(10):
                y = 9 + (i * 31 - f * 6) % 310
                b.append(f'<circle cx="{side}" cy="{y}" r="1.25" fill="none" stroke="#9ceaff" stroke-width=".6"/>')
    elif style == 5:
        for side in (0, 1):
            for i in range(13):
                y = 9 + i * 25
                x, d = (1, 1) if side == 0 else (167, -1)
                h = 4 + (i + f) % 4
                b.append(f'<path d="M{x} {y-h}L{x+d*3} {y}L{x} {y+h}Z" fill="#dbfaff" opacity=".8"/><path d="M{x} {y-h}V{y+h}" stroke="#fff" stroke-width=".6"/>')
    elif style == 6:
        for i in range(24):
            y = 8 + (i * 29 + f * 4) % 312
            x = 2 if i % 2 else 166
            color = ['#ae91ff', '#ed9eea', '#8cdcff'][i % 3]
            b.append(f'<ellipse cx="{x}" cy="{y}" rx="1.8" ry="6" fill="{color}" opacity=".25"/><path d="M{x-1.5} {y}H{x+1.5}M{x} {y-2}V{y+2}" stroke="{color}" stroke-width=".6"/>')
        for x in range(12, 160, 23):
            y = 2 if (x + f) % 2 else 326
            b.append(f'<circle cx="{x}" cy="{y}" r=".8" fill="#e9d6ff"/>')
    elif style == 7:
        for side in (2, 166):
            for i in range(20):
                y = 9 + i * 16
                b.append(f'<path d="M{side-1.7} {y-2}L{side} {y-3.5}L{side+1.7} {y-2}V{y+2}L{side} {y+3.5}L{side-1.7} {y+2}Z" fill="{["#ffca49", "#fff1a0"][(i+f)%2]}" opacity=".8"/>')
        for x in range(14, 158, 24):
            y = 2 if (x // 24 + f) % 2 else 326
            b.append(f'<path d="M{x-3} {y}H{x+3}" stroke="#ffe18a" stroke-width="2"/><path d="M{x-1} {y-1.5}V{y+1.5}M{x+1} {y-1.5}V{y+1.5}" stroke="#8b5714" stroke-width=".8"/>')
    return svg(''.join(b), 168, 328)
