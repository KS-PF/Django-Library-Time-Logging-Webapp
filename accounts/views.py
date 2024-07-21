from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('time_logging:message', kwargs={'type': 'signup'})
    template_name = 'registration/signup.html'



def user_page(request):
    return render(request, 'accounts/user_page.html')
