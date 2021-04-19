from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta
import redis
from .models import VideoModel
from apikey.models import ApiKeyModel


logger = get_task_logger(__name__)


def youtube(query, max_results, next_token, api_key, published_after):
    """
    This function creates a youtube api object and gets the data for us
    """

    youtube_object = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                        developerKey=api_key,  cache_discovery=False)

    try:
        response = youtube_object.search().list(q = query, type ='video',
                                order = 'date', part='snippet',
                                publishedAfter = published_after,
                                maxResults = max_results,
                                pageToken = next_token)

        request = response.execute()
        return request

    except HttpError as e:
        print(e)


def saveVideo(videos):
    """
    The data which we got from the API is stored in the VideoModel database
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
                            thumbnail_url= v['snippet']['thumbnails']['default']['url'])
        new_video.save()


@shared_task()
def fetchVideo():
    """
    Task which is run periodically by celery beat scheduler to fetch and save video data
    in the database using API keys present in the ApiKeyModel
    """ 
    
    r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

    
    published_after = datetime.utcnow() - timedelta(minutes=10)

    max_results = 50
    next_token = None

     
    # fetching all API keys from the database
    api_keys = ApiKeyModel.objects.all()

    # if no api keys are present, exit
    if not api_keys.exists():
        logger.error("No API Key present in the database")
        return
    
    # check if the apikey_id is present in redis
    if r.exists('apikey_id') == 0:
        apikey_id = api_keys.first().id
        r.set('apikey_id', apikey_id)

    #get apikey_id from redis 

    a = int(r.get('apikey_id'))
    current_api_key = ApiKeyModel.objects.get(id = a).key

    videos = VideoModel.objects.all().order_by('-published_date')

    # if there are videos in database,
    # then service will fetch videos after that time

    if videos.exists():
        published_after = videos.first().published_date.replace(tzinfo=None)

    published_after_str = published_after.isoformat("T") + "Z"
    
    # Iterate through all the pages of the Youtube API and save videos in db
    while True:
        try:
            results = youtube(
                query =  'football',
                max_results= max_results,
                next_token= next_token,
                api_key =current_api_key,
                published_after= published_after_str,
            )
            
            if len(results['items']) == 0:
                return

            # see if we have nextToken
            if 'nextPageToken' in results:
                next_token = results['nextPageToken']
                print(next_token)
                
            else:
                break

            # save the results into the database
            saveVideo(results)

        #handling the error when API quota is exceeded 
        except HttpError as e:
            if e.code == 403:
                logger.warning('The API key has exceeded its quota, try next APIKey')

                #get apikey_id from redis
                a = int(r.get('apikey_id'))
                lastid = api_keys.last().id

                #check if id number is valid
                if a<lastid:
                    a= a+1
                    current_api_key = ApiKeyModel.objects.get(id = a).key
                    #recursion here
                    fetchVideo()    
                    
                
                else:
                    logger.warning('No more API keys in the database, please add some')

            logger.error('Unknown error occured')
        
        
        
        
        
        
