from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm, EventForm)

from django.contrib.staticfiles import finders


# Create your views here.


# from upack.uproject import *
from uproject.models.user import *
from uproject.models.bases import UtemBase
from uproject.models.project import UProject
from uproject.models.contract import UContract
from uproject.models.skill import USkill

from uproject.utils.utils import *

from uproject.storage.filestorage import FileStorage


import logging
import os
from datetime import datetime


""" Operating Data"""
## There is always a user - by define 'Guest'


public_skills = None
public_contracts = None
public_projects = None


WORK_PATH = os.path.join(os.getcwd(), "file_store")

local_user = UUser(GUEST_USER)
local_user.init_storage(FileStorage(WORK_PATH))

def show_index(request):
    global local_user

    ## dictionary of args for HTML page
    def_context = {}

    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname})

    return render(request, 'index.html', context = def_context)


def show_user(request, args=None):
    '''
        Make main.html
        args: Utem has taken from list to view info {skill, contract, project}
    '''
    global local_user

    ## dictionary of args for HTML page
    def_context = {}

    ## if no user
    if not local_user.commu_id:
        return redirect("/")

    # logging.info(f'local user: {local_user}\n')

    logging.info(f"method {request.method} ")
    if request.method == "POST":
        ## POST by search 
        ## check up searching field
        form = TaskForm(request.POST)
        if form.is_valid():
            ##remember search
            local_user.search = form.cleaned_data['new_task']
    else:    
        def_context.update({'form': TaskForm()})

    '''
        Perform arguments
    '''
    logging.info(f'get utem: {args}\n')
    ## Close utem's info
    if args == "close":
        local_user.temp_utem = None
        return redirect("/user/")

    '''
        Prepare to show Utem attributes
    '''
    ## load info of choosen utem
    if args: ## new utem has choosen
        utem_type, utem_name = parse_link(args)

        logging.info(f'{utem_type}: {utem_name}\n')
        for cls, label in [(USkill, "uskill"), (UContract, "ucontract"), (UProject, "uproject")]:
            if utem_type == label:
                local_user.temp_utem = cls(utem_name)

        if local_user.temp_utem:
            load = FileStorage(WORK_PATH).load(local_user.temp_utem)
            logging.info(f"Load utem: {load} ")
            if not load:
                local_user.temp_utem = None

    logging.info(f'local user utem: {local_user.temp_utem}\n')            

    ## add data of choosen utem
    if local_user.temp_utem:
        def_context.update(get_utem_info(local_user.temp_utem))
        logging.info(f"Context: {def_context} ")

        if isinstance(local_user.temp_utem, USkill):
            def_context.update({"edit_link": "/skill/temp"})
            def_context.update({"add_link": "/event/"})

        if isinstance(local_user.temp_utem, UContract):
            pass
        if isinstance(local_user.temp_utem, UProject):
            pass
    

    '''
        Fill user's info
    '''
    ## if real user
    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname})
        def_context.update({"user_staff": get_project_tree(local_user)})


    '''
        load search result
    '''
    # logging.info(f"search {local_user.search} ")
    def_context.update({"index_search": local_user.search})
    ## show new or last searching results
    if local_user.search:
        def_context.update(find_utems(key_name=local_user.search, path=WORK_PATH))

    '''
        Load public utems
    '''
    ## Make list of public skills
    public_skills = find_public_skills(WORK_PATH)
    logging.info(f"founded skills: {public_skills}\n")
    # print(make_skill_context(public_skills))
    def_context.update({'public_skills': make_skill_context(public_skills, WORK_PATH)})

    
    logging.info(f"Context: {def_context} ")
    return render(request, 'main.html', context=def_context)


def show_info(request, args=None):
    '''
        Make info pages depends on
        args: 'about', 'terms', 'laws', 'rules'  .html
    '''
    global local_user

    ## dictionary of args for HTML page
    def_context = {}
    
    if local_user.commu_id:
        def_context = {"local_user": local_user.nickname}
   
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

            '''
                In base we looking for user by hash - no passwords

            '''
            # if password == repassword:
            ## if no such user
            local_user = UUser(name)
            ## hash for real user
            local_user.commu_id = hash(local_user.nickname)
            '''
                Save In base user by hash - no passwords

            '''            
            logging.info(f'new user: {local_user}')

            local_user.init_utem_base(UtemBase(), root=UProject(local_user, "Life"))

            local_user.init_storage(FileStorage(WORK_PATH))
            
            
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
            ## hash for real user
            local_user.commu_id = hash(local_user.nickname)
            '''
                Save In base user by hash - no passwords

            '''            
            logging.info(f'new user: {local_user}')

            local_user.init_utem_base(UtemBase(), root=UProject(local_user, "Life"))

            local_user.init_storage(FileStorage(WORK_PATH))
            return redirect('/user/') 
            # else:
            #     def_context.update({'passstate': "... passwords is not equal. Try again."})

    else:
        form = SignUpForm()  ## form is a html-template that django try to find in html page by name
        
    def_context = {'form': form}
    return render(request, 'login.html', context=def_context )


def logout(request):
    global local_user

    local_user = UUser(GUEST_USER)
    return redirect('/')
    # return render(request, 'index.html')        
            

def crud_skill(request, args=None):
    '''
        make Skill's page for C.R.U.D. in skill.html 
        args: None - create new skill
              'temp' - work with local_user.temp_  skill
              'event' - open event(skill+schedule) from user's project
    '''
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user}\n')

    ## don't open skill page for none
    # if args == None: return redirect("/")

    def_context = {}

    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname})
    else:
        return redirect("/")


    if args == 'temp': 
        if local_user.temp_utem:
            def_context.update(local_user.temp_utem.to_dict())
        logging.info(f"load template {def_context}\n")
    # elif args == "event":
    #     if hasattr(local_user, 'pro_event') and local_user.pro_event:
    #         def_context.update(local_user.pro_event.to_dict())
        
    
    logging.info(f" method: {request.method} cont: {request.POST}\n")
    if request.method == "POST":
        if request.POST.get('delete'):
            if hasattr(local_user, 'storage'):
                local_user.storage.delete(local_user.temp_utem)
            local_user.temp_utem = None
            return redirect("/user/")

        elif request.POST.get('save'):
            form = SkillForm(request.POST)
            
            logging.info(f"valid POST {form.is_valid()} \n")
            logging.info(f'data: {form.cleaned_data}\n')
            
            if form.is_valid(): ## is_valid also makes cleaned_data
                skill_name = form.cleaned_data['skill_name']
                skill_desc = form.cleaned_data['skill_desc']
                skill_resources = form.cleaned_data['skill_resources']
                skill_goal = form.cleaned_data['skill_goal']
                skill_public = form.cleaned_data['skill_public']

                local_user.temp_utem = USkill(name=skill_name,
                                              resources=skill_resources,
                                              description=skill_desc,
                                              goal=skill_goal)
                
                local_user.temp_utem.sign(author=local_user.nickname,
                                          geosocium=local_user.geosocium,
                                          public=skill_public
                                         )
                logging.info(f"new skill {local_user.temp_utem}")
                
                if hasattr(local_user, 'storage'):
                    local_user.storage.save(local_user.temp_utem)
                return redirect("/user/")
        else:
            form = SkillForm(request.POST)
            logging.info(f"POST failed\n")
        
    else:
        form = SkillForm(request)
    
    def_context.update({"form": form})
    
    return render(request, "skill.html", context=def_context)


def crud_contract(request, args=None):
    '''
        Make contract.html
        args: none - create, UContract
    '''
    global local_user

    ## dictionary of args for HTML page
    def_context = {}

    ## if no user
    if not local_user.commu_id: return redirect("/")
    else:
        def_context.update({"local_user": local_user.nickname})

    if args == None: ## create(add) 
        logging.info(f'create contract\n')


    else:  ## read & edit event
        utem_type, utem_id = parse_link(args)
        logging.info(f'get contract {utem_type}, {utem_id}\n')
  
    logging.info(f"request.method {request.method} \n")

    if request.method == "POST":
        form = EventForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
        
            if request.POST.get('set'):
               
                return redirect('/user/')
            elif request.POST.get('delete'):
                
                return redirect('/user/')
                
    else:
       form = EventForm()
        
    def_context.update({"form": form})
    

    
    return render(request, "contract.html", context=def_context)


def crud_project(request, args=None):
    '''
        Make project.html
        args: none - create, UContract
    '''
    global local_user

    ## dictionary of args for HTML page
    def_context = {}

    ## if no user
    if not local_user.commu_id: return redirect("/")
    else:
        def_context.update({"local_user": local_user.nickname})
    
    return render(request, "index_temp.html", context=def_context)


def crud_event(request, args=None):
    global local_user

    logging.info(f'open skill: {args}\n')
    logging.info(f'local user: {local_user.nickname}\n')

    if local_user.commu_id == None:
        return redirect("/")

    '''
        def_context has parameters to show end form to change parameters
    '''
    def_context = {}
    
    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname,
                            "user_root": local_user.root_utem.get_title()
                          })
        # if local_user.pro_contract:
        #     def_context.update({"user_contract": local_user.pro_contract})

    
    if args == None: ## create(add) event
        logging.info(f'create event\n')

        def_context.update({"user_skill": local_user.temp_utem.name})

        now = datetime.now(tz=local_user.timezone)
        
        start_date_day = f"{now.day:02d}"
        start_date_month = f"{now.month:02d}"
        start_month_name = now.strftime("%B")
        start_date_year = now.year
        start_weekday = now.weekday()

        end_date = f"{now.year}-{now.month:02d}-{now.day:02d}"
        start_time = f"{now.hour:02d}:{now.minute:02d}"

    else:  ## read & edit event
        utem_type, utem_id = parse_link(args)
        logging.info(f'get event {utem_type}, {utem_id}\n')
        
        ## !!! take from user
        item = local_user.utems.read(utem_id)
        if item:
            logging.info(f'find event {item}\n')
            
            local_user.pro_event = item
            def_context.update({"user_skill": local_user.pro_event.name})

            now = datetime(year=2025, month=1, day=1, hour=8, minute=0, tzinfo=local_user.timezone)

        start_date_day = f"{now.day:02d}"
        start_date_month = f"{now.month:02d}"
        start_month_name = now.strftime("%B")
        start_date_year = now.year
        start_weekday = now.weekday()

        end_date = f"{now.year}-{now.month:02d}-{now.day:02d}"
        start_time = f"{now.hour:02d}:{now.minute:02d}"
    # else:
        # logging.info(f"wrong args to crud_event {args}\n")


    logging.info(f"request.method {request.method} \n")
    if request.method == "POST":
        form = EventForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
        
            if request.POST.get('set'):
                local_user.temp_utem.set_event(local_user, form.cleaned_data)
                local_user.add_utem(local_user.temp_utem)
                
                                
                logging.info(f'exit by set\n')
                return redirect('/user/')
            elif request.POST.get('delete'):
                ## delete skill from current project
                ## !!! FIRST check parents (project, contract) state !!!
                ## skill._event = None
                ## skill._state = 'template'

                logging.info(f'exit by delete\n')
                return redirect('/user/')
                
    else:
       form = EventForm()
        

    def_context.update({"form": form})
    def_context.update({"start_date_day": start_date_day,
                        "start_date_month": start_date_month,
                        "start_month_name": start_month_name,
                        "start_date_year": start_date_year,
                        "start_weekday": start_weekday,
                        "end_date": end_date,
                        "start_time": start_time,
                        "end_time": start_time
                        })

    logging.info(f"def_context {def_context} \n")

    return render(request, "event.html", context=def_context)