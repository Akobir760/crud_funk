from django.urls import path
from .views import post_list, post_detail, post_update, post_delete, post_create

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('update/<int:pk>/', post_update, name='post_update'),
    path('delete/<int:pk>/', post_delete, name='post_delete'),
    # path('list/', PostListCreateAPIView.as_view())
]