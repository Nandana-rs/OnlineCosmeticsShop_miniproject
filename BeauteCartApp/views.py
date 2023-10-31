
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
from .models import Product  # Import your Product model

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

def add_product(request):
   return render(request, 'add_product.html')
    

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
            
                if request.user.user_types==CustomUser.CUSTOMER:
                #     #here session start
                #     request.session["username"]=user.username
                # #here session end
                    return redirect('home2')
                elif request.user.user_types == CustomUser.SELLER:
                #      #here session start
                #     request.session["username"]=user.username
                # #here session end
                    return redirect('seller_template')
                #     print("user is therapist")
                #     return redirect(reverse('therapist'))
                elif request.user.user_types == CustomUser.ADMIN:
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
 #here session started @never_cache
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
        user_typeS='SELLER'
        # Check if required fields are provided
        if shop_name and user_name and email and password and confirm_password and phone and shop_address and tax_id:
            if password != confirm_password:
                messages.success(request, "Passwords don't match. Please try again.")
            else:
                # Create a new seller user
                user = CustomUser.objects.create_user(username=user_name, email=email, password=password,user_typeS=user_typeS)
                user.shop_name = shop_name
                user.phone = phone
                user.shop_address = shop_address
                user.tax_id = tax_id
                user.user_types = CustomUser.SELLER
                user.save()

                messages.success(request, "Seller registration successful. You can now login.")
                return redirect('login')
        else:
            messages.success(request, "Please fill out all fields.")

    return render(request, 'sellerRegistration.html')

#admin add products
def product_list(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'product_list.html', {'products': products})
# def sellerRegistration(request):
#      return render(request, 'sellerRegistration.html')

#heresellerregistration ends  



# def logout_user(request):
#     logout(request)
#     messages.success(request,("Logged out"))
#     return  redirect('userhome')

# def register_pump(request):
#     return render(request, 'registerPump.html')

# def userhome(request):
#     return render(request, 'userhome.html')