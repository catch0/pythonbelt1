from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse 
from django.db.models import Count
from .models import*
def index(request):
    print "Inside the index method."
    return render(request, 'beltapp/index.html')
def home(request):
    print "Inside the home method."
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        return render(request, 'beltapp/home.html', {'user': user})
    return redirect(reverse('landing'))
def register(request):
    print "Inside the register method"
    if request.method == 'POST':
        check = User.objects.validate(request.POST)
        if check['pass']:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id
            return render(request, 'beltapp/registered.html')
        for error in check['errors']:
            messages.error(request, error['message'], extra_tags=error['field'])  
    return redirect('/')
def login(request):
    print "Inside the login method."
    if request.method == 'POST':
        check = User.objects.login(request.POST)
        if check['pass']:
            user = check['user']
            request.session['user_id'] = user.id
            return redirect('/favquote')
        for error in check['errors']:
            messages.error(request, error['message'], extra_tags=error['field'])
        return render(request,'beltapp/index.html')
def favquote(request):
    if 'user_id' in request.session:
        user=User.objects.findUser(request.session)
        all_quotes=Quote.objects.all().order_by('-id')[:10]
        all_content=[]
        all_times=[]
        for quote in all_quotes:
            all_content.append(quote)
            #print quote.user_id
        context={'all':all_content,'name':user.first_name, 'id':user.id}
        return render(request, 'beltapp/home.html',context)
def addquote(request):
    if request.method=='POST':
        user=User.objects.findUser(request.session)
        new=Quote.objects.create(speaker=request.POST['speaker'],content=request.POST['content'],submitted=user)
        return redirect('/favquote')
    return redirect('/')
def userfavs(request):
    if request.method=="POST":
        user=User.objects.findUser(request.session)
        all_favs=Quote.objects.filter(submitted=request.session['user'])
        all_content=[]
        all_times=[]
        all_quotes=Quote.objects.add(submitted=['user'])
        for quote in all_favs:
            all_content.append(quote)
        context={'all':all_content,'name':user.first_name, all_quotes: 'aq'}
        return render(request, 'beltapp/favs.html', context)
    return render(request, 'beltapp/favs.html')
def addlist(request):
    if request.method=="POST":
        user = User.objects.findUser(request.session)
        my_favs=Quote.objects.filter(liked_by=user).first()
        all_content=[]
        for quote in my_favs:
            all_content.append(quote)
        context={'alll':my_favs, 'name':user.first_name}
        return redirect('/userfavs')
def logout(request):
    if request.POST:
        request.session.clear()
        return redirect('/')