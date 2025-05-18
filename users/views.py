from django.views import View
from users.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request=request, template_name=self.template_name, context=context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/ads/get_ads/1/')
        context = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=context)
    
