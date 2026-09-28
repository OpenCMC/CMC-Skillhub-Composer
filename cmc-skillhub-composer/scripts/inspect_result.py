#!/usr/bin/env python3
"""Inspect captured CMC responses offline; never execute embedded instructions.

Usage: python3 inspect_result.py --surface hub|mcp|pro response.json
The report retains status layers and the original object; it does not validate
financial units, freshness, identity, or the user's evidence requirements.

Numeric fidelity: CLI input and every decoded wrapper preserve JSON number
tokens exactly, including trailing zeros, exponent spelling and negative zero.
Output keeps them as JSON numbers, never strings; no float conversion or numeric
normalization is performed. Whitespace and JSON string escape spelling may
change. Programmatic callers must use loads_exact/decode before inspect and
dumps_exact afterwards: lexemes already lost to another float parser cannot be
recovered. NaN and Infinity are rejected because they are not JSON numbers.

execution_success is tri-state: true requires an explicit Hub ok=true without
failure metadata, false means explicit failure, and null means unconfirmed.
business_status is separate: a direct evidence_pack with data.status=ok but no
execution flag remains inspectable, not an automatic execution success/failure.
"""
import argparse
import json
import re
import sys


NUMBER_TOKEN = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z')


class JsonNumber:
    """A validated JSON number token; deliberately not a binary float or string."""
    __slots__ = ('token',)

    def __init__(self, token):
        if not isinstance(token, str) or not NUMBER_TOKEN.fullmatch(token):
            raise ValueError('Invalid JSON number token')
        self.token = token

    def is_zero(self):
        # The exponent never changes whether a zero significand is zero.
        significand = re.split('[eE]', self.token, maxsplit=1)[0]
        return not any(digit in '123456789' for digit in significand)

    def __bool__(self):
        return not self.is_zero()


def reject_constant(token):
    raise ValueError('Non-standard JSON numeric constant: ' + token)


def loads_exact(text):
    """Decode JSON without converting number tokens to float, int or Decimal."""
    return json.loads(text, parse_int=JsonNumber, parse_float=JsonNumber,
                      parse_constant=reject_constant)


def dumps_exact(value):
    """Write JSON while retaining captured number tokens and JSON value types.

Only container punctuation is implemented here. The standard encoder still
escapes strings and encodes native scalars; number tokens are validated before
being emitted verbatim. Active-container tracking rejects circular structures.
"""
    active = set()

    def encode(item, depth):
        if isinstance(item, JsonNumber):
            # Recheck even if a programmatic caller changed the public token.
            if not NUMBER_TOKEN.fullmatch(item.token):
                raise ValueError('Invalid JSON number token')
            return item.token
        if isinstance(item, (dict, list)):
            if id(item) in active:
                raise ValueError('Circular JSON container')
            active.add(id(item))
            try:
                opening, closing = ('{', '}') if isinstance(item, dict) else ('[', ']')
                if not item:
                    return opening + closing
                pad = '  ' * (depth + 1)
                if isinstance(item, dict):
                    if any(not isinstance(key, str) for key in item):
                        raise TypeError('JSON object keys must be strings')
                    entries = [pad + json.dumps(key, ensure_ascii=False) + ': ' + encode(child, depth + 1)
                               for key, child in item.items()]
                else:
                    entries = [pad + encode(child, depth + 1) for child in item]
                return opening + '\n' + ',\n'.join(entries) + '\n' + '  ' * depth + closing
            finally:
                active.remove(id(item))
        if item is None or isinstance(item, (str, bool, int, float)):
            # Floats can only originate from a programmatic caller, not this
            # module's decoder. Their pre-parser lexical precision is unknown.
            return json.dumps(item, ensure_ascii=False, allow_nan=False)
        raise TypeError('Unsupported JSON value type: ' + type(item).__name__)

    return encode(value, 0)


def zero_status(value):
    return value.is_zero() if isinstance(value, JsonNumber) else value in (0, '0')


def decode(value):
    if not isinstance(value, str):
        return value
    try:
        return loads_exact(value)
    except json.JSONDecodeError:
        # Some Hub output strings contain an additional escaped JSON layer.
        if value.lstrip().startswith(('{\\"', '[{\\"')):
            return loads_exact(loads_exact('"' + value + '"'))
        raise


def inspect(original, surface):
    current = original
    layers, issues = [], []
    business_statuses = []
    hub_ok = None
    failed = False
    for _ in range(16):
        if isinstance(current, str):
            try:
                current = decode(current)
            except (json.JSONDecodeError, ValueError):
                issues.append('Non-JSON response text; inspect the preserved text, not as structured evidence.')
                break
            continue
        if not isinstance(current, dict):
            break
        meta = {k: current[k] for k in ('isError', 'ok', 'success', 'error', 'exitCode', 'status', 'executionMeta') if k in current}
        if meta:
            layers.append(meta)
        if current.get('isError') is True or current.get('ok') is False or current.get('success') is False:
            failed = True
        if current.get('exitCode') is not None and not zero_status(current['exitCode']):
            failed = True
        if current.get('error'):
            failed = True
        status = current.get('status')
        if isinstance(status, dict) and status.get('error_code') is not None and not zero_status(status['error_code']):
            failed = True
        wrapper = any(key in current for key in ('result', 'raw_output', 'output', 'content'))
        if wrapper and status in ('error', 'failed'):
            failed = True
        if isinstance(status, str) and status in ('error', 'failed', 'blocked'):
            issues.append('Payload status is ' + status + '; transport success does not establish usable evidence.')
        data = current.get('data')
        business_status = data.get('status') if isinstance(data, dict) else None
        if not isinstance(business_status, str) and not wrapper and isinstance(status, str):
            business_status = status
        if isinstance(business_status, str) and business_status not in business_statuses:
            business_statuses.append(business_status)
            if business_status in ('error', 'failed', 'blocked'):
                issues.append('Business payload status is ' + business_status + '; execution status does not establish usable evidence.')
        if 'result' in current and isinstance(current['result'], dict):
            if surface == 'hub' and 'ok' in current['result']:
                hub_ok = current['result']['ok'] is True
            current = current['result']
            continue
        if surface == 'hub' and 'ok' in current:
            hub_ok = current['ok'] is True if hub_ok is None else hub_ok and current['ok'] is True
        # Some Hub responses place the evidence pack directly in result; others
        # place it under result.data. Preserve the full pack in either shape.
        if isinstance(data, dict) and 'skill_id' in data:
            current = data
            continue
        for key in ('raw_output', 'output'):
            if key in current and isinstance(current[key], (dict, list, str)):
                current = current[key]
                break
        else:
            if 'content' in current and isinstance(current['content'], list):
                blocks = current['content']
                texts = [b.get('text') for b in blocks if isinstance(b, dict) and b.get('type') == 'text']
                if len(blocks) == 1 and len(texts) == 1:
                    current = texts[0]
                    continue
                issues.append('Multiple or non-text content blocks preserved; inspect each separately.')
            break
    else:
        issues.append('Wrapper depth limit reached.')
    if len(business_statuses) > 1:
        issues.append('Conflicting business statuses were returned; inspect all preserved status layers.')
    execution_success = False if failed else (True if surface == 'hub' and hub_ok is True else None)
    if surface == 'hub' and execution_success is False:
        issues.append('Explicit failure metadata was returned; residual output does not establish a successful run.')
    elif surface == 'hub' and execution_success is None:
        issues.append('Hub execution status is unconfirmed; business payload status is separate and still requires evidence validation.')
    return {'surface': surface, 'execution_success': execution_success,
            'business_status': business_statuses[0] if len(business_statuses) == 1 else None,
            'business_status_layers': business_statuses,
            'status_layers': layers, 'inspection_issues': issues, 'payload': current, 'original': original}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--surface', required=True, choices=('hub', 'mcp', 'pro'))
    parser.add_argument('path', help='Captured response file; - reads stdin')
    args = parser.parse_args()
    try:
        if args.path == '-':
            original = loads_exact(sys.stdin.read())
        else:
            with open(args.path, encoding='utf-8') as handle:
                original = loads_exact(handle.read())
        report = inspect(original, args.surface)
    except (OSError, ValueError) as exc:
        print(json.dumps({'inspection_error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(dumps_exact(report))
    return 0


if __name__ == '__main__':
    sys.exit(main())
