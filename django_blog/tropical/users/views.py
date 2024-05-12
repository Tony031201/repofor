from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from .forms import *
import random
import smtplib
import os
from dotenv import load_dotenv

# Create your views here.
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


@method_decorator(login_required(login_url='users/login'),name='dispatch')
class UserProfileUpdateView(SuccessMessageMixin,UpdateView):
    template_name = 'users/profile-update.html'
    model = UserProfile
    form_class = UserProfileForm
    success_message = "Your profile is updated."

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:update_profile',kwargs={'slug':self.object.slug})

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            return super(UserProfileUpdateView,self).get(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/')

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        print("Debug: UserProfile object:", self.object)

        if self.object.subscript:
            print("sub true")
            print("email : " ,self.object.email)

            if not code_1.objects.filter(email=self.object.email):
                code = random.randint(100000, 999999)
                code_1.objects.create(email=self.object.email,code=code)

                my_email = "atuony0312@gmail.com"
                load_dotenv()
                password = os.getenv("SMTP_PASSWORD")

                if not password:
                    raise ValueError("SMTP_PASSWORD environment variable is not set")

                email_content = f"Subject: Welcome for your subscription for The tropical island restaurant!!\n\nDear {self.object.user.username}, your Promo Code is {code}"

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
                    connection.login(user=my_email, password=password)
                    connection.sendmail(
                        from_addr=my_email,
                        to_addrs=self.object.email,
                        msg=email_content
                    )

            return super(UserProfileUpdateView,self).post(request,*args,**kwargs)
        else:
            print("sub false")
            return super(UserProfileUpdateView, self).post(request, *args, **kwargs)


def add_user_slug_to_context(request):
    user_slug = slugify(request.user.username)
    return {'user_slug':user_slug}

@login_required(login_url='users/login')
def create_code2(request):
    if request.user.username != 'weiting':
        return HttpResponseRedirect('/')
    else:
        return render(request,'create_code/create_code2.html')

@login_required(login_url='users/login')
def create_now(request):
    if request.user.username != 'weiting':
        return HttpResponseRedirect('/')
    else:
        users = UserProfile.objects.filter(subscript=True)
        for user in users:
            if not code_2.objects.filter(email=user.email):
                code = random.randint(100000, 999999)
                code_2.objects.create(email=user.email,code=code)

    return render(request,'create_code/create_success.html')

@login_required(login_url='users/login')
def delete_now(request):
    if request.user.username != 'weiting':
        return HttpResponseRedirect('/')
    else:
        codes = code_2.objects.all()
        for code in codes:
            code.delete()

    return render(request,'create_code/delete_success.html')

