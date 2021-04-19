# Assignment- YOUTUBE API

An Application using the Youtube v3 API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Features:
    1. Fetches new videos for a specific query(football) in the background in periodic time interval(30 secs in this case) using Celery and Redis.
    2. An API endpoint with GET and POST request to return latest videos in descending order of their publishing date in a paginated response. 
        -GET request fetches all the videos/
        -POST request sends a query which videos can be filtered( eg - Messi)
        
## Setup :
### Prerequisites:
    1. Redis Server - [redis](https://redis.io/download)
    2. Python 3 

### Steps :
    1. Create a virtual environment using ```python python3 -m venv env ```
    2. Activate virtual enviornmen using ``` source env/bin/activate ```
    3. Clone this repository with command ```bash git clone https://github.com/AdityaKhandelwal10/youtube-api.git```
    4. Change working directory to youtube_api using ``` cd youtube_api ```
    5. Install requirements of the project using command ```python pip3 install -r requirements.txt ```
    6. Run all the migrations using commands ```python python manage.py migrate```
    7. Now run the background task in celery using the following commands, in different command prompts, in order:
        ``` celery -A youtube_api worker -l info ```
        ``` celery -A youtube_api beat -l info ```
    8. Run the server using the command ```python python manage.py runserver ```
        
    
