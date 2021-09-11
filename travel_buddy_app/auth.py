from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import Users

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/register")
    
def login(request):
    if request.method == "POST":
        user = Users.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "username": log_user.username,
                    "email": log_user.email
                }

                request.session['user'] = user
                messages.success(request, "Login Successful.")
                return render(request, 'index.html')
            else:
                messages.error(request, "Email or password is wrong")
        else:
            messages.error(request, "Email or password is wrong")

        return redirect('/register')
    else:
        return render(request, 'register.html')


def register(request):
    if request.method == "POST":

        errors = Users.objects.validate(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['name'] =  request.POST['name']
            request.session['username'] =  request.POST['username']
            request.session['email'] =  request.POST['email']

        else:
            request.session['name'] = ""
            request.session['username'] = ""
            request.session['email'] = ""

            password_encrypt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            new_user = Users.objects.create(
                name = request.POST['name'],
                username = request.POST['username'],
                email=request.POST['email'],
                password = password_encrypt,
            )

            messages.success(request, "User successfully created")
            
            request.session['user'] = {
                "id" : new_user.id,
                "username": f"{new_user.username}",
                "email": new_user.email
            }
            return redirect("/")

        return redirect("/register")
    else:
        return render(request, 'register.html')
