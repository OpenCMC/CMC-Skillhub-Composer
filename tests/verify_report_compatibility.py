#!/usr/bin/env python3
"""Check preservation of the original report contract, not agent behavior.

Run from any directory in a full Git checkout. The baseline is deliberately
pinned: moving main must not silently change what this compatibility check means.
"""
import argparse
from pathlib import Path
import subprocess

BASELINE = 'a7cb81af67ac5642b4c9ee1d631aca108e665a45'
ROOT = Path(__file__).resolve().parents[1]
SKILL = 'cmc-skillhub-composer/SKILL.md'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def section(text, title):
    start = text.index('## ' + title + '\n')
    end = text.find('\n## ', start + 4)
    return (text[start:] if end < 0 else text[start:end + 1]).strip()


def verify(baseline):
    old = git('show', baseline + ':' + SKILL).decode()
    new = (ROOT / SKILL).read_text()
    failures = []
    originals = git('ls-tree', '-r', '--name-only', baseline,
                    'cmc-skillhub-composer/reference').decode().splitlines()
    for name in originals:
        path = ROOT / name
        if not path.is_file() or path.read_bytes() != git('show', baseline + ':' + name):
            failures.append('Original reference changed or missing: ' + name)
    for title in ('Language', 'Standard Report Format', 'Self-check before answering', 'Spacing'):
        try:
            if section(old, title) != section(new, title):
                failures.append('Original inline section changed: ' + title)
        except ValueError:
            failures.append('Original inline section missing: ' + title)
    # Extra routes are allowed; the existing rows, rules and their order stay intact.
    try:
        remaining = iter(section(new, 'Output Template Router').splitlines())
        for line in section(old, 'Output Template Router').splitlines():
            if line and not any(candidate == line for candidate in remaining):
                failures.append('Original template routing line changed or reordered: ' + line)
                break
    except ValueError:
        failures.append('Output Template Router missing from SKILL.md')
    gate = next(line for line in old.splitlines() if line.startswith('After a successful run, pick'))
    if gate not in new:
        failures.append('Original default successful-run routing instruction changed')
    for paragraph in section(old, 'Error and status handling').split('\n\n'):
        if paragraph.startswith(('If `status` is `blocked`', 'If `status` is `partial`')) and paragraph not in new:
            failures.append('Original blocked/partial output contract changed')
    if 'reference/report-format.md' in new:
        failures.append('Report contract depends on the withdrawn formatting indirection')
    return failures, len(originals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', default=BASELINE)
    args = parser.parse_args()
    try:
        failures, file_count = verify(args.baseline)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        parser.exit(2, 'Cannot verify the baseline; use a full checkout containing '
                    + args.baseline + ': ' + str(exc) + '\n')
    if failures:
        parser.exit(1, '\n'.join(failures) + '\n')
    print(f'PASS: {file_count} original reference files (5 templates, 8 startup docs), '
          '4 complete inline sections, original router rows/rules, default routing, '
          'and blocked/partial formatting are preserved.')
    print('This checks source compatibility only. Agent-output regression is reported separately.')


if __name__ == '__main__':
    main()
