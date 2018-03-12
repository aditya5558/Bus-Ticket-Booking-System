from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^bus_operator/$', views.bus_operator_home, name='bus_operator'),
    url(r'^add_bus/$', views.add_bus, name='add_bus'),
    url(r'^remove_bus/$', views.remove_bus, name='remove_bus'),
    url(r'^passenger/$', views.passenger_home, name='passenger_home'),
    url(r'^wallet/$', views.add_money, name='wallet_home'),
    url(r'^book_ticket/$', views.book_ticket, name='book_ticket'),
    url(r'^book_ticket_1/$', views.book_ticket_1, name='book_ticket_1'),
    url(r'^view_trips/$', views.view_trips, name='view_trips'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^view_feedback/$', views.view_feedback, name='view_feedback'),

]