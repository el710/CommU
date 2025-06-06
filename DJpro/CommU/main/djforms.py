'''
    Using Django input html-template forms 
'''
from django import forms
from django.forms import formset_factory

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
    '''
        Form for search query at index.html
    '''
    new_task = forms.CharField(label="New point", max_length=100)


class SkillForm(forms.Form):
    '''
        Form of Utem-skill's parameters
    '''
    name = forms.CharField(label="Name:", max_length=100,  required=True)
    description = forms.CharField(label="Description:", max_length=300,widget=forms.Textarea, required=False)
    public = forms.BooleanField(label="Public", required=False)

class EventForm(forms.Form):
    '''
        Form of Event's parameters
    '''
    event_string = forms.CharField(max_length=500)

    start_date = forms.CharField(max_length=100)
    
    once = forms.BooleanField(label="Once", required=False)
    daily = forms.BooleanField(label="Daily", required=False)
    work = forms.BooleanField(label="Work days", required=False)
    weekly = forms.BooleanField(label="Weekly", required=False)
    atday = forms.BooleanField(label="Monthly on day", required=False)
    atweek = forms.BooleanField(label="Monthly weekday", required=False)
    yearly = forms.BooleanField(label="Annually", required=False)
    wdays = forms.BooleanField(label="Week days", required=False)
    
    w_monday = forms.BooleanField(label="Monday", required=False)
    w_tuesday = forms.BooleanField(label="Tuesday", required=False)
    w_wednsday = forms.BooleanField(label="Wednsday", required=False)
    w_thirsday = forms.BooleanField(label="Thirsday", required=False)
    w_friday = forms.BooleanField(label="Friday", required=False)
    w_saturday = forms.BooleanField(label="Saturday", required=False)
    w_sunday = forms.BooleanField(label="Sunday", required=False)

    start_time = forms.CharField(max_length=100)
    end_time = forms.CharField(max_length=100, required=False)
    duration = forms.BooleanField(label="Duration", required=False)

    rem_5 = forms.BooleanField(label="5 Min", required=False)
    rem_15 = forms.BooleanField(label="15 Min", required=False)
    rem_30 = forms.BooleanField(label="30 Min", required=False)
    rem_1h = forms.BooleanField(label="1 Hour", required=False)
    rem_1d = forms.BooleanField(label="1 Day", required=False)


class EventItem(forms.Form):
    start_date = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    anount = forms.DecimalField(max_digits=10, decimal_places=2)
    state = forms.CharField(max_length=100)

personFormSet = formset_factory(EventItem, extra=3, can_delete=True)

class ContractForm(forms.Form):
    '''
        Form of Utem-Contract's parameters
    '''
    context_root = forms.ChoiceField(choices=[("Life","Life")])
    contract_name = forms.CharField(label="Name:", max_length=100,  required=True)
    contract_dealer = forms.CharField(label="Dealer:", max_length=100,  required=False)
    contract_description = forms.CharField(label="Description:", max_length=300, widget=forms.Textarea, required=False)
    public = forms.BooleanField(label="Public", required=False)


EVENT_TYPE_CHOICES = [
    ('debit', 'Дебет'),
    ('credit', 'Кредит'),
]

class ContractEventForm(forms.Form):
    '''
        Table row
    '''
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    name = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES)

ContractEventFormSet = formset_factory(ContractEventForm, extra=2, can_delete=True)