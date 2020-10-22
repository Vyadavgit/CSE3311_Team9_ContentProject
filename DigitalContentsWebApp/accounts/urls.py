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
    path('edit_profile/', views.editProfilePage, name="edit_profile"),
    path('upload_video/', views.uploadVideoPage, name="upload_video"),
    path('my_contents/', views.viewMyContentsPage, name="my_contents"),

    path('comedy_content/', views.comedyCategoryPage, name="comedy_content"),
    path('fitness_content/', views.fitnessCategoryPage, name="fitness_content"),
    path('cooking_content/', views.cookingCategoryPage, name="cooking_content"),
    path('entertainment_content/', views.entertainmentCategoryPage, name="entertainment_content"),
    path('technology_content/', views.technologyCategoryPage, name="technology_content"),
    path('music_content/', views.musicCategoryPage, name="music_content"),
    path('other_content/', views.otherCategoryPage, name="other_content"),

]

