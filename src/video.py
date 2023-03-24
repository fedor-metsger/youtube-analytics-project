
import json
import os
import isodate
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""

    @staticmethod
    def get_service():
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __init__(self, id):
        self.id = id
        self.url = f"https://youtu.be/{id}"

        self.api_key: str = os.getenv('YT_API_KEY')
        youtube = Video.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=id).execute()
        # printj(video_response)
        self.title = video_response['items'][0]['snippet']['title']
        self.iso_8601_duration = video_response['items'][0]['contentDetails']['duration']
        self.duration = isodate.parse_duration(self.iso_8601_duration)
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(video_response['items'][0]['statistics']['likeCount'])
        comment_count: int = int(video_response['items'][0]['statistics']['commentCount'])

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        """Возвращает строковое представление класса"""
        return f'class Video(API_KEY:"{self.api_key}", CHANNEL_ID:"{self.__channel_id}")'
class PLVideo(Video):
    """Класс для ютуб-видео"""
    def __init__(self, id, playlist_id):
        super().__init__(id)

        self.playlist_id = playlist_id