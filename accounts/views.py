from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'pages/profile.html', context)
#
# def user_login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user=authenticate(request, username=data['username'], password=data['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse("success")
#                 else:
#                     return HttpResponse("error")
#     else:
#         form = LoginForm()
#         context = {
#             'form': form,
#         }
#     return render(request, 'accounts/login.html', context)
#
