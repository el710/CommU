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
## last search word at index.html
index_search = None
public_dealers = None



WORK_PATH = os.path.join(os.getcwd(), "static")

def make_searching_data(search):
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
        function make index.html
    '''
    global index_search

    ## make dictionary of args for page
    def_context = {} 

    ## find out what item about need to show info; format: <type>=<name>
    if args:
        try:
            item = str.split(args,'=')
            logging.info(f"about detail {item} {len(item)}\n")

            if len(item) == 2:
                info = []
                match(item[0]):
                    case "skill":
                        skill = USkill(None, item[1])
                        skill.load_template(WORK_PATH)
                        for key, value in skill.json().items():
                            if (value != None) and (isinstance(value, str) and len(value) or not isinstance(value, str)):
                                logging.info(f"make dict of object: {key} : {value}")
                                info.append(f"{key}: {value}")
                    # case "user": 
                    # case "contract":
                    # case "project":

                logging.info(f"add object's info: {info}")
                if len(info):
                    def_context.update({"about_type": item[0], "about_name": item[1], "about_value": info, "about_link": f"{item[0]}/{item[1]}"})
        except Exception as exc:
            logging.info(f"wrong item info {args} {exc}\n")

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
            def_context.update(make_searching_data(index_search))
    else:
        ## show last searching results
        def_context.update(make_searching_data(index_search))
        def_context.update({'form': TaskForm()})

    logging.info(f"search {index_search} ")
    def_context.update({"index_search": index_search})    
 
    return render(request, 'index.html', context=def_context)


def show_userpage(request):
    """
        This function shows user's page
    """
    global local_user

    USkill.load_public_skills("static")
    logging.info(f"show_userpage(): {USkill.get_public_skills()}")
    def_context = {'public_skills': USkill.get_public_skills()}
        
    logging.info(f"\nshow_userpage(): user {local_user}")
    if local_user:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.work_project
                        })
    

    logging.info(f"\nshow_userpage(): method {request.method} ")



    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['new_task']
         
            ## find skill templates    
            skill = USkill(local_user, task)
    
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
                
            if public_dealers:
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

    if local_user:
        return render(request, 'userpage.html', context=def_context)
    
    return redirect('/')

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
    global local_user

    logging.info(f'\ncrud_skill(): open skill: {args}')

    def_context={"local_user": local_user}

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
