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

import json
import os

# JSON 파일이 있는 디렉토리
directory = './output'

# 디렉토리 내의 모든 파일을 반복
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # JSON 파일만 처리
        file_path = os.path.join(directory, filename)
        
        # 파일을 열고 JSON 데이터 로드
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                
                # tracks가 있는 경우 처리
                if 'tracks' in data:
                    for track in data['tracks']:
                        # title, artist, duration이 있는지 확인
                        if 'title' in track and 'artist' in track and 'duration' in track:
                            print(f"{track['title']} {track['artist']} {track['duration']}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {filename}")
