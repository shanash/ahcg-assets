#!/usr/bin/env bash
#
# Upload cached TTS assets to Cloudflare R2 using AWS CLI (S3-compatible).
#
# Prerequisites:
#   1. AWS CLI installed: brew install awscli
#   2. Configure R2 credentials:
#      aws configure --profile r2
#        AWS Access Key ID: <your R2 access key>
#        AWS Secret Access Key: <your R2 secret key>
#        Default region name: auto
#        Default output format: json
#
# Usage:
#   ./upload_to_r2.sh <ACCOUNT_ID> <BUCKET_NAME>
#
# Example:
#   ./upload_to_r2.sh abc123def456 ahcg-assets

set -euo pipefail

ACCOUNT_ID="${1:?Usage: $0 <ACCOUNT_ID> <BUCKET_NAME>}"
BUCKET_NAME="${2:?Usage: $0 <ACCOUNT_ID> <BUCKET_NAME>}"

R2_ENDPOINT="https://${ACCOUNT_ID}.r2.cloudflarestorage.com"
CACHE_BASE="/Users/shanash/Library/Tabletop Simulator/Mods"
AWS_PROFILE="r2"

echo "=== Cloudflare R2 Upload ==="
echo "Endpoint: ${R2_ENDPOINT}"
echo "Bucket:   ${BUCKET_NAME}"
echo ""

# Upload Images
echo "Uploading Images..."
aws s3 sync "${CACHE_BASE}/Images/" "s3://${BUCKET_NAME}/images/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --profile "${AWS_PROFILE}" \
    --exclude "*" \
    --include "httpcloud3steamusercontent*" \
    --no-progress

# Upload Models
echo "Uploading Models..."
aws s3 sync "${CACHE_BASE}/Models/" "s3://${BUCKET_NAME}/models/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --profile "${AWS_PROFILE}" \
    --exclude "*" \
    --include "httpcloud3steamusercontent*" \
    --no-progress

# Upload Assetbundles
echo "Uploading Assetbundles..."
aws s3 sync "${CACHE_BASE}/Assetbundles/" "s3://${BUCKET_NAME}/assetbundles/" \
    --endpoint-url "${R2_ENDPOINT}" \
    --profile "${AWS_PROFILE}" \
    --exclude "*" \
    --include "httpcloud3steamusercontent*" \
    --no-progress

echo ""
echo "=== Upload Complete ==="
echo "Verify with: aws s3 ls s3://${BUCKET_NAME}/ --endpoint-url ${R2_ENDPOINT} --profile ${AWS_PROFILE} --recursive --summarize"
