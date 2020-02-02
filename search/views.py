from django.shortcuts import render, redirect
import requests
from django.conf import settings
from isodate import parse_duration


def index(request):
    videos = []
    video_ids = []


    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'



        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 12,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)
        #  /youtube/v3/search?part=snippet&q=learn+python&key=AIzaSyBBxn8-j3uU6scxYIINsnKhkZ96x6abWBc&maxResults=10&type=video
        results = r.json()['items']
        
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')


        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 12
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']






        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    # print(videos)
    context = {
        'videos' : videos
    }

    return render(request, 'search/index.html', context)


