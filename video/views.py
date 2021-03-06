from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from .models import VideoModel

class YoutubeData(APIView):
    """
    An API View for fetching Videos for the Video model.
    Contains a get and a post request to return data.
    """
    
    def get(self, request, format = None):
        """
        A get request which returns all the videos in the database 
        in descending order of published date, in a paginated response.
        """
        video_data = VideoModel.objects.all()

        if video_data:
            page_size = 50
            page_number = self.request.GET.get('page', 1)
            paginator = Paginator(video_data.values() , page_size)
            page_obj = paginator.get_page(page_number)

            try:
                page = paginator.page(page_number)
            except EmptyPage:
                return JsonResponse({"details": "Page out of range"}, status=404)

            data = list(page_obj)
            if page.has_next():
                nextpage = page.next_page_number()
            else:
                nextpage = None
            if page.has_previous():
                prevpage = page.previous_page_number()
            else:
                prevpage = None

            return Response({"Next Page": nextpage,"Previous Page": prevpage,"data" : data})
        else :
            return Response({"Empty" : "No results found"})

    def post(self, request):
        """
        A post request with query to search for the same in the 
        database and return a paginaed response.

        """
        try:
            search_parameter = request.data.get('search')

            videos = VideoModel.objects.filter(Q(title__icontains = search_parameter) or Q(desc__icontains = search_parameter))

            if videos:
                page_size = 5
                page_number = self.request.GET.get('page', 1)
                paginator = Paginator(videos.values() , page_size)
                page_obj = paginator.get_page(page_number)


                try:
                    page = paginator.page(page_number)
                except EmptyPage:
                    return JsonResponse({"details": "Page out of range"}, status=404)

                data = list(page_obj)

                if page.has_next():
                    nextpage = page.next_page_number()
                else:
                    nextpage = None
                if page.has_previous():
                    prevpage = page.previous_page_number()
                else:
                    prevpage = None

                        # return JsonResponse({"Next Page": nextpage,"Previous Page": prevpage,"data" : data})
                return Response({"Next Page": nextpage,"Previous Page": prevpage,"data" : data})
                
            else :
                return Response({"Empty" : "No results found"})

        except  Exception as e:
            return Response({'Error' : str(e)})