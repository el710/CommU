from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm)

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

    logging.info(f'get utem: {args}\n')
    logging.info(f'local user: {local_user}\n')

    ## dictionary of args for HTML page
    def_context = {}

    ## if real user
    if local_user.commu_id:
        def_context = {"local_user": local_user.nickname,
                       "user_project": local_user.projects[local_user.work_project].name
                    }
    '''
        perform args
    '''
    logging.info(f'local user utem: {local_user.work_utem}\n')
    if args == None and local_user.work_utem:
        utem_type = local_user.work_utem[0]
        utem_name = local_user.work_utem[1]
    else:
        utem_type, utem_name = utemname_parse(args)
        
    if utem_type == UTYPE_SKILL:
        if isthere_utem(UTYPE_SKILL, utem_name, WORK_PATH):
            local_user.work_skill = USkill(utem_name)
            local_user.work_skill.load_template(WORK_PATH)
            def_context.update({"edit_link": "/skill/edit"})
            if local_user.commu_id:
                def_context.update({"add_link": "/event/"})
            
            ## add data of choosen utem
            def_context.update(get_utem_info(local_user.work_skill))
    
    elif utem_type == "contract":
        pass
    
    elif utem_type == "project":
        pass
              
    ## save what we work with
    if utem_type and utem_name:
        local_user.work_utem = [utem_type, utem_name]              

    ## Make list of public skills
    USkill.load_public_skills("static")
    logging.info(f"loaded {USkill.get_public_skills()}")
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
    
    logging.info(f"search {local_user.search} ")
    def_context.update({"index_search": local_user.search})

    logging.info(f"Context: {def_context} ")
 
    return render(request, 'index.html', context=def_context)


def show_userpage(request, args=None):
    pass
    # """
    #     This function shows user's page
    # """
    # global local_user

    # if local_user.commu_id == None: 
    #     return redirect('/')
    
    # logging.info(f'get utem: {args}\n')
    # logging.info(f'local user: {local_user}\n')

    ## make dictionary of args for page
    # def_context = {}

    # '''
    #     perform args
    # '''
    # logging.info(f'local user utem: {local_user.work_utem}\n')
    # if args == None and local_user.work_utem:
    #     utem_type = local_user.work_utem[0]
    #     utem_name = local_user.work_utem[1]
    # else:
    #     utem_type, utem_name = utemname_parse(args)
    
    # if utem_type == UTYPE_SKILL:
    #     if isthere_utem(UTYPE_SKILL, utem_name, WORK_PATH):
    #         local_user.work_skill = USkill(utem_name)
    #         local_user.work_skill.load_template(WORK_PATH)
    #         def_context.update({"add_link": "/event/",
    #                             "edit_link": "/skill/edit"
    #                            })
    #         ## add 'about' data as searching result
    #         def_context.update(get_utem_info(local_user.work_skill))
    # elif utem_type == "contract":
    #     pass
    # elif utem_type == "project":
    #     pass

    # ## save what we work with
    # if utem_type and utem_name:
    #     local_user.work_utem = [utem_type, utem_name]

    # USkill.load_public_skills("static")
    # logging.info(f"{USkill.get_public_skills()}\n")
    # def_context.update({'public_skills': USkill.get_public_skills()})

    # logging.info(f"method {request.method} ")
    # if request.method == "POST":
    #     ## check up searching field
    #     form = TaskForm(request.POST)
    #     if form.is_valid():
    #         ##remember search
    #         local_user.search = form.cleaned_data['new_task']
    # else:
    #     def_context.update({'form': TaskForm()})

    '''
        Variable part of page constractor
    '''
    # logging.info(f"user {local_user.nickname}\n")

    # def_context.update({"local_user": local_user.nickname,
    #                     "user_project": local_user.projects[local_user.work_project].name
    #                    })
    # '''
    #     End of variable part of page constractor
    # '''    

    # ## show new or last searching results
    # def_context.update(find_utems(local_user.search, path=WORK_PATH, local_user=local_user, public_dealers=public_dealers))

    # logging.info(f"search {local_user.search} ")
    # def_context.update({"index_search": local_user.search})

    # logging.info(f"Context: {def_context} ")
    # return render(request, 'userpage.html', context=def_context)


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
        args: 'edit' or None
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


    if args: ## there is only one argument - 'edit'
        def_context.update(local_user.work_skill.json())
        logging.info(f"load template {def_context}\n")
    # else:
    #     local_user.work_skill = None
    
    if request.method == "POST":
        if request.POST.get('delete'):
            local_user.work_skill.delete_template(WORK_PATH)
            local_user.work_skill = None

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
                
                if local_user.work_skill == None or local_user.work_skill != new_skill:
                    local_user.work_skill = new_skill
                    local_user.work_skill.update(author=local_user.nickname,
                                                 geosocium=local_user.geosocium,
                                                 public=skill_public
                                                )
                    logging.info(f"new skill {local_user.work_skill}")
                    local_user.work_skill.save_as_template(True, WORK_PATH)
            
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

    if local_user.commu_id==None:
        return redirect("/")

    '''
        def_context has parameters to show end form to change parameters
    '''
    def_context = {}
    
    if local_user.commu_id:
        def_context.update({"local_user": local_user.nickname,
                            "user_project": local_user.projects[local_user.work_project].name,
                            "user_skill": local_user.work_skill.name
                          })
    
    if args == None: ## create event
        logging.info(f'create event\n')
        now = datetime.now(tz=local_user.timezone)
        start_date_day = f"{now.day:02d}"
        start_date_month = f"{now.month:02d}"
        start_date_year = now.year
        start_weekday = now.weekday

        end_date = f"{now.year}-{now.month:02d}-{now.day:02d}"

        start_time = f"{now.hour}:{now.minute}"
        def_context.update({"start_date_day": start_date_day,
                            "start_date_month": start_date_month,
                            "start_date_year": start_date_year,
                            "start_wekday": start_weekday,
                            "end_date": end_date,
                            "start_time": start_time,
                            "end_time": start_time
                          })
    elif args == 'edit': ## read & edit event 
        logging.info(f'read event\n')
        pass
    else:
        logging.info(f"wrong args to crud_event {args}\n")


    logging.info(f"request.method {request.method} \n")
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
                
    else:
        form = SkillForm(request.POST)

    def_context.update({"form": form})

    logging.info(f"def_context {def_context} \n")

    return render(request, "event.html", context=def_context)