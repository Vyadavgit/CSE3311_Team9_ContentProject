from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings

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

    path('add_content_viewers/<int:pk>/', views.contentViewersCount, name="add_content_viewers"),

    path('room_chat/', views.roomShowChatHome, name='room_chat'),
    path('room_chat/room/<str:room_name>/<str:person_name>', views.roomShowChatPage, name='room_showchat'),

    path('customers_list/', views.customersListPage, name='customers_list'),
    path('chat/', views.ShowChatHome, name='chat'),
    # path('chat/room/<str:room_name>/<str:person_name>', views.ShowChatPage, name='showchat'),
    # path('showchat/<Decimal:((sender_id*pk)/(sender_id+pk))>/', views.ShowChatPage, name='showchat'),
    path('showchat/<int:pk>/', views.ShowChatPage, name='showchat'),

    path('upgrade/', views.upgrade, name="upgrade"),
    path('payment_method/', views.payment_method, name="payment_method"),
    path('card/', views.card, name="card"),
    path('stripe_webhooks', views.stripe_webhooks, name="stripe_webhooks"),

]

