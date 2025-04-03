from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm)

from django.contrib.staticfiles import finders


# Create your views here.


from upack.uproject import *
from upack.user import UUser


import logging
import os

""" Operating Data"""
local_user = None
## last search word at index.html
index_search = None
public_dealers = None



WORK_PATH = os.path.join(os.getcwd(), "static")

def make_searching_data(search):
    '''
        Search Uitem by 'search' word 
        Return Uitem info as dict()
    '''
    context = {}

    if search:
        ## find skill templates    
        skill = USkill(local_user, search)
        if skill.load_template(WORK_PATH):
            context.update({"skills": [skill.get_slug_name()] })
            logging.info(f"has found skill {skill.get_slug_name()}")
        else:
            context.update({"skills": None})
            
        ## find project templates
        project = UProject(local_user, search)
        _path = finders.find(project.get_file_name())
        if project.load_template(_path):
            context.update({"project": index_search})
        else:
            context.update({"project": None})

        ## find public contacts
        user_dealers_list = []
        if local_user != None:
            if isinstance(local_user, UUser):
                user_dealers_list.append(local_user.partners)
                
        if public_dealers:
            user_dealers_list.append(public_dealers)
                
        if len(user_dealers_list):
            context.update({"dealers": user_dealers_list})
        else: 
            context.update({"dealers": None})    
        
    return context


def show_index(request, args=None):
    '''
        Make index.html
        args: Uitems to view info {skill, contract, project}
    '''
    global local_user, index_search

    ## make dictionary of args for page
    def_context = {} 

    ## add 'about' data of searching result
    def_context.update(get_uitem_info(args, filepath=WORK_PATH))


    ## Make list of public skills
    USkill.load_public_skills("static")
    logging.info(f"show_index(): {USkill.get_public_skills()}")
    def_context.update({'public_skills': USkill.get_public_skills()})
    

    logging.info(f"method {request.method} ")
    if request.method == "POST":

        ## check up searching field
        form = TaskForm(request.POST)
        if form.is_valid():
            ##remember search
            index_search = form.cleaned_data['new_task']
    else:    
        def_context.update({'form': TaskForm()})

    '''
        Variable part of page constractor
    '''
    logging.info(f"user {local_user}\n")
    if local_user:          
        return redirect('/user/')
    '''
        End of variable part of page constractor
    '''  

    ## show new or last searching results
    def_context.update(make_searching_data(index_search))
    
    logging.info(f"search {index_search} ")
    def_context.update({"index_search": index_search})    
 
    return render(request, 'index.html', context=def_context)


def show_userpage(request, args=None):
    """
        This function shows user's page
    """
    global local_user

    ## make dictionary of args for page
    def_context = {}

    ## add 'about' data as searching result
    def_context.update(get_uitem_info(args, filepath=WORK_PATH))

    USkill.load_public_skills("static")
    logging.info(f"{USkill.get_public_skills()}\n")
    def_context.update({'public_skills': USkill.get_public_skills()})

    logging.info(f"method {request.method} ")
    if request.method == "POST":
        ## check up searching field
        form = TaskForm(request.POST)
        if form.is_valid():
            ##remember search
            local_user.search = form.cleaned_data['new_task']
    else:
        def_context.update({'form': TaskForm()})

    '''
        Variable part of page constractor
    '''
    logging.info(f"user {local_user}\n")
    if local_user:          
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })
    else:
        return redirect('/')
    '''
        End of variable part of page constractor
    '''    

    ## show new or last searching results
    def_context.update(make_searching_data(local_user.search))

    logging.info(f"search {local_user.search} ")
    def_context.update({"index_search": local_user.search})    

    return render(request, 'userpage.html', context=def_context)


def show_info(request, args=None):
    '''
        Make info pages depends on
        args: 'about', 'terms', 'laws', 'rules'  .html
    '''
    global local_user

    ## make dictionary of args for page
    def_context = {}

    logging.info(f"user {local_user}\n")
    if local_user:          
        def_context.update({"local_user": local_user.nickname})
    
    if args == 'terms':
        page = 'terms.html'
    elif args == 'laws':
        page = 'laws.html'
    elif args == 'rules':
        page = 'rules.html'
    else:
        page = 'about.html'

    return render(request, page, context=def_context)



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
            return redirect('/user/') 
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
            local_user = UUser(name)
            return redirect('/user/') 
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
            

def crud_skill(request, args=None):
    '''
        Make data about skill
        args: <name> - show CRUD page - skill.html
    '''
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user}\n')

    def_context = {}

    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })

    if args:
        new_skill = USkill(owner_id=local_user, name=args)
        new_skill.load_template()
        def_context.update({"skill_name": new_skill.name,
                            "skill_resources": new_skill.resources,
                            "skill_desc": new_skill.description,
                            "skill_goal": new_skill.goal,
                            "skill_public": new_skill.public,
                            "skill_author": new_skill.author
                            })
        logging.info(f"load template {def_context}\n")

    
    if request.method == "POST":
        form = SkillForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
            skill_name = form.cleaned_data['skill_name']
            skill_resources = form.cleaned_data['skill_resources']
            skill_desc = form.cleaned_data['skill_desc']
            skill_goal = form.cleaned_data['skill_goal']
            skill_public = form.cleaned_data['skill_public']
            skill_author = form.cleaned_data['skill_author']

            new_skill = USkill(owner_id=local_user.nickname,
                               name=skill_name,
                               goal=skill_goal,
                               description=skill_desc,
                               resources=skill_resources)
            if skill_public:
                new_skill.set_public(skill_author)
            
            if request.POST.get('delete'):
                new_skill.delete_template(WORK_PATH)
            else:
                new_skill.save_as_template(True, WORK_PATH)
            
            if local_user:
                return redirect("/user/")
            else:
                return redirect("/")
     
    else:
        form = SkillForm(request.POST)
    
    def_context.update({"form": form})
    
    return render(request, "skill.html", context=def_context)


def crud_contract(request, args=None):
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user}\n')

    def_context = {}

    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })

    if args:
        logging.info(f"\ncrud_skill(): load template {def_context} ")

    
    if request.method == "POST":
        
        if local_user:
            return redirect("/user/")
        else:
            return redirect("/")
    
    return render(request, "index_temp.html", context=def_context)


def crud_project(request, args=None):
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user}\n')

    def_context = {}

    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })

    if args:
        logging.info(f"\ncrud_skill(): load template {def_context} ")

    
    if request.method == "POST":
        
        if local_user:
            return redirect("/user/")
        else:
            return redirect("/")
    
    return render(request, "index_temp.html", context=def_context)


def crud_event(request, args=None):
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user}\n')

    def_context = {}

    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })

    if args:
        logging.info(f"load template {args}\n")

    
    if request.method == "POST":
        form = SkillForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
            ## take data

            if request.POST.get('set'):
                pass
            elif request.POST.get('delete'):
                pass

            
            if local_user:
                return redirect("/user/")
            else:
                return redirect("/")
     
    else:
        form = SkillForm(request.POST)
    
    def_context.update({"form": form})
    
    return render(request, "event.html", context=def_context)