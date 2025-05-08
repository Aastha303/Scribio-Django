from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('search/', views.search_view, name='search'),  # URL for search
    path('index/', views.index, name='index'),
    path('theme/', views.theme, name='theme'),
    path('rec_topic/', views.rec_topic, name='rec_topic'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.my_profile_redirect, name='my-profile'),
    path('profile/chat/', include('blog2.urls', namespace='profiles')), 
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('toggle_follow/', views.toggle_follow, name='toggle_follow'),
    path('list/', views.blog_list_view, name='blog_list'),
    path('write/', views.write_blog_view, name='write_blog'),
    path('submit_blog/', views.submit_blog, name='submit_blog'),
    path('blogs/<int:blog_id>/', views.blog_detail_view, name='blog_detail'),
    path('delete/<int:blog_id>/', views.delete_blog_view, name='delete_blog'),
    path('update/<int:blog_id>/', views.update_blog_view, name='edit_blog'),
    path('blog/', views.blog_view, name='blog_view'),
    path('damon/', views.damon, name='damon'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/clap/<int:comment_id>/', views.clap_comment, name='clap_comment'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)