from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SiteUser, Address, UserPaymentMethod
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

@csrf_exempt
def get_users_list(request):
    if request.method == 'GET':
        users = SiteUser.objects.all()
        users_list = []

        for user in users:
            users_list.append({
                'id': user.id,
                'username': user.user.username,
                'email': user.user.email,
                'avatar': user.avatar.url if user.avatar else None,
                'phone_number': user.phone_number,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
            })

        return JsonResponse({'users': users_list}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def get_user_by_id(request, id):
    if request.method == 'GET':
        user = get_object_or_404(SiteUser, id=id)
        user_data = {
            'id': user.id,
            'username': user.user.username,
            'email': user.user.email,
            'avatar': user.avatar.url if user.avatar else None,
            'phone_number': user.phone_number,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }
        return JsonResponse(user_data, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def create_site_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        avatar = data.get('avatar')
        phone_number = data.get('phone_number')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            site_user = SiteUser(user=user, avatar=avatar, phone_number=phone_number)
            site_user.save()
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'SiteUser created successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def update_site_user(request, id):
    if request.method == 'PUT':
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
    if request.method == 'DELETE':
        try:
            user = SiteUser.objects.get(id=id)
            user.delete()
            return JsonResponse({'message': 'SiteUser deleted successfully!'}, status=200)
        except SiteUser.DoesNotExist:
            return JsonResponse({'error': 'SiteUser not found!'}, status=404)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def get_addresses_list(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(SiteUser, id=user_id)
        addresses = Address.objects.filter(site_user=user)
        addresses_list = [{
            'id': address.id,
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'postal_code': address.postal_code,
            'country': address.country,
        } for address in addresses]

        return JsonResponse({'addresses': addresses_list}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
def update_address(request, user_id, address_id):
    if request.method == 'PUT':
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
    if request.method == 'DELETE':
        address = get_object_or_404(Address, id=address_id, site_user_id=user_id)
        address.delete()
        return JsonResponse({'message': 'Address deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
@csrf_exempt
def get_payment_methods_list(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(SiteUser, id=user_id)
        payment_methods = UserPaymentMethod.objects.filter(user=user)
        payment_methods_list = [{
            'id': payment_method.id,
            'card_number': payment_method.card_number,
            'expiry_date': payment_method.expiry_date,
            'cvv': payment_method.cvv,
            'cardholder_name': payment_method.cardholder_name,
        } for payment_method in payment_methods]

        return JsonResponse({'payment_methods': payment_methods_list}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
@csrf_exempt
def update_payment_method(request, user_id, payment_method_id):
    if request.method == 'PUT':
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
    if request.method == 'DELETE':
        payment_method = get_object_or_404(UserPaymentMethod, id=payment_method_id, user_id=user_id)
        payment_method.delete()
        return JsonResponse({'message': 'Payment method deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
