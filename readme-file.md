# 3D Mouse Reveal Effect - Streamlit App

이 Streamlit 애플리케이션은 마우스가 움직이는 주변에만 이미지가 표시되는 3D 패럴랙스 효과를 구현합니다.

## 기능

- 사용자가 자신의 이미지를 업로드할 수 있습니다
- 마우스 커서 주변에만 이미지가 보입니다
- 마우스 움직임에 따라 이미지가 3D 효과로 회전합니다
- 마우스가 영역을 벗어나면 이미지가 완전히 가려집니다

## 설치 방법

1. 필요한 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

2. 애플리케이션 실행:
   ```
   streamlit run app.py
   ```

## 사용 방법

1. 상단의 파일 업로더를 이용해 이미지를 업로드합니다
2. 검은색 영역 위에 마우스를 움직여 이미지의 일부를 확인합니다
3. 마우스를 움직일 때 이미지가 3D 효과로 회전하는 것을 볼 수 있습니다

## 커스터마이징

`app.py` 파일에서 다음 값을 조정하여 효과를 변경할 수 있습니다:

- `revealRadius`: 마우스 주변에 보이는 영역의 크기 (픽셀)
- `maxRotation`: 3D 회전 효과의 최대 각도 (도)

## 주의사항

- 이 애플리케이션은 모던 웹 브라우저에서 가장 잘 작동합니다
- CSS 마스크 및 WebGL 기능을 지원하는 브라우저가 필요합니다
