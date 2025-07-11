### sprint 06/06 backlog

+ refactoring project structure
+ rename 06_06_sprint branch to main
+ delete 06_06_sprint branch
+ delete in .git/config double records about main branch
+ git pull --set-upstream origin main
+ checkout git

- finish user authorization (MU.md sprint)
+1: checkout django.contrib.auth config:
  + Django INSTALLED_APPS by default
  + Django MIDDLEWARE includes
+2: Run Migrations
    python manage.py makemigrations
    python manage.py migrate
3: Implement Basic User Login/Logout
  + add django urls path('accounts/', include('django.contrib.auth.urls'))
  + Update your settings.py for login/logout redirects:
      LOGIN_REDIRECT_URL = '/user/' # Redirect to homepage after successful login
      LOGOUT_REDIRECT_URL = '/' # Redirect to homepage after successful logout
      LOGIN_URL = '/accounts/login/' # Where to redirect users if they try to access a login-required page
  + checkout signup.html  with Django {{ form.as_p }}
  + view signup.html with:
    form = UserCreationForm()"
    user = form.save()
    login(request, user) # Log the user in immediately after registration
  + add django logout method
  + add django login form & use embedded view
  + local_user staff init in dashboard view
  !!! after reload server local_user disapperes and request.user stays
      need to base local_user.init on request.user



  + UI signup
  - make DataBase for users
  - add checkout users files - find user_id.ptp at signup & login
  
- check out existance of utems in projects and contracts accorded with files
- only project can be root - choosen project becomes root

- finish event functionality

- different between template and work utems
    status devides temp & work, all links are saved as names as the same

Next sprint
- contruct CRUD
  - switch credit/debit in contract