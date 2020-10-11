"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from socialapp.views import HomePageView, UserPageView, SendMesageView, CreateUserView, NotificationView, LikeView, update_profile
from rest_framework import routers
from socialapp.views import UserView

router = routers.DefaultRouter()
router.register(r'users', UserView)


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', HomePageView.as_view(), name="homepage"),
                  path('', NotificationView.as_view(), name="notihomepage"),
                  path('<int:pk>', LikeView.as_view(), name="likehomepage"),
                  path('login/', auth_views.LoginView.as_view(), name="login"),
                  path('logout/', auth_views.LogoutView.as_view(), name="logout"),
                  path('profile/<int:pk>', UserPageView.as_view(), name="userpage"),
                  path('mesage/', SendMesageView.as_view(), name="mesage"),
                  path('avatar/', include('avatar.urls')),
                  path('createuser/', CreateUserView.as_view(), name="createuser"),
                  path('updateuser/', update_profile, name="updateuser"),
                  path('', include(router.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
