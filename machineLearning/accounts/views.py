from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import joblib
import pandas as pd





reloadModel = joblib.load('./models/carPrice.pkl')

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    
    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists(): 
                messages.info(request,'username exists')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'email id exists')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                user.save();
                print('user created')
                return redirect('login')
            
        else:
            messages.info(request,'password does not match')
            return redirect('register')
        return redirect('/')

    else:
        return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
    

    
def price(request):
    if request.method == 'POST':
        temp = {}
        temp['fueltype'] = request.POST['fueltype']
        temp['aspiration'] = request.POST['aspiration']
        temp['carbody'] = request.POST['carbody']
        temp['drivewheel'] = request.POST['drivewheel']
        temp['enginelocation'] = request.POST['enginelocation']
        temp['wheelbase'] = request.POST['wheelbase']
        temp['carlength'] = request.POST['carlength']
        temp['carwidth'] = request.POST['carwidth']
        temp['curbweight'] = request.POST['curbweight']
        temp['enginetype'] = request.POST['enginetype']
        temp['cylindernumber'] = request.POST['cylindernumber']
        temp['enginesize'] = request.POST['enginesize']
        temp['boreratio'] = request.POST['boreratio']
        temp['horsepower'] = request.POST['horsepower']
        temp['highwaympg'] = request.POST['highwaympg']
        testData=pd.DataFrame(temp,index=['x'])
        predPrice = reloadModel.predict(testData)[0]
        values = {'price':predPrice}
        print(predPrice)
        return render(request,'price.html',values)
    else:
        return render(request,'price.html')