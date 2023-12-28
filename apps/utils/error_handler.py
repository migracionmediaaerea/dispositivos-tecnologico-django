# error handling middleware
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render


class PermissionDeniedErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # This is the method that responsible for the safe-exception handling
        if isinstance(exception, PermissionDenied):
            # TODO: remove redirect and use our own error page
            messages.error(request, 'No tiene permisos para acceder a esta página')
            return HttpResponseRedirect("/")
            # return render(
            #     request=request,
            #     template_name="page_403.html",
            #     status=403
            # )
        return None