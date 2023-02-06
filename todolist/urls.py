from django.urls import path
from . import views

# Adding a namespace to this urls.py help django distinguish this set of routes from other urls.py files in other packages.
app_name = 'todolist'
urlpatterns = [
	# localhost:8000/todolist/
	path('', views.index, name="index"),
	path('<int:todoitem_id>/', views.todoitem, name="viewtodoitem"),
	path('add_task/', views.add_task, name="add_task"),
	path('add_event/', views.add_event, name="add_event"),
	path('<int:eventitem_id>/event', views.eventitem, name="vieweventitem"),
	path('update_profile/', views.update_profile, name="update_profile"),
	path('login/', views.login_view, name="login"),
	path('register/', views.register, name="register"),
	path('logout/', views.logout_view, name="logout"),
	path('<int:todoitem_id>/update', views.update_task, name="update_task"),
	path('<int:todoitem_id>/delete', views.delete_task, name="delete_task")
]	
