from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SiteUser, Address, UserPaymentMethod,LikedProduct
from Products.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ShoppingCart.models import ShoppingCart
from ProductsItem.models import ProductItem
import logging
import requests
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import  IsAdminUser,IsAuthenticated
import json
import logging
import random
import string
from django.core.mail import send_mail

logging.basicConfig(level=logging.DEBUG)

from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')

            if response.status_code != 200:
                return JsonResponse({'error': 'Invalid token!'}, status=400)

            user_info = response.json()

            if 'email' in user_info:
                email = user_info['email']
                username = user_info['name']
                avatar = user_info.get('picture')
                phone_number = user_info.get('phone_number', None)
                site_user = SiteUser.objects.filter(user__email=email).first()

                if site_user:
                    site_user.avatar = avatar
                    site_user.phone_number = phone_number
                    site_user.save()

                    refresh = RefreshToken.for_user(site_user.user)

                    liked_products = site_user.liked_products.all()
                    liked_products_list = [{
                        'id': liked_product.product.id,
                    } for liked_product in liked_products]

                    cart = ShoppingCart.objects.filter(site_user=site_user).first()
                    cart_items = []
                    if cart:
                        for item in cart.items.all():
                            product_item = get_object_or_404(ProductItem, id=item.product_id)
                            product = get_object_or_404(Product, id=item.product_id)
                            cart_items.append({
                                'product_id': item.product_id,
                                'product_name': item.product_name,
                                'status': item.status,
                                'qty': item.qty,
                                'notes': item.notes,
                                'image': [image.url for image in product_item.images.all()],
                                'description': product.description,  
                                'sku': product_item.SKU,  
                                'size': product_item.size,  
                                'qty_in_stock': product_item.qty_in_stock ,
                                'price': product_item.price ,
                            })

                    return JsonResponse({
                        'message': 'User exists, token saved!',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'userInfo': {
                            'id': site_user.id,
                            'email': email,
                            'username': username,
                            'avatar': avatar,
                            'phone_number': phone_number,
                            'liked_products': liked_products_list,
                            'cart_items': cart_items
                        }
                    }, status=200)
                else:
                    user = User.objects.create_user(username=username, email=email)
                    user.set_unusable_password()
                    user.save()
                    site_user = SiteUser(user=user, avatar=avatar, phone_number=phone_number ,user_type='customer') 
                    site_user.save()

                    refresh = RefreshToken.for_user(site_user.user)

                    return JsonResponse({
                        'message': 'New user created!',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'userInfo': {
                            'id': site_user.id,
                            'email': email,
                            'username': username,
                            'avatar': avatar,
                            'phone_number': phone_number,
                            'liked_products': [],
                            'cart_items': []
                        }
                    }, status=201)

            return JsonResponse({'error': 'Invalid token!'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON!'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred!'}, status=500)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        User = get_user_model()  
        print(User)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials!'}, status=401)

        if user.check_password(password):
            site_user = SiteUser.objects.get(user=user)

            if site_user.user_type != 'admin':
                return JsonResponse({'error': 'Access denied! Admins only.'}, status=403)

            refresh = RefreshToken.for_user(user)

            liked_products = site_user.liked_products.all()
            liked_products_list = [{
                'id': liked_product.product.id,
            } for liked_product in liked_products]

            return JsonResponse({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'userInfo': {
                    'id': site_user.id,
                    'email': user.email,
                    'username': user.username,
                    'avatar': site_user.avatar if site_user.avatar else None,
                    'user_type': site_user.user_type,
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials!'}, status=401)

    return JsonResponse({'error': 'Invalid request!'}, status=400)



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        User = get_user_model()  
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials!'}, status=401)

        if user.check_password(password):
            site_user = SiteUser.objects.get(user=user)
            if site_user.user_type == 'admin':
                return JsonResponse({'error': 'Admin accounts are not allowed to login here!'}, status=403)

            refresh = RefreshToken.for_user(user)

            liked_products = site_user.liked_products.all()
            liked_products_list = [{
                'id': liked_product.product.id,
            } for liked_product in liked_products]

            cart = ShoppingCart.objects.filter(site_user=site_user).first()
            cart_items = []
            if cart:
                for item in cart.items.all():
                    product_item = get_object_or_404(ProductItem, id=item.product_id)    
                    product = get_object_or_404(Product, id=item.product_id)
                    cart_items.append({
                        'product_id': item.product_id,
                        'product_name': item.product_name,
                        'status': item.status,
                        'qty': item.qty,
                        'notes': item.notes,
                        'image': [image.url for image in product_item.images.all()],
                        'description': product.description,  
                        'sku': product_item.SKU, 
                        'size': product_item.size, 
                        'qty_in_stock': product_item.qty_in_stock,
                        'price': product_item.price,
                    })

            return JsonResponse({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'userInfo': {
                    'id': site_user.id,
                    'email': user.email,
                    'username': user.username,
                    'avatar': site_user.avatar if site_user.avatar else None,
                    'phone_number': site_user.phone_number,
                    'liked_products': liked_products_list,
                    'user_type': site_user.user_type,
                    'cart_items': cart_items  
                }
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials!'}, status=401)

    return JsonResponse({'error': 'Invalid request!'}, status=400)



@csrf_exempt
@permission_classes([IsAuthenticated])

def like_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            user_id = data.get('userId')

            if not user_id or not product_id:
                return JsonResponse({'error': 'User ID and Product ID are required!'}, status=400)

            site_user = get_object_or_404(SiteUser, id=user_id)
            product = get_object_or_404(Product, id=product_id)

            liked_product = LikedProduct.objects.filter(user=site_user, product=product).first()

            if liked_product:
                liked_product.delete()
                return JsonResponse({'message': 'Product unliked successfully!', 'liked': False}, status=200)
            else:
                LikedProduct.objects.create(user=site_user, product=product)
                return JsonResponse({'message': 'Product liked successfully!', 'liked': True}, status=201)

        except SiteUser.DoesNotExist:
            return JsonResponse({'error': 'No SiteUser matches the given query.'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'No Product matches the given query.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def get_liked_products(request, user_id):
    if request.method == 'GET':
        site_user = get_object_or_404(SiteUser, id=user_id)
        liked_products = site_user.liked_products.all()
        
        liked_products_list = [{
            'id': liked_product.product.id,
            'name': liked_product.product.name,
            'description': liked_product.product.description,  
            'price': liked_product.product.price,
            'image': liked_product.product.image.url if liked_product.product.image else None,
        } for liked_product in liked_products]

        return JsonResponse({'liked_products': liked_products_list}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
@csrf_exempt
@permission_classes([IsAdminUser])
def get_users_list(request, user_type=None):
    if request.method == 'GET':
        if user_type:
            users = SiteUser.objects.filter(user_type=user_type)
        else:
            users = SiteUser.objects.exclude(user_type='admin')  

        users_list = []

        for user in users:
            users_list.append({
                'id': user.id,
                'username': user.user.username,  
                'email': user.user.email,  
                'avatar': user.avatar if user.avatar else None,
                'phone_number': user.phone_number,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'user_type': user.user_type,
                'status': user.user.is_active,
            })

        return JsonResponse({'users': users_list}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            site_user = SiteUser.objects.filter(user__email=email).first()
            if not site_user:
                return JsonResponse({'error': 'User not found!'}, status=404)

            verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            site_user.verification_code = verification_code  
            site_user.save()

            send_mail(
                'Password Reset Verification Code',
                f'Your verification code is: {verification_code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Verification code sent successfully!'}, status=200)

        except Exception as e:
            logging.error(f'Error sending verification code: {str(e)}')
            return JsonResponse({'error': 'An unexpected error occurred!'}, status=500)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')

        try:
            site_user = SiteUser.objects.filter(user__email=email).first()
            if not site_user:
                return JsonResponse({'error': 'User not found!'}, status=404)

            if site_user.verification_code == code:
                return JsonResponse({'message': 'Verification code is valid!'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid verification code!'}, status=400)

        except Exception as e:
            logging.error(f'Error verifying code: {str(e)}')
            return JsonResponse({'error': 'An unexpected error occurred!'}, status=500)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        new_password = data.get('new_password')

        try:
            site_user = SiteUser.objects.filter(user__email=email).first()
            if not site_user:
                return JsonResponse({'error': 'User not found!'}, status=404)

            user = site_user.user
            user.set_password(new_password)
            user.save()
            site_user.verification_code = None
            site_user.save()

            return JsonResponse({'message': 'Password has been reset successfully!'}, status=200)

        except Exception as e:
            logging.error(f'Error resetting password: {str(e)}')
            return JsonResponse({'error': 'An unexpected error occurred!'}, status=500)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
def get_user_by_id(request, id, user_type):
    if request.method == 'GET':
        user = get_object_or_404(SiteUser, id=id, user_type=user_type)
        user_data = {
            'id': user.id,
            'username': user.user.username,
            'email': user.user.email,
            'avatar': user.avatar.url if user.avatar else None,
            'phone_number': user.phone_number,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'user_type': user.user_type,
        }
        return JsonResponse(user_data, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def update_staff_user(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            site_user = get_object_or_404(SiteUser, id=id, user_type='staff')
            if 'avatar' in data:
                site_user.avatar = data['avatar']
            if 'phone_number' in data:
                site_user.phone_number = data['phone_number']
            auth_user = site_user.user
            if 'username' in data:
                new_username = data['username']
                if User.objects.exclude(id=auth_user.id).filter(username=new_username).exists():
                    return JsonResponse({'error': 'Username already taken!'}, status=400)
                auth_user.username = new_username
            if 'email' in data:
                auth_user.email = data['email']
            auth_user.save()
            site_user.save()

            return JsonResponse({'message': 'Staff user updated successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def update_customer_user(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            site_user = get_object_or_404(SiteUser, id=id, user_type='customer')
            if 'avatar' in data:
                site_user.avatar = data['avatar']
            if 'phone_number' in data:
                site_user.phone_number = data['phone_number']
            auth_user = site_user.user
            if 'username' in data:
                new_username = data['username']
                if User.objects.exclude(id=auth_user.id).filter(username=new_username).exists():
                    return JsonResponse({'error': 'Username already taken!'}, status=400)
                auth_user.username = new_username
            if 'email' in data:
                auth_user.email = data['email']
            auth_user.save()
            site_user.save()

            return JsonResponse({'message': 'Customer user updated successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    if request.method == 'GET':
        user = get_object_or_404(SiteUser, id=id)
        user_data = {
            'id': user.id,
            'username': user.user.username,
            'email': user.user.email,
            'avatar': user.avatar if user.avatar else None,
            'phone_number': user.phone_number,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }
        addresses = Address.objects.filter(site_user=user)
        user_data['addresses'] = [
            {
                'street': address.street,
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
                'country': address.country,
                'is_primary': address.is_primary,
                'notes': address.notes,
            }
            for address in addresses
        ]
        payment_methods = UserPaymentMethod.objects.filter(user=user)
        user_data['payment_methods'] = [
            {
                'card_number': payment.card_number,
                'expiry_date': payment.expiry_date,
                'cardholder_name': payment.cardholder_name,
                'is_active': payment.is_active,
            }
            for payment in payment_methods
        ]

        return JsonResponse(user_data, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
def create_site_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        email = data.get('email')
        avatar = "https://as2.ftcdn.net/v2/jpg/08/19/66/31/1000_F_819663119_che4sZSrmQv8uQJOzuN9TVQFQNHJlfQ2.webp"
        phone_number = data.get('phone_number')

        try:
            user = User.objects.create_user(username=username, password=password, email=email,last_name=last_name,first_name=first_name )
            site_user = SiteUser(user=user, avatar=avatar, phone_number=phone_number,user_type='customer')
            site_user.save()
            return JsonResponse({'message': 'SiteUser created successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=400)



@csrf_exempt
@permission_classes([IsAuthenticated])
def update_site_user(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            site_user = SiteUser.objects.get(id=id)
            if 'avatar' in data:
                site_user.avatar = data['avatar']
            if 'phone_number' in data:
                site_user.phone_number = data['phone_number']
            auth_user = site_user.user  
            if 'username' in data:
                new_username = data['username']
                if User.objects.exclude(id=auth_user.id).filter(username=new_username).exists():
                    return JsonResponse({'error': 'Username already exists!'}, status=400)
                auth_user.username = new_username
            
            if 'email' in data:
                auth_user.email = data['email']
            if 'first_name' in data:
                auth_user.first_name = data['first_name']
            if 'last_name' in data:
                auth_user.last_name = data['last_name']
            site_user.save()
            auth_user.save()

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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_address(request, user_id, address_id):
    if request.method == 'DELETE':
        address = get_object_or_404(Address, id=address_id, site_user_id=user_id)
        address.delete()
        return JsonResponse({'message': 'Address deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)

@csrf_exempt
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_payment_method(request, user_id, payment_method_id):
    if request.method == 'DELETE':
        payment_method = get_object_or_404(UserPaymentMethod, id=payment_method_id, user_id=user_id)
        payment_method.delete()
        return JsonResponse({'message': 'Payment method deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request!'}, status=400)
