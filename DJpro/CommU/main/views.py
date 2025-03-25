from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm)

from django.contrib.staticfiles import finders


# Create your views here.


from upack.uproject import USkill, UProject
from upack.user import UUser


import logging
import os

""" Operating Data"""
local_user = None
public_dealers = []


def show_title(request):
    global local_user
    """
        This function shows main title Web page
    """
    
    logging.info(f"\nshow_title(): user {local_user}")
    logging.info(f"\nshow_title(): method {request.method} ")

    def_context = {"local_user": local_user}

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['new_task']
         
            ## find skill templates    
            skill = USkill(local_user, task)
            _path = finders.find(skill.get_file_name())
    
            if skill.load_template(_path):
                def_context.update({"skills": [skill.get_slug_name()] })
                logging.info(f"show_title(): has found skill {skill.get_slug_name()}")
            else:
                def_context.update({"skills": None})
            
            ## find project templates
            project = UProject(local_user, task)
            _path = finders.find(project.get_file_name())
            if project.load_template(_path):
                def_context.update({"project": task})
            else:
                def_context.update({"project": None})

            ## find public dealers & user's contacts
            user_dealers_list = []
            if local_user != None:
                if isinstance(local_user, UUser):
                    user_dealers_list.append(local_user.partners)
                
            if len(public_dealers):
                user_dealers_list.append(public_dealers)
                
            if len(user_dealers_list):
                def_context.update({"dealers": user_dealers_list})
            else: 
                def_context.update({"dealers": None})
                
        else:
            task = None

        def_context.update({"task": task})
    else:
        def_context.update({'form': TaskForm()})

    USkill.load_public_skills("static")
    logging.info(f"show_title(): {USkill.get_public_skills()}")
    def_context.update({'public_skills': USkill.get_public_skills()})        
    
    if local_user == None:
        return render(request, 'index.html', context=def_context)
    else:
        return render(request, 'main.html', context=def_context)


def show_about(request):
    """
        This function shows about page
        with template - about.html
    """
    return render(request, 'about.html')

def show_terms(request):
    """
        This function shows terms page
        with template - terms.html
    """
    return render(request, 'terms.html')

def show_laws(request):
    """
        This function shows laws page
        with template - laws.html
    """
    return render(request, 'laws.html')

def show_rules(request):
    """
        This function shows rules page
        with template - rules.html
    """
    return render(request, 'rules.html')



def signup(request):
    global local_user
    """
        This function shows signup Web page
    """
    logging.info(f"\nsignup(): method {request.method} ")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
            
        logging.info(f"\nsignup(): valid POST {form.is_valid()} ")
        logging.info(f'\nsignup(): {form.cleaned_data}')

        if form.is_valid(): ## is_valid also makes cleaned_data
            name = form.cleaned_data['username']
            # password = request.POST.get("user_password")
            # repassword = request.POST.get("user_repassword")
            # email = form.cleaned_data['email']

            # print(f"ext_post(): POST: {name} {email} {password} {repassword} ")
            
            # if password == repassword:
            local_user = name
            return redirect('/') 
            # else:
            #     def_context.update({'passstate': "... passwords is not equal. Try again."})

    else:
        form = SignUpForm()  ## form is a html-template that django try to find in html page by name
        
    def_context = {'form': form}
    return render(request, 'signup.html', context=def_context )

def login(request):
    global local_user
    """
        This function shows login Web page
    """
    logging.info(f"\nlogin(): method {request.method} ")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
            
        logging.info(f"\nsignup(): valid POST {form.is_valid()} ")
        logging.info(f'\nsignup(): {form.cleaned_data}')

        if form.is_valid(): ## is_valid also makes cleaned_data
            name = form.cleaned_data['username']
            # password = request.POST.get("user_password")

            # print(f"ext_post(): POST: {name} {email} {password} ")
            
            # if password == repassword:
            local_user = name
            return redirect('/') 
            # else:
            #     def_context.update({'passstate': "... passwords is not equal. Try again."})

    else:
        form = SignUpForm()  ## form is a html-template that django try to find in html page by name
        
    def_context = {'form': form}
    return render(request, 'login.html', context=def_context )

def logout(request):
    global local_user

    local_user = None
    return redirect('/')
    # return render(request, 'index.html')        
            

def get_post_request(request):
    ## first enter to page
    if request.method == "GET":                          
        def_context = {
            "hist": "zero",
            "title": "Get & Post"
        } 
    elif request.method == 'POST':
        mess = request.POST.get("data", '')
        ## return HttpResponse(f"Get from user data: {mess}") ## simple output

        '''
            get data by html form's <name> 
        '''
        username = request.POST.get("username")
        password = request.POST.get("user_password")
        repassword = request.POST.get("user_repassword")
        age = request.POST.get("user_age")
        premium = request.POST.get("premium") == 'on'


        print(f"get_post_request(): {username} {password}-{repassword} {age} premium: {premium}")
        
        def_context = {
            "hist": mess,
            "title": "Get & Post"
        }

    return render(request, "post.html", context=def_context)
