from django.shortcuts import render
from .models import Chat,Group
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request,group_name):
    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
    return render(request,'app/index.html',{'groupname':group_name,'chats':chats})