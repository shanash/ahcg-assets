# Arkham Horror LCG - Super Complete Edition (TTS)

Asset management for the Tabletop Simulator mod (Workshop ID: 2139398986).

## Problem
Steam Cloud image URLs for this mod returned 403 errors, breaking all card images.

## Solution
- Original mod JSON backed up as `original_mod.json`
- Cached assets (images, models, assetbundles) hosted on Cloudflare R2
- `url_mapping.json` maps old Steam URLs → new R2 URLs
- `modified_mod.json` is the patched version with working URLs

## Files
| File | Description |
|------|-------------|
| `original_mod.json` | Unmodified mod JSON (backup) |
| `modified_mod.json` | Patched JSON with R2 URLs |
| `url_mapping.json` | Steam URL → R2 URL mapping table |
| `lost_images_report.md` | Report of missing/cached images |
| `scripts/upload_to_r2.sh` | Script to upload cached assets to R2 |
| `scripts/replace_urls.py` | Script to replace URLs in mod JSON |

## Asset Hosting
- **Provider**: Cloudflare R2 (S3-compatible)
- **Free tier**: 10GB storage, unlimited bandwidth
- **Total assets**: ~1.67GB (471 cached files)
