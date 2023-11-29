
from django.shortcuts import render,redirect
from .models import CustomUser,ProfileUser
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
#

#here session
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
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


#razorpay import begins


from django.http import JsonResponse

from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt


#razorpay import ends


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

    # You can fetch additional information from the user's profile if needed
    # For example: profile = user.profileuser

    context = {
        'user': user,
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

def checkout(request):
    # Assuming you have a one-to-one relationship between CustomUser and Cart1
    try:
        cart = request.user.cart1
        cart_items = CartItem1.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        cart_count = get_cart_count(request)

        context = {
            'cart_count': cart_count,
            'cart_items': cart_items,
            'total_amount': total_amount,
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
# def Brideindex(request):
#     return render(request, 'Brideindex.html')

# def Brideabout(request):
#     return render(request, 'Brideabout.html')

# def Bridecontact(request):
#     return render(request, 'Bridecontact.html')

def bride_index_view(request):
    return render(request, 'Brideindex.html')

def bride_about_view(request):
    return render(request, 'Brideabout.html')

def bride_contact_view(request):
    return render(request, 'Bridecontact.html')

