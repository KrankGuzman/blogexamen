from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from App import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('Home/', app_views.home, name="Home"),
    path('LogIn/',app_views.log_in_view, name="LogIn"),
    path('LogOut/',app_views.log_out_view, name="LogOut"),
    path('SignIn/', app_views.sign_in_view, name="SignIn"),

    path('PostIndex/', app_views.post_index_view, name='PostIndex'),
    path('CreatePost/', app_views.create_post_view, name='CreatePost'),
    path('ReadPost/<int:post_pk>/', app_views.read_post_view, name='ReadPost'),
    path('PostCommentsIndex/<int:post_pk>/', app_views.post_comment_index_view, name='PostCommentsIndex'),
    path('DeletePostComment/<int:post_comment_pk>/', app_views.delete_post_comment_view, name='DeletePostComment'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
