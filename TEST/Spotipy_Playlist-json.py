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
import os  # os 모듈을 추가하여 디렉토리 작업

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

# 스포티파이 API의 인증 정보 로드
client_id, client_secret = load_settings()

# 인증 설정
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# 파일명으로 사용할 수 있도록 플레이리스트 이름을 안전하게 처리하는 함수
def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)  # 파일명에 사용할 수 없는 문자는 제거

# 플레이리스트 링크에서 플레이리스트 ID 추출
def extract_playlist_id(playlist_url):
    try:
        if "playlist" in playlist_url:
            return playlist_url.split("/")[-1].split("?")[0]  # URL에서 ID만 추출
        else:
            raise ValueError  # "playlist"가 URL에 없을 경우 예외 발생
    except (IndexError, ValueError):
        print("에러: 올바른 플레이리스트 URL을 입력해주세요. 예시: https://open.spotify.com/playlist/플레이리스트_ID")
        os.system("pause") 
        return None  # 예외 발생 시 None 반환

# 밀리초를 시:분:초 형식으로 변환하는 함수
def convert_duration(duration_ms):
    total_seconds = duration_ms // 1000  # 초로 변환
    hours = total_seconds // 3600  # 시간
    minutes = (total_seconds % 3600) // 60  # 분
    seconds = total_seconds % 60  # 초
    
    if hours > 0:
        return f"{hours}시간 {minutes}분 {seconds}초"  # "X hours Y minutes Z seconds" 형식으로 반환
    else:
        return f"{minutes}분 {seconds}초"  # "Y minutes Z seconds" 형식으로 반환

# 플레이리스트 정보 가져오기 함수
def get_playlist_info(playlist_url):
    try:
        playlist_id = extract_playlist_id(playlist_url)  # 에러가 발생할 수 있는 부분
        playlist = sp.playlist(playlist_id)

        # 플레이리스트 소유자 이름과 제목을 안전하게 파일명으로 변환
        owner_name = sanitize_filename(playlist['owner']['display_name'])
        playlist_name = sanitize_filename(playlist['name'])
        json_filename = f"{owner_name} - {playlist_name}.json"  # 파일명 설정

        # "output" 폴더가 없으면 생성
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        json_file_path = os.path.join(output_dir, json_filename)  # 전체 경로 설정

        # 트랙 정보를 담을 리스트 생성
        track_info_list = []
        total_duration_ms = 0  # 전체 재생 시간을 위한 변수

        # 모든 트랙을 가져오기 위한 페이지네이션
        while True:
            for idx, item in enumerate(playlist['tracks']['items'], start=len(track_info_list) + 1):
                track = item['track']
                track_name = track['name']  # 제목
                artists = [artist['name'] for artist in track['artists']]  # 아티스트 리스트
                album_name = track['album']['name']  # 앨범 제목
                track_number = track['track_number']  # 트랙 번호
                release_date = track['album']['release_date'][:4]  # 연도
                cover_art = track['album']['images'][0]['url'] if track['album']['images'] else None  # 커버 아트 URL

                track_duration_ms = track['duration_ms']
                total_duration_ms += track_duration_ms  # 전체 재생 시간 누적
                
                # 수집된 정보를 딕셔너리로 저장
                track_info = {
                    'position': idx,            # 몇 번째 트랙인지 저장
                    'title': track_name,
                    'artists': artists,        # 아티스트 리스트
                    'album': album_name,       # 앨범 정보 추가
                    'track_number': track_number,  # 트랙 번호 추가
                    'year': release_date,      # 연도 추가
                    'duration': convert_duration(track_duration_ms),  # 재생 시간 변환
                    'cover_art': cover_art     # 커버 아트 추가
                }
                track_info_list.append(track_info)

            # 다음 페이지가 있는지 확인
            if playlist['tracks']['next']:
                playlist['tracks'] = sp.next(playlist['tracks'])  # 다음 페이지 요청
            else:
                break  # 더 이상 페이지가 없으면 종료

        # 전체 재생 시간을 시:분:초 형식으로 변환
        total_duration = convert_duration(total_duration_ms)

        # 저장할 데이터를 구성
        data_to_save = {
            'playlist_name': playlist['name'],
            'owner': playlist['owner']['display_name'],  # 플레이리스트 소유자 추가
            'total_duration': total_duration,  # 전체 재생 시간 추가
            'tracks': track_info_list
        }
        
        # JSON 파일로 저장
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)  # 보기 좋게 정리된 JSON 저장

        print(f"\n'{json_file_path}' 파일에 플레이리스트 정보가 저장되었습니다.")
        print(f"전체 재생 시간: {total_duration}")
        os.system("pause")
    except ValueError as e:
        print(e)  # ValueError 발생 시 메시지 출력
        os.system("pause") 
    except KeyError as e:
        print(f"에러: '{e}' 키가 없습니다. 필요한 데이터가 누락되었습니다.")  # KeyError 발생 시 메시지 출력
        os.system("pause") 

# 예시로 사용할 플레이리스트 링크
playlist_url = input("저장할 플레이리스트 URL을 입력해 주세요 : ")

# 플레이리스트 정보 출력 및 파일 저장
get_playlist_info(playlist_url)
