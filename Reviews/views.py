from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from SiteUser.models import SiteUser

@api_view(['GET'])
@permission_classes([AllowAny])
def get_reviews_by_product(request, product_id):
    reviews = Review.objects.filter(product_id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_review(request, product_id):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    site_user = get_object_or_404(SiteUser, user=request.user)

    data = request.data
    data['product'] = product_id 
    serializer = ReviewSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=site_user) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if review.user != request.user:
        return Response({'detail': 'You do not have permission to edit this review.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ReviewSerializer(review, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if review.user != request.user:
        return Response({'detail': 'You do not have permission to delete this review.'}, status=status.HTTP_403_FORBIDDEN)
    review.delete()
    return Response({'detail': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
