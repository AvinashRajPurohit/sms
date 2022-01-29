from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from core.forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from core.models import Profile, Sales
import pandas as pd
from django.shortcuts import get_object_or_404



def insert_data_in_sales_model(data: list, user_id):
    """
    This function will insert data in sales model
    """
    user = get_object_or_404(User, id=user_id) # getting the user to which i have to update the sales data
    for row in data:
        row['user'] = user
        Sales.objects.create(**row)

    return "Data has been inserted successfully...."

# Create your views here.

def create_user(request):
    print(request.POST)
    data = request.POST
    username = data.get("username", None)
    password = data.get("password", None)

    if username != None and password != None:
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        print("user is created")
        profile = Profile.objects.get(user=user)
        profile.age = data.get('age', None)
        profile.gender = data.get('gender', None)
        profile.city = data.get('city', None)
        profile.country = data.get('country', None)
        profile.save()
        print("profile is save")
        return HttpResponse("<h1>User is created</h1>")
    form = UserForm()
    data = {
        "user_form": form
    }
    return render(request, 'core/create_user.html', data)




def update_user(request, user_id):
    user = User.objects.get(id=user_id) # get the user from database using user id
    profile = Profile.objects.get(user=user) # get the profile of perticular user
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        if request.POST.get("user_submit", None) == 'user_form':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('update-user', user_id=user_id)
            else:
                print(form.errors)
        else:
            print(request.FILES)
            print(request.POST)
            csv_file = request.FILES.get("sales_file")  # getting the csv file...
            print(csv_file)
            dict_data = pd.read_csv(csv_file).to_dict('records') # converting the csv to python dict
            insert_data_in_sales_model(dict_data, user_id)
            return HttpResponse("sales data is updated")
    context = {"user": user, "user_profile": profile, "profile_form": form}
    return render(request, 'core/update_user.html', context)



def list_sales_user(request):
    users = Profile.objects.all()
    context = {"users": users}
    return render(request, 'core/user_list.html', context)