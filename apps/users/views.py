from catalogos_modular.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import EditProfileForm, NewUserForm


class RegisterView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
            
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

        return redirect(self.get_success_url())

# Forgot Password (TODO)
def forgot_password(request):
    context = {}
    return render(request=request, template_name="registration/forgot-password.html")

# Profile
class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('profile')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(ProfileView, self).post(request, *args, **kwargs)
    
    def get_object(self, **kwargs):
        return self.request.user

class RegisterViewAdmin(generic.FormView):
    template_name = 'registration/register.html'
    form_class = NewUserForm
    success_url = reverse_lazy('login')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('/')
            
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

        return redirect(self.get_success_url())