from django.shortcuts import render,redirect
# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView,UpdateView
from .forms import LoginForm,UserRegistrationForm,PostForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from api.models import Posts,Comments,Friends
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")



    def form_invalid(self, form):
        if form.is_valid():
            messages.success(self.request, 'Account has been created')
        else:
            messages.error(self.request, 'An error occured try again')
        return super().form_invalid(form)

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})



class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    
    success_url=reverse_lazy("index")
    model=Posts
    queryset=Posts.objects.all().order_by('-created_date')
    context_object_name="posts"

    
    def get_queryset(self):
        return self.model.objects.all().order_by("-created_date")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"your question added successfully")
        return super().form_valid(form)
    # def get_queryset(self):
    #       return Posts.objects.all()

def add_comments(request,*args, **kwargs):
    id=kwargs.get("id")
    pst=Posts.objects.get(id=id)
    cmt=request.POST.get("comment")
    Comments.objects.create(post=pst,comment=cmt,user=request.user)
    messages.success(request,"your comment add successfully")
    return redirect("index")



def like_post(request,*args, **kwargs):
    id=kwargs.get("id")
    post=Posts.objects.get(id=id)
    if post.like.contains(request.user):
         post.like.remove(request.user)
    else:     
      post.like.add(request.user)
    return redirect("index")

class ListPeopleView(ListView):
    template_name="people.html"
    model=User
    context_object_name = 'people'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followings"] = Friends.objects.filter(follower=self.request.user)
        context["posts"] = Posts.objects.all().order_by('-created_date')
        return context
    

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


def add_follower(request, *args, **kwargs):
    id = kwargs.get('id')
    usr = User.objects.get(id=id)
    if not Friends.objects.filter(user=usr, follower=request.user):
        Friends.objects.create(user=usr, follower=request.user)
    else:
        Friends.objects.get(user=usr, follower=request.user).delete()
    return redirect("people")

  


def sign_out_view(request,*args, **kwargs):
    logout(request)
    return redirect("signin")   



def post_delete(request,*args,**kw):
    id=kw.get("id")
    Posts.objects.get(id=id).delete()
    return redirect("index")


class ProfileView(ListView):
    template_name="profile.html"
    model=Posts
    context_object_name="posts"

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user).order_by("-created_date")



# class EditprofileView(UpdateView):
#     template_name="proedit.html"
#     form_class=ProfileForm
#     model=Userprofile
#     pk_url_kwarg="id"
#     success_url=reverse_lazy("listpost")        


