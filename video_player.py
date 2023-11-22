import requests

class VideoPlayer:
    def __init__(self) -> None:
        
        pass

    @staticmethod
    def is_video(url):
        try:
            response = requests.get(url)
            content_type = response.headers.get('Content-Type', '').lower()
            video_content_types = ['video/mp4', 'video/webm', 'video/quicktime']
            return any(content_type.startswith(video_type) for video_type in video_content_types)
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return False