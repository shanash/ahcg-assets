# AHCG Assets - Arkham Horror LCG TTS 모드 이미지 복구 프로젝트

## 프로젝트 개요
아컴호러 카드게임 Super Complete Edition (Workshop ID: 2139398986) 모드의 Steam Cloud 이미지 URL이 전부 403으로 차단됨.
로컬 캐시에서 살린 파일을 Cloudflare R2에 호스팅하고, 모드 JSON의 URL을 교체하는 프로젝트.

## 현재 진행 상황

### 완료
- [x] **Step 1**: GitHub 저장소 생성 + 원본 백업 (https://github.com/shanash/ahcg-assets)
- [x] **Step 2 준비**: 스크립트 4개 작성 + url_mapping.json 생성

### 다음 단계
- [ ] **Step 2**: Cloudflare R2 설정 (사용자가 Cloudflare 대시보드에서 수동 진행)
  - R2 버킷 생성 + Public Access 활성화
  - API 토큰 발급 (S3 호환)
  - 완료 후 필요 정보: Account ID, Bucket name, Access Key, Public URL
- [ ] **Step 3**: 캐시 이미지 R2 업로드 (`scripts/upload_to_r2.sh`)
- [ ] **Step 4**: JSON 내 URL 일괄 교체 (`scripts/replace_urls.py`)
- [ ] **Step 5**: 검증 (`scripts/verify.py`)
- [ ] **Step 6**: 유실 712개 이미지 재제작 (별도 작업)

## 핵심 수치
| 항목 | 값 |
|------|-----|
| 총 Steam Cloud URL | 1,182개 |
| 캐시 보유 (업로드 가능) | 470개 |
| 유실 (재제작 필요) | 712개 |
| 캐시 총 용량 | ~1.67GB |

## TTS 캐시 파일명 규칙
URL → 캐시 파일명 변환: 모든 비영숫자 문자 제거 + 확장자 추가
```
http://cloud-3.steamusercontent.com/ugc/123/ABC/
→ httpcloud3steamusercontentcomugc123ABC.png
```

## 파일 구조
```
ahcg-assets/
├── CLAUDE.md              ← 이 파일
├── README.md
├── WORKFLOW.md            ← 단계별 가이드
├── original_mod.json      ← 수정 전 원본 백업 (9MB)
├── lost_images_report.md  ← 유실 이미지 분석 보고서
├── url_mapping.json       ← Steam URL ↔ R2 URL 매핑 (현재 placeholder)
└── scripts/
    ├── generate_url_mapping.py  ← 매핑 생성
    ├── upload_to_r2.sh          ← R2 업로드 (AWS CLI)
    ├── replace_urls.py          ← JSON URL 교체
    └── verify.py                ← 검증
```

## 관련 TTS 경로
- 원본 JSON: `/Users/shanash/Library/Tabletop Simulator/Mods/Workshop/2139398986.json`
- 캐시 이미지: `/Users/shanash/Library/Tabletop Simulator/Mods/Images/`
- 캐시 모델: `/Users/shanash/Library/Tabletop Simulator/Mods/Models/`
- 캐시 에셋번들: `/Users/shanash/Library/Tabletop Simulator/Mods/Assetbundles/`

## Cloudflare R2 참고
- 무료: 10GB 저장 + 무제한 대역폭 + 월 100만 요청
- S3 호환 API → AWS CLI로 업로드 가능
- Public URL로 직접 핫링크 → TTS에서 바로 로드
