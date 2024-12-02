from django.urls import path
from .views import signup, user_logout, edit_profile, profile, PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('logout/', user_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # PASSWORD RESET
    path('password_reset/', PasswordReset.as_view(), name='password_reset',),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),

]