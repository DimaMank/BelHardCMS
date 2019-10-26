
from time import perf_counter
from collections import defaultdict
from client.models import Client, CV
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.edit import FormView
from django.template.context_processors import csrf

from django.urls import reverse
from django.http import HttpResponse
from .models import *
from recruit.models import Recruiter
from client.models import Chat, Message, Tasks, UserModel, SubTasks, Settings, Client, State
from datetime import datetime

# There is Poland's views #################################################################################
def recruiter_main_page(request):
    return render(request, template_name='recruit/recruit_main_template.html', )





def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})


def applicant(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    return render(request, 'recruit/recruiter_applicant.html', context={'applicant_user': applicant_user})


class CreateJobInterview(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        if CV.objects.filter(client_cv=applicant_user):
            accepted_vacancies = applicant_user.cv_set.all()[0].vacancies_accept.all()
            for resume in applicant_user.cv_set.all()[1:]:
                accepted_vacancies |= resume.vacancies_accept.all()
            print(accepted_vacancies)
        else:
            accepted_vacancies = None
        return render(request, 'recruit/recruiter_tasks_for_applicant.html',
                      context={'applicant_user': applicant_user, 'accepted_vacancies': accepted_vacancies})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        vac = request.POST.get('vacancy')
        files = request.FILES.getlist('files')
        print('vacancy_id  ', vac)
        print(len(files))
        for file in files:
            print(file)

        return redirect(applicant_user.get_tasks_url())

# End Poland's views #######################################################################################


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html', context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user, message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новое сообщение', to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message, 'message_id': mes.id,
             'pub_date': mes.pub_date.ctime()}
    return JsonResponse(send, safe=False)


def chat_update(request):

    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(Message.objects.filter(chat=c, is_read=False).exclude(author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


def add_task(request):
    context = {}
    context['users_list'] = UserModel.objects.all()
    #context['newtask'] = newtask
    return render(request=request, template_name='recruit/add_task.html', context=context)


def add_new_task(requset):
    try:
        user = UserModel.objects.get(username=requset.POST['name'])
    except UserModel.DoesNotExist: #TODO сделать проверку в отправек формы?
        return HttpResponse('Необходимо задать юзера')
    newtask = Tasks.objects.create()
    newtask.user = user
    newtask.title = requset.POST['task_title']
    newtask.comment = str(requset.POST['task_comment'])
    #newtask.time = datetime.now() TODO
    newtask.save()
    i = 1
    reqpost = requset.POST
    while True:
        try:
            newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
        except:
            break
        i += 1
        newsubtask.save()

        try:
            if Settings.objects.get(user=user).email_messages:
                send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(user.email)])
                send_email.send()
        except Exception:
            print('Exception: нет адреса электронной почты')

    return redirect(to='add_task')



def favorites(request):
    recruit = Recruiter.objects.get(recruiter=request.user)
    clients = Client.objects.filter(own_recruiter=recruit)
    context = {'clients': clients}

    return render(request, template_name='recruit/favorites.html', context=context)

#обработка избранного рекрутера
def check_favor(request):
    client_id = (request.GET['client'])
    client = Client.objects.get(id=client_id)
    recruit_id = (request.GET['recruit'])
    recruit = Recruiter.objects.get(recruiter=UserModel.objects.get(id=recruit_id))
    if client.is_reserved == True:
        client.is_reserved = False
        client.own_recruiter = None
    else:
        client.is_reserved = True
        client.own_recruiter = recruit
    client.save()
    return HttpResponse(client_id)


def recruit_base(request):
    recruit = Recruiter.objects.get(recruiter=request.user)
    search_request = request.GET.get('recruit_search', '')
    clients_after_search = set()
    if search_request:
        search_params = search_request.split(' ')
        print(search_params)
        clients = Client.objects.all()

        for s in search_params:
            users_for_first_name_list = UserModel.objects.filter(first_name__contains=s)
            users_for_last_name_list = UserModel.objects.filter(last_name__contains=s)
            users_for_patronymic = clients.filter(patronymic__contains=s)
            try:
                users_for_state = clients.filter(state__contains=State.objects.get(state_word=s))
                clients_after_search.update(users_for_state)
            except:
                print('ясно')
            users_for_first_name = set()
            users_for_last_name = set()
            for u in users_for_first_name_list:
                users_for_first_name.add(clients.get(user_client=u))
            for u in users_for_last_name_list:
                users_for_last_name.add(clients.get(user_client=u))

            clients_after_search.update(users_for_first_name)
            clients_after_search.update(users_for_last_name)
            clients_after_search.update(users_for_patronymic)

    else:
        clients_after_search = Client.objects.filter(own_recruiter=None)
    context = {'free_clients': clients_after_search}
    return render(request, template_name='recruit/recruit_base.html', context=context)
