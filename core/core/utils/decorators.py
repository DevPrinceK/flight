from django.shortcuts import redirect
from django.contrib import messages


class MustLogin(object):
    def __init__(self, original_method):
        self.original_method = original_method

    def __call__(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            if (request.user.is_superuser or request.user.is_staff or request.user.is_agency_admin):  # noqa
                return self.original_method(request, *args, **kwargs)
            else:
                messages.error(
                    request, "Access Denied!")
                return redirect('accounts:login')
        else:
            messages.error(
                request, 'Please login to continue.')
            return redirect('accounts:login')
