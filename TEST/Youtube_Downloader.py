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

from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

def download_first_video(search_query):
    # 검색어로 유튜브 검색 실행
    video_search = VideosSearch(search_query, limit=1)
    result = video_search.result()

    if result['result']:
        # 첫 번째 검색 결과 가져오기
        first_video = result['result'][0]
        video_url = first_video['link']
        
        print(f"Downloading: {first_video['title']}")
        print(f"Video URL: {video_url}")

        # yt-dlp를 이용한 다운로드 설정
        ydl_opts = {
            'format': 'bestaudio/best',  # 오디오만 다운로드
            'outtmpl': '%(title)s.%(ext)s',  # 파일 저장 형식
            'ffmpeg_location': './ffmpeg.exe',  # FFmpeg 경로 설정
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # MP3 파일 최고 품질 설정
            }],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print("Download completed.")
    else:
        print("No results found.")

# 검색어 입력
download_first_video('비밀번호 486 Younha -"mv" +"가사"')
