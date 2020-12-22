from django.shortcuts import render
from django.views import View
from .models import Gossip, Mesage, Notification, Like, Comment, Profile, UserImage
from .forms import GossipForm, MessageForm, CreateUserForm, Notiform, CommentForm, UserForm, ProfileForm, AddUserPhotoForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .serializers import UserSerializer
from rest_framework import viewsets
import requests
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, DeleteView


class UserView(viewsets.ModelViewSet, LoginRequiredMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def weather_city(self, city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0a46cddf36d359427e8aa984fb4f0eca'
    city_weather = requests.get(url.format(city)).json()
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }
    return weather


class HomePageView(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_authenticated:
            gossips = Gossip.objects.all().order_by("-id")
            noti = Notification.objects.filter(receiver=request.user, read=False)
            noti_form = Notiform()
            form = GossipForm()
            weather = weather_city(self, request.user.profile.location)
            ctx = {
                "gossips": gossips,
                "form": form,
                "noti": noti,
                "noti_form": noti_form,
                'weather': weather
            }
        else:
            return redirect("/login/")
        return render(request, "homapageone.html", ctx)


    def post(self, request):
        gossips = Gossip.objects.all().order_by("-id")
        weather = weather_city(self, request.user.profile.location)
        form = GossipForm(request.POST or None, request.FILES or None)
        noti = Notification.objects.filter(receiver=request.user, read=False)
        noti_form = Notiform()
        if form.is_valid():
            if request.user.is_authenticated:
                Gossip.objects.create(**form.cleaned_data, user=request.user)
                form = GossipForm()
            else:
                Gossip.objects.create(**form.cleaned_data)

        ctx = {
            "gossips": gossips,
            "form": form,
            "noti": noti,
            "noti_form": noti_form,
            'weather': weather
        }
        return render(request, "homapageone.html", ctx)


class UserPageView(View, LoginRequiredMixin):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = GossipForm()
        weather = weather_city(self, request.user.profile.location)
        if request.user.is_authenticated:
            gossips = Gossip.objects.filter(user=request.user).order_by("-id")
            ctx = {
                "user": user,
                "gossips": gossips,
                "form": form,
                'weather': weather
            }
        else:
            return redirect("/login/")
        return render(request, "userprofile.html", ctx)

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        gossips = Gossip.objects.filter(user=request.user).order_by("-id")
        form = GossipForm(request.POST or None, request.FILES or None)
        weather = weather_city(self, request.user.profile.location)
        if form.is_valid():
            Gossip.objects.create(**form.cleaned_data, user=request.user)
            ctx = {
                "user": user,
                "gossips": gossips,
                "form": form,
                'weather': weather
            }
        return render(request, "userprofile.html", ctx)


class SendMesageView(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_authenticated:
            noti = Notification.objects.filter(receiver=request.user, read=False)
            user_mesage = Mesage.objects.filter(receiver=request.user).order_by("-id")
            form = MessageForm()
            ctx = {
                "form": form,
                "user_mesage": user_mesage,
                "noti": noti,
            }
        else:
            return redirect("/login/")
        return render(request, "sendmesage.html", ctx)

    def post(self, request):
        form = MessageForm(request.POST or None, request.FILES or None)
        user_mesage = Mesage.objects.filter(receiver=request.user).order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        if form.is_valid():
            Mesage.objects.create(**form.cleaned_data, sender=request.user)
            receiver_not = form.cleaned_data["receiver"]
            Notification.objects.create(sender=request.user, receiver=receiver_not,
                                        content=f'{request.user.first_name} {request.user.last_name} send you Mesage!!')
            form = MessageForm()
        ctx = {
            "form": form,
            "user_mesage": user_mesage,
            "noti": noti,
        }
        return render(request, "sendmesage.html", ctx)

class ReadMesageView(View, LoginRequiredMixin):
    def post(self, request, pk):
        if request.user.is_authenticated:
            form = MessageForm(request.POST or None, request.FILES or None)
            user_mesage = Mesage.objects.filter(receiver=request.user).order_by("-id")
            mesage = Mesage.objects.get(id=pk)
            if form.is_valid():
                Mesage.objects.create(**form.cleaned_data, sender=request.user)
                receiver_not = form.cleaned_data["receiver"]
                Notification.objects.create(sender=request.user, receiver=receiver_not,
                                            content=f'{request.user.first_name} {request.user.last_name} send you Mesage!!')
                form = MessageForm()
            ctx = {
                "form": form,
                "user_mesage": user_mesage,
            }
            if 'read' in request.POST:
                mesage.read=True
                mesage.save()
        else:
            return redirect("/login/")
        return render(request, "sendmesage.html", ctx)
class CreateUserView(View):
    def get(self, request):
        logout(request)
        form = CreateUserForm()
        ctx = {
            "form": form,
        }
        return render(request, "createuser.html", ctx)

    def post(self, request):
        form = CreateUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("repeated_password")
            user = get_user_model().objects.create_user(**form.cleaned_data)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return redirect("/")
        return render(request, "createuser.html", {"form": form})


class NotificationView(View, LoginRequiredMixin):
    def post(self, request):
        weather = weather_city(self, request.user.profile.location)
        gossips = Gossip.objects.all().order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        form = GossipForm(request.POST or None, request.FILES or None)
        if request.POST is not None:
        # if request.POST.get('read') is not None:
            noti.update(read=True)
        return render(request, "homapageone.html",
                      {"form": form, "gossips": gossips, "noti": noti, 'weather': weather})




class LikeView(View, LoginRequiredMixin):
    def post(self, request, pk):
        weather = weather_city(self, request.user.profile.location)
        gossips = Gossip.objects.all().order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        gos_com_id = pk
        gos_user = Gossip.objects.get(pk=pk).user
        noti_form = Notiform()
        form = GossipForm()
        if 'add' in request.POST:
            Like.objects.get_or_create(user=request.user, gossip_id=pk)
            Notification.objects.create(sender=request.user, receiver=gos_user,
                                        content=f'{request.user.first_name} {request.user.last_name} liked you Post!!')

            comment_form = None
        if 'sub' in request.POST:
            Like.objects.filter(user=request.user).delete()
            Notification.objects.create(sender=request.user, receiver=gos_user,
                                        content=f'{request.user.first_name} {request.user.last_name} unliked you Post!!')
            comment_form = None
        if 'com' in request.POST:
            comment_form = CommentForm()
        if 'add_com' in request.POST:
            content = request.POST["content"]
            Comment.objects.get_or_create(user=request.user, gossip_id=pk, content=content)
            Notification.objects.create(sender=request.user, receiver=gos_user,
                                        content=f'{request.user.first_name} {request.user.last_name} live you comment!!')

            comment_form = None
        ctx = {
            "gossips": gossips,
            "noti": noti,
            "noti_form": noti_form,
            "comment_form": comment_form,
            "gos_com_id": gos_com_id,
            "weather": weather,
            "form": form,

        }
        return render(request, "homapageone.html", ctx)



@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'updateuser.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
class AddUserPhoto(LoginRequiredMixin, CreateView):
    model = UserImage
    fields = ['title', 'photo']
    template_name = "adduserphoto.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            photo = UserImage.objects.filter(user=request.user).order_by('-pk')
            add_image = AddUserPhotoForm(instance=request.user)
            ctx = {
                "photo": photo,
                "add_image": add_image,
            }
            return render(request, "adduserphoto.html", ctx)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        photos = request.FILES.getlist('photo')
        if form.is_valid():
            for pic in photos:
                UserImage.objects.create(user=request.user, photo=pic)
            return redirect('/adduserphoto/')


class DelPhoto(LoginRequiredMixin, DeleteView):
    model = UserImage
    template_name = "delphotouser.html"

    context_object_name = "photo"
    success_url = '/adduserphoto/'
