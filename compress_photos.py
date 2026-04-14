#!/usr/bin/env python3
"""
NADAUN 포트폴리오 이미지 웹 압축 스크립트
사용법: python3 compress_photos.py <입력폴더> [출력폴더]

- JPG/PNG → WebP 변환 (최고 압축, 웹 최적화)
- 가로 최대 1000px 리사이즈 (세로 비율 유지)
- 목표 용량: 200KB 이하
- 원본 파일 유지, 출력 폴더에 별도 저장
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    os.system("pip3 install Pillow --break-system-packages -q")
    from PIL import Image

# ── 설정 ──────────────────────────────────────────
MAX_WIDTH   = 1000          # px (가로 최대)
WEBP_QUALITY = 82           # 0-100 (82 = 품질/용량 최적 균형)
TARGET_KB   = 200           # 목표 용량 (초과 시 품질 자동 조정)
EXTS        = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff'}
# ─────────────────────────────────────────────────

def compress(src: Path, dst: Path):
    img = Image.open(src).convert('RGB')

    # 가로 1000px 초과 시 리사이즈
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)

    # 먼저 목표 품질로 저장
    quality = WEBP_QUALITY
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, 'WEBP', quality=quality, method=6)

    # 200KB 초과 시 품질 낮춰 재시도
    while dst.stat().st_size > TARGET_KB * 1024 and quality > 55:
        quality -= 5
        img.save(dst, 'WEBP', quality=quality, method=6)

    orig_kb = src.stat().st_size // 1024
    new_kb  = dst.stat().st_size // 1024
    ratio_pct = int((1 - new_kb / max(orig_kb, 1)) * 100)
    print(f"  ✓ {src.name} → {dst.name}  {orig_kb}KB → {new_kb}KB  (-{ratio_pct}%)  [q={quality}]")
    return new_kb


def main():
    if len(sys.argv) < 2:
        print("사용법: python3 compress_photos.py <입력폴더> [출력폴더]")
        print("예시:   python3 compress_photos.py ./원본사진 ./images/portfolio/pepsi-festa")
        sys.exit(1)

    src_dir = Path(sys.argv[1]).expanduser().resolve()
    dst_dir = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else src_dir.parent / (src_dir.name + '_web')

    if not src_dir.exists():
        print(f"❌ 입력 폴더 없음: {src_dir}")
        sys.exit(1)

    files = sorted([f for f in src_dir.rglob('*') if f.suffix.lower() in EXTS])
    if not files:
        print(f"❌ 이미지 파일 없음: {src_dir}")
        sys.exit(1)

    print(f"\n📁 입력: {src_dir}")
    print(f"📁 출력: {dst_dir}")
    print(f"📸 {len(files)}장 처리 중...\n")

    total_orig = total_new = 0
    for i, f in enumerate(files):
        # 출력 경로: 하위폴더 구조 유지
        rel = f.relative_to(src_dir)
        out = dst_dir / rel.with_suffix('.webp')
        try:
            orig_kb = f.stat().st_size // 1024
            new_kb  = compress(f, out)
            total_orig += orig_kb
            total_new  += new_kb
        except Exception as e:
            print(f"  ✗ {f.name}: {e}")

    saved = total_orig - total_new
    pct   = int(saved / max(total_orig, 1) * 100)
    print(f"\n{'─'*50}")
    print(f"✅ 완료: {len(files)}장")
    print(f"   원본 합계: {total_orig:,} KB")
    print(f"   압축 후:   {total_new:,} KB")
    print(f"   절약:      {saved:,} KB  (-{pct}%)")
    print(f"   출력 위치: {dst_dir}")
    print(f"{'─'*50}\n")


if __name__ == '__main__':
    main()
