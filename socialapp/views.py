from django.shortcuts import render
from django.views import View
from .models import Gossip
from .forms import GossipForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
# PresenceList.objects.create(**form.cleaned_data)

class HomePageView(View):
    def get(self, request):
        gossips = Gossip.objects.all().order_by("-id")
        form = GossipForm()
        ctx = {
            "gossips": gossips,
            "form": form
        }
        return render(request, "homapageone.html", ctx)

    def post(self, request):
        gossips = Gossip.objects.all().order_by("-id")
        form = GossipForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if request.user.is_authenticated:
                Gossip.objects.create(**form.cleaned_data, user=request.user)
            else:
                Gossip.objects.create(**form.cleaned_data)
        return render(request, "homapageone.html", {"form": form, "gossips": gossips})



class UserPageView(View):
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
    #
    # class SendMesageView(View):
    #     def get(self, request):
    #