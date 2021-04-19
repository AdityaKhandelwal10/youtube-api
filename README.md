# Assignment- YOUTUBE API

An Application using the Youtube v3 API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

...Features:
    1. Fetches new videos for a specific query(football) in the background in periodic time interval(30 secs in this case) using Celery and Redis.
    2. An API endpoint with GET and POST request to return latest videos in descending order of their publishing date in a paginated response. 
    ..* GET request fetches all the videos/
    ..* POST request sends a query which videos can be filtered( eg - Messi)
    
