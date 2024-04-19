from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import auth
from django.contrib.auth import logout as django_logout

from django.contrib.auth.decorators import permission_required

from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PasswordResetRequestForm

from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SetPasswordForm

# Create your views here.
def index(request):
    return HttpResponse('<h1><center>X:Hapenning now</center></h1>')




def register_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    try:
        # Create a new user
        user = auth.create_user(
            email=email,
            password=password
        )
        return HttpResponse(f"User {user.uid} created successfully!")
    except Exception as e:
        return HttpResponse(f"Error creating user: {str(e)}")



def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        # Get the user by email
        user = auth.get_user_by_email(email)
        # Verify the password (implement your password verification function)
        if verify_password(user, password):
            # Manage user session or token (you can use Django's session management)
            request.session['user_id'] = user.uid
            return HttpResponse(f"User {user.uid} logged in successfully!")
        else:
            return HttpResponse("Invalid email or password")
    except Exception as e:
        return HttpResponse(f"Error logging in: {str(e)}")


def verify_password(email, password):
    try:
        user = auth.verify_password(email, password)
        return True
    

    except auth.AuthError:
        return False



from django.http import HttpResponse
from firebase_admin import auth

def logout_user(request):
    # Clear the user's session using Django's logout function
    django_logout(request)
    
    # If you are using Firebase Authentication, you may want to revoke the user's token
    user_id = request.session.get('user_id')
    if user_id:
        try:
            # Revoke the user's token using Firebase Authentication
            auth.revoke_refresh_tokens(user_id)
        except Exception as e:
            # Handle any errors during token revocation
            return HttpResponse(f"Error revoking token: {str(e)}")

    # Return a response indicating that the user has logged out successfully
    return HttpResponse("User logged out successfully")



@login_required
def secure_view(request):
    return HttpResponse("This is a secure view!")




@permission_required('app.can_access_special_view')
def special_view(request):
    return HttpResponse("This view is restricted to users with the 'can_access_special_view' permission.")





def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[user.pk, token]))
            # Send an email with the reset link
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}',
                'your-email@example.com',
                [email]
            )
            return HttpResponse('Password reset link sent to your email')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'password_reset_request.html', {'form': form})



def password_reset_confirm(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("Invalid user ID")

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Password has been reset successfully')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('Invalid or expired token')

from django.shortcuts import render, redirect
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        # Handle signup logic here
        return HttpResponse('Sign up logic not implemented yet.')
    else:
        return render(request, 'your_html_file.html')  # Replace with your HTML file name

def create_account(request):
    if request.method == 'POST':
        # Handle account creation logic here
        return HttpResponse('Account creation logic not implemented yet.')


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]


from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('create_account/', views.create_account, name='create_account'),
    # Add other URL patterns...
]