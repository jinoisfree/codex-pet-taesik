# 태식이 1.1.0 전체 디자인 보정

## 기준

- 참고 저장소: `https://github.com/jinoisfree/AIpet`
- 입력: 1.0.0 `pet/spritesheet.webp`
- 방식: 기존 아틀라스 전체를 참조한 이미지 편집
- 목표: 자세·소품·셀 배치는 유지하고 선·색·음영·실루엣의 일관성만 개선

## 주요 프롬프트

```text
Refine the attached Taesik spritesheet into a cleaner, more cohesive modern
hand-drawn 2D sticker design while preserving every animation pose and the
exact 8-column by 11-row atlas layout. Keep the exact same chubby calico cat,
cream-white body, dark brown head/back/tail patches, tiny dot eyes, deadpan
mouth, round belly, short limbs, long curved tail, pale blue cushion, dark
phone, silver laptop, glasses and pink pen where already present.

Change visual polish only. Keep pose, props, direction, frame count, row order,
cell occupancy, scale, anchor points, and animation meaning unchanged. Preserve
all 16 look-direction frames. Empty cells must remain fully transparent. No
text, grid, borders, shadows, watermarks, detached marks, stray pixels, extra
characters, or cropped props.
```

## 후처리

`scripts/prepare_redesign.py`로 원본 PNG를 1536×2288 RGBA로 규격화하고, 낮은 알파의 색 오염과 14개 빈 셀을 제거한 뒤 `exact` 무손실 WebP로 저장한다.
