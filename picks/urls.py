from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('league_select/', views.league_select, name='league_select'),
    path('league_create/', views.league_create, name='league_create'),
    path('league/<int:league_id>/', views.league, name='league'),
    path('league/<int:league_id>/<int:current_week>/make_pick/',
         views.make_pick, name='make_pick'),
]
