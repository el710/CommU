'''
    Using Django input html-template forms 
'''
from django import forms

class SignUpForm(forms.Form):
    '''
        get from html forms data by "name":

        Example: 
        if there is in some ***.html
        ...
            <input type="text" name="NAME" maxlength="30" > 
        ...
        
        so we should create
        NAME = forms.CharField(...)
    '''

    username = forms.CharField(label="Name:", max_length=100)
    # user_password = forms.CharField(label="Password:", widget=forms.PasswordInput)
    # user_repassword = forms.CharField(label="Repeat password:", widget=forms.PasswordInput)
    # email = forms.EmailField(label="E-mail:")
    # message = forms.CharField(label="Message:", widget=forms.Textarea)
    # box = forms.BooleanField(label="Premium", required=False)

    '''
        this template Django will try to find in ***.html
    '''

class TaskForm(forms.Form):
    new_task = forms.CharField(label="New point", max_length=100)


class SkillForm(forms.Form):
    skill_name = forms.CharField(label="Name:", max_length=100,  required=True)
    skill_resources = forms.CharField(label="Resources:", max_length=300, widget=forms.Textarea, required=False)
    skill_desc = forms.CharField(label="Description:", max_length=300,widget=forms.Textarea, required=False)
    skill_goal = forms.CharField(label="Goal:", max_length=300, widget=forms.Textarea, required=False)
    skill_public = forms.BooleanField(label="Public", required=False)
    skill_author = forms.CharField(label="Author:", max_length=100,  required=False)