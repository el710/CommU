from django.shortcuts import render


# Create your views here.

def show_title(request):
    """
        This function shows main title Web page
        with template - main.html
    """

    return render(request, 'main.html')