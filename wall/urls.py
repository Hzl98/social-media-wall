from django.urls import path
from .views import WallListView, WallDetailView, WallCreateView, SourceAddView, PostListView, PostCreateView, WallUpdateView, mod_list, mod_PostListView, wall_display, reset, wall_chart
# from .views import WallListView, WallDetailView, WallCreateView
from . import views

urlpatterns = [
    path('', views.index, name='wall-index'),
    path('home/', WallListView.as_view(), name='wall-home'),
    path('new/', WallCreateView.as_view(), name='wall-createnew'),
    path('wall/<int:pk>/', WallDetailView.as_view(), name='wall-details'),
    path('wall/<int:pk>/settings/', WallUpdateView.as_view(), name='settings'),
    path('wall/<int:pk>/sources/', SourceAddView.as_view(), name='source-add'),
    path('wall/<int:pk>/content/', PostListView.as_view(), name='post-list'),
    path('wall/<int:pk>/content/native/', PostCreateView.as_view(), name='post-create'),
    path('post/show/<int:pk>/<int:returnpoint>/', views.showPost, name='post-show'),
    path('post/hide/<int:pk>/<int:returnpoint>/', views.hidePost, name='post-hide'),
    path('post/get/', views.get_posts, name='posts-get'),
    path('post/getdisplay/', views.get_posts_display, name='posts-get-display'),
    path('post/pshow/', views.p_show, name='p-show'),
    path('post/phide/', views.p_hide, name='p-hide'),
    path('post/filter/', views.filter, name='post-filter'),
    path('wall/<int:pk>/moderators/', mod_list.as_view(), name='wall-moderators'),
    path('wall/getmods/', views.get_mods, name='wall-getmods'),
    path('wall/sendmodinvite/', views.send_mod_invite, name='wall-sendmodinvite'),
    path('wall/<int:pk>/moderation/', mod_PostListView.as_view(), name='wall-moderation'),
    path('wall/<int:pk>/display/', wall_display.as_view(), name='wall-display'),
    path('wall/<int:pk>/reset/', reset.as_view(), name='wall-reset'),
	path('wall/<int:pk>/delete', views.delete_all, name='wall-delete_all'),
	# path('wall/<int:pk>/chart', wall_chart.as_view(), name='wall-chart'),
	path('wall/<int:pk>/chart', views.wall_chart, name='wall-chart'),
	path('wall/<int:pk>/logo', views.upload_logo, name='wall-logo')
    # path('wall/<int:pk>/reset/', wall_reset.as_view(), name='wall-reset'),
]