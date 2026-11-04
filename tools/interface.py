"""Shared native-Scratch hover bounds for every clickable interface control.

Coordinates use the 480 x 360 canvas, with its origin at the upper left.
Tab zero is always visible; other tabs belong to Settings or Cosmetics.
"""
from visuals import svg, rect, THEME_NAMES
from progression import DIFFICULTY_NAMES, EFFECT_NAMES, SKIN_NAMES, AURA_NAMES
from impact_art import DROP_NAMES


BUTTONS = []


def _button(screen, box, label, tab=0):
    BUTTONS.append((screen, tab, box, label))


for box, label in [
    ((32, 112, 246, 150), 'Play / Resume'),
    ((32, 162, 246, 192), 'New Run'),
    ((32, 204, 246, 234), 'Themes'),
    ((32, 246, 246, 276), 'Run History'),
    ((270, 266, 468, 290), 'Cosmetics'),
    ((270, 300, 358, 328), 'Settings'),
    ((364, 300, 468, 328), 'Achievements'),
]:
    _button('menu', box, label)
_button('play', (8, 10, 100, 34), 'Menu')

_button('themes', (16, 16, 100, 42), 'Back')
for index, name in enumerate(THEME_NAMES[:12]):
    x, y = 12 + 116 * (index % 4), 86 + 70 * (index // 4)
    _button('themes', (x, y, x + 106, y + 62), name)

for screen, top, bottom in [('history', 288, 316), ('achievements', 306, 334)]:
    _button(screen, (16, 16, 100, 42), 'Back')
    _button(screen, (96, top, 196, bottom), 'Previous')
    _button(screen, (284, top, 384, bottom), 'Next')

_button('difficulty', (16, 16, 100, 42), 'Back')
for index, name in enumerate(DIFFICULTY_NAMES):
    y = 98 + index * 44
    _button('difficulty', (32, y, 448, y + 34), name)

for box, label in [
    ((16, 16, 100, 42), 'Back'),
    ((112, 16, 198, 42), 'Clear tab'),
    ((202, 16, 288, 42), 'Blocks tab'),
    ((292, 16, 378, 42), 'Auras tab'),
    ((382, 16, 468, 42), 'Drops tab'),
    ((18, 316, 164, 344), 'RGB / Rainbow'),
    ((310, 316, 462, 344), 'Save Profile'),
]:
    _button('cosmetics', box, label)
for tab, names in enumerate([EFFECT_NAMES, SKIN_NAMES, AURA_NAMES, DROP_NAMES], 1):
    for index, name in enumerate(names):
        x, y = 12 + 94 * (index % 5), 100 + 100 * (index // 5)
        _button('cosmetics', (x, y, x + 82, y + 82), name, tab)

for box, label in [
    ((16, 16, 100, 42), 'Back'),
    ((166, 16, 306, 42), 'General tab'),
    ((316, 16, 456, 42), 'RGB Colors tab'),
    ((310, 316, 462, 344), 'Save Profile'),
]:
    _button('settings', box, label)
_button('settings', (126, 78, 456, 104), 'Player name', 1)
for index, name in enumerate(DIFFICULTY_NAMES):
    x = 126 + index * 66
    _button('settings', (x, 116, x + 60, 140), name, 1)
_button('settings', (140, 153, 420, 175), 'Shake intensity', 1)
_button('settings', (424, 153, 462, 175), 'Shake Off', 1)
_button('settings', (126, 214, 456, 252), 'Cosmetics', 1)

for title, offset in [('Game accent', 0), ('Key highlight', 120)]:
    for index, channel in enumerate(['R', 'G', 'B']):
        y = 112 + 30 * index + offset
        _button('settings', (136, y - 7, 366, y + 7), title + ' ' + channel + ' slider', 2)
        _button('settings', (376, y - 10, 418, y + 10), title + ' ' + channel + ' value', 2)
for box, label in [
    ((18, 182, 164, 202), 'Rainbow Accent'),
    ((174, 316, 296, 344), 'Rainbow Keys'),
    ((18, 316, 164, 344), 'Use Theme Colors'),
]:
    _button('settings', box, label, 2)


def button_glow(box):
    """A transparent, full-stage highlight aligned with the native hitbox."""
    x1, y1, x2, y2 = box
    x, y, w, h = x1 + .5, y1 + .5, x2 - x1 - 1, y2 - y1 - 1
    radius = min(4, h / 4)
    body = rect(x, y, w, h, '#b9eeff', r=radius, extra='fill-opacity=".055"')
    for width, opacity, color in [(7, .07, '#90ccff'), (3, .25, '#a9dfff'), (.9, .95, '#e4f8ff')]:
        body += rect(x, y, w, h, 'none', color, r=radius,
                     extra=f'stroke-width="{width}" stroke-opacity="{opacity}"')
    return svg(body)


assert len(BUTTONS) == 101
assert len({(screen, tab, label) for screen, tab, _, label in BUTTONS}) == len(BUTTONS)
