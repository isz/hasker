from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db import transaction

from .forms import SignUpForm, UserForm, ProfileForm


@login_required
@transaction.atomic
def profile_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request,
        "profile/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.avatar = form.cleaned_data.get("avatar")
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "profile/signup.html", {"form": form})
