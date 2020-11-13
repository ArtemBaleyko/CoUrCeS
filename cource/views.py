from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Cource, Organization, Topic, Schedule, UserCource
from .forms import UserRegistrationForm, LoginForm, OrganizationForm, CourceForm, TopicForm, ScheduleForm



# Home page

def index(request):
    cources = Cource.objects.order_by('-id')
    #cources = Cource.objects.filter(organization__name__contains="папвапвап")
    template = 'cource/base.html'
    if request.user.is_authenticated and request.user.organization_set.count() > 0:
        template = 'cource/base_user.html'
    context = {
        'title':'Главная страница сайта',
        'cources': cources,
        'template':template,
    }
    return render(request, 'cource/index.html', context)

# Registration / Authentication

def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'cource/register_done.html', {'new_user': new_user})
            #return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'cource/register_user.html', {'user_form': user_form})

def login_user(request):
    errors = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    errors = "Disabled account"
                    return render(request, 'cource/login.html', {'form': form, 'errors':errors})
            else:
                errors = "Пользователь с таким именем не найден"
                return render(request, 'cource/login.html', {'form': form, 'errors':errors})
    else:
        form = LoginForm()
    return render(request, 'cource/login.html', {'form': form, 'errors':errors})

def logged_out(request):
    logout(request)
    return redirect('home')

# CRUD for Organization

def create_organization(request):
    if request.method == "POST":
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.user = request.user
            organization.save()
            form.save()      
            return redirect('home')
    else:
        form = OrganizationForm()
        context = {
            'form': form,
        }
        return render(request, 'cource/organization/create_organization.html', context)

def view_organization(request):
    organization = Organization.objects.get(user=request.user)
    context = {
        'organization': organization,
        'template': 'cource/base_user.html'
    }
    return render(request, 'cource/organization/view_organization.html', context)

def delete_organization(request):
    organization = Organization.objects.get(user=request.user)
    organization.delete()
    return redirect('home')

def edit_organization(request):
    organization = Organization.objects.get(user=request.user)
    if request.method == "POST":
        organization.name = request.POST.get("name")
        organization.email = request.POST.get("email")
        organization.web_site = request.POST.get("web_site")
        organization.document_series = request.POST.get("document_series")
        organization.document_number = request.POST.get("document_number")
        organization.document_type = request.POST.get("document_type")
        organization.save()
        return redirect('home')
    else:
        context = {
            'organization':organization,
        }
        return render(request, 'cource/organization/edit_organization.html', context)

# CRUD for Cource

def create_cource(request):
    if request.method == "POST":
        form = CourceForm(request.POST)
        if form.is_valid():
            cource = form.save(commit=False)
            organization = Organization.objects.get(user=request.user)
            cource.organization = organization
            cource.save()
            form.save()
            return redirect('view_cources')
    else:
        form = CourceForm()
        context = {
            'form': form,
        }
        return render(request, 'cource/cources/create_cource.html', context)

def view_cources(request):
    organization = Organization.objects.get(user=request.user)
    cources = Cource.objects.filter(organization=organization)
    template = 'cource/base_user.html'
    title = 'Курсы Вашей организации'
    context = {
        'cources': cources,
        'is_taking_cources':False,
        'template': template,
        'title': title,
    }
    return render(request, 'cource/cources/view_cources.html', context)

def delete_cource(request, cource_id):
    cource = Cource.objects.get(id=cource_id)
    cource.delete()
    return redirect('view_cources')

def edit_cource(request, cource_id):
    cource = Cource.objects.get(id=cource_id)
    schedule = cource.schedule_set.all()
    topics = cource.topic_set.all()
    if request.method == "POST":
        cource.title = request.POST.get("title")
        cource.description = request.POST.get("description")
        cource.type_of_cource = request.POST.get("type_of_cource")
        cource.attendance = request.POST.get("attendance")
        cource.start_date = request.POST.get("start_date")
        cource.end_date = request.POST.get("end_date")
        cource.study_hours = request.POST.get("study_hours")
        cource.base_education = request.POST.get("base_education")
        cource.graduate_control = request.POST.get("graduate_control")
        cource.graduate_document = request.POST.get("graduate_document")
        cource.price = request.POST.get("price")
        cource.save()
        return redirect('view_cources')
    else:
        context = {
            'cource':cource,
            'schedule': schedule,
            'topics': topics,
            'TYPE_OF_COURCE_CHOICES': Cource.TYPE_OF_COURCE_CHOICES,
            'ATTENDANCE_CHOICES': Cource.ATTENDANCE_CHOICES,
            'BASE_EDUCATION_CHOICES': Cource.BASE_EDUCATION_CHOICES,
            'GRADUATE_CONTROL_CHOICES': Cource.GRADUATE_CONTROL_CHOICES,
            'GRADUATE_DOCUMENT_CHOICES': Cource.GRADUATE_DOCUMENT_CHOICES,
        }
        return render(request, 'cource/cources/edit_cource.html', context)

def cource(request, cource_id):
    try:
        cource = Cource.objects.get(id=cource_id)
    except:
        raise Http404("Курс не найден")
    
    schedule = cource.schedule_set.all()
    topics = cource.topic_set.all()
    organization = Organization.objects.get(id=cource.organization_id)
    template = 'cource/base.html'
    is_owner = False
    is_taking_cource = False
    if request.user.is_authenticated: 
        if request.user.organization_set.count() > 0:
            template = 'cource/base_user.html'
            if organization.user == request.user:
                is_owner = True
        if request.user.usercource_set.filter(user=request.user, cource=cource):
            is_taking_cource = True
    
    context = {
        'template': template,
        'cource':cource,
        'schedule': schedule,
        'topics': topics,
        'organization': organization,
        'is_owner': is_owner,
        'is_taking_cource': is_taking_cource,
    }
    return render(request, 'cource/cource.html', context)

def view_user_cources(request):
    cources = Cource.objects.raw('''SELECT * FROM cource_cource c 
    LEFT JOIN cource_usercource u 
    ON c.id = u.cource_id 
    WHERE u.user_id=%s''', [request.user.id])
    template = 'cource/base.html'
    title = "Курсы на которые вы записались"
    if request.user.is_authenticated and request.user.organization_set.count() > 0:
        template = 'cource/base_user.html'
    
    context = {
        'cources': cources,
        'is_taking_cources':True,
        'template':template,
        'title': title,
    }
    return render(request, 'cource/cources/view_cources.html', context)

def search_cources(request):
    template = 'cource/base_user.html' if request.user.is_authenticated and request.user.organization_set.count() > 0 else 'cource/base.html'

    cources = Cource.objects.all()
    organizations = Organization.objects.all()

    title = request.GET.get("title")
    type_of_cource = request.GET.get("type_of_cource")
    attendance = request.GET.get("attendance")
    base_education = request.GET.get("base_education")
    graduate_control = request.GET.get("graduate_control")
    graduate_document = request.GET.get("graduate_document")
    organization = request.GET.get("organization")
    sort = request.GET.get("sort")
    
    topics_id = Topic.objects.filter(name=title).values_list('cource_id', flat=True)
    cources_with_topics = Cource.objects.filter(id__in=list(topics_id))
    if title is not None:
        cources = cources.filter(title__contains=title)
    if type_of_cource != "":
        cources = cources.filter(type_of_cource=type_of_cource)
    if attendance != "":
        cources = cources.filter(attendance=attendance)
    if base_education != "":
        cources = cources.filter(base_education=base_education)
    if graduate_control != "":
        cources = cources.filter(graduate_control=graduate_control)
    if graduate_document != "":
        cources = cources.filter(graduate_document=graduate_document)
    if organization != "":
        cources = cources.filter(organization__name=organization)
    if sort != "":
        cources = cources.order_by(sort)

    cources = cources | cources_with_topics

    SORT_CHOICES = [
        ('price', 'От дешевых к дорогим'),
        ('-price', 'От дорогих к дешевым'),
    ]
    context = {
        'template': template,
        'cources': cources,
        'organizations': organizations,
        'TYPE_OF_COURCE_CHOICES': Cource.TYPE_OF_COURCE_CHOICES,
        'ATTENDANCE_CHOICES': Cource.ATTENDANCE_CHOICES,
        'BASE_EDUCATION_CHOICES': Cource.BASE_EDUCATION_CHOICES,
        'GRADUATE_CONTROL_CHOICES': Cource.GRADUATE_CONTROL_CHOICES,
        'GRADUATE_DOCUMENT_CHOICES': Cource.GRADUATE_DOCUMENT_CHOICES,
        'SORT_CHOICES': SORT_CHOICES,
    }
    return render(request, 'cource/cources/search_cources.html', context)

def view_search_result(request):
    template = 'cource/base_user.html' if request.user.is_authenticated and request.user.organization_set.count() > 0 else 'cource/base.html'
    cources = Cource.objects.all()
    SORT_CHOICES = [
        ('price', 'От дешевых к дорогим'),
        ('-price', 'От дорогих к дешевым'),
    ]
    context = {
        'template': template,
        'cources': cources,
        'TYPE_OF_COURCE_CHOICES': Cource.TYPE_OF_COURCE_CHOICES,
        'ATTENDANCE_CHOICES': Cource.ATTENDANCE_CHOICES,
        'BASE_EDUCATION_CHOICES': Cource.BASE_EDUCATION_CHOICES,
        'GRADUATE_CONTROL_CHOICES': Cource.GRADUATE_CONTROL_CHOICES,
        'GRADUATE_DOCUMENT_CHOICES': Cource.GRADUATE_DOCUMENT_CHOICES,
        'SORT_CHOICES': SORT_CHOICES,
    }
    return render(request, 'cource/cources/search_cources.html', context)

# CRUD for UserCource

def take_cource(request, cource_id):
    user_cource = UserCource(user=request.user, cource=Cource.objects.get(id=cource_id))
    user_cource.save()
    return redirect('view_user_cources')

def leave_cource(request, cource_id):
    cource=Cource.objects.get(id=cource_id)
    print(cource)
    user_cource = UserCource.objects.get(cource=cource, user=request.user)
    user_cource.delete()
    return redirect('view_user_cources')

# CRUD for Topic

def create_topic(request, cource_id):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            cource = Cource.objects.get(id=cource_id)
            topic.cource = cource
            topic.save()
            form.save()
            return redirect('edit_cource', cource_id)
    else:
        form = TopicForm()
        context = {
            'form': form,
        }
        return render(request, 'cource/topic/create_topic.html', context)

def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    cource_id = topic.cource.id
    topic.delete()
    return redirect('edit_cource', cource_id)

def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == "POST":
        topic.name = request.POST.get("name")
        topic.hours = request.POST.get("hours")
        cource_id = topic.cource.id
        topic.save()
        return redirect('edit_cource', cource_id)
    else:
        context = {
            'topic':topic,
        }
        return render(request, 'cource/topic/edit_topic.html', context)

# CRUD for Schedule

def create_schedule(request, cource_id):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            cource = Cource.objects.get(id=cource_id)
            schedule.cource = cource
            schedule.save()
            form.save()
            return redirect('edit_cource', cource_id)
    else:
        form = ScheduleForm()
        context = {
            'form': form,
        }
        return render(request, 'cource/schedule/create_schedule.html', context)

def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    cource_id = schedule.cource.id
    schedule.delete()
    return redirect('edit_cource', cource_id)

def edit_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == "POST":
        schedule.day = request.POST.get("day")
        schedule.from_time = request.POST.get("from_time")
        schedule.to_time = request.POST.get("to_time")
        cource_id = schedule.cource.id
        schedule.save()
        return redirect('edit_cource', cource_id)
    else:
        context = {
            'schedule': schedule,
            'DAY_CHOICES': Schedule.DAY_CHOICES,
        }
        return render(request, 'cource/schedule/edit_schedule.html', context)

