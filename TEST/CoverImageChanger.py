# Project: Spotify Playlist Downloader
# Version: 1.0
# Author: 201580ag
# Description:
#   This project downloads playlist information from Spotify using its API,
#   retrieves the songs from YouTube, converts them to MP3, and adds metadata
#   and cover images to the MP3 files.
#
# Resources:
# - GitHub Repository: https://github.com/201580ag/SpotifyPlaylist
# - Documentation: docs/README.md
# - Issues & Support: https://github.com/201580ag/SpotifyPlaylist/issues
#
# Developed by 201580ag and contributors.
# See LICENSE.txt for copyright and licensing details (MIT License).
#
# Disclaimer:
#   This software is provided "as is", without warranty of any kind, express or implied,
#   including but not limited to the warranties of merchantability, fitness for a
#   particular purpose and noninfringement. In no event shall the authors or copyright
#   holders be liable for any claim, damages or other liability, whether in an action
#   of contract, tort or otherwise, arising from, out of or in connection with the
#   software or the use or other dealings in the software.
#
#   By using this software, you acknowledge that you are solely responsible for any
#   risks or issues that may arise, including but not limited to data loss, copyright
#   infringement, or any other legal matters. The author assumes no responsibility for
#   any misuse or consequences from using this software.
#
# This software is free and open-source. Support the project through contributions
# or by reporting issues on GitHub. Contact: 201580ag@gmail.com

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
