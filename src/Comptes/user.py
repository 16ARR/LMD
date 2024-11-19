
from smtplib import SMTPAuthenticationError

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

# from accounts.forms import ExChangerSignupForm
# from accounts.models import ExChangerAdresses
#
# from verify_email.email_handler import send_verification_email

import logging

def exchanger_logout(request):
    logout(request)
    return redirect("home")