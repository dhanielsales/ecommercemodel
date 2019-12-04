from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # View Baseada em Classe
#from django.contrib.auth.decorators import login_required # View Baseada em Função


from .models import User
from .forms import UserAdminCreationForm


class AccountView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/account.html'

account = AccountView.as_view()

class RegisterView(CreateView):

    model = User
    template_name = 'register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')

register = RegisterView.as_view()

class UpdateUserView(UpdateView):

    model = User
    template_name = 'accounts/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user

update_user = UpdateUserView.as_view()