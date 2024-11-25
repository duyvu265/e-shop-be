from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Discount
from .serializer import DiscountSerializer
from django.shortcuts import get_object_or_404
import datetime



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  
def list_discounts(request):
    discounts = Discount.objects.all()
    serializer = DiscountSerializer(discounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  
def create_discount(request):
    if request.method == 'POST':
        serializer = DiscountSerializer(data=request.data)
        
        if serializer.is_valid():
            if serializer.validated_data['expiration_date'] <= datetime.date.today():
                return Response({"detail": "Ngày hết hạn phải lớn hơn ngày hiện tại."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  
def update_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    serializer = DiscountSerializer(discount, data=request.data)
    
    if serializer.is_valid():
       
        if serializer.validated_data['expiration_date'] <= datetime.date.today():
            return Response({"detail": "Ngày hết hạn phải lớn hơn ngày hiện tại."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser]) 
def get_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    serializer = DiscountSerializer(discount)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser]) 
def delete_discount(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    discount.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
