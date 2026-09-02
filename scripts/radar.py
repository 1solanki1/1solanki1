import json, math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'assets' / 'skills.json').read_text())
axes = data['axes']

W, H, CX, CY, R = 760, 560, 380, 300, 190


def point(i, radius):
    a = -math.pi / 2 + 2 * math.pi * i / len(axes)
    return CX + radius * math.cos(a), CY + radius * math.sin(a)


def svg(dark):
    bg = '#0d1117' if dark else '#ffffff'
    fg = '#39d353' if dark else '#1a7f37'
    grid = '#30363d' if dark else '#d0d7de'
    accent = '#39d353' if dark else '#1a7f37'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
        f'<rect width="100%" height="100%" rx="18" fill="{bg}"/>',
    ]

    for level in range(1, 6):
        pts = ' '.join(
            f'{point(i, R * level / 5)[0]:.1f},{point(i, R * level / 5)[1]:.1f}'
            for i in range(len(axes))
        )
        parts.append(
            f'<polygon points="{pts}" fill="none" stroke="{grid}" stroke-width="1"/>'
        )

    for i, a in enumerate(axes):
        x, y = point(i, R)
        parts.append(
            f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{grid}"/>'
        )
        lx, ly = point(i, R + 34)
        parts.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{fg}" '
            f'font-family="Arial,sans-serif" font-size="15" '
            f'text-anchor="middle" dominant-baseline="middle">{a["label"]}</text>'
        )

    vals = [max(0, min(100, a['value'])) for a in axes]
    pts = ' '.join(
        f'{point(i, R * v / 100)[0]:.1f},{point(i, R * v / 100)[1]:.1f}'
        for i, v in enumerate(vals)
    )
    parts.append(
        f'<polygon points="{pts}" fill="{accent}" fill-opacity="0.20" '
        f'stroke="{accent}" stroke-width="3"/>'
    )
    parts.append('</svg>')
    return ''.join(parts)


out = root / 'assets'
(out / 'skills-dark.svg').write_text(svg(True))
(out / 'skills-light.svg').write_text(svg(False))
print('Generated neon-green skill radar SVGs')
