from django.urls import path
from . import views

#below are the URL to call the function in view file
#in the account app URL goes like
#        .../account/login/ or acccounts/signup/ or just account/
app_name = 'Accounts'

urlpatterns = [
    path("",views.profile_view,name="profile_view"),
    path("login/",views.login_view,name="login_view"),
    path("signup/",views.signup_view,name="signup_view"),
    path("signout/",views.signout,name="signout"),
    path('profile-info/',views.profile_info,name="personal_info"),
    path('activate/<uidb64>/<token>',views.activate_acc,name="activate"),
    path('changename/',views.check_auth,name="change_name"),
    path('change/',views.change_name,name="change"),
    path('changepass/',views.change_pass,name="change_pass")
]