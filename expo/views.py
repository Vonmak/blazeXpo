from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =  form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            form.save()
        return HttpResponse('Registered Successfully')
    return render(request, 'auth/register.html',locals())
