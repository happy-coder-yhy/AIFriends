from django.shortcuts import render

# Create your views here.

def frontend_view(request):
    """返回前端页面"""
    return render(request, 'index.html')
