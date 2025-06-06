from django.shortcuts import render, redirect
from .djforms import (SignUpForm, TaskForm, SkillForm, EventForm, ContractForm, ContractEventFormSet)

from django.contrib.staticfiles import finders


# Create your views here.
from uproject.models.project import UProject
from uproject.models.contract import UContract
from uproject.models.skill import USkill

from uproject.models.user import *

from uproject.storage.filestorage import FileStorage
from uproject.storage.bases import UtemBase

from uproject.storage.keepmanager import KeepManager

import logging
import os
from datetime import datetime, timedelta


""" Operating Data"""
## There is always a user - by define 'Guest'

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

            '''
                Save In base user by hash - no passwords
            '''            
            logging.info(f'new user: {local_user.nickname}')

            # ## hard storage (file | DB)
            # local_user.init_storage(FileStorage(WORK_PATH, f"{local_user.nickname}"))

            # ## RAM storage for all utems
            # local_user.init_utem_base(UtemBase())

            ## base manager
            local_user.init_keep_manager( KeepManager( FileStorage(WORK_PATH, f"{local_user.nickname}") ) )

            ## basic project Life for User
            root=UProject(name="Life", starter_user_id=local_user.commu_id, state=ROOT_PROJECT, my_token=local_user.commu_id)
            root.sign(local_user)
            ## root of user tree
            local_user.root_utem = root

            # local_user.work_utem = root
            logging.info(f'new user: root - {local_user.root_utem} work - {local_user.work_utem}')
            local_user.keep_manager.save_utem(root)
            #local_user.utem_tree.add(root.get_token(), root.get_classname)
            
            return redirect('/user/') 
            # else:
            #     def_context.update({'passstate': "... passwords is not equal. Try again."})

    else:
        form = SignUpForm()  ## form is a html-template that django try to find in html page by name
        
    def_context = {'form': form}
    return render(request, 'signup.html', context=def_context )

def show_user(request, args=None):
    '''
        Make main.html
        args: Utem has taken from list to view info {skill, contract, project}
    '''
    global local_user

    ## if no user
    if not local_user.commu_id: return redirect("/")

    if args == 'close': 
        local_user.search = None
        return redirect("/user/")

    ## utem we has worked with on other pages
    local_user.work_utem = None
    local_user.origin_utem_id = None
        
    ## dictionary of args for HTML page
    def_context = {}

    logging.info(f"method {request.method} ")
    if request.method == "POST":
        ## POST by search 
        ## check up searching field
        form = TaskForm(request.POST)
        if form.is_valid():
            ##remember search
            local_user.search = form.cleaned_data['new_task']
    else:
        form = TaskForm()

    def_context.update({'form': form})
    def_context.update({"local_user": local_user.nickname})

    '''
        Load utems list
    '''   
    local_user.keep_manager.upload_base(['UProject', 'UContract', 'USkill'])
    # logging.info(f"Base {[utem for utem in local_user.keep_manager.base]} ")

    ## Load search result
    # logging.info(f"search {local_user.search} ")
    def_context.update({"index_search": local_user.search})
    ## show new or last searching results
    if local_user.search:
        def_context.update(local_user.keep_manager.find_by_name(local_user.search))


    ## Template utems
    # logging.info(f"templates {local_user.keep_manager.find_by_state(TEMPLATE_UTEM)} ")
    def_context.update(local_user.keep_manager.find_by_state(TEMPLATE_UTEM))

    ## Fill user's Life
    def_context.update({"user_staff": local_user.keep_manager.get_tree(local_user)})
    
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

            local_user.init_storage(FileStorage(WORK_PATH))
            local_user.init_utem_base(UtemBase(user=local_user))
            local_user.init_utem_tree(UtemTreeBase(user=local_user))

            ## basic project Life for User
            root=UProject(local_user, "Life")
            local_user.utem_base.add(root)
            local_user.utem_tree.add(utem_id=root.get_token())

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
              'token' - open event with id == token
    '''
    global local_user

    logging.info(f'local user: {local_user}')
    logging.info(f'open skill: {args}\n')
    
    if not local_user.commu_id: return redirect("/")

    def_context = {}      
    
    logging.info(f" method: {request.method} cont: {request.POST}\n")
    
    if request.method == "POST":

        ## delete skill no matter changes
        if request.POST.get('delete'):
            local_user.keep_manager.delete_utem(local_user.work_utem)
            return redirect("/user/")

        form = SkillForm(request.POST)
        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid():
            ## add or change event
            if request.POST.get('event'):
                if not local_user.work_utem:
                    local_user.work_utem = USkill()

                ## for enable to make back link token
                local_user.work_utem.from_dict(form.cleaned_data)
                return redirect("/event/")

            ## set last data
            local_user.work_utem.from_dict(form.cleaned_data)
            

            if request.POST.get('save'):
                ## if sign data hasn't change
                if local_user.work_utem.get_token() == local_user.origin_utem_id:
                    local_user.keep_manager.edit_utem(local_user.origin_utem_id, local_user.work_utem)
                else:
                    ## it's a new utem or old utem became new
                    local_user.work_utem.sign(local_user)
                    local_user.keep_manager.save_utem(local_user.work_utem)
            
            ## add to root
            if request.POST.get('add'):
        
                ## it's always new utem - not template
                local_user.work_utem.set_executor(local_user)
                local_user.work_utem.set_state(WORKING_UTEM)
                local_user.work_utem.sign(local_user)
                local_user.work_utem.set_parent(local_user.root_utem.get_token())
                local_user.keep_manager.save_utem(local_user.work_utem)

                logging.info(f"add to root {local_user.root_utem.get_classname()}")
                ## Add id to root list
                if local_user.root_utem.get_classname() == 'UProject':
                    local_user.root_utem.add_event(local_user.work_utem.get_token())
                elif local_user.root_utem.get_classname() == 'UContract':
                    pass

            logging.info(f"save skill {local_user.work_utem.to_dict()}")

            return redirect("/user/")

        ## error POST   
        else:
            form = SkillForm(request.POST)
            logging.info(f"POST failed\n")

    ## POST    
    else:
        form = SkillForm(request)

    if args:
        ## in case when we came from user page !!! not from event page
        if not local_user.work_utem:
            ## work_utem must be copy - not the object in Base
            local_user.work_utem = copy.deepcopy(local_user.keep_manager.read_utem(args))
            if local_user.work_utem:
                local_user.origin_utem_id = local_user.work_utem.get_token()

    if local_user.work_utem:
        def_context.update(local_user.work_utem.to_dict())
        def_context.update({"saved": local_user.work_utem.is_signed()})

        if local_user.work_utem.get_state() == TEMPLATE_UTEM:
            def_context.update({"root": local_user.root_utem.get_title()})
        else:
            parent = local_user.keep_manager.read_utem(local_user.work_utem.get_parent())
            if not parent:
                def_context.update({"root": local_user.root_utem.get_title()})
            else:
                def_context.update({"context": parent.get_title(), "context_link": parent.make_link()})
    else:
        def_context.update({"root": local_user.root_utem.get_title()})

    def_context.update({"form": form,
                        "local_user": local_user.nickname
                        })
 
    logging.info(f"Skill CRUD context {def_context} \n")

    return render(request, "skill.html", context=def_context)


def crud_event(request, args=None):
    global local_user

    if local_user.commu_id == None or local_user.work_utem == None:
        return redirect("/")

    logging.info(f'local user: {local_user.nickname}\n')

    logging.info(f"request.method {request.method} \n")
    if request.method == "POST":
        form = EventForm(request.POST)

        logging.info(f"valid POST {form.is_valid()} \n")
        logging.info(f'data: {form.cleaned_data}\n')

        if form.is_valid(): ## is_valid also makes cleaned_data
            if request.POST.get('save'):
                local_user.work_utem.set_event(form.cleaned_data)
                
                logging.info(f'exit by save\n')

            elif request.POST.get('delete'):
                local_user.work_utem.set_event(None)
                                
                logging.info(f'exit by delete\n')
                
            return redirect(local_user.work_utem.make_link())    
    else:
       form = EventForm()

    '''
        def_context has parameters to show end form to change parameters
    '''
    def_context = {"form": form,
                   "local_user": local_user.nickname
                  }
    
    def_context.update({"back_link": local_user.work_utem.make_link()})
            
    ## create(add) event
    if local_user.work_utem.get_event() == None:
        logging.info(f'create event\n')
        now = datetime.now(tz=local_user.timezone)

        def_context.update({"event": {"start_date": now.date().isoformat(),
                                      "start_time": now.strftime("%H:%M"),
                                      "once": True,
                                      "name": local_user.work_utem.get_name()
                                     },
                            "event_create": True
                        })
    ## read & edit event
    else:
        def_context.update({"event": local_user.work_utem.get_event(),
                            "event_edit": True
                        })

        
    def_context.update({"user_root": local_user.root_utem.get_title() })    
        
    logging.info(f"Event CRUD context {def_context} \n")

    return render(request, "event.html", context=def_context)


def crud_contract(request, args=None):
    '''
        Make contract.html
        args: None - create new UContract
              'token' - open UContract by id

    '''
    global local_user
    
    logging.info(f'local user: {local_user}')
    logging.info(f'open contract: {args}\n')

    if not local_user.commu_id: return redirect("/")
  
    def_context = {}

    logging.info(f"request.method {request.method} \n")

    if request.method == "POST":

        ## delete no matter changes
        if request.POST.get('delete'):
            local_user.keep_manager.delete_utem(local_user.work_utem)
            return redirect("/user/")

        form = ContractForm(request.POST)
        logging.info(f"valid form {form.is_valid()}")
        logging.info(f'data: {form.cleaned_data}\n')

        formset = ContractEventFormSet(request.POST)
        logging.info(f"valid form {formset.is_valid()}")

        if form.is_valid() and formset.is_valid() : ## is_valid also makes cleaned_data
            
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    print(form.cleaned_data)

            if request.POST.get('save'):
                logging.info(f'exit by save\n')

            if request.POST.get('add'):
                logging.info(f'exit by add\n')
      
            if request.POST.get('sendto'):
                logging.info(f'exit by sendto\n')                
            
            if request.POST.get('sendback'):
                logging.info(f'exit by sendback\n')

            if request.POST.get('sign'):
                logging.info(f'exit by sign\n')

            logging.info(f"save contract {local_user.work_utem.to_dict()}")                   
            return redirect('/user/')
        
        ## error POST   
        else:
            form = ContractForm(request.POST)
            formset = ContractEventFormSet(request.POST)
            logging.info(f"POST failed\n")

    ## POST
    else:
       form = ContractForm()
       formset = ContractEventFormSet()


    if args:
        ## in case when we came from user page !!! not from event page
        if not local_user.work_utem:
            ## work_utem must be copy - not the object in Base
            local_user.work_utem = copy.deepcopy(local_user.keep_manager.read_utem(args))
            if local_user.work_utem:
                local_user.origin_utem_id = local_user.work_utem.get_token()

    if local_user.work_utem:
        def_context.update(local_user.work_utem.to_dict())
        def_context.update({"saved": local_user.work_utem.is_signed()})

        if local_user.work_utem.get_state() == TEMPLATE_UTEM:
            def_context.update({"root": local_user.root_utem.get_title()})
        else:
            parent = local_user.keep_manager.read_utem(local_user.work_utem.get_parent())
            if not parent:
                def_context.update({"root": local_user.root_utem.get_title()})
            else:
                def_context.update({"context": parent.get_title(), "context_link": parent.make_link()})
    else:
        def_context.update({"root": local_user.root_utem.get_title()})
        
    def_context.update({"form": form,
                        "formset": formset,
                        "local_user": local_user.nickname
                        })
 
    logging.info(f"Contract CRUD context {def_context} \n")
    
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


