from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader 
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.utils import timezone

# We import the built-in 'User' model to be able to do operations to the built-in Users table from Django.
from django.contrib.auth.models import User
from .models import ToDoItem, EventItem
from .forms import LoginForm, AddTaskForm, UpdateTaskForm, AddEventForm

# Create your views here.
def index(request):
	todoitem_list = ToDoItem.objects.filter(user_id=request.user.id)
	eventitem_list = EventItem.objects.filter(user_id=request.user.id)
	
	template = loader.get_template('todolist/index.html')
	context = {
		'todoitem_list': todoitem_list,
		'eventitem_list': eventitem_list,
		'user': request.user
	}

	return HttpResponse(template.render(context, request))

	# You can also render a template using this way
	# return render(request, "todolist/index.html", context)

def todoitem(request, todoitem_id):
	# 'model_to_dict' function translates a data model into a python dictionary (object). This is so that we can use the data as a regular object/dictionary.
	todoitem = get_object_or_404(ToDoItem, pk=todoitem_id)

	# try: 
	# 	todoitem = model_to_dict(ToDoItem.objects.get(pk=todoitem_id))
	# except ToDoItem.DoesNotExist:
	# 	return HttpResponse("Error: Task Not Found")

	return render(request, "todolist/todoitem.html", model_to_dict(todoitem))

	# ACTIVITY (until 9:35PM)
	# 1. Create a todoitem template
	# 2. In the template, show the 'task_name', 'description', 'status' of the todo item. (each enlosed in an HTML tag)
	# 3. At the end of the template, create an anchor tag that will return the user to the 'index' page


def eventitem(request, eventitem_id):

	eventitem = get_object_or_404(EventItem, pk=eventitem_id)

	return render(request, "todolist/eventitem.html", model_to_dict(eventitem))


def register(request):
	users = User.objects.all()
	is_user_registered = False
	
	# Loops through each existing user and checks if they already exist in the table
	for individual_user in users:
		if individual_user.username == "johndoe":
			is_user_registered = True
			break

	# The context 'is_user_registered' is put after the for loop in order for it to get the updated value if 'for' loop above equals to True.
	context = {
		"is_user_registered": is_user_registered
	}

	if is_user_registered == False:
		# 1. Creating a new instance of the User model.
		user = User()

		# 2. Assign data values to each property of the model.
		user.username = "johndoe"
		user.first_name = "John"
		user.last_name = "Doe"
		user.email = "john@mail.com"
		user.set_password("john1234")
		user.is_staff = False
		user.is_active = True

		# 3. Save the new instance of a user into the database.
		user.save()

		# The context will be the data to be passed to the template
		context = {
			"first_name": user.first_name,
			"last_name": user.last_name
		}

	return render(request, "todolist/register.html", context)

def change_password(request):
	is_user_authenticated = False

	user = authenticate(username="johndoe", password="john1234")

	if user is not None:
		authenticated_user = User.objects.get(username="johndoe")

		authenticated_user.set_password("johndoe1")
		authenticated_user.save()

		is_user_authenticated = True

	context = {
		"is_user_authenticated": is_user_authenticated
	}

	return render(request, "todolist/change_password.html", context)

def login_view(request):
	context = {}

	if request.method == 'POST':
		# request.POST contains all the fields coming from the Login.html form
		form = LoginForm(request.POST)

		if form.is_valid() == False:
			form = LoginForm()

		else:
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)

			context = {
				"username": username,
				"password": password
			}

			if user is not None:
				# The 'login' function saves the user's ID in Django's session. The request will be the one that handles the user's data and we can access the user by using 'request.user'.
				login(request, user)
				return redirect("todolist:index")
			else:
				context = {
					"error":  True
				}

	return render(request, "todolist/login.html", context)

def logout_view(request):
	logout(request)
	return redirect("todolist:index")


def add_task(request):
	context = {}

	if request.method == 'POST':
		form = AddTaskForm(request.POST)

		if form.is_valid() == False:
			form = AddTaskForm()

		else:
			task_name = form.cleaned_data['task_name']
			description = form.cleaned_data['description']

			duplicates = ToDoItem.objects.filter(task_name=task_name)

			if not duplicates:
				ToDoItem.objects.create(
					task_name=task_name,
					description=description,
					date_created=timezone.now(),
					user_id=request.user.id
				)

				return redirect('todolist:index')

			else:
				context = {
					"error": True
				}

	return render(request, "todolist/add_task.html", context)


def update_task(request, todoitem_id):
	# Returns a queryset
    todoitem = ToDoItem.objects.filter(pk=todoitem_id)

    context = {
        "user": request.user,
        "todoitem_id": todoitem_id,
        # Accessing the first element is necessary because the "ToDoItem.objects.filter()" method returns a queryset
        "task_name": todoitem[0].task_name,
        "description": todoitem[0].description,
        "status": todoitem[0].status
    }

    if request.method == 'POST':

        form = UpdateTaskForm(request.POST)

        if form.is_valid() == False:

            form = UpdateTaskForm()

        else:

            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            
            if todoitem:

                todoitem[0].task_name = task_name
                todoitem[0].description = description
                todoitem[0].status = status

                todoitem[0].save()
                return redirect("todolist:index")

            else:

                context = {
                    "error": True
                }

    return render(request, "todolist/update_task.html", context)


def delete_task(request, todoitem_id):
    todoitem = ToDoItem.objects.filter(pk=todoitem_id)

    todoitem.delete()

    return redirect("todolist:index")



def add_event(request):
	context = {}

	if request.method == 'POST':
		form = AddEventForm(request.POST)

		if form.is_valid() == False:
			form = AddEventForm()

		else:
			event_name = form.cleaned_data['event_name']
			description = form.cleaned_data['description']

			duplicates = EventItem.objects.filter(event_name=event_name)

			if not duplicates:
				EventItem.objects.create(
					event_name=event_name,
					description=description,
					# event_date=timezone.now() + timedelta(days=1),
					user_id=request.user.id
				)

				return redirect('todolist:index')

			else:
				context = {
					"error": True
				}

	return render(request, "todolist/add_event.html", context)



def update_profile(request):


    return redirect("todolist:index")

