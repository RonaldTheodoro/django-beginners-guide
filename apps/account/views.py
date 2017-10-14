from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from . import forms


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})
