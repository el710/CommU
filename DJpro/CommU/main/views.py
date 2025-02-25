from django.shortcuts import render, redirect
from .djforms import RegForm

# Create your views here.

import logging

def show_title(request):
    """
        This function shows main title Web page
        with template - main.html
    """
    return render(request, 'main.html')


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
    return render(request, 'terms.html')

def show_rules(request):
    """
        This function shows rules page
        with template - rules.html
    """
    return render(request, 'rules.html')

def registration(request):
    logging.info(f"\nregistration(): ...")
    def_context = {}


    if request.method == 'POST':
        form = RegForm(request.POST)
       
        print(f"\next_post(): POST {form.is_valid()} ")
    
        print(f'\next_post(): {form.cleaned_data}')
        if form.is_valid(): ## is_valid also makes cleaned_data
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']

            password = request.POST.get("user_password")
            repassword = request.POST.get("user_repassword")

            print(f"ext_post(): POST: {name} {email} {password} {repassword} ")
            
            if password == repassword:
                
                return redirect('/') 
            else:
                def_context.update({'passstate': "... passwords is not equal. Try again."})

    else:
        form = RegForm()  ## form is a html-template that django try to find in html page by name
        ## print(f"\next_post(): render {form}")
    
    def_context.update({'form': form})
    return render(request, 'regform.html', context=def_context )

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
