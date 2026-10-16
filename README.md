# SMASH 대학교

![SMASH 대학교](site/og.png)

우리 학교 캠퍼스를 3D로 부수는 게임을 모아 둔 첫 화면입니다. 학교와 관계없는 비공식 팬 게임입니다.

**바로 가기:** https://hong-iron.github.io/SMASH/

## 학교

| 학교 | 게임 | 소스 |
|---|---|---|
| 건국대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-KONKUK/ | [SMASH-KONKUK](https://github.com/Hong-Iron/SMASH-KONKUK) |
| 경희대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-KHU/ | [SMASH-KHU](https://github.com/Hong-Iron/SMASH-KHU) |
| 고려대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-KU/ | [SMASH-KU](https://github.com/Hong-Iron/SMASH-KU) |
| 국민대학교 | https://hong-iron.github.io/SMASH-KMU/ | [SMASH-KMU](https://github.com/Hong-Iron/SMASH-KMU) |
| 동국대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-DGU/ | [SMASH-DGU](https://github.com/Hong-Iron/SMASH-DGU) |
| 서강대학교 | https://hong-iron.github.io/SMASH-SOGANG/ | [SMASH-SOGANG](https://github.com/Hong-Iron/SMASH-SOGANG) |
| 서울대학교 관악캠퍼스 | https://hong-iron.github.io/SMASH-SNU/ | [SMASH-SNU](https://github.com/Hong-Iron/SMASH-SNU) |
| 서울시립대학교 | https://hong-iron.github.io/SMASH-UOS/ | [SMASH-UOS](https://github.com/Hong-Iron/SMASH-UOS) |
| 성균관대학교 인문사회과학캠퍼스 | https://hong-iron.github.io/SMASH-SKKU/ | [SMASH-SKKU](https://github.com/Hong-Iron/SMASH-SKKU) |
| 세종대학교 | https://hong-iron.github.io/SMASH-SEJONG/ | [SMASH-SEJONG](https://github.com/Hong-Iron/SMASH-SEJONG) |
| 숙명여자대학교 | https://hong-iron.github.io/SMASH-SOOKMYUNG/ | [SMASH-SOOKMYUNG](https://github.com/Hong-Iron/SMASH-SOOKMYUNG) |
| 숭실대학교 캠퍼스 | https://hong-iron.github.io/SMASH-SSU/ | [SMASH-SSU](https://github.com/Hong-Iron/SMASH-SSU) |
| 연세대학교 신촌캠퍼스 | https://hong-iron.github.io/SMASH-YONSEI/ | [SMASH-YONSEI](https://github.com/Hong-Iron/SMASH-YONSEI) |
| 이화여자대학교 | https://hong-iron.github.io/SMASH-EWHA/ | [SMASH-EWHA](https://github.com/Hong-Iron/SMASH-EWHA) |
| 인하대학교 | https://hong-iron.github.io/SMASH-INHA/ | [SMASH-INHA](https://github.com/Hong-Iron/SMASH-INHA) |
| 중앙대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-CAU/ | [SMASH-CAU](https://github.com/Hong-Iron/SMASH-CAU) |
| 한국외국어대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-HUFS/ | [SMASH-HUFS](https://github.com/Hong-Iron/SMASH-HUFS) |
| 한양대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-HYU/ | [SMASH-HYU](https://github.com/Hong-Iron/SMASH-HYU) |
| 홍익대학교 서울캠퍼스 | https://hong-iron.github.io/SMASH-HONGIK/ | [SMASH-HONGIK](https://github.com/Hong-Iron/SMASH-HONGIK) |

부수고 싶은 학교가 있으면 [이슈](https://github.com/Hong-Iron/SMASH/issues/new)로 알려 주세요.

## 학교 추가하는 법

1. 학교 게임 레포를 하나 만듭니다(기존 레포를 복사해 `config.json`과 데이터만 바꿈).
2. 이 레포의 `schools.json`에 학교를 한 줄 넣습니다(`code`, `name`, `campus`, `nameEn`, `region`, `url`, `buildings`, `added`). 허브의 검색은 이름·지역·영문·초성으로, 정렬은 이름순·최근 추가순·건물 많은 순으로 됩니다.
3. `python3 tools/build.py`로 `site/index.html`을 다시 만들고 `main`에 push하면 GitHub Pages에 올라갑니다.

## 앱 아이콘

폭탄과 폭발을 그린 아이콘입니다. 원본은 `assets/icon.svg`이고, 크기별 PNG는 `site/icon-1024.png`, `icon-512.png`, `icon-180.png`(홈 화면), `icon-128.png`, `icon-32.png`(브라우저 탭)입니다.

## 개발자 응원하기

- 카카오페이: https://qr.kakaopay.com/FKcOJKyOy1f405462
- Buy Me a Coffee: https://buymeacoffee.com/hongiron

건물·도로 © OpenStreetMap 기여자 (ODbL) · 고도 AWS Terrain Tiles (SRTM 30 m 기반)
