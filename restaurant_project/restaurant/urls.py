from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',                                     views.home,                  name='home'),
    path('about/',                               views.about,                 name='about'),
    path('menu/',                                views.todays_menu,           name='menu'),
    path('reservations/',                        views.reserve,               name='reserve'),
    path('reservations/<int:pk>/confirmed/',     views.reservation_confirmed, name='reservation_confirmed'),
    path('contact/',                             views.contact,               name='contact'),
    path('staff/reservations/',                  views.staff_reservations,    name='staff_reservations'),
    path('staff/reservations/<int:pk>/update/',  views.update_reservation,    name='update_reservation'),
    path('staff/login/',                         auth_views.LoginView.as_view(template_name='restaurant/staff_login.html'),  name='staff_login'),
    path('staff/logout/',                        auth_views.LogoutView.as_view(next_page='home'), name='staff_logout'),
    path('gallery/',                             views.gallery,               name='gallery'),
]