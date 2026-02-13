from django.urls import path, re_path

from . import views
from .views.create.character.create import CreateCharacterView
from .views.create.character.get_list import GetListCharacterView
from .views.create.character.get_single import GetSingleCharacterView
from .views.create.character.remove import RemoveCharacterView
from .views.create.character.update import UpdateCharacterView
from .views.friend.get_list import GetListFriendView
from .views.friend.get_or_create import GetOrCreateFriendView
from .views.friend.remove import RemoveFriendView
from .views.homepage.index import HomepageIndexView
from .views.index import index
from .views.user.account.get_user_info import GetUserInfoView
from .views.user.account.login import LoginView
from .views.user.account.logout import LogoutView
from .views.user.account.refresh_token import RefreshTokenView
from .views.user.account.register import RegisterView
from .views.user.profile.update import UpdateProfileView

urlpatterns = [
    # 用户
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),

    # 编辑个人信息
    path('api/user/profile/update/', UpdateProfileView.as_view()),

    # 创作
    path('api/create/character/create/', CreateCharacterView.as_view()),
    path('api/create/character/update/', UpdateCharacterView.as_view()),
    path('api/create/character/remove/', RemoveCharacterView.as_view()),
    path('api/create/character/get_single/', GetSingleCharacterView.as_view()),

    # 个人空间
    path('api/create/character/get_list/', GetListCharacterView.as_view()),

    # 首页
    path('api/homepage/index/', HomepageIndexView.as_view()),

    # 好友
    path('api/friend/get_or_create/', GetOrCreateFriendView.as_view()),
    path('api/friend/remove/', RemoveFriendView.as_view()),
    path('api/friend/get_list/', GetListFriendView.as_view()),

    # 前端页面路由
    path('', index),
    re_path(r'^(?!media/|static/|assets/).*$', index),
]

