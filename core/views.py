from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class LoginView(View):
    template_name = 'core/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, self.template_name, {'error': 'Identifiants invalides'})

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'core/dashboard.html'

    def get(self, request):
        context = {
            'user': request.user,
            'role': request.user.role
        }
        return render(request, self.template_name, context)
