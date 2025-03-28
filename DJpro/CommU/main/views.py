from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm)

from django.contrib.staticfiles import finders


# Create your views here.


from upack.uproject import USkill, UProject
from upack.user import UUser


import logging
import os

""" Operating Data"""
local_user = None
about_item = None
public_dealers = []


WORK_PATH = os.path.join(os.getcwd(), "static")


def show_title(request, about=None):
    global local_user, about_item

    """
        This function shows main title Web page
    """
    USkill.load_public_skills("static")
    logging.info(f"show_title(): {USkill.get_public_skills()}")
    def_context = {'public_skills': USkill.get_public_skills()}
        
    
    logging.info(f"\nshow_title(): user {local_user}")
    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })
        
    

    logging.info(f"\nshow_title(): method {request.method} ")
    logging.info(f"\nshow_title(): about {about} ")
    logging.info(f"\nshow_title(): about state {about_item} ")



    if about:
        item = str.split(about,'=')
        logging.info(f"\nshow_title(): about detail {item} ")
        if len(item) > 1:
            if item[0] == 'skill':
                about_item = {'skill': item[1]}
                logging.info(f"\nshow_title(): new about state {about_item} ")
                return redirect('/')
        else:
            about_item = None

    if about_item:
        for k, v in about_item.items():
            def_context.update({"about_type": k, "about_item": v})

    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['new_task']
         
            ## find skill templates    
            skill = USkill(local_user, task)
            ##_path = finders.find(skill.get_file_name())
    
            if skill.load_template(WORK_PATH):
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
            local_user = UUser(name)
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
            

def crud_skill(request, name=None):
    logging.info(f'\ncrud_skill(): open skill: {name}')

    def_context={}

    if name:
        new_skill = USkill(owner_id=local_user, name=name)
        new_skill.load_template()
        def_context.update({"skill_name": new_skill.name,
                            "skill_resources": new_skill.resources,
                            "skill_desc": new_skill.description,
                            "skill_goal": new_skill.goal,
                            "skill_public": new_skill.public,
                            "skill_author": new_skill.author
                            })
        logging.info(f"\ncrud_skill(): load template {def_context} ")

    
    if request.method == "POST":
        form = SkillForm(request.POST)

        logging.info(f"\ncrud_skill(): valid POST {form.is_valid()} ")
        logging.info(f'\ncrud_skill(): {form.cleaned_data}')

        if form.is_valid(): ## is_valid also makes cleaned_data
            skill_name = form.cleaned_data['skill_name']
            skill_resources = form.cleaned_data['skill_resources']
            skill_desc = form.cleaned_data['skill_desc']
            skill_goal = form.cleaned_data['skill_goal']
            skill_public = form.cleaned_data['skill_public']
            skill_author = form.cleaned_data['skill_author']

            new_skill = USkill(owner_id=local_user,
                               name=skill_name,
                               goal=skill_goal,
                               description=skill_desc,
                               resources=skill_resources)
            if skill_public:
                new_skill.set_public(skill_author)
            
            if request.POST.get('delete'):
                new_skill.delete_template(WORK_PATH)
            else:
                new_skill.save_as_template(True,WORK_PATH)
    
            return redirect("../")
     
    else:
        form = SkillForm(request.POST)
    
    def_context.update({"form": form})
    
    return render(request, "skill.html", context=def_context)
