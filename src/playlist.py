
import json
import os
from datetime import timedelta
from googleapiclient.discovery import build
from src.video import Video


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class PlayList:
    """Класс для плэй листа"""

    @staticmethod
    def get_service():
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def get_videos(self):
        """
        Загружает через API информацию о видосах в плэйлисте
        """
        self.videos = []
        for i in self.playlist_videos["items"]:
            self.videos.append(Video(i["contentDetails"]["videoId"]))

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.api_key: str = os.getenv('YT_API_KEY')
        self.__playlist_id = playlist_id
        youtube = PlayList.get_service()
        self.playlist = youtube.playlists().list(id=self.__playlist_id,
                                                 part='snippet,contentDetails'
                                                 ).execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

        self.get_videos()
        return

    def __repr__(self):
        """Возвращает строковое представление класса"""
        return f'class Playlist(API_KEY:"{self.api_key}", PLAYLIST_ID:"{self.__channel_id}")'

    @property
    def total_duration(self) -> timedelta:
        """
        Возвращает суммарную продолжительность всех видео в плэйлисте
        """
        total_delta = timedelta(0)
        for v in self.videos:
            total_delta += v.duration
        return total_delta

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на видео с максимальным количеством лайков
        """
        max_likes, url = None, None
        for v in self.videos:
            if not max_likes or v.like_count > max_likes:
                max_likes = v.like_count
                url = v.url
        return url