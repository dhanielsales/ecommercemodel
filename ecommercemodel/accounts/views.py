from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # View Baseada em Classe
#from django.contrib.auth.decorators import login_required # View Baseada em Função
from django.contrib.auth.forms import PasswordChangeForm

from .models import User
from .forms import UserAdminCreationForm

class AccountView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/account.html'

account = AccountView.as_view()

class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')

register = RegisterView.as_view()

class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'accounts/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user

update_user = UpdateUserView.as_view()

class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('accounts:account')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

update_password = UpdatePasswordView.as_view()
