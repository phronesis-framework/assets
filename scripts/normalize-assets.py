"""Regenerate the four local brand packages with matching variant semantics.

Run with Python and rsvg-convert on PATH. --check validates existing exports.
"""
from pathlib import Path
import hashlib
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from html import escape

BASE = Path('C:/develop')
FONT = 'Arial, Helvetica, sans-serif'
BACKGROUND = '#2D2D2D'
BRANDS = [
    ('phronesis-framework', 'phronesis', 'FRAMEWORK', 'public/assets', 'public_png/assets', 'phronesis', (35, 20, 130, 160)),
    ('terecode', 'Terecode', 'CROSS-PLATFORM UI COMPILER', 'svg', 'png', 'terecode', (3, 3, 60, 60)),
    ('theracode-es', 'TheraCode-ES', 'MACHINE LEARNING RESEARCH', 'svg', 'png', 'thera', (0, 0, 32, 28)),
    ('atlas', 'ATLAS', 'Personal Life Assistant', 'public-svg', 'public-png', 'atlas', (8.75, 3.75, 42.5, 55.5)),
]


def geometry(brand, color=None):
    if brand == 'phronesis':
        return f'<circle cx="100" cy="100" r="60" fill="none" stroke="{color or "#000000"}" stroke-width="10"/><line x1="100" y1="20" x2="100" y2="180" stroke="{color or "#000000"}" stroke-width="10"/>'
    if brand == 'terecode':
        return ''.join(f'<rect x="{x}" y="{y}" width="18" height="18" rx="2.5" fill="{color or fill}"/>' for x, y, fill in [(3, 3, '#2563EB'), (24, 3, '#2563EB'), (45, 3, '#2563EB'), (24, 24, '#2563EB'), (24, 45, '#14B8A6')])
    if brand == 'thera':
        return ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="1.5" fill="{color or fill}"/>' for x, y, w, fill in [(0, 0, 32, '#14B8A6'), (0, 11, 19, '#2563EB'), (22, 11, 10, '#2563EB'), (0, 22, 9, '#0F172A'), (11.5, 22, 9, '#0F172A'), (23, 22, 9, '#0F172A')])
    primary, accent = color or '#246BFD', color or '#36C5F0'
    return f'<defs><clipPath id="sphere"><circle cx="30" cy="25" r="20"/></clipPath></defs><circle cx="30" cy="25" r="20" fill="none" stroke="{primary}" stroke-width="2.5"/><g clip-path="url(#sphere)" fill="none" stroke="{accent}" stroke-width="1.5"><ellipse cx="30" cy="25" rx="20" ry="6"/><line x1="30" y1="5" x2="30" y2="45"/></g><g stroke="{primary}" stroke-width="2.5" stroke-linecap="round"><line x1="30" y1="45" x2="30" y2="58"/><line x1="15" y1="58" x2="45" y2="58"/></g>'


def symbol(brand, bounds, cx, cy, size, color=None):
    x, y, w, h = bounds
    scale = size / max(w, h)
    return f'<g transform="translate({cx - (x+w/2)*scale:g} {cy - (y+h/2)*scale:g}) scale({scale:g})">{geometry(brand, color)}</g>'


def text(name, tagline, x, y, color, secondary, centered=False):
    anchor = 'middle' if centered else 'start'
    return f'<g font-family="{FONT}" text-anchor="{anchor}"><text x="{x}" y="{y}" font-size="64" font-weight="600" fill="{color}">{escape(name)}</text><text x="{x}" y="{y+42}" font-size="18" letter-spacing="2" fill="{secondary}">{escape(tagline)}</text></g>'


def svg(width, height, content, background=None):
    ground = f'<rect width="{width}" height="{height}" fill="{background}"/>' if background else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{ground}{content}</svg>\n'


def exports(spec):
    root, name, tagline, _, _, brand, bounds = spec
    regular = symbol(brand, bounds, 130, 120, 160) + text(name, tagline, 250, 125, '#111111', '#666666')
    dark = symbol(brand, bounds, 130, 120, 160, '#FFFFFF') + text(name, tagline, 250, 125, '#FFFFFF', '#FFFFFF')
    mono = symbol(brand, bounds, 130, 120, 160, '#000000') + text(name, tagline, 250, 125, '#000000', '#000000')
    files = {
        'lockup/lockup-horizontal.svg': (svg(1000, 240, regular), 2000, 480),
        'lockup/lockup-horizontal-dark.svg': (svg(1000, 240, dark, BACKGROUND), 2000, 480),
        'lockup/lockup-horizontal-monochrome.svg': (svg(1000, 240, mono), 2000, 480),
        'lockup/lockup-vertical.svg': (svg(600, 600, symbol(brand, bounds, 300, 200, 240) + text(name, tagline, 300, 420, '#111111', '#666666', True)), 1200, 1200),
        'favicon/favicon.svg': (svg(200, 200, symbol(brand, bounds, 100, 100, 160, '#FFFFFF'), BACKGROUND), 256, 256),
        'favicon/safari-pinned-tab.svg': (svg(200, 200, symbol(brand, bounds, 100, 100, 160, '#000000')), 256, 256),
        f'{brand}-master.svg': (svg(1000, 1000, f'<g transform="translate(0 20)">{regular}</g><g transform="translate(0 300)"><rect width="1000" height="240" fill="{BACKGROUND}"/>{dark}</g><g transform="translate(0 580)">{mono}</g>', '#FFFFFF'), 2000, 2000),
    }
    for filename, color in [('symbol', '#000000'), ('symbol-light', '#FFFFFF'), ('symbol-color', None)]:
        files[f'symbol/{filename}.svg'] = (svg(200, 200, symbol(brand, bounds, 100, 100, 160, color)), 1024, 1024)
    # Keep Terecode's existing white filename as an identical compatibility alias.
    if root == 'terecode':
        files['symbol/symbol-white.svg'] = files['symbol/symbol-light.svg']
    for filename in ['wordmark', 'wordmark-light', 'wordmark-dark']:
        is_dark = filename.endswith('-dark')
        files[f'wordmark/{filename}.svg'] = (svg(800, 200, text(name, tagline, 50, 100, '#FFFFFF' if is_dark else '#111111', '#FFFFFF' if is_dark else '#666666'), BACKGROUND if is_dark else None), 1600, 400)
    return files


def check(spec, files):
    root, _, _, svgdir, pngdir, _, _ = spec
    assetroot = BASE / root / 'assets'
    for relative, (expected, width, height) in files.items():
        source = assetroot / svgdir / relative
        assert source.read_text(encoding='utf-8') == expected, source
        ET.fromstring(expected)
        png = assetroot / pngdir / Path(relative).with_suffix('.png')
        header = png.read_bytes()[:24]
        assert header[:8] == b'\x89PNG\r\n\x1a\n', png
        assert struct.unpack('>II', header[16:24]) == (width, height), png
    assert 'opacity=' not in ''.join(v[0] for v in files.values())


def main():
    for spec in BRANDS:
        root, _, _, svgdir, pngdir, _, _ = spec
        assetroot = BASE / root / 'assets'
        files = exports(spec)
        if '--check' not in sys.argv:
            for relative, (content, width, height) in files.items():
                source = assetroot / svgdir / relative
                png = assetroot / pngdir / Path(relative).with_suffix('.png')
                source.parent.mkdir(parents=True, exist_ok=True)
                png.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(content, encoding='utf-8')
                subprocess.run(['rsvg-convert', '-w', str(width), '-h', str(height), '-o', str(png), str(source)], check=True)
            readme = assetroot / ('public/assets/README.md' if root == 'phronesis-framework' else 'README.md')
            readme.write_text(f'# {spec[1]} — Brand assets\n\n'
                'Shared variant convention across the four organizations.\n\n'
                '| Variant | Background | Artwork |\n|---|---|---|\n'
                '| Horizontal / vertical | Transparent | Brand-colored symbol, dark text |\n'
                '| Dark lockup / wordmark | `#2D2D2D` | Solid white |\n'
                '| Monochrome | Transparent | Solid black |\n'
                '| Symbol / symbol-light / symbol-color | Transparent | Black / white / brand colors |\n'
                '| Wordmark / wordmark-light | Transparent | Dark text |\n'
                '| Favicon / avatar | `#2D2D2D` | Solid white symbol |\n'
                '| Safari pinned tab | Transparent | Solid black symbol |\n\n'
                'PNG sizes: horizontal 2000×480, vertical 1200×1200, symbols 1024×1024, '
                'wordmarks 1600×400, favicons 256×256. Typography uses Arial with Helvetica '
                'and sans-serif fallbacks; no remote font imports.\n\n'
                'Regeneration: `python C:/develop/phronesis-framework/assets/scripts/normalize-assets.py`. '
                'Requires `rsvg-convert`. Validation: append `--check`.\n', encoding='utf-8')
            destinations = {
                'phronesis-framework': ['branding/public/assets', 'phronesis-web/public/assets', 'phronesis-framework/public/assets'],
                'terecode': ['terecode-web/assets/svg'],
                'theracode-es': ['theracode-template/assets/svg', 'theracode-llm/assets/svg'],
                'atlas': ['atlas-system/atlas/assets/public-svg'],
            }[root]
            for destination in destinations:
                target = BASE / root / destination
                shutil.copytree(assetroot / svgdir, target, dirs_exist_ok=True)
                pngtarget = target.parent.parent / 'public_png/assets' if root == 'phronesis-framework' else target.parent / pngdir
                if root == 'phronesis-framework' and 'branding' not in destination:
                    continue
                shutil.copytree(assetroot / pngdir, pngtarget, dirs_exist_ok=True)
                if root != 'phronesis-framework':
                    shutil.copyfile(readme, target.parent / 'README.md')
            if root == 'theracode-es':
                for project in ['theracode-template', 'theracode-llm']:
                    shutil.copyfile(assetroot / pngdir / 'lockup/lockup-horizontal-dark.png',
                                    BASE / root / project / 'public/assets/lockup/lockup-horizontal-dark.png')
            if root == 'phronesis-framework':
                for project in ['phronesis-web', 'phronesis-framework']:
                    shutil.copyfile(assetroot / pngdir / 'lockup/lockup-horizontal-dark.png',
                                    BASE / root / project / 'public/assets/phronesis-banner.png')
            banner = BASE / root / '.github/profile/assets/lockup-horizontal-dark.png'
            shutil.copyfile(assetroot / pngdir / 'lockup/lockup-horizontal-dark.png', banner)
        check(spec, files)
        banner = BASE / root / '.github/profile/assets/lockup-horizontal-dark.png'
        canonical = assetroot / pngdir / 'lockup/lockup-horizontal-dark.png'
        assert hashlib.sha256(banner.read_bytes()).digest() == hashlib.sha256(canonical.read_bytes()).digest()
        print(f'{root}: OK')


if __name__ == '__main__':
    main()
