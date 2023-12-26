from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user # Who is the current user ?
        if user.is_authenticated:
            if user.user_type == '1': # Is it the HR/Admin
                if modulename ==  'StaffApp.views' or modulename == 'FacultyApp.views' or modulename == 'StudentApp.views' :
                    return redirect(reverse('Admin_Home'))
            elif user.user_type == '2': #  Faculty :-/ ?
                if modulename == 'StudentApp.views' or modulename == 'StaffApp.views' or modulename == 'admin_app.views':
                    return redirect(reverse('Faculty_Home'))
            elif user.user_type == '3': #  Staff :-/ ?
                if modulename == 'StudentApp.views' or modulename == 'FacultyApp.views' or modulename == 'admin_app.views':
                    return redirect(reverse('Staff_Home'))
            elif user.user_type == '4': # ... or Student ?
                if modulename ==  'FacultyApp.views' or modulename == 'admin_app.views' or modulename == 'StaffApp.views':
                    return redirect(reverse('Student_Home'))
            else: # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('signin_page'))
        else:
            if request.path == reverse('signin_page') or modulename == 'django.contrib.auth.views' or request.path == reverse('signin'): # If the path is login or has anything to do with authentication, pass
                pass
            else:
                return redirect(reverse('/'))
