
from django.shortcuts import render,redirect
from .models import CustomUser,ProfileUser
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
#

#here session
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
#here sesssion end

# from django.contrib.auth.models import User

# admin adding product
# from .models import Product  # Import your Product model
from django.http import JsonResponse

from .models import Product, Category, Subcategory, Brand , WishlistItem ,Cart1 , CartItem1 ,Order, OrderItem
from django.shortcuts import render, get_object_or_404 , reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from .models import Service
from django.views.generic.base import View


#razorpay import begins


from django.http import JsonResponse

from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt

#razorpay import ends


#order history
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def bill_invoice(request):
    # Fetch the latest order for the logged-in user (or implement your logic)
    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'billinvoice.html', {'order': order})

def seller_orders(request):
    # Fetch products associated with the logged-in seller
    seller_products = Product.objects.filter(seller=request.user)

    # Fetch orders related to the seller's products
    orders = OrderItem.objects.filter(product__in=seller_products).select_related('order__user')

    return render(request, 'seller_orders.html', {'orders': orders})


#chatbot begins
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud import dialogflow
from google.protobuf import struct_pb2 
from google.protobuf import struct_pb2 as struct_pb

import logging

#chatbot ends

#home page
@never_cache
def home(request):
    return render(request, 'home.html')

#userhome page
@never_cache
@login_required(login_url='login')
def home2(request):
    return render(request, 'home2.html')

#about page
def about(request):
    return render(request, 'about.html')

#sellers home page
def seller_template(request):
     return render(request, 'seller_template.html')

#makeup artist template
def MakeupArtistTemplate(request):
     return render(request, 'MakeupArtistTemplate.html')
   
#user registartion page
@never_cache 
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm-password', None)
        
        if username and email and password:
            if CustomUser.objects.filter(email=email, username=username).exists():
                messages.success(request, "Email is already registered.")
            elif password != confirm_password:
                messages.success(request, "Passwords don't match. Enter the correct password.")
            else:
                user = CustomUser(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                
                # Now use the correct model for user profile
                user_profile = ProfileUser(user=user)
                user_profile.save()
                
                return redirect('login')
    
    return render(request, 'registration.html')

#login page
# @never_cache
def login(request):
    #here session start
    if request.user.is_authenticated:
        return redirect(home2)
   #here session end
    if request.method == 'POST':
        username = request.POST["username"]

        password = request.POST["password"]
       

        if username and password:
            user = authenticate(request, username =username , password=password)
           
            if user is not None:
                auth_login(request,user)
            
                if request.user.user_type==CustomUser.CUSTOMER:
              
                    return redirect('home2')
                elif request.user.user_type == CustomUser.SELLER:
                    return redirect('seller_template')
                
                elif request.user.user_type == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('http://127.0.0.1:8000/admin/')
                
            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')
 #here session started

#logout 
#@never_cache
@login_required(login_url='login')
def logout_view(request):
    logout(request)
   # request.session.clear()  
    return redirect('login')
#here session ended

#heresellerregistration view start
def sellerRegistration(request):
    if request.method == 'POST':
       
        shop_name = request.POST.get('shopName', None)
        user_name = request.POST.get('userName', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        phone = request.POST.get('phone', None)
        shop_address = request.POST.get('shopAddress', None)
        tax_id = request.POST.get('taxID', None)

        
        if shop_name and user_name and email and password and confirm_password and phone and shop_address and tax_id:
            if password != confirm_password:
                messages.success(request, "Passwords don't match. Please try again.")
            else:
                
                user = CustomUser.objects.create_user(username=user_name, email=email, password=password, user_type=CustomUser.SELLER)
                user.shop_name = shop_name
                user.phone = phone
                user.shop_address = shop_address
                user.tax_id = tax_id
                user.save()

                messages.success(request, "Seller registration successful. You can now login.")
                return redirect('/login')
        else:
            messages.success(request, "Please fill out all fields")

    return render(request, 'sellerRegistration.html')

#here Makeup Artist Registration view start

from .models import CustomUser, Beautician
from django.views.decorators.csrf import csrf_protect

@csrf_protect

def MakeupArtist(request):
    if request.method == 'POST':
        parlour_name = request.POST.get('shopName')
        user_name = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        phone = request.POST.get('phone')
        parlour_address = request.POST.get('shopAddress')
        tax_id = request.POST.get('taxID')

        if not all([parlour_name, user_name, email, password, confirm_password, phone, parlour_address, tax_id]):
            messages.error(request, "Please fill out all fields.")
        elif password != confirm_password:
            messages.error(request, "Passwords don't match. Please try again.")
        else:
            try:
                # Create a CustomUser
                user = CustomUser.objects.create_user(username=user_name, email=email, password=password, user_type=CustomUser.SELLER)
                user.parlour_name = parlour_name
                user.phone = phone
                user.parlour_address = parlour_address
                user.tax_id = tax_id
                user.save()

                # Create a corresponding Beautician object
                Beautician.objects.create(user=user)

                messages.success(request, "Makeup Artist registration successful. You can now login.")
                return redirect('/login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")

    return render(request, 'MakeupArtist.html')

# def MakeupArtist(request):
     


#     if request.method == 'POST':
       
#         parlour_name = request.POST.get('shopName', None)
#         user_name = request.POST.get('userName', None)
#         email = request.POST.get('email', None)
#         password = request.POST.get('password', None)
#         confirm_password = request.POST.get('confirmPassword', None)
#         phone = request.POST.get('phone', None)
#         parlour_address = request.POST.get('shopAddress', None)
#         tax_id = request.POST.get('taxID', None)

        
#         if parlour_name and user_name and email and password and confirm_password and phone and parlour_address and tax_id:
#             if password != confirm_password:
#                 messages.success(request, "Passwords don't match. Please try again.")
#             else:
                
#                 user = CustomUser.objects.create_user(username=user_name, email=email, password=password, user_type=CustomUser.SELLER)
#                 user.parlour_name = parlour_name
#                 user.phone = phone
#                 user.parlour_address = parlour_address
#                 user.tax_id = tax_id
#                 user.save()

#                 messages.success(request, "Makeup Artist registration successful. You can now login.")
#                 return redirect('/login')
#         else:
#             messages.success(request, "Please fill out all fields")

#         return render(request, 'MakeupArtist.html')
    




# Update your existing product_list view in views.py

from django.db.models import Q

def product_list(request, category_id=None, subcategory_id=None):
    category = None
    subcategory = None
    categories = Category.objects.all()

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if subcategory_id:
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        products = products.filter(subcategory=subcategory)

    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        # Search in product name, brand, and description
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
        'current_subcategory': subcategory,
    })

#adding prodcuts

def add_product(request):
    if request.method == 'POST':
       
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_price')
        product_category = request.POST.get('product_category')
        product_subcategory = request.POST.get('product_subcategory')
        product_brand = request.POST.get('product_brand')
        stock_quantity = request.POST.get('stock_quantity')
        product_image = request.FILES['product_image']

        
        seller_id = request.POST.get('product_seller')
        category, _ = Category.objects.get_or_create(name=product_category)
        subcategory, _ = Subcategory.objects.get_or_create(category=category, name=product_subcategory)
        brand, _ = Brand.objects.get_or_create(name=product_brand)

        
        try:
            seller = CustomUser.objects.get(pk=seller_id)
        except CustomUser.DoesNotExist:
            seller = None  # Handle the case where the seller is not found

        # Create the new product, associating it with the selected seller
        product = Product(
            category=category,
            subcategory=subcategory,
            brand=brand,
            seller=seller,  # Associate the seller with the product
            name=product_name,
            quantity=stock_quantity,
            image=product_image,
            price=product_price,
            description=product_description,
        )
        product.save()

        messages.success(request, "Product added successfully.")
        return redirect('seller_template')

    # Retrieve the list of sellers from your database
    sellers = CustomUser.objects.filter(user_type=4)

    return render(request, 'add_product.html', {'sellers': sellers})



#SELLER VIWEING PRODUCTS VIA SELLER DASHBOARD
@login_required
def seller_products(request):
    
    seller = request.user  # Assuming the seller is a logged-in user
    seller_products = Product.objects.filter(seller=seller)

    return render(request, 'seller_products.html', {'seller_products': seller_products})

def edit_product(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)
    

    if request.method == 'POST':
        print(request.POST) 
        
        category_name = request.POST['product_category']
        subcategory_name = request.POST['product_subcategory']

        
        category = Category.objects.get(name=category_name)
        subcategory = Subcategory.objects.get(name=subcategory_name)

       
        product.product_name = request.POST['product_name']
        product.category = category
        product.subcategory = subcategory
        product.quantity = request.POST['stock_quantity']
        product.description = request.POST['product_description']
        product.price = request.POST['product_price']
        product.status = request.POST['product_status']


        if 'product_image' in request.FILES:
            product.image = request.FILES['product_image']

       
        product.save()

      
        return redirect('seller_products')

  
    return render(request, 'edit_product.html', {'product': product})

#deactivate option for seller
def deactivate_product(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)

    if product.status == 'active':
      
        product.status = 'inactive'
        product.save()

   
    return redirect('seller_products')




#page for displaying subcategory serums

def serums_products(request):
    
    skincare_category = Category.objects.get(name="Skincare")
    serums_subcategory = Subcategory.objects.get(name="Serums", category=skincare_category)
    products = Product.objects.filter(subcategory=serums_subcategory, status="active")
    return render(request, 'serums_products.html', {'products': products})


#page for displaying subcategoery foundations
def foundations_products(request):
  
    face_makeup_category = Category.objects.get(name="Face Makeup")
    foundations_subcategory = Subcategory.objects.get(name="Foundations", category=face_makeup_category)
    products = Product.objects.filter(subcategory=foundations_subcategory, status="active")
    return render(request, 'foundations_products.html', {'products': products})

#viewing product details by clciking prodcut image 

def product_detail(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


#add to wishlist
def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    return redirect('wishlist')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    return HttpResponseRedirect(reverse('wishlist'))

def wishlist(request):
    # Get the wishlist items for the currently logged-in user
    wishlist_items = WishlistItem.objects.filter(user=request.user)

    # Pass the wishlist_items to the template
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')






#user profile
@login_required
def user_profile(request):
    # Retrieve the logged-in user's information
    user = request.user
    product = Product.objects.first() 
    

    # You can fetch additional information from the user's profile if needed
    # For example: profile = user.profileuser

    context = {
        'user': user,
        'product': product,  
        # Add additional context variables as needed
    }

    return render(request, 'user_profile.html', context)




# views.py

# ... (existing code)

def save_profile(request):
    if request.method == 'POST':
        try:
            # Retrieve the user's profile instance or create it if it doesn't exist
            user_profile, created = ProfileUser.objects.get_or_create(user=request.user)

            # Get form data from the request
            phone_number = request.POST.get('phone_number')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            state = request.POST.get('state')

            # Update the user's profile fields
            user_profile.phone_number = phone_number
            user_profile.pincode = pincode
            user_profile.address = address
            user_profile.gender = gender
            user_profile.city = city
            user_profile.state = state

            # Save the changes
            user_profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')  # Redirect to the user profile page
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')

    return render(request, 'user_profile.html')
@login_required
def user_details(request):
    # Assuming you have a template named 'userdetails.html' in the 'templates' folder
    return render(request, 'userdetails.html', {'user': request.user})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')


#admin dashboard

def admin_dashboard(request):
    # Add any logic you need for the dashboard view
    return render(request, 'admintemplate.html')
def user_view(request):
    # Your view logic here
    return render(request, 'user_template.html')




#nandana new cart

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart1.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem1.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('product_list')

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    try:
        # Assuming you haven't specified a related_name
        cart_item = CartItem1.objects.get(cart__user=request.user, product=product)
        
        if cart_item.quantity >= 1:
            cart_item.delete()
    except CartItem1.DoesNotExist:
        pass
    
    return redirect('cart')




@login_required(login_url='login')
def view_cart(request):
    # Get or create the user's cart
    cart, created = Cart1.objects.get_or_create(user=request.user)

    # Retrieve cart items associated with the user's cart
    cart_items = CartItem1.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items,'total_amount': total_amount})


    



@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem1.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem1.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})
def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem1.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count


#nandana razorpay

from django.shortcuts import get_object_or_404
@csrf_exempt
@login_required  # Apply login_required decorator to ensure the user is authenticated


def create_order(request):
    if request.method == 'POST':
        user = request.user
        # Use get_or_create to get the user's cart or create a new one if it doesn't exist
        cart, created= Cart1.objects.get_or_create(user=user)

        cart_items = CartItem1.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            order_data = client.order.create(data=payment_data)
            order.payment_id = order_data['id']
            order.save()

            return JsonResponse({'order_id': order_data['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

# def create_order(request):
#     if request.method == 'POST':
#         user = request.user
#         cart = user.cart
        

#         cart_items = CartItem1.objects.filter(cart=cart)
#         total_amount = sum(item.product.price * item.quantity for item in cart_items)

#         try:
#             order = Order.objects.create(user=user, total_amount=total_amount)
#             for cart_item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     item_total=cart_item.product.price * cart_item.quantity
#                 )

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment_data = {
#                 'amount': int(total_amount * 100),
#                 'currency': 'INR',
#                 'receipt': f'order_{order.id}',
#                 'payment_capture': '1'
#             }
#             orderData = client.order.create(data=payment_data)
#             order.payment_id = orderData['id']
#             order.save()

#             return JsonResponse({'order_id': orderData['id']})
        
#         except Exception as e:
#             print(str(e))
#             return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        


        #nandana new checkout

# def checkout(request):
#     cart_items = CartItem1.objects.filter(cart=request.user.cart)
#     total_amount = sum(item.product.price * item.quantity for item in cart_items)

#     cart_count = get_cart_count(request)
#     # email = request.user.email
#     # full_name = request.user.profile.full_name

#     context = {
#         'cart_count': cart_count,
#         'cart_items': cart_items,
#         'total_amount': total_amount,
#         # 'email':email,
#         # 'full_name': full_name
#     }
#     return render(request, 'checkout.html', context)
def get_cart_count(request):
    if request.user.is_authenticated:
        # Assuming you have a one-to-one relationship between CustomUser and Cart1
        try:
            cart = request.user.cart1
            return CartItem1.objects.filter(cart=cart).count()

        except Cart1.DoesNotExist:
            # If the user does not have a cart, return 0
            return 0

    else:
        # If the user is not authenticated, return 0
        return 0


@login_required(login_url='login')

def checkout(request):
    try:
        cart = request.user.cart1
        cart_items = CartItem1.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Fetch user details from ProfileUser model
        try:
            user_profile = ProfileUser.objects.get(user=request.user)
            user_details = {
                'email': user_profile.email,
                'full_name': user_profile.username,
                'phone_number': user_profile.phone_number,
                'pincode': user_profile.pincode,
                'address': user_profile.address,
                
                'city': user_profile.city,
                'state': user_profile.state,
            }
        except ProfileUser.DoesNotExist:
            # Handle the case where user profile doesn't exist
            user_details = {}

        cart_count = get_cart_count(request)

        context = {
            'cart_count': cart_count,
            'cart_items': cart_items,
            'total_amount': total_amount,
            **user_details,  # Add user details to the context
            
        }
        
        return render(request, 'checkout.html', context)

    except Cart1.DoesNotExist:
        # Handle the case where the user does not have a cart
        # You might want to redirect them to the cart page or handle it in some way
        return HttpResponse("You don't have a cart.")


@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                #user = request.user
                #user.cart.cartitem_set.all().delete()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})
#chatbot

# ... your other views ...

def chatbot(request):
    return render(request, 'chatbot.html')


logger = logging.getLogger(__name__)

def get_dialogflow_response(request):
    message = request.GET.get('message', '')
    logger.info(f"Received message: {message}")

    # Use an appropriate method to generate a session ID dynamically
    # For example, you can use the user's ID or any unique identifier
    session_id = hash(request.user.id) if request.user.is_authenticated else 'default-session-id'

    session_client = dialogflow.SessionsClient(credentials=settings.DIALOGFLOW_CREDENTIALS_PATH)
    session = session_client.session_path(settings.DIALOGFLOW_PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=message, language_code=settings.DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        fulfillment_text = response.query_result.fulfillment_text
        logger.info(f"Dialogflow response: {fulfillment_text}")
        return JsonResponse({'response': fulfillment_text})
    except Exception as e:
        logger.error(f"Error processing Dialogflow response: {str(e)}")
        return JsonResponse({'response': 'Error processing response'})




#bridal makeup booking


def bride_index_view(request):
    return render(request, 'Brideindex.html')

def bride_about_view(request):
    return render(request, 'Brideabout.html')

def bride_contact_view(request):
    return render(request, 'Bridecontact.html')


from django.forms import ModelForm

# # from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Service
# from django.contrib.auth.decorators import login_required

# @login_required
# def add_edit_service(request, service_id=None):
#     # Fetch the existing service if editing
#     if service_id:
#         service = Service.objects.get(id=service_id)
#     else:
#         service = None

#     if request.method == 'POST':
#         makeup_type = request.POST.get('makeup_type')
#         pricing = request.POST.get('pricing')
#         portfolio_images = request.FILES.get('portfolio_images')
#         service_offerings = request.POST.get('service_offerings')

#         # Assuming the user is a beautician
#         beautician = request.user.beautician

#         # Create or update the service
#         if service:
#             service.makeup_type = makeup_type
#             service.pricing = pricing
#             service.portfolio_images = portfolio_images
#             service.service_offerings = service_offerings
#             service.save()
#         else:
#             service = Service.objects.create(
#                 beautician=beautician,
#                 makeup_type=makeup_type,
#                 pricing=pricing,
#                 portfolio_images=portfolio_images,
#                 service_offerings=service_offerings
#             )

#         return redirect('MakeupArtistTemplate')  # Redirect to the beautician's dashboard or a relevant page

#     else:
#         # Handle the GET request and render the form
#         return render(request, 'add_edit_service.html', {'service': service})
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Service, Beautician
from django.contrib.auth.decorators import login_required

@login_required
def add_edit_service(request, service_id=None):
    # Fetch the existing service if editing
    if service_id:
        service = Service.objects.get(id=service_id)
    else:
        service = None

    # Ensure the user has a Beautician object
    try:
        beautician = request.user.beautician
    except Beautician.DoesNotExist:
        # Redirect or handle the case where Beautician object doesn't exist
        return HttpResponse("You are not registered as a beautician.")

    if request.method == 'POST':
        makeup_type = request.POST.get('makeup_type')
        pricing = request.POST.get('pricing')
        portfolio_images = request.FILES.get('portfolio_images')
        service_offerings = request.POST.get('service_offerings')

        # Create or update the service
        if service:
            service.makeup_type = makeup_type
            service.pricing = pricing
            service.portfolio_images = portfolio_images
            service.service_offerings = service_offerings
            service.save()
        else:
            service = Service.objects.create(
                beautician=beautician,
                makeup_type=makeup_type,
                pricing=pricing,
                portfolio_images=portfolio_images,
                service_offerings=service_offerings
            )

        return redirect('MakeupArtistTemplate')  # Redirect to the beautician's dashboard or a relevant page

    else:
        # Handle the GET request and render the form
        return render(request, 'add_edit_service.html', {'service': service})

    
def view_bridal_packages(request):
    services = Service.objects.all()
    return render(request, 'BridalPackage.html', {'services': services})

#hey



class BeauticianCRUD(View):
    template_name = 'beautician_crud.html'

    def get(self, request, *args, **kwargs):
        beautician = request.user.beautician
        services = Service.objects.filter(beautician=beautician)
        context = {'beautician': beautician, 'services': services}
        return render(request, self.template_name, context)
    

    from .models import Service
from django import forms  # Import Django forms module

@login_required
def edit_beautician(request, service_id):
    service = Service.objects.get(id=service_id)

    class ServiceForm(forms.ModelForm):
        class Meta:
            model = Service
            fields = ['makeup_type', 'pricing', 'portfolio_images', 'service_offerings']

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            edited_service = form.save(commit=False)
            edited_service.save()
            return redirect('beautician_crud')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'edit_beautician.html', {'form': form, 'service': service})



from .models import Service

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})


def beautician_profile_form(request):
    if request.method == 'POST':
        # Handle form submission here
        # You can access form data using request.POST.get('field_name')

        # For example, you can print the data for now
        print('Bio:', request.POST.get('bio'))
        print('Phone Number:', request.POST.get('phone_number'))
        # Add similar lines for other fields

        return HttpResponse('Form submitted successfully')  # You can redirect or render another page
    else:
        return render(request, 'beautician_profile_form.html')  # Change the template name as needed
    


    #chatgpt nrs commented which is useful
    # chatapp/views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# @csrf_exempt
# def chatgpt(request):
#     return render(request, 'chatgpt.html')



# def generate_response(request):
#     if request.method == 'POST':

#         user_input = request.POST.get('user_input').lower()
#         if 'beautecart' in user_input:
#             response_data = {'response': "BeauteCart is your go-to destination for high-quality cosmetics! How can I assist you today?"}
#         elif 'products' in user_input:
#             response_data = {'response': "We offer a wide range of beauty products, including makeup, skincare, and more. Browse our collection online!"}
#         elif 'hi' in user_input:
#             response_data = {'response': "hellooo"}
#         elif 'skincare for oily skin' in user_input:
#             response_data = {'response': "For oily skin, we recommend starting with a gentle cleanser, followed by a toner to balance oil production. Consider using a lightweight, oil-free moisturizer and a mattifying sunscreen during the day. "}
#         elif 'makeup brands' in user_input:
#             response_data = {'response': "Beautecart proudly offers a wide range of renowned makeup brands, including but not limited to MAC, Maybelline, NYX, and Urban Decay. Explore our collection to find your favorite brands and discover new ones!"}
#         elif 'bridal makeup booking' in user_input:
#             response_data = {'response': "Booking a bridal makeup session is easy! Log in ,navigate to the 'Bookings' section, and choose your preferred date and time. Select a skilled beautician, and you're all set! "}
#         elif ' return policy' in user_input:
#             response_data = {'response': "We want you to be satisfied with your purchase! Our return policy allows for returns within 30 days of delivery."}
#         elif 'offers' in user_input or 'discounts' in user_input:
#             response_data = {'response': "Check out our latest offers and discounts on premium beauty products. Don't miss out on great deals!"}
#         elif 'order' in user_input or 'delivery' in user_input:
#             response_data = {'response': "For information about your order or delivery, please contact our customer support at support@beautecart.com."}
#         else:
            
#             response_data = {'response': "Sorry Idk"}
#             # response = generate_gpt2_response(user_input)
#             # response_data = {'response': response}

#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

# def generate_gpt2_response(user_input, max_length=100):
#     input_ids = tokenizer.encode(user_input, return_tensors="pt")
#     output = model.generate(input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response


# upload videaos
from .forms import VideoForm

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home2')  # Update with your template name
    else:
        form = VideoForm()
    
    return render(request, 'upload_video.html', {'form': form})

from .models import Video

def display_videos(request):
    videos = Video.objects.all()
    return render(request, 'display_videos.html', {'videos': videos})


from .models import Video

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('video_list')
    return redirect('video_list')  # Redirect to video list page

from .models import Video

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})


def edit_video(request, video_id):
    # Fetch video details based on video_id and pass it to the template
    video = Video.objects.get(id=video_id)
    return render(request, 'edit_video.html', {'video': video})

from django.core.files.base import ContentFile
import os

def save_edits(request, video_id):
    if request.method == 'POST':
        # Fetch the video instance
        video = Video.objects.get(id=video_id)

        # Update title and description
        video.title = request.POST.get('title')
        video.description = request.POST.get('description')

        # Handle video file upload
        if 'video_file' in request.FILES:
            # Delete the existing video file if it exists
            if video.video_file:
                os.remove(video.video_file.path)
            # Get the new video file from the request
            video_file = request.FILES['video_file']
            # Save the new video file
            video.video_file.save(video_file.name, video_file)

        # Save the updated video
        video.save()

        # Redirect back to the videos page
        return redirect('videos')

from django.shortcuts import render, redirect
from .models import Beautician
from .forms import BeauticianProfileForm

def beautician_profile_form(request):
    return render(request, 'beautician_profile_form.html')

# def submit_profile(request):
#     if request.method == 'POST':
        
#         form = BeauticianProfileForm(request.POST)

#         if form.is_valid():
#             # Save the form data to the Beautician model
#             beautician = Beautician(
#                 bio=form.cleaned_data['bio'],
#                 phone_number=form.cleaned_data['phone_number'],
#                 address=form.cleaned_data['address'],
#                 website=form.cleaned_data['website'],
#                 social_media_links=form.cleaned_data['social_media_links'],
#                 experience_years=form.cleaned_data['experience_years'],
#                 certifications=form.cleaned_data['certifications'],
#                 availability=form.cleaned_data['availability']
#             )
#             beautician.save()

#             # Redirect to a success page or any other desired page
#             return redirect('success_page')  # Update with your desired URL name
#     else:
#         form = BeauticianProfileForm()

#     return render(request, 'beautician_profile_form.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Beautician
from django.contrib.auth.decorators import login_required

@login_required
def submit_profile(request):
    if request.method == 'POST':
        # Assuming the user is already logged in
        user = request.user

        # Retrieve or create the Beautician instance for the user
        beautician, created = Beautician.objects.get_or_create(user=user)

        # Update the Beautician instance with the form data
        beautician.bio = request.POST.get('bio', '')
        beautician.phone_number = request.POST.get('phone_number', '')
        beautician.address = request.POST.get('address', '')
        beautician.website = request.POST.get('website', '')
        beautician.social_media_links = request.POST.get('social_media_links', '')
        beautician.experience_years = request.POST.get('experience_years', '')
        beautician.certifications = request.POST.get('certifications', '')
        beautician.availability = request.POST.get('availability', '')

        # Save the updated Beautician instance
        beautician.save()

        return redirect('success_page')  # Redirect to a success page

    return render(request, 'beautician_profile_form.html')  # Adjust the template name as needed


def success_page(request):
    return render(request, 'success_page.html')



from .models import Beautician

def beautician_list(request):
    beauticians = Beautician.objects.all()
    return render(request, 'beautician_list.html', {'beauticians': beauticians})


from .models import Beautician

def beautician_profile(request):
    # Retrieve the logged-in beautician's profile
    beautician = Beautician.objects.get(user=request.user)

    return render(request, 'beautician_profile.html', {'beautician': beautician})

def blog_view(request):
    return render(request, 'blog.html')

def nandanablog(request):
    return render(request, 'nandanablog.html')



from .models import Beautician, Service

def beautician_services(request, beautician_id):
    beautician = get_object_or_404(Beautician, id=beautician_id)
    beautician_services = Service.objects.filter(beautician=beautician)

    context = {
        'beautician_services': beautician_services,
    }

    return render(request, 'beautician_services.html', context)


def naveen_view(request):
    return render(request, 'naveen.html')

from django.http import JsonResponse
from .models import MakeupType

def get_makeup_types(request):
    makeup_types = MakeupType.objects.all()
    data = [{'id': type.id, 'category': type.category} for type in makeup_types]
    return JsonResponse(data, safe=False)

from .models import MakeupType

def your_view_name(request):
    makeup_types = MakeupType.objects.all()
    return render(request, 'naveen.html', {'makeup_types': makeup_types})


#booking starts
# views.py
from django.shortcuts import render, redirect
from .models import Service, Booking
from .forms import BookingForm

def book_service(request, service_id):
    service = Service.objects.get(pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.beautician = service.beautician
            booking.service = service
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)  # Pass booking_id to confirmation page
    else:
        form = BookingForm()

    return render(request, 'book_service.html', {'form': form, 'service': service})

def booking_confirmation(request, booking_id):
    # Retrieve the booking using the provided booking_id
    booking = Booking.objects.get(pk=booking_id)

    # Your existing code to handle booking confirmation
    # ...

    return render(request, 'booking_confirmation.html', {'booking': booking})
# views.py
from django.shortcuts import render

def book_checkout(request):
    # Add any logic to fetch details for checkout if needed
    total_amount = 1000  # Replace with your actual total amount
    return render(request, 'book_checkout.html', {'total_amount': total_amount})

# views.py

# from .models import CustomizeBooking
# from .forms import CustomizeBookingForm

# def customise_booking(request):
#     if request.method == 'POST':
#         form = CustomizeBookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Add a success message
#             messages.success(request, 'Requested Successfully')
#             return redirect('home2')  # Redirect to the desired page
#     else:
#         form = CustomizeBookingForm()

#     return render(request, 'customise_booking.html', {'form': form})


from .models import CustomizeBooking
from .forms import CustomizeBookingForm

from .models import CustomizeBooking
from .forms import CustomizeBookingForm

def customise_booking(request,beautician_id):
    if request.method == 'POST':
        form = CustomizeBookingForm(request.POST)
        if form.is_valid():
            # Check if the logged-in user has a beautician profile
            beautician, created = CustomUser.objects.get_or_create(id=beautician_id)

            customize_booking = form.save(commit=False)
            customize_booking.beautician = beautician
            customize_booking.save()

            # Add a success message
            messages.success(request, 'Requested Successfully')
            return redirect('home2')  # Redirect to the desired page
    else:
        form = CustomizeBookingForm()

    return render(request, 'customise_booking.html', {'form': form})
#appointments

# views.py
# BeauteCartApp/views.py


# def appointments(request):
#     # Your logic to retrieve appointments
#     return render(request, 'appointments.html')


# views.py
from django.shortcuts import get_object_or_404

def beautician_appointments(request, beautician_id):
    beautician_appointments = CustomizeBooking.objects.filter(beautician_id=beautician_id)
    
    context = {
        'beautician_appointments': beautician_appointments,
    }
    
    return render(request, 'appointments.html', context)
   

   #customer viewing his booking details
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomizeBooking

@login_required
def my_bookings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Print debug information
    print(f"User Username: {request.user.username}")
    
    # Fetch and print customer bookings
    customer_bookings = CustomizeBooking.objects.filter(name= request.user.username)
    print(f"Customer Bookings: {customer_bookings}")

    context = {
        'customer_bookings': customer_bookings,
    }

    return render(request, 'mybookings.html', context)



#nandananaveen

# views.py

# from django.shortcuts import redirect, get_object_or_404
# from .models import CustomizeBooking

# def handle_appointment(request, booking_id):
#     booking = get_object_or_404(CustomizeBooking, id=booking_id)

#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'accept':
#             # Implement your logic for accepting the appointment here
#             booking.status = 'Approved'
#             # You may want to implement additional logic for payment here

#         elif action == 'reject':
#             # Implement your logic for rejecting the appointment here
#             booking.status = 'Rejected'

#         booking.save()

#     # Redirect back to the appointments page
#     return redirect('beautician_appointments', beautician_id=booking.beautician.id)



# views.py
from django.core.mail import send_mail
from .models import CustomizeBooking
from django.shortcuts import redirect, get_object_or_404

def send_approval_email(customer_email, status):
    subject = f'Your Request Status - {status}'
    message = f'Your request for services has been {status.lower()}.'
    message += f'For more details contact me on 99946095781'
   
    from_email = 'nandanars2024b@mca.ajce.in'
    recipient_list = [customer_email]

    send_mail(subject, message, from_email, recipient_list)

def handle_appointment(request, booking_id):
    booking = get_object_or_404(CustomizeBooking, id=booking_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'accept':
            booking.status = 'Approved'
            send_approval_email(booking.email, 'Approved')
            # Additional logic for payment here if needed

        elif action == 'reject':
            booking.status = 'Rejected'
            send_approval_email(booking.email, 'Rejected')

        booking.save()

    return redirect('beautician_appointments', beautician_id=booking.beautician_id)
    

# def handle_appointment(request, booking_id):
#     booking = get_object_or_404(CustomizeBooking, id=booking_id)

#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'accept':
#             booking.status = 'Approved'
#             send_approval_email(booking.email, 'Approved')

#             # Additional logic for payment here
#             client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#             order_amount = int(booking.total_price * 100)  # Example amount
#             data = {
#                 "amount": order_amount,
#                 "currency": "INR",
#                 "receipt": f"order_rcptid_{booking.id}"  # Use booking ID to generate a unique receipt ID
#             }

#             payment = client.order.create(data=data)

#             new_payment = BookingPayment(
#                 order=booking,
#                 razor_pay_order_id=payment['id'],
#                 amount=booking.total_price,
#                 is_paid=False,
#                 customer=request.user
#             )
#             new_payment.save()

#         elif action == 'reject':
#             booking.status = 'Rejected'
#             send_approval_email(booking.email, 'Rejected')

#         booking.save()

#     return redirect('beautician_appointments', beautician_id=booking.beautician_id)

# views.py


from django.shortcuts import render, get_object_or_404
from .models import CustomizeBooking, BookingPayment

def payment_info(request, booking_id):
    try:
        booking = get_object_or_404(CustomizeBooking, id=booking_id)
        payment = BookingPayment.objects.filter(order=booking).first()
        if not payment:
            print(f"No payment found for booking {booking_id}.")
    except CustomizeBooking.DoesNotExist:
        print(f"Booking with ID {booking_id} does not exist.")
        booking = None
        payment = None

    return render(request, 'payment_info.html', {'booking': booking, 'payment': payment, 'rzp_api_key': 'your_razorpay_api_key'})

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BookingPayment

@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = data.get('event')
        payment_id = data.get('payload', {}).get('payment', {}).get('entity', {}).get('id')

        if event == 'payment.authorized':
            # Payment authorized, update BookingPayment model
            try:
                payment = BookingPayment.objects.get(razor_pay_order_id=payment_id)
                payment.is_paid = True
                payment.save()
            except BookingPayment.DoesNotExist:
                print(f"Payment with ID {payment_id} not found.")

        return HttpResponse(status=200)
    return HttpResponse(status=400)







def payment_success(request):
    return render(request, 'payment_success.html')

#nandana blog
from .forms import PostForm

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MakeupArtistTemplate')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


from .models import Post

def post(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})

def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
    return redirect('post')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})


#nnadana new subcategory
# views.py

from django.http import JsonResponse

def get_subcategories(request, category_id):
    category = Category.objects.get(id=category_id)
    subcategories = category.subcategory_set.all()
    subcategory_html = ''
    for subcategory in subcategories:
        subcategory_html += f'<a href="#">{subcategory.name}</a>'
    return JsonResponse({'html': subcategory_html})


#customer review
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user

    # Check if the user has purchased the product
    has_purchased = check_user_has_purchased_product(user, product)

    if has_purchased:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.customer = user
                review.save()
                return redirect('product_detail', product_id=product_id)
        else:
            form = ReviewForm()
        return render(request, 'add_review.html', {'form': form})
    else:
        # Handle the case where the user has not purchased the product
        return render(request, 'home2.html', {'product': product})

def check_user_has_purchased_product(user, product):
    # Implement your logic to check if the user has purchased the product
    # For example, you can check if there is a purchase record for the user and product
    # Return True if the user has purchased the product, otherwise return False
    # Example:
    return user.purchase_set.filter(product=product).exists()

from .models import OrderItem

def check_user_has_purchased_product(user, product):
    # Check if there is any order item associated with the user and product
    return OrderItem.objects.filter(order__user=user, product=product).exists()
from django.shortcuts import render
from .models import Review

def review_list(request):
    # Fetch all reviews from the database
    reviews = Review.objects.all()
    return render(request, 'review.html', {'reviews': reviews})


#order cancellation

    

    # views.py
from django.contrib.auth.decorators import login_required

@login_required
def order_status(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_status.html', {'orders': orders})


# views.py

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

def cancel_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        if order.payment_status:
            order.cancelled = True
            order.save()
            messages.success(request, 'Order cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel unpaid orders.')
    return redirect('order_status')  # Redirect to the order status page



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

def order_cancellation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        # Assuming you handle the cancellation logic here
        order.cancel()  # You may have a method like cancel() in your Order model
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})



from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Order

def order_status(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_status.html', {'orders': orders})


#tryon
import requests
from django.shortcuts import render
from django.http import JsonResponse

def try_on(request):
    if request.method == 'POST' and 'image_data' in request.POST:
        image_data = request.POST['image_data']
        feature = request.POST.get('feature', 'lips')  # Default feature is 'lips', you can change it as needed

        try:
            response = requests.post('http://127.0.0.1:8000/api/apply-makeup/', data={'image_data': image_data, 'feature': feature})
            if response.status_code == 200:
                modified_image_data = response.content
                return JsonResponse({'modified_image_data': modified_image_data})
            else:
                return JsonResponse({'error': 'Failed to process image'}, status=500)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'tryon.html')
