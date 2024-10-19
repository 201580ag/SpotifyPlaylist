[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2F201580ag%2FSpotifyPlaylist&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
# Spotify 플레이리스트 다운로더

## 버전: 1.0

### 개발자: 201580ag

### 설명
***본 프로젝트는 스포티파이의 공식 api를 이용했지만, 스포티파이와 관련이 없음을 알려드립니다.**  
```이 프로젝트는 Spotify API를 사용하여 플레이리스트 정보를 다운로드하고, YouTube에서 곡을 검색하여 MP3로 변환한 후, MP3 파일에 메타데이터와 커버 이미지를 추가합니다.```  
프로젝트를 만든 이유 : ~~돈은 없는데 노래는 듣고 싶어서...~~  
프로젝트를 만드는데 소요시간 : 5시간 이상  

### 추가예정
`mp3` 확장자이외에 다른 확장자 추가할 예정  
플레이리스트 출력 형식을 `json` 이외에 다른 형식도 추가할 예정  
음질을 다른 음악 스트리밍 사이트보다 더 좋은 음질을 지원 할 예정 `(24비트/48kHz)` 이상  
~~예정이지 언제할지 모름~~

### 리소스
- **GitHub 저장소**: [Spotify 플레이리스트 다운로더](https://github.com/201580ag/SpotifyPlaylist)
- **문제 및 지원**: [GitHub Issues](https://github.com/201580ag/SpotifyPlaylist/issues)

### 사전 준비사항
이 프로젝트를 실행하려면, 다음이 필요합니다:

- Python 3.x
- pip (Python 패키지 설치 관리자)

### 필요한 모듈
다음 Python 패키지를 설치해야 합니다:

1. `spotipy`: Spotify API와 상호작용하기 위해 사용합니다.
2. `yt-dlp`: YouTube에서 비디오를 다운로드하기 위해 사용합니다.
3. `youtube-search-python`: YouTube에서 비디오를 검색하기 위해 사용합니다.
4. `mutagen`: 오디오 메타데이터 처리를 위해 사용합니다.
5. `requests`: HTTP 요청을 수행하기 위해 사용합니다.

다음 명령어를 터미널에 입력하여 필요한 패키지를 설치할 수 있습니다:
```bash
pip install spotipy yt-dlp youtubesearchpython mutagen requests
```

### API 키 설정
1. 프로젝트의 루트 디렉토리에 `setting.json` 파일을 생성합니다.
2. 다음 형식으로 Spotify API 자격 증명을 추가합니다:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

Spotify API 자격 증명은 [Spotify 개발자 대시보드](https://developer.spotify.com/dashboard/applications)에서 애플리케이션을 등록하여 얻을 수 있습니다.

### 사용법
1. 저장소를 로컬 머신에 클론합니다:

```bash
git clone https://github.com/201580ag/SpotifyPlaylist.git
cd SpotifyPlaylist
```

2. 스크립트를 실행합니다:

```bash
python main.py
```

3. 요청 시 다운로드할 Spotify 플레이리스트의 URL을 입력합니다.

### 지원
기여하거나 GitHub 저장소에서 문제를 보고해 주시면 감사하겠습니다. 이메일 [201580ag@gmail.com](mailto:201580ag@gmail.com)으로 연락하실 수도 있습니다.

# **면책 조항(Disclaimer)**
### English
By using this code, the author bears no responsibility for any issues that may arise. The usage of this code is at the user's discretion, and any consequences resulting from it are solely the responsibility of the user. The author assumes no liability for any outcomes or damages incurred from the use of this code. The user absolves the author of any accountability for losses or damages resulting from the usage of this code. By using this code, the user agrees to the following terms and acknowledges being sufficiently warned of any potential risks associated with its use:

1. **Freedom of Use:** The usage of the code is at the user's discretion, and the author imposes no restrictions.
2. **Responsibility:** The user bears sole responsibility for any issues arising from the use of the code.
3. **Consequences of Usage:** The author disclaims all responsibility for any outcomes resulting from the use of the code.
4. **Liability Waiver:** The user holds the author harmless from any losses or damages resulting from the usage of the code.

### Korean
이 코드를 사용함으로써 발생하는 어떤 문제에도, 작성자는 일체의 책임을 지지 않습니다. 코드를 사용하는 것은 사용자의 자유이며, 이로 인해 발생하는 모든 문제에 대한 책임은 오로지 사용자에게 있습니다. 이 코드를 사용함으로써 발생하는 어떠한 결과에도 작성자는 일체의 책임을 지지 않으며, 이 코드를 사용함으로써 발생하는 어떠한 손실이나 손해에 대해 사용자는 작성자를 책임 지지 않습니다. 이 코드를 사용함으로써 사용자는 다음 사항에 동의하며, 이 코드를 사용함으로써 발생할 수 있는 모든 위험에 대해 충분히 경고받았음을 인지해야 합니다:

1. **자유로운 사용**: 코드를 사용하는 것은 사용자의 자유이며, 작성자는 사용 제약을 가하지 않습니다.
2. **책임의 귀속**: 코드 사용으로 발생하는 모든 문제에 대한 책임은 오로지 사용자에게 있습니다.
3. **코드 사용의 결과**: 작성자는 코드 사용으로 발생하는 모든 결과에 대해 일체의 책임을 지지 않습니다.
4. **손실 또는 손해에 대한 면책**: 사용자는 코드 사용으로 발생하는 어떠한 손실이나 손해에 대해 작성자를 책임 지지 않습니다.
