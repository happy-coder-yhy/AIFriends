from django.urls import path, re_path

from . import views
from .views.index import index
from .views.user.account.get_user_info import GetUserInfoView
from .views.user.account.login import LoginView
from .views.user.account.logout import LogoutView
from .views.user.account.refresh_token import RefreshTokenView
from .views.user.account.register import RegisterView

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),
    # 前端页面路由
    path('', index),
    re_path(r'^(?!media/|static/|assets/).*$', index),
]

