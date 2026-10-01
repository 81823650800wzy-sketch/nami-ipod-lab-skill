#!/usr/bin/env python3
"""Check this skill bundle from any cwd; no USB/network/dependency installation."""
import ast
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def inspect(root):
    root = Path(root).resolve()
    errors = []
    required = ('SKILL.md', 'agents/openai.yaml', 'references/agent-handoff.md',
                'references/safety-and-evidence.md', 'references/workflows.md',
                'references/troubleshooting.md', 'references/manifest-validation.md',
                'references/publishing.md', 'scripts/validate_evidence.py',
                'scripts/test_validate_evidence.py', 'assets/nami-ipod-lab.svg')
    for name in required:
        if not (root / name).is_file():
            errors.append('missing: ' + name)
    for path in root.rglob('*.md'):
        content = path.read_text(encoding='utf-8-sig')
        for link in re.findall(r'\]\(([^)]+)\)', content):
            target = link.split('#', 1)[0]
            if not target or re.match(r'^[a-z]+:', target):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f'{path.relative_to(root)}: unresolved local link {link}')
    entry = root / 'SKILL.md'
    if entry.is_file():
        text = entry.read_text(encoding='utf-8-sig')
        header = re.match(r'^---\r?\n(.*?)\r?\n---', text, re.S)
        if not header or not re.search(r'^name: nami-ipod-lab$', header[1], re.M):
            errors.append('invalid name/frontmatter')
        if not header or not re.search(r'^description: .+', header[1], re.M):
            errors.append('missing description')
    metadata = root / 'agents/openai.yaml'
    if metadata.is_file():
        text = metadata.read_text(encoding='utf-8-sig')
        if '$nami-ipod-lab' not in text:
            errors.append('default prompt lacks invocation')
        for asset in re.findall(r'icon_(?:small|large): "([^"]+)"', text):
            if not (root / asset).is_file():
                errors.append('missing UI asset: ' + asset)
    for path in (root / 'scripts').glob('*.py'):
        try:
            ast.parse(path.read_text(encoding='utf-8-sig'))
        except SyntaxError as error:
            errors.append(f'{path.name}: {error}')
    return {'result': 'FAILED' if errors else 'PASS', 'skillRoot': str(root),
            'pythonSupported': sys.version_info >= (3, 10), 'errors': errors,
            'limitations': 'Bundle/link/syntax checks only; no live catalog or hardware validation'}


if __name__ == '__main__':
    report = inspect(Path(__file__).resolve().parents[1])
    if not report['pythonSupported']:
        report['result'] = 'FAILED'
        report['errors'].append('Python 3.10+ required')
    print(json.dumps(report, indent=2))
    raise SystemExit(report['result'] != 'PASS')
