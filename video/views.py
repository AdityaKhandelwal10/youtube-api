from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from rest_framework.views import APIView
from .models import VideoModel

class YoutubeData(APIView):
    
    def get(self, request, format = None):
        video_data = VideoModel.objects.all()
        if video_data:
            page_size = 5
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
            if page.has_previous():
                prevpage = page.previous_page_number()
            else:
                prevpage = None

            # return JsonResponse({"Next Page": nextpage,"Previous Page": prevpage,"data" : data})
            return Response({"Next Page": nextpage,"Previous Page": prevpage,"data" : data})
        else :
            return Response({"Empty" : "No results found"})