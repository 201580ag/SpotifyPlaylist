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
