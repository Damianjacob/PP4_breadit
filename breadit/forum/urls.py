from django.urls import path

from .views import DeletePostView, PostView, PostDetailView, MyProfileView, CreatePostView, UpdatePostView

urlpatterns = [
    path('', PostView.as_view(), name='index'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('update_post/<slug:slug>/', UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<slug:slug>/', DeletePostView.as_view(), name='delete_post'),
    path('accounts/profile/', MyProfileView.as_view(), name='profile'),

]