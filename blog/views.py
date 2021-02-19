from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm , LoginForm ,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group


# Create your views here.
#home page
def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})
def about(request):
    return render(request, 'blog/about.html')
def contact(request):
    return render(request, 'blog/contact.html')

def deshboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name= user.get_full_name()
        gps=user.groups.all()
        return render(request, 'blog/dasboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_singup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You have become an authot.')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
            form=SignUpForm()
    else:
        form=SignUpForm()
    return render(request, 'blog/singup.html',{'form':form})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/deshboard/')
    else:

    
        if request.method=="POST":
            form=LoginForm( request=request,data=request.POST)
            if form.is_valid():
                
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully!!')
                    form=LoginForm()
                    return HttpResponseRedirect('/deshboard/')

        else:
            form=LoginForm()
        return render(request, 'blog/login.html',{'form':form})
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)

                pst.save()
                messages.success(request,'Post Add in Successfully!!')
                form=PostForm()
        else:
             form=PostForm()

        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect("/login/")

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Post Update in Successfully!!')
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect("/login/")
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
            messages.success(request,'Post Delete in Successfully!!')

        return HttpResponseRedirect("/deshboard/")
    else:
        return HttpResponseRedirect("/login/")
