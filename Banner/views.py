from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status as http_status
from .models import Banner
from .serializers import BannerSerializer
import logging

logging.basicConfig(level=logging.DEBUG)
@api_view(['GET'])
@permission_classes([AllowAny])
def banner_list(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data, status=http_status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])  
def create_banner(request):
    serializer = BannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=http_status.HTTP_201_CREATED)
    return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_banner_by_id(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    serializer = BannerSerializer(banner)
    return Response(serializer.data, status=http_status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])  
def update_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    serializer = BannerSerializer(banner, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=http_status.HTTP_200_OK)
    return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])  
def update_banner_status(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    new_status = request.data.get('status')
    if new_status is None:
        return Response({'error': 'Status field is required!'}, status=http_status.HTTP_400_BAD_REQUEST)

    banner.status = new_status
    banner.save()
    return Response({'message': 'Banner status updated successfully!', 'status': banner.status}, status=http_status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])  
def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    banner.delete()  
    return Response({'message': 'Banner deleted successfully!'}, status=http_status.HTTP_204_NO_CONTENT)
