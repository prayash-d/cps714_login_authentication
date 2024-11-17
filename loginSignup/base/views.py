from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model

@login_required
def home(request):
    return render(request, "home.html", {})

#this view is for the signup page
def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')  # Manually extract the email
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.email = email  # Save email to user instance
            user.save() #savigng user wuth email and password to the database

            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            else:
                return redirect('verify-email') #The user is then redirected to the verify-email URL if there isn't a next parameter in the URL.

    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

###Views to singup email verification
# Verify email: send the verification link to the user’s email.
# Verify email done: tell the user to check his/her email.
# Verify email confirm: verify the link.
# Verify email complete: redirect the user to your website after verification.

# Add below existing imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages



# so we can reference the user model as User instead of CustomUser
User = get_user_model()

## send email with verification link
# In the code above, if the user’s email is unverified, an account activation token is generated using the account_activation_token class 
# This token can be used to verify a user through email. 
# A uid was also generated and encoded to ensure that the appropriate user - to whom the email was sent - gets verified.
def verify_email(request):
    if request.method == "POST":
        if request.user.email_is_verified != True:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string('user/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('signup')
    return render(request, 'user/verify_email.html')


def verify_email_done(request):
    return render(request, 'user/verify_email_done.html')

#verify the link that the user clicks on...
# This view decodes the link that the user clicked on and confirms if it is valid or not. 
# If the token is valid, the email_is_verified field of the user is set to True and the user is redirected to the verify-email-complete URL.
# if the link is invalid, the user is sent to the verify_email_confirm.html page.

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'user/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user/verify_email_complete.html')
