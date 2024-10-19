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
