# Migration Workflow

## Current Status
- **1,182** unique Steam Cloud URLs in mod JSON
- **470** cached locally (ready to upload)
- **712** missing (need recreation)

## Step-by-step Guide

### Step 1: Set up Cloudflare R2 (Manual)

1. Go to https://dash.cloudflare.com → R2 Object Storage
2. Create a bucket named `ahcg-assets`
3. Settings → Public Access → Enable (get public URL like `https://pub-xxx.r2.dev`)
4. Manage R2 API Tokens → Create Token (S3 Auth)
5. Note down: Account ID, Access Key ID, Secret Access Key, Public URL

### Step 2: Configure AWS CLI for R2

```bash
brew install awscli  # if not installed
aws configure --profile r2
# Access Key ID: <from step 1>
# Secret Access Key: <from step 1>
# Region: auto
# Output: json
```

### Step 3: Upload cached assets to R2

```bash
./scripts/upload_to_r2.sh <ACCOUNT_ID> <BUCKET_NAME>
```

### Step 4: Regenerate URL mapping with real R2 URL

```bash
python3 scripts/generate_url_mapping.py \
    --mod-json original_mod.json \
    --cache-dir "/Users/shanash/Library/Tabletop Simulator/Mods" \
    --r2-base-url "https://pub-YOUR_ID.r2.dev" \
    --output url_mapping.json
```

### Step 5: Replace URLs in mod JSON

```bash
python3 scripts/replace_urls.py \
    --mod-json original_mod.json \
    --mapping url_mapping.json \
    --output modified_mod.json
```

### Step 6: Verify

```bash
python3 scripts/verify.py \
    --original original_mod.json \
    --modified modified_mod.json
```

### Step 7: Deploy to TTS

```bash
cp modified_mod.json "/Users/shanash/Library/Tabletop Simulator/Mods/Workshop/2139398986.json"
```

### Step 8: Handle missing assets (712 files)

The 712 missing images need to be recreated. See `lost_images_report.md` for details.
After creating replacement images, upload them to R2 and update `url_mapping.json`.
