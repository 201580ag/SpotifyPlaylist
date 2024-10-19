from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
import os

def add_cover_to_mp3(mp3_file_path, cover_image_path):
    try:
        # MP3 파일 열기
        audio = MP3(mp3_file_path)

        # ID3 태그가 없으면 생성
        if not audio.tags:
            audio.add_tags()

        # 커버 이미지 추가
        with open(cover_image_path, 'rb') as img_file:
            img_data = img_file.read()
            audio.tags.add(APIC(mime='image/jpeg',  # 이미지 타입 (jpg)
                                type=3,  # 3은 커버 아트 타입
                                desc='Cover',
                                data=img_data))

        # 변경 사항 저장
        audio.save()
        print(f"Successfully added cover image to {mp3_file_path}")

    except ID3NoHeaderError:
        print("ID3 header is missing, adding it now.")
        audio = MP3(mp3_file_path, ID3=ID3)
        audio.add_tags()
        add_cover_to_mp3(mp3_file_path, cover_image_path)

    except Exception as e:
        print(f"Error: {e}")

# 사용 예제
mp3_file = 'example.mp3'  # MP3 파일 경로
cover_image = 'cover.jpg'  # 커버 이미지 파일 경로
add_cover_to_mp3(mp3_file, cover_image)
