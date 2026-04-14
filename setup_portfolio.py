#!/usr/bin/env python3
"""
NADAUN Portfolio 사진 셋업 스크립트
- 기존 테스트 사진 → 휴지통
- 1000PX 모음 → images/portfolio/ 복사 + 00.jpg, 01.jpg 순번 리네임
- PROJECTS JS 배열 출력
"""

import os, shutil, sys
from pathlib import Path

SRC_BASE = Path("/Users/james/Desktop/14.1000PX 모음")
DST_BASE = Path("/Volumes/NADAUNPROJECT/_DAVINCI NADAUN PROJECT/_Site/_웹베이직/images/portfolio")
TRASH    = Path.home() / ".Trash"
EXTS     = {'.jpg', '.jpeg', '.png', '.webp'}

# ── 프로젝트 정의 ──────────────────────────────────────────────────────────
# (source_folder, slug, display_name, category, year)
PROJECTS = [
    ('2022_베토벤모음',                   'beethoven',      '베토벤 콘서트',          '콘서트',   '2022'),
    ('20220516_키친밸리',                  'kitchen-valley-1','키친밸리',               '기업행사', '2022'),
    ('20220613_에스테반',                  'estevan',        '에스테반',               '콘서트',   '2022'),
    ('20220618_제이비 스케치',             'jb-sketch',      'JB 스케치',              '기업행사', '2022'),
    ('20220629_헥토사진컷',                'hecto',          '헥토',                   '기업행사', '2022'),
    ('20220706_던킨나주배',                'dunkin-naju',    '던킨 나주배',            '기업행사', '2022'),
    ('20220805_키친밸리',                  'kitchen-valley-2','키친밸리 II',            '기업행사', '2022'),
    ('20220924_와이아웃캠핑페스티벌',      'wyout-camping',  '와이아웃 캠핑 페스티벌', '축제',     '2022'),
    ('20221009_IMM 대표님 가족 모임촬영',  'imm-family',     'IMM 가족 행사',          '기업행사', '2022'),
    ('20221019_리치앤코',                  'rich-n-co',      '리치앤코',               '기업행사', '2022'),
    ('20221109_엔버갤러리',                'enver-gallery',  '엔버갤러리',             '기업행사', '2022'),
    ('20221128_미래DNS',                   'mirae-dns',      '미래DNS',                '기업행사', '2022'),
    ('20221129_고용노동부',                'moel',           '고용노동부',             '기업행사', '2022'),
    ('20221215_유미코아',                  'umicore',        '유미코아',               '기업행사', '2022'),
    ('20221221_IMM 종무식',                'imm-yearend',    'IMM 종무식',             '기업행사', '2022'),
    ('20231004_약속된 플레이 페스티벌',    'play-festival',  '약속된 플레이 페스티벌', '축제',     '2023'),
    ('20231005_로얄살루트',                'royal-salute',   '로얄살루트',             '기업행사', '2023'),
    ('20231008_인테리어',                  'interior',       '인테리어 촬영',          '기업행사', '2023'),
    ('20240922_PEPSI FESTA',               'pepsi-festa',    'PEPSI FESTA',            '축제',     '2024'),
    ('20241026_영실업 베이블레이드',       'beyblade-2024',  '영실업 베이블레이드',    '기업행사', '2024'),
    ('20250213_CMDS',                      'cmds',           'CMDS',                   '기업행사', '2025'),
    ('20250304_이동욱 지면 스케치',        'dong-wook',      '이동욱 지면 스케치',     '기업행사', '2025'),
    ('20250509_바리락스 서울',             'varilux-seoul',  '바리락스 서울',          '기업행사', '2025'),
    ('20250517_영실업 N 페스티벌 또봇',    'n-festival',     '영실업 N 페스티벌',      '축제',     '2025'),
    ('20250521_바리락스 부산',             'varilux-busan',  '바리락스 부산',          '기업행사', '2025'),
    ('20250524_영실업 베이블레이드',       'beyblade-2025',  '영실업 베이블레이드 2025','기업행사','2025'),
    ('20250617_히드라암',                  'hydra-arm',      '히드라암',               '기업행사', '2025'),
    ('20250627_더케이',                    'the-k',          '더케이',                 '기업행사', '2025'),
    ('20250810_베이블레이드',              'beyblade-aug',   '베이블레이드',           '기업행사', '2025'),
    ('20250927_LAON 밴드 뮤직비디오 스케치사진','laon-band','LAON 밴드',              '기업행사', '2025'),
    ('20251102_SYLFIRM X SKECTCH',         'sylfirm',        'SYLFIRM X',              '기업행사', '2025'),
    ('20251102_반얀트리 CAT SKETCH',       'banyan-tree',    '반얀트리 CAT',           '기업행사', '2025'),
    ('20251106_KICT',                      'kict',           'KICT',                   '기업행사', '2025'),
    ('20251222_THENEWGREY',                'thenewgrey',     'THE NEW GREY',           '기업행사', '2025'),
    ('20251228_VENDORS',                   'vendors',        'VENDORS',                '기업행사', '2025'),
    ('20260124_인간지능 컨퍼런스',         'human-intel',    '인간지능 컨퍼런스',      '기업행사', '2026'),
    ('202604 메리츠 드림 승격식',          'meritz-dream',   '메리츠 드림 승격식',     '기업행사', '2026'),
    ('202604 한마음 페스트',               'hanmaeum-fest',  '한마음 페스트',          '축제',     '2026'),
]

def trash(path):
    dst = TRASH / path.name
    # 이름 충돌 방지
    i = 1
    while dst.exists():
        dst = TRASH / f"{path.stem}_{i}{path.suffix}"
        i += 1
    shutil.move(str(path), str(dst))
    print(f"  🗑  {path.name} → Trash")

def get_photos(src_dir):
    files = [f for f in sorted(src_dir.rglob('*')) if f.suffix.lower() in EXTS and f.is_file()]
    return files

# ── 1. 기존 portfolio 폴더 → 휴지통 ──────────────────────────────────────
print("\n━━━ STEP 1: 기존 테스트 사진 → 휴지통 ━━━")
if DST_BASE.exists():
    for item in DST_BASE.iterdir():
        trash(item)
    print(f"  ✓ {DST_BASE} 비워짐")
else:
    DST_BASE.mkdir(parents=True, exist_ok=True)

# ── 2. 새 사진 복사 + 순번 리네임 ────────────────────────────────────────
print("\n━━━ STEP 2: 사진 복사 ━━━")
js_lines = []
total_photos = 0

for src_name, slug, display, category, year in PROJECTS:
    src_dir = SRC_BASE / src_name
    if not src_dir.exists():
        print(f"  ⚠  소스 없음: {src_name}")
        continue

    photos = get_photos(src_dir)
    if not photos:
        print(f"  ⚠  사진 없음: {src_name}")
        continue

    dst_dir = DST_BASE / slug
    dst_dir.mkdir(parents=True, exist_ok=True)

    for i, photo in enumerate(photos):
        dst = dst_dir / f"{str(i).zfill(2)}.jpg"
        shutil.copy2(str(photo), str(dst))

    count = len(photos)
    total_photos += count
    print(f"  ✓  {display} ({count}장) → {slug}/")

    # JS 배열 항목 생성
    js_lines.append(
        f"  {{ id:{len(js_lines)}, name:'{display}', category:'{category}', year:'{year}', "
        f"cover:'images/portfolio/{slug}/00.jpg', photos: imgs('{slug}',{count}) }}"
    )

# ── 3. JS PROJECTS 배열 출력 ─────────────────────────────────────────────
print(f"\n━━━ STEP 3: JS PROJECTS 배열 ({len(js_lines)}개 프로젝트, {total_photos}장) ━━━\n")
print("const PROJECTS = [")
print(",\n".join(js_lines))
print("];")
print(f"\nconst CATS_MAIN = ['all','기업행사','콘서트','축제'];")

print(f"\n✅ 완료! {len(js_lines)}개 프로젝트, 총 {total_photos}장\n")
