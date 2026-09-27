"""Check the shared README presentation across the four local organizations."""
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

BASE = Path('C:/develop')
ORG_NAMES = ['phronesis-framework', 'terecode', 'theracode-es', 'atlas']


def check(path):
    text = path.read_text(encoding='utf-8-sig')
    prose = re.sub(r'(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*$', '', text)
    assert len(re.findall(r'(?m)^# ', prose)) == 1, (path, 'one title required')
    assert not re.search(r'(?m)^#\s*$', prose), (path, 'empty title')
    images = re.findall(r'<img\b[^>]*>', prose)
    assert images and 'lockup-horizontal-dark.png' in images[0], (path, 'dark banner required')
    assert 'width="100%"' in images[0], (path, 'full-width banner required')
    assert 'https://go-skill-icons.vercel.app/api/icons?' in prose, (path, 'shared icon provider')
    assert '## 🎯 Purpose' in prose, (path, 'purpose required')
    assert prose.count('<div') == prose.count('</div>'), (path, 'unbalanced HTML')
    for heading in re.findall(r'(?m)^## [^\n]+', prose):
        assert f'<div align="center">\n\n{heading}\n\n</div>' in prose, (path, heading)
    for image in images:
        source = re.search(r'src="([^"]+)"', image).group(1)
        if not source.startswith(('https:', 'http:', 'data:')):
            assert (path.parent / unquote(source)).exists(), (path, source)
    assert 'https://github.com/terecode/terecode' not in prose, (path, 'stale repository link')


def main():
    checked = 0
    for name in ORG_NAMES:
        result = subprocess.run(['rg', '--files', '--hidden', str(BASE / name),
                                 '-g', 'README.md', '-g', '!.git', '-g', '!node_modules',
                                 '-g', '!.next', '-g', '!.venv', '-g', '!dist', '-g', '!build'],
                                capture_output=True, text=True, check=True)
        for filename in result.stdout.splitlines():
            check(Path(filename))
            checked += 1
    template = BASE / 'atlas/atlas-system/_harness/template/README.md.tpl'
    if template.exists():
        check(template)
        assert '{{MODULE_NAME}}' in template.read_text(encoding='utf-8')
    print(f'{checked} READMEs: OK')


if __name__ == '__main__':
    main()
