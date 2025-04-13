from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm, EventForm)

from django.contrib.staticfiles import finders


# Create your views here.


from upack.uproject import *
from upack.user import UUser


import logging
import os
from datetime import datetime


""" Operating Data"""
## There is always a user - by define 'Guest'
local_user = UUser(GUEST_USER)

public_dealers = None

WORK_PATH = os.path.join(os.getcwd(), "static")

def show_index(request, args=None):
    '''
        Make index.html
        args: Utem has taken from list to view info {skill, contract, project}
    '''
    global local_user

    # logging.info(f'get utem: {args}\n')
    # logging.info(f'local user: {local_user}\n')

    ## dictionary of args for HTML page
    def_context = {}

    ## if real user
    if local_user.commu_id:
        def_context = {"local_user": local_user.nickname,
                       "user_project": local_user.projects[local_user.pro_project].name
                    }
    '''
        perform args
    '''
    # logging.info(f'local user utem: {local_user.temp_utem}\n')

    if args == "close":
        local_user.temp_utem = None
        return redirect("/")

    if args: ## new utem has choosen
        utem_type, utem_name = utemname_parse(args)

        # logging.info(f'{utem_type}: {type(USkill)} {type(UContract)} {type(UProject)} \n')

        if utem_type == type(USkill):
            local_user.temp_utem = USkill(utem_name)
        elif utem_type == type(UContract):
            local_user.temp_utem = UContract(utem_name)
        elif utem_type == type(UProject):
            local_user.temp_utem = UProject(utem_name)            
    
        # logging.info(f'local user utem: {local_user.temp_utem}\n')

        if not local_user.temp_utem.load_template(WORK_PATH):
            local_user.temp_utem = None

    ## add data of choosen utem
    if local_user.temp_utem:
        def_context.update(get_utem_info(local_user.temp_utem))
        if isinstance(local_user.temp_utem, USkill):
            def_context.update({"edit_link": "/skill/temp"})
            def_context.update({"add_link": "/event/"})

        if isinstance(local_user.temp_utem, UContract):
            pass
        if isinstance(local_user.temp_utem, UProject):
            pass


    ## Make list of public skills
    USkill.load_public_skills("static")
    # logging.info(f"loaded {USkill.get_public_skills()}")
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

    ## show new or last searching results
    def_context.update(find_utems(local_user.search, path=WORK_PATH, local_user=local_user, public_dealers=public_dealers))
    
    # logging.info(f"search {local_user.search} ")
    def_context.update({"index_search": local_user.search})

    # logging.info(f"Context: {def_context} ")
 
    return render(request, 'index.html', context=def_context)


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

            # print(f"ext_post(): POST: {name} {email} {password} {repassword} ")
            
            # if password == repassword:
            local_user = UUser(name)
            local_user.commu_id = hash(local_user.nickname)
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
            local_user = UUser(name)
            local_user.commu_id = hash(local_user.nickname)
            return redirect('/') 
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
    if args == None and local_user.commu_id == None:
        return redirect("/")

    def_context = {}

    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname})


    if args == 'temp': 
        def_context.update(local_user.temp_utem.json())
        logging.info(f"load template {def_context}\n")
    elif args == "event":
        def_context.update(local_user.pro_skill.json())
    
    
    if request.method == "POST":
        if request.POST.get('delete'):
            local_user.temp_utem.delete_template(WORK_PATH)
            local_user.temp_utem = None

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

                new_skill = USkill(name=skill_name,
                                   resources=skill_resources,
                                   description=skill_desc,
                                   goal=skill_goal)
                
                if local_user.temp_utem == None or local_user.work_skill != new_skill:
                    local_user.temp_utem = new_skill
                    local_user.temp_utem.update(author=local_user.nickname,
                                                 geosocium=local_user.geosocium,
                                                 public=skill_public
                                                )
                    logging.info(f"new skill {local_user.temp_utem}")
                    local_user.temp_utem.save_as_template(True, WORK_PATH)
            
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
    logging.info(f'local user: {local_user.nickname}\n')

    if local_user.commu_id==None:
        return redirect("/")

    '''
        def_context has parameters to show end form to change parameters
    '''
    def_context = {}
    
    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.projects[local_user.pro_project].name
                          })
        if local_user.pro_contract:
            def_context.update({"user_contract": local_user.pro_contract})

    
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

    elif args == 'edit': ## read & edit event 
        logging.info(f'read event\n')
        ## !!! take from user
        if local_user.pro_skill:
            def_context.update({"user_skill": local_user.pro_skill.name})

        now = datetime(year=2025, month=1, day=1, hour=8, minute=0, tzinfo=local_user.timezone)

        start_date_day = f"{now.day:02d}"
        start_date_month = f"{now.month:02d}"
        start_month_name = now.strftime("%B")
        start_date_year = now.year
        start_weekday = now.weekday()

        end_date = f"{now.year}-{now.month:02d}-{now.day:02d}"
        start_time = f"{now.hour:02d}:{now.minute:02d}"
    else:
        logging.info(f"wrong args to crud_event {args}\n")


    logging.info(f"request.method {request.method} \n")
    if request.method == "POST":
        form = EventForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
            local_user.save_event(form.cleaned_data)
            ## we  have got it all of these in form.cleaned_data {}
            # start_date = form.cleaned_data['start_date']
            # once = form.cleaned_data['start_date']
            # daily = form.cleaned_data['start_date']
            # work = form.cleaned_data['start_date']
            # weekly = form.cleaned_data['start_date']
            # atday = form.cleaned_data['start_date']
            # atweek = form.cleaned_data['start_date']
            # atweek = form.cleaned_data['start_date']
            # yearly = form.cleaned_data['start_date']
            # wdays = form.cleaned_data['start_date']
            # w_monday = form.cleaned_data['start_date']
            # w_tuesday = form.cleaned_data['start_date']
            # w_wednsday = form.cleaned_data['start_date']
            # w_thirsday = form.cleaned_data['start_date']
            # w_friday = form.cleaned_data['start_date']
            # w_saturday = form.cleaned_data['start_date']
            # w_sunday = form.cleaned_data['start_date']
            # start_time = form.cleaned_data['start_date']
            # end_time = form.cleaned_data['start_date']
            # duration = form.cleaned_data['start_date']
            # rem_5 = form.cleaned_data['start_date']
            # rem_15 = form.cleaned_data['start_date']
            # rem_30 = form.cleaned_data['start_date']
            # rem_1h = form.cleaned_data['start_date']
            # rem_1d = form.cleaned_data['start_date'] 

            if request.POST.get('set'):
                

                
                logging.info(f'exit by set\n')
                return redirect('/')
            elif request.POST.get('delete'):
                ## delete skill from current project
                ## !!! FIRST check parents (project, contract) state !!!
                ## skill._event = None
                ## skill._state = 'template'

                logging.info(f'exit by delete\n')
                return redirect('/')
                
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