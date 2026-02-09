#!/usr/bin/env python3
"""
Verify the modified mod JSON:
  1. Check for remaining Steam Cloud URLs
  2. Test sample R2 URLs for accessibility
  3. Compare URL counts before/after

Usage:
    python3 verify.py --original ../original_mod.json --modified ../modified_mod.json
"""

import json
import re
import argparse
import urllib.request
import random


def count_steam_urls(text: str) -> int:
    return len(re.findall(r'cloud-3\.steamusercontent\.com', text))


def count_unique_urls(text: str, pattern: str) -> set:
    return set(re.findall(pattern, text))


def test_url(url: str, timeout: int = 10) -> tuple:
    """Test if a URL is accessible. Returns (status_code, ok)."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, True
    except urllib.error.HTTPError as e:
        return e.code, False
    except Exception as e:
        return str(e), False


def main():
    parser = argparse.ArgumentParser(description='Verify mod JSON URL migration')
    parser.add_argument('--original', required=True, help='Path to original mod JSON')
    parser.add_argument('--modified', required=True, help='Path to modified mod JSON')
    parser.add_argument('--test-count', type=int, default=5,
                        help='Number of R2 URLs to test (default: 5)')
    args = parser.parse_args()

    print("=== Mod JSON URL Migration Verification ===\n")

    # Load files
    with open(args.original, 'r') as f:
        original = f.read()
    with open(args.modified, 'r') as f:
        modified = f.read()

    # 1. Steam URL count comparison
    orig_steam = count_steam_urls(original)
    mod_steam = count_steam_urls(modified)
    print(f"1. Steam Cloud URL references:")
    print(f"   Original: {orig_steam}")
    print(f"   Modified: {mod_steam}")
    print(f"   Replaced: {orig_steam - mod_steam}")
    if mod_steam == 0:
        print(f"   STATUS: COMPLETE MIGRATION")
    else:
        print(f"   STATUS: {mod_steam} references remain (from missing assets)")

    # 2. Find R2 URLs in modified
    r2_urls = set(re.findall(r'https?://[^"]*r2\.dev/[^"]*', modified))
    if not r2_urls:
        r2_urls = set(re.findall(r'https?://[^"]*\.r2\.dev[^"]*', modified))
    print(f"\n2. R2 URLs in modified JSON: {len(r2_urls)} unique")

    # 3. Test sample R2 URLs
    if r2_urls and args.test_count > 0:
        sample = random.sample(list(r2_urls), min(args.test_count, len(r2_urls)))
        print(f"\n3. Testing {len(sample)} random R2 URLs:")
        for url in sample:
            status, ok = test_url(url)
            symbol = "OK" if ok else "FAIL"
            print(f"   [{symbol}] {status} - {url[:80]}...")
    else:
        print("\n3. No R2 URLs to test")

    # 4. Validate JSON structure
    print(f"\n4. JSON validation:")
    try:
        json.loads(modified)
        print(f"   Valid JSON: YES")
    except json.JSONDecodeError as e:
        print(f"   Valid JSON: NO - {e}")

    # 5. Size comparison
    print(f"\n5. File sizes:")
    print(f"   Original: {len(original):,} bytes")
    print(f"   Modified: {len(modified):,} bytes")
    print(f"   Difference: {len(modified) - len(original):+,} bytes")


if __name__ == '__main__':
    main()
