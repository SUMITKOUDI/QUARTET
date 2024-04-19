from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from firebase_admin import auth
from django.contrib.auth import logout as django_logout

from django.contrib.auth.decorators import permission_required



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
