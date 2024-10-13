from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SiteUser, Address, UserPaymentMethod
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@csrf_exempt
def create_site_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        avatar = data.get('avatar')
        phone_number = data.get('phone_number')

        try:
            user = User.objects.get(id=user_id)
            site_user = SiteUser(user=user, avatar=avatar, phone_number=phone_number)
            site_user.save()
            return JsonResponse({'message': 'SiteUser created successfully!'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found!'}, status=404)
    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def update_site_user(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = SiteUser.objects.get(id=id)
            user.avatar = data.get('avatar', user.avatar)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.save()
            return JsonResponse({'message': 'SiteUser updated successfully!'}, status=200)
        except SiteUser.DoesNotExist:
            return JsonResponse({'error': 'SiteUser not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def delete_site_user(request, id):
    if request.method == 'POST':
        try:
            user = SiteUser.objects.get(id=id)
            user.delete()
            return JsonResponse({'message': 'SiteUser deleted successfully!'}, status=200)
        except SiteUser.DoesNotExist:
            return JsonResponse({'error': 'SiteUser not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def create_address(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_object_or_404(SiteUser, id=user_id)
        address = Address(
            site_user=user,
            street=data.get('street'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country')
        )
        address.save()
        return JsonResponse({'message': 'Address created successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def update_address(request, user_id, address_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = get_object_or_404(Address, id=address_id, site_user_id=user_id)
        address.street = data.get('street', address.street)
        address.city = data.get('city', address.city)
        address.state = data.get('state', address.state)
        address.postal_code = data.get('postal_code', address.postal_code)
        address.country = data.get('country', address.country)
        address.save()
        return JsonResponse({'message': 'Address updated successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def delete_address(request, user_id, address_id):
    if request.method == 'POST':
        address = get_object_or_404(Address, id=address_id, site_user_id=user_id)
        address.delete()
        return JsonResponse({'message': 'Address deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def create_payment_method(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_object_or_404(SiteUser, id=user_id)
        payment_method = UserPaymentMethod(
            user=user,
            card_number=data.get('card_number'),
            expiry_date=data.get('expiry_date'),
            cvv=data.get('cvv'),
            cardholder_name=data.get('cardholder_name')
        )
        payment_method.save()
        return JsonResponse({'message': 'Payment method created successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def update_payment_method(request, user_id, payment_method_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = get_object_or_404(UserPaymentMethod, id=payment_method_id, user_id=user_id)
        payment_method.card_number = data.get('card_number', payment_method.card_number)
        payment_method.expiry_date = data.get('expiry_date', payment_method.expiry_date)
        payment_method.cvv = data.get('cvv', payment_method.cvv)
        payment_method.cardholder_name = data.get('cardholder_name', payment_method.cardholder_name)
        payment_method.save()
        return JsonResponse({'message': 'Payment method updated successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def delete_payment_method(request, user_id, payment_method_id):
    if request.method == 'POST':
        payment_method = get_object_or_404(UserPaymentMethod, id=payment_method_id, user_id=user_id)
        payment_method.delete()
        return JsonResponse({'message': 'Payment method deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
