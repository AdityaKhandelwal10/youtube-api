# Assignment- YOUTUBE API

An Application using the Youtube v3 API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Features:
1. Fetches new videos for a specific query(football) in the background in periodic time interval(30 secs in this case) using Celery and Redis.
2. An API endpoint with GET and POST request to return latest videos in descending order of their publishing date in a paginated response. 
     * GET request fetches all the videos
     * POST request sends a query which videos can be filtered( eg - Messi) against their Title and Description.
3. Support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
4. A dashboard to view the stored videos and API keys with filters. 

## Description:
  * This Django application is used to fetch videos in the background, it accomplishes that by using __Celery__ to perfrom Async task in the background with __Redis__ as a message broker. Celery uses a seperate server, we need to run the workers and beat-scheduler in the background for the asyn process to happen periodically. 
  * The data stored in the database is retrieved using a django rest framework __APIView__ (instead of a generic ListView of DRF) because it gives more flexibilty and helps understand the code and make it optimised later.
  * API keys are to be added using the admin dashboard, to support multiple api keys Redis has been used to manage passing of information. 
  * Pagination has been done using the __Paginator class__ of Django. Although serializers and pagination class can be used to achieve the same result. 
  * Both GET and POST methods are available at `http://127.0.0.1:8000/videos/`
  * Application uses _Q()_ and _icontains_ for filtering.

## Setup :
### Prerequisites:
1. Redis Server - [redis](https://redis.io/download)
2. Python 3 

### Steps :
1. Create a virtual environment using ` python3 -m venv env`
2. Activate virtual enviornmen using ` source env/bin/activate `
3. Clone this repository with command ` git clone https://github.com/AdityaKhandelwal10/youtube-api.git`
4. Change working directory to youtube_api using ` cd youtube_api `
5. Install requirements of the project using command ` pip3 install -r requirements.txt `
6. Run all the migrations using commands `python manage.py makemigrations` and ` python manage.py migrate`
7. __Add API Keys__ :
     * Create a superuser with your credentials by running `python manage.py createsuperuser`
     * Login to the ___Admin dashboard___ with your credentials on the server.
     * Add API keys here at the API Key Table to start using this service. 
8. Now run the background task in celery using the following commands, in different command prompts, in order:     
    1.`celery -A youtube_api worker -l info ` 
    2. ` celery -A youtube_api beat -l info `
        
9. Run the server using the command `python python manage.py runserver`
        

