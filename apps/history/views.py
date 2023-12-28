from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from ..users.models import User

# Create your views here.


class IndexView(PermissionRequiredMixin, TemplateView):
    permission_required = 'history.view_history'
    template_name = "history/logs.html"
    

# App 'Users'
class UserLogsView(PermissionRequiredMixin, ListView):
    permission_required = 'history.view_history'
    model = User
    template_name = "history/users.html"
    context_object_name = 'history'
    paginate_by = 20
    queryset = User.history.all()
    
    
class UserRollbackView(PermissionRequiredMixin, View):
    permission_required = 'history.change_history'
    model = User
    success_url = reverse_lazy('history:users')
    
    def post(self, request, pk, *args, **kwargs):
        history = self.model.history.get(pk=pk)
        history.save()
        return redirect(self.success_url)