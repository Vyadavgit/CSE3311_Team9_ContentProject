from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutFn, name="logout"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/reset_Password.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/sent_reset_Email.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_Confirmation.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_Complete.html"),
         name="password_reset_complete"),


    path('dashboard/', views.viewDashboard, name="dashboard"),
    path('view_profile/', views.viewProfilePage, name="view_profile"),
    path('edit_profile/', views.editProfilePage, name="edit_profile")

]

