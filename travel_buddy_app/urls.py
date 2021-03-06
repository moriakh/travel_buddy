from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index, name = "index"),
    path('register', auth.register, name = "register"),
    path('travels/destination/<int:trip_id>', views.destination, name = "destination"),
    path('add_trip', views.add_trip, name = "add_trip"),
    path('travels/add', views.add_view, name = "add_view"),
    path('travels/join/<int:trip_id>', views.join_trip, name = "join_trip"),
    path('login', auth.login, name = "login"),
    path('cancel/<int:trip_id>', views.cancel, name = "cancel"),
    path('delete/<int:trip_id>', views.delete, name = "delete"),
    path('logout', auth.logout, name = "logout")
]
