
# Create your views here.
# from django.shortcuts import render
# #from django.http import HttpResponse

# # Create your views here.
# def home(request):
#     return render(request,'home.html')
# def about(request):
#     return render(request,'about.html')



# def login(request):


#     return render(request,'login.html')

# def registration(request):

#     return render(request,'registration.html')/

from django.shortcuts import render,redirect
from .models import CustomUser,UserProfile
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
# from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
def logout_view(request):
    logout(request)
    return redirect('login')
#here
def sellerRegistration(request):
     return render(request, 'sellerRegistration.html')

def seller_template(request):
     return render(request, 'seller_template.html')
    

 
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


def login(request):
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
                
                    return redirect('/')
                # elif request.user.user_typ == CustomUser.VENDOR:
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


# def logout_user(request):
#     logout(request)
#     messages.success(request,("Logged out"))
#     return  redirect('userhome')

# def register_pump(request):
#     return render(request, 'registerPump.html')

# def userhome(request):
#     return render(request, 'userhome.html')