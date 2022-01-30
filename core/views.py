from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from core.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from core.models import Profile, Sales
import pandas as pd
from django.shortcuts import get_object_or_404



def insert_data_in_sales_model(data: list, user_id):
    """This function is an helper function for inserting the data in to the sales model.

    Args:
        data: list = list of dictionory which have the sales data (Required)
        user_id: int = user which owns that sales data (Required)
    
    """
    user = get_object_or_404(User, id=user_id) # getting the user to which i have to update the sales data
    for row in data:
        row['user'] = user
        Sales.objects.create(**row)

    return "Data has been inserted successfully...."

# Create your views here.

def create_user(request):
    """Django view function for create or adding new sales user in to the database.
    Args:
        request: WSGI (Required)
    """
    data = request.POST
    username = data.get("username", None)
    password = data.get("password", None)

    if username != None and password != None:
        # this is creating new user in db.
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        # Getting the user profile and updating the profile by user data.
        profile = Profile.objects.get(user=user)
        profile.age = data.get('age', None)
        profile.gender = data.get('gender', None)
        profile.city = data.get('city', None)
        profile.country = data.get('country', None)
        profile.save()
        return HttpResponse("<h1>User is created</h1>")

    form = UserForm()
    data = {
        "user_form": form
    }

    return render(request, 'core/create_user.html', data)


def update_the_user(data: dict, profile: Profile):
    """helper function for updating the user

    Args:
        data: dict = request.POST data is here (required)
        profile: Profile = profile of user (required)
    """
    
    form = ProfileForm(data, instance=profile)
    if form.is_valid():
        form.save()
        return True
    print(form.errors)
    return False


def update_sales_data(csv_file, user_id):
    dict_data = pd.read_csv(csv_file).to_dict('records') # converting the csv to python dict
    insert_data_in_sales_model(dict_data, user_id)
    return True



def update_user(request, user_id):
    """Django view for updating the user information and also updating the sales data of user using csv file.
    Args:
        request: WSGI = (Required) 
        user_id: int = User that we want to update (Required)
    """
    user = User.objects.get(id=user_id) # get the user from database using user id
    profile = Profile.objects.get(user=user) # get the profile of perticular user


    form = ProfileForm(instance=profile)
    if request.method == "POST":

        if request.POST.get("user_submit", None) == 'user_form':
            if update_the_user(request.POST, profile):
                return redirect('update-user', user_id=user_id)
            else:
                return HttpResponse("Something went worng...")
        else:
            csv_file = request.FILES.get("sales_file")  # getting the csv file...
            update_sales_data(csv_file, user_id)
            return HttpResponse("sales data is updated")

    context = {"user": user, "user_profile": profile, "profile_form": form}
    return render(request, 'core/update_user.html', context)



def list_sales_user(request):
    users = Profile.objects.all()
    context = {"users": users}
    return render(request, 'core/user_list.html', context)