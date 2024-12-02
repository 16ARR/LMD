from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

class PasswordReset(PasswordResetView):
    template_name = "password/password_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = "password/password_reset_email.html"


class PasswordResetDone(PasswordResetDoneView):
    template_name = "password/password_reset_done.html"

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "password/password_reset_complete.html"