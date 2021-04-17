from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.error import HttpError

from .models import VideoModel

logger = get_task_logger(__name__)

def youtube(query, max_results, next_token, api_key, published_after):
    """
    This function creates a youtube api object and gets the data for us
    """

    youtube_object = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                        developerKey=api_key)

    try:
        response = youtube_object.search().list(q = query, type ='video',
                                order = 'date', part='snippet',
                                publishedAfter = published_after,
                                maxResults = max_results,
                                pageToken = next_token)

        request = response.execute()
        return request

    except HttpError as e:
        raise e


def saveVideo(videos):
    """
    The data which we got from the API is stored
    """
    for v in videos['items']:

        #first we check if the video already exists in the database
        vid = VideoModel.objects.filter(vid_id=v['id']['videoId'])
        
        #if video exists we go to the next one
        if vid.exists(): 
            continue

        new_video = VideoModel(vid_id = v['id']['videoId'], 
                            title = v['snippet']['title'],
                            desc = v['snippet']['description'],
                            published_date=v['snippet']['publishedAt'],
                            thumbnail_url= v['snippet']['thumbnails'],['default'],['url']
                            )    