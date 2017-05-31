from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^home$', views.home, name="home"),
    url(r'^login$',views.login, name="login"),
    url(r'^addquote$',views.addquote, name="quote"),
    url(r'^favquote$', views.favquote, name="favquote"),
    url(r'^logout$',views.logout, name="logout"),
    url(r'^userfavs$', views.userfavs, name="userfavs"),
    url(r'^user(?P<find>\d*)',views.user, name="user"),
]