from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')  # Manually extract the email
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email  # Save email to user instance
            user.save()
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
