
from django.shortcuts import render,redirect
from .models import CustomUser,UserProfile
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
# from django.http import JsonResponse
from .models import Product, Category, Subcategory, Brand , WishlistItem
from django.shortcuts import render, get_object_or_404 , reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse



@never_cache
def home(request):
    return render(request, 'home.html')

@never_cache
@login_required(login_url='login')
def home2(request):
    return render(request, 'home2.html')

def about(request):
    return render(request, 'about.html')


def seller_template(request):
     return render(request, 'seller_template.html')

 


    

@never_cache 
def registration(request):
    if request.method == 'POST':
        #name = request.POST.get('name', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        #phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm-password', None)
        # role = CustomUser.CUSTOMER
        if username and email  and password:
            if CustomUser.objects.filter(email=email,username=username).exists():
                messages.success(request,("Email is already registered."))
            
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                user = CustomUser(username=username, email=email)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                # activateEmail(request, user, email)
                return redirect('login')  
            
    return render(request, 'registration.html')

# @never_cache
def login(request):
    #here session start
    if request.user.is_authenticated:
        return redirect(home2)
   #here session end
    if request.method == 'POST':
        username = request.POST["username"]

        password = request.POST["password"]
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('/userhome')
        # else:
        #    messages.success(request,("Invalid credentials."))
        # print(username)  # Print the email for debugging
        # print(password)  # Print the password for debugging

        if username and password:
            user = authenticate(request, username =username , password=password)
           
            if user is not None:
                auth_login(request,user)
            
                if request.user.user_type==CustomUser.CUSTOMER:
                #     #here session start
                #     request.session["username"]=user.username
                # #here session end
                    return redirect('home2')
                elif request.user.user_type == CustomUser.SELLER:
                    return redirect('seller_template')
                
                elif request.user.user_type == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('http://127.0.0.1:8000/admin/')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')
 #here session started
 
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
        # Extract form data
        shop_name = request.POST.get('shopName', None)
        user_name = request.POST.get('userName', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        phone = request.POST.get('phone', None)
        shop_address = request.POST.get('shopAddress', None)
        tax_id = request.POST.get('taxID', None)

        # Check if required fields are provided
        if shop_name and user_name and email and password and confirm_password and phone and shop_address and tax_id:
            if password != confirm_password:
                messages.success(request, "Passwords don't match. Please try again.")
            else:
                # Create a new seller user
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


#admin add products
def product_list(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'product_list.html', {'products': products})



#adding prodcuts

# from .models import Product, Category, Subcategory, Brand


def add_product(request):
    if request.method == 'POST':
        # Get form data
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_price')
        product_category = request.POST.get('product_category')
        product_subcategory = request.POST.get('product_subcategory')
        product_brand = request.POST.get('product_brand')
        stock_quantity = request.POST.get('stock_quantity')
        product_image = request.FILES['product_image']

        # Get the selected seller from the form data
        seller_id = request.POST.get('product_seller')
  # Assuming you have a 'seller' input field in your form

        # Check if the category, subcategory, and brand exist, if not, create them
        category, _ = Category.objects.get_or_create(name=product_category)
        subcategory, _ = Subcategory.objects.get_or_create(category=category, name=product_subcategory)
        brand, _ = Brand.objects.get_or_create(name=product_brand)

        # Use the seller_id to get the seller object
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
    # Query the seller's products from the database
    seller = request.user  # Assuming the seller is a logged-in user
    seller_products = Product.objects.filter(seller=seller)

    return render(request, 'seller_products.html', {'seller_products': seller_products})

#edit prodcut option for seller
# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)  # Fetch the product by its ID
#     # Other view logic if needed
#     return render(request, 'edit_product.html', {'product': product})
def edit_product(request, product_id):
    # Retrieve the product using get_object_or_404 to handle cases where the product doesn't exist
    product = get_object_or_404(Product, pk=product_id)
    

    if request.method == 'POST':
        print(request.POST) 
        # Handle form submission and update the product
        # You can access form data using request.POST and request.FILES
        # Perform validation and update the product data in the database

        # Get the category and subcategory names from the form data
        category_name = request.POST['product_category']
        subcategory_name = request.POST['product_subcategory']

        # Retrieve the Category and Subcategory instances that correspond to the names
        category = Category.objects.get(name=category_name)
        subcategory = Subcategory.objects.get(name=subcategory_name)

        # Update the product fields
        product.product_name = request.POST['product_name']
        product.category = category
        product.subcategory = subcategory
        product.quantity = request.POST['stock_quantity']
        product.description = request.POST['product_description']
        product.price = request.POST['product_price']
        product.status = request.POST['product_status']

        # Handle product image upload if needed
        if 'product_image' in request.FILES:
            product.image = request.FILES['product_image']

        # Save the updated product
        product.save()

        # Redirect to a product detail page or a success page
        # You need to replace 'seller_products' with the actual URL pattern name for your product list page
        return redirect('seller_products')

    # If the request method is GET, render the edit product form
    return render(request, 'edit_product.html', {'product': product})

#deactivate option for seller
def deactivate_product(request, product_id):
    # Retrieve the product using get_object_or_404
    product = get_object_or_404(Product, pk=product_id)

    # Check if the current status is 'active'
    if product.status == 'active':
        # Change the status to 'inactive'
        product.status = 'inactive'
        product.save()

    # Redirect back to the seller's product list
    return redirect('seller_products')

#customers profile view in home2.html
def user_profile(request):
    # Your profile view logic here
    return render(request, 'user_profile.html')
#customer changing password
def change_password(request):
    # Your profile view logic here
    return render(request, 'change_password.html')
#seller viewing profile
def seller_profile(request):
    # Your view logic here
    return render(request, 'seller_template/seller_profile.html')


#page for displaying subcategory serums

def serums_products(request):
    # Get the Category instance for "Skincare"
    skincare_category = Category.objects.get(name="Skincare")

    # Get the Subcategory instance for "Serums" within the "Skincare" category
    serums_subcategory = Subcategory.objects.get(name="Serums", category=skincare_category)

    # Retrieve all products with this subcategory
    products = Product.objects.filter(subcategory=serums_subcategory, status="active")

    return render(request, 'serums_products.html', {'products': products})

#page for displaying subcategoery foundations
def foundations_products(request):
    # Get the Category instance for "Face Makeup"
    face_makeup_category = Category.objects.get(name="Face Makeup")

    # Get the Subcategory instance for "Foundations" within the "Face Makeup" category
    foundations_subcategory = Subcategory.objects.get(name="Foundations", category=face_makeup_category)

    # Retrieve all products with this subcategory
    products = Product.objects.filter(subcategory=foundations_subcategory, status="active")

    return render(request, 'foundations_products.html', {'products': products})

#viewing product details by clciking prodcut image 

def product_detail(request, product_id):
    # Get the product by its ID, or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {'product': product})


#add to wishlist
def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    # Implement your wishlist functionality here (e.g., store in session or a database table)
    return redirect('wishlist')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Get or create the user's wishlist
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
    # Remove the product from the user's wishlist
    WishlistItem.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')



#add to cart
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    # Implement your cart functionality here (e.g., store in session or a database table)
    return redirect('cart')

def cart(request):
    # Logic to display cart items, if any
    return render(request, 'cart.html')