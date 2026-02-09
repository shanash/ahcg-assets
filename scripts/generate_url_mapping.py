#!/usr/bin/env python3
"""
Generate url_mapping.json by scanning the mod JSON for Steam Cloud URLs
and matching them to locally cached files.

Usage:
    python3 generate_url_mapping.py \
        --mod-json ../original_mod.json \
        --cache-dir "/Users/shanash/Library/Tabletop Simulator/Mods" \
        --r2-base-url "https://YOUR_R2_PUBLIC_URL" \
        --output ../url_mapping.json
"""

import json
import re
import os
import argparse
from pathlib import Path


def url_to_cache_basename(url: str) -> str:
    """Convert a URL to the TTS cache filename (without extension)."""
    return re.sub(r'[^a-zA-Z0-9]', '', url)


def find_all_urls(obj, urls=None):
    """Recursively find all URL-like string values in a JSON object."""
    if urls is None:
        urls = set()

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and 'cloud-3.steamusercontent.com' in value:
                urls.add(value)
            else:
                find_all_urls(value, urls)
    elif isinstance(obj, list):
        for item in obj:
            find_all_urls(item, urls)

    return urls


def find_cached_file(cache_basename: str, cache_dirs: dict) -> tuple:
    """Find cached file matching the basename in any cache directory.
    Returns (relative_path, asset_type) or (None, None)."""
    extensions_by_type = {
        'images': ['.png', '.jpg', '.jpeg'],
        'models': ['.obj'],
        'assetbundles': ['.unity3d'],
    }

    for asset_type, dir_path in cache_dirs.items():
        for ext in extensions_by_type.get(asset_type, []):
            filename = cache_basename + ext
            full_path = os.path.join(dir_path, filename)
            if os.path.exists(full_path):
                return f"{asset_type}/{filename}", asset_type
    return None, None


def main():
    parser = argparse.ArgumentParser(description='Generate URL mapping for R2 migration')
    parser.add_argument('--mod-json', required=True, help='Path to original mod JSON')
    parser.add_argument('--cache-dir', required=True, help='Path to TTS Mods directory')
    parser.add_argument('--r2-base-url', default='https://PLACEHOLDER.r2.dev',
                        help='R2 public base URL')
    parser.add_argument('--output', default='url_mapping.json', help='Output mapping file')
    args = parser.parse_args()

    cache_dirs = {
        'images': os.path.join(args.cache_dir, 'Images'),
        'models': os.path.join(args.cache_dir, 'Models'),
        'assetbundles': os.path.join(args.cache_dir, 'Assetbundles'),
    }

    # Load mod JSON
    print(f"Loading mod JSON from {args.mod_json}...")
    with open(args.mod_json, 'r', encoding='utf-8') as f:
        mod_data = json.load(f)

    # Extract all Steam URLs
    steam_urls = find_all_urls(mod_data)
    print(f"Found {len(steam_urls)} unique Steam Cloud URLs")

    # Map each URL to cached file and R2 URL
    mapping = {}
    cached_count = 0
    missing_count = 0

    for url in sorted(steam_urls):
        cache_basename = url_to_cache_basename(url)
        relative_path, asset_type = find_cached_file(cache_basename, cache_dirs)

        if relative_path:
            r2_url = f"{args.r2_base_url.rstrip('/')}/{relative_path}"
            mapping[url] = {
                "r2_url": r2_url,
                "cached_file": relative_path,
                "asset_type": asset_type,
                "status": "cached"
            }
            cached_count += 1
        else:
            mapping[url] = {
                "r2_url": None,
                "cached_file": None,
                "asset_type": None,
                "status": "missing"
            }
            missing_count += 1

    # Write mapping
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"\nResults:")
    print(f"  Cached (ready to upload): {cached_count}")
    print(f"  Missing (need recreation): {missing_count}")
    print(f"  Total: {cached_count + missing_count}")
    print(f"\nMapping written to {args.output}")


if __name__ == '__main__':
    main()
