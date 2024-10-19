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

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import re
import os
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK, ID3NoHeaderError
import requests

# 설정 파일에서 API 키를 로드하는 함수
def load_settings():
    settings_file = 'setting.json'
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            return settings['client_id'], settings['client_secret']
    except FileNotFoundError:
        print(f"에러: '{settings_file}' 파일이 없습니다. 이 파일을 생성하고 API 키를 입력하세요.\n 형식은 client_id, client_secret 입니다.")
        os.system("pause") 
        raise

# 파일명으로 사용할 수 있도록 플레이리스트 이름을 안전하게 처리하는 함수
def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

# 플레이리스트 링크에서 플레이리스트 ID 추출
def extract_playlist_id(playlist_url):
    if "playlist" in playlist_url:
        return playlist_url.split("/")[-1].split("?")[0]
    else:
        raise ValueError("에러: 올바른 플레이리스트 URL을 입력해주세요.")

# 밀리초를 시:분:초 형식으로 변환하는 함수
def convert_duration(duration_ms):
    total_seconds = duration_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}분 {seconds}초"

# 스포티파이 API의 인증 정보 로드
client_id, client_secret = load_settings()
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# 플레이리스트 정보 가져오기 함수
def get_playlist_info(playlist_url):
    try:
        playlist_id = extract_playlist_id(playlist_url)
        playlist = sp.playlist(playlist_id)

        owner_name = sanitize_filename(playlist['owner']['display_name'])
        playlist_name = sanitize_filename(playlist['name'])
        json_filename = f"{owner_name} - {playlist_name}.json"

        output_dir = os.path.join("output", f"{owner_name} - {playlist_name}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        json_file_path = os.path.join(output_dir, json_filename)

        track_info_list = []
        total_duration_ms = 0

        while True:
            for idx, item in enumerate(playlist['tracks']['items'], start=len(track_info_list) + 1):
                track = item['track']
                track_name = track['name']
                artists = [artist['name'] for artist in track['artists']]
                album_name = track['album']['name']
                track_number = track['track_number']
                release_date = track['album']['release_date'][:4]
                cover_art = track['album']['images'][0]['url'] if track['album']['images'] else None

                track_duration_ms = track['duration_ms']
                total_duration_ms += track_duration_ms

                track_info = {
                    'position': idx,
                    'title': track_name,
                    'artists': artists,
                    'album': album_name,
                    'track_number': track_number,
                    'year': release_date,
                    'duration': convert_duration(track_duration_ms),
                    'cover_art': cover_art
                }
                track_info_list.append(track_info)

            if playlist['tracks']['next']:
                playlist['tracks'] = sp.next(playlist['tracks'])
            else:
                break

        total_duration = convert_duration(total_duration_ms)
        data_to_save = {
            'playlist_name': playlist['name'],
            'owner': playlist['owner']['display_name'],
            'total_duration': total_duration,
            'tracks': track_info_list
        }

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        print(f"플레이리스트 정보가 '{json_file_path}' 파일에 저장되었습니다.")
        return json_file_path

    except ValueError as e:
        print(e)
        os.system("pause") 
    except KeyError as e:
        print(f"에러: '{e}' 키가 없습니다.")
        os.system("pause") 

# 유튜브 검색 후 첫 번째 비디오 다운로드 함수
def download_first_video(search_query, output_dir, track_title):
    video_search = VideosSearch(search_query, limit=1)
    result = video_search.result()

    if result['result']:
        first_video = result['result'][0]
        video_url = first_video['link']

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, f"{sanitize_filename(track_title)}.%(ext)s"),  # title을 파일명으로 설정
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print(f"'{track_title}' 다운로드 완료")
        return os.path.join(output_dir, f"{sanitize_filename(track_title)}.mp3")

    else:
        print("검색 결과가 없습니다.")
        os.system("pause") 
        return None

# MP3 파일에 커버 이미지와 메타데이터 추가 함수
def add_metadata_to_mp3(mp3_file_path, track_info):
    cover_image_url = track_info.get('cover_art')
    cover_image_path = mp3_file_path.replace('.mp3', '_cover.jpg')

    # 커버 이미지 다운로드
    if cover_image_url:
        try:
            response = requests.get(cover_image_url)
            with open(cover_image_path, 'wb') as f:
                f.write(response.content)

            audio = MP3(mp3_file_path, ID3=ID3)
            if not audio.tags:
                audio.add_tags()

            # 커버 이미지 추가
            with open(cover_image_path, 'rb') as img_file:
                audio.tags.add(APIC(
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=img_file.read()
                ))

            # 메타데이터 추가
            audio.tags.add(TIT2(encoding=3, text=track_info['title']))  # 제목
            audio.tags.add(TPE1(encoding=3, text=', '.join(track_info['artists'])))  # 참여 음악가
            audio.tags.add(TALB(encoding=3, text=track_info['album']))  # 앨범명
            audio.tags.add(TDRC(encoding=3, text=track_info['year']))  # 발매 연도
            audio.tags.add(TRCK(encoding=3, text=str(track_info['track_number'])))  # 트랙 번호

            audio.save()
            print(f"메타데이터가 {mp3_file_path}에 성공적으로 추가되었습니다.")

            # 커버 이미지 파일 삭제
            os.remove(cover_image_path)

        except Exception as e:
            print(f"메타데이터 추가 중 오류 발생: {e}")
            os.system("pause") 

# 전체 프로세스를 실행하는 함수
def process_playlist(playlist_url):
    json_file_path = get_playlist_info(playlist_url)

    if json_file_path:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            playlist_data = json.load(f)

        playlist_name = playlist_data['playlist_name']
        owner_name = playlist_data['owner']
        output_dir = os.path.join("output", f"{owner_name} - {playlist_name}")

        for track in playlist_data['tracks']:
            # search_query = f"{track['title']} {', '.join(track['artists'])} - \"MV\""
            search_query = f"{track['title']} {', '.join(track['artists'])}"
            mp3_file_path = download_first_video(search_query, output_dir, track['title'])

            if mp3_file_path:
                add_metadata_to_mp3(mp3_file_path, track)

# 예시로 사용할 플레이리스트 링크
playlist_url = input("저장할 플레이리스트 URL을 입력해 주세요 : ")

# 전체 프로세스 실행
process_playlist(playlist_url)
