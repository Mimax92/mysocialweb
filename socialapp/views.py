from django.shortcuts import render
from django.views import View
from .models import Gossip, Mesage, Notification, Like, Comment
from .forms import GossipForm, MessageForm, CreateUserForm, Notiform, CommentForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
# PresenceList.objects.create(**form.cleaned_data)

class HomePageView(View, LoginRequiredMixin):
    def get(self, request):
        gossips = Gossip.objects.all().order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        noti_form = Notiform()
        form = GossipForm()
        ctx = {
            "gossips": gossips,
            "form": form,
            "noti": noti,
            "noti_form": noti_form,
        }
        return render(request, "homapageone.html", ctx)

    def post(self, request):
        gossips = Gossip.objects.all().order_by("-id")

        form = GossipForm(request.POST or None, request.FILES or None)
        # gossip_voted = Gossip.objects.get(pk=form.id))
        # if 'add' in request.POST:
        #     new_like, created = Like.objects.get_or_create(user=request.user, gossip_id=)
        if form.is_valid():
            if request.user.is_authenticated:
                Gossip.objects.create(**form.cleaned_data, user=request.user)
            else:
                Gossip.objects.create(**form.cleaned_data)
        return render(request, "homapageone.html", {"form": form, "gossips": gossips})


class UserPageView(View, LoginRequiredMixin):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = GossipForm()
        if request.user.is_authenticated:
            gossips = Gossip.objects.filter(user=request.user).order_by("-id")
            ctx = {
                "user": user,
                "gossips": gossips,
                "form": form,
            }
        else:
            return redirect("/login/")
        return render(request, "userprofile.html", ctx)

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        gossips = Gossip.objects.filter(user=request.user).order_by("-id")
        form = GossipForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            Gossip.objects.create(**form.cleaned_data, user=request.user)
            ctx = {
                "user": user,
                "gossips": gossips,
                "form": form,
            }
        return render(request, "userprofile.html", ctx)


class SendMesageView(View, LoginRequiredMixin):
    def get(self, request):
        user_mesage = Mesage.objects.filter(receiver=request.user).order_by("-id")
        form = MessageForm()
        ctx = {
            "form": form,
            "user_mesage": user_mesage,
        }
        return render(request, "sendmesage.html", ctx)

    def post(self, request):
        form = MessageForm(request.POST or None, request.FILES or None)
        user_mesage = Mesage.objects.filter(receiver=request.user).order_by("-id")
        if form.is_valid():
            Mesage.objects.create(**form.cleaned_data, sender=request.user)
            receiver_not = form.cleaned_data["receiver"]
            Notification.objects.create(sender=request.user, receiver=receiver_not,
                                        content=f'{request.user.username} send you Mesage!!')
            form = MessageForm()
        ctx = {
            "form": form,
            "user_mesage": user_mesage,
        }
        return render(request, "sendmesage.html", ctx)


class CreateUserView(View):
    def get(self, request):
        logout(request)
        form = CreateUserForm()
        ctx = {
            "form": form
        }
        return render(request, "createuser.html", ctx)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop("repeated_password")
            user = get_user_model().objects.create_user(**form.cleaned_data)
            return redirect("/logout/")
        return render(request, "createuser.html", {"form": form})


class NotificationView(View):
    def post(self, request):
        gossips = Gossip.objects.all().order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        form = GossipForm(request.POST or None, request.FILES or None)
        if request.POST.get('read') is not None:
            noti.update(read=True)
        return render(request, "homapageone.html",
                      {"form": form, "gossips": gossips, "noti": noti})


class LikeView(View):
    def post(self, request, pk):
        gossips = Gossip.objects.all().order_by("-id")
        noti = Notification.objects.filter(receiver=request.user, read=False)
        gos_com_id = pk
        noti_form = Notiform()
        form = GossipForm()
        if 'add' in request.POST:
            Like.objects.get_or_create(user=request.user, gossip_id=pk)
            comment_form = None
        if 'sub' in request.POST:
            Like.objects.filter(user=request.user).delete()
            comment_form = None
        if 'com' in request.POST:
            comment_form = CommentForm()
        if 'add_com' in request.POST:
            content = request.POST["content"]
            Comment.objects.get_or_create(user=request.user, gossip_id=pk, content=content)
            comment_form = None
        ctx = {
            "gossips": gossips,
            "noti": noti,
            "noti_form": noti_form,
            "comment_form": comment_form,
            "gos_com_id": gos_com_id,
        }
        return render(request, "homapageone.html", ctx)

# class CommentView(View):
#     def post(self, request, pk):
#         gossips = Gossip.objects.all().order_by("-id")
#         noti = Notification.objects.filter(receiver=request.user, read=False)
#         gos_com_id = pk
#         noti_form = Notiform()
#         form = GossipForm()
#         if 'add_com' in request.POST:
#             content = form["content"]
#             Comment.objects.get_or_create(user=request.user, gossip_id=pk, comment_content=content)
#         ctx = {
#             "form":form,
#             "gossips": gossips,
#             "noti": noti,
#             "noti_form": noti_form,
#             "gos_com_id": gos_com_id,
#         }
#         return render(request, "homapageone.html", ctx)
