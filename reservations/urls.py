

from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),  # 👈 redirects '/' to login
    path('reserve/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:id>/', views.edit_reservation, name='edit_reservation'),
    path('delete/<int:id>/', views.delete_reservation, name='delete_reservation'),


    path('admin-dashboard/rooms/', views.admin_manage_rooms, name='admin_manage_rooms'),
    path('admin-dashboard/rooms/add/', views.admin_add_room, name='admin_add_room'),
    path('admin-dashboard/rooms/edit/<int:id>/', views.admin_edit_room, name='admin_edit_room'),
    path('admin-dashboard/rooms/delete/<int:id>/', views.admin_delete_room, name='admin_delete_room'),

path('admin-dashboard/reservations/', views.admin_manage_reservations, name='admin_manage_reservations'),
path('admin-dashboard/reservations/delete/<int:id>/', views.admin_delete_reservation, name='admin_delete_reservation'),

path('admin-dashboard/users/', views.admin_manage_users, name='admin_manage_users'),
path('admin-dashboard/users/delete/<int:id>/', views.admin_delete_user, name='admin_delete_user'),
path('admin-dashboard/users/promote/<int:id>/', views.admin_promote_user, name='admin_promote_user'),
path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]

