from django.urls import path, include
from .views import UserGetView, PostGetView, CommentGetView, RegisterPageView, UserLoginView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('users/', UserGetView.as_view(), name='users'),
    path('post/', PostGetView.as_view(), name='post'),
    path('comment/', CommentGetView.as_view(), name='comment'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterPageView.as_view(), name='register'),
]
