from django.urls import path
from .views import post_list, post_detail, post_update, post_delete, post_create, register_view, login_view, logout_view, tag_create, comment_delete, comment_create

urlpatterns = [
    path('lists/', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('update/<int:pk>/', post_update, name='post_update'),
    path('delete/<int:pk>/', post_delete, name='post_delete'),
    # path('list/', PostListCreateAPIView.as_view())
    path("register/", register_view, name="register"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('tag_create/', tag_create, name="tag_create"),
    path('comment_c/', comment_create, name="create_com" ),
    path('comment_d/', comment_delete, name="del_com" ),
]