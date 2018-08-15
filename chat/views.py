from django.shortcuts import render, redirect
from .forms import RegistationForm, LoginForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import RoomChat, LoggedInRoom, RoomChatReply, Conversation, ConversationReply
from django.http import JsonResponse
import  redis
from itertools import chain
from operator import attrgetter


def show_index_page(request):
    return render(request, 'pages/index.html')


@login_required(login_url='/accounts/login/')
def show_home_page(request):
    chat_rooms = RoomChat.objects.all()
    return render(request, 'pages/home.html', {'chat_rooms': chat_rooms})


@csrf_exempt
def create_room_chat(request):
    name = request.POST.get('name', False)
    user = request.user
    room_chat = RoomChat(name=name, created_by=user)
    room_chat.save()
    data = {
        'name_room': room_chat.name,
        'time_created': room_chat.time_created,
        'created_by': room_chat.created_by.username,
        'a_link_start': "<a href='/show-roow-chat/"+str(room_chat.id)+"/' class='link-to-each-room'>",
        'a_link_end': "</a>",
    }
    return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def show_room_chat(request, id):
    room_chat = RoomChat.objects.get(id=id)
    user = request.user
    if LoggedInRoom.objects.all().filter(user=user,room_chat=room_chat).exists() == False:
        LoggedInRoom.objects.create(user=user, room_chat=room_chat)

    logged_in_room_users = LoggedInRoom.objects.all().filter(room_chat=room_chat)

    #load reply history to room chat
    chat_replies = RoomChatReply.objects.all().filter(room_chat=room_chat)[0:100]
    return render(request, 'pages/room_chat.html', {'room_chat': room_chat,
                                                    'logged_in_room_users': logged_in_room_users,
                                                    'chat_replies': chat_replies})


@csrf_exempt
def exit_room_chat(request):
    id = request.POST.get('id', False)
    room_chat = RoomChat.objects.all().filter(id=id).first()
    user = request.user
    data = {}
    if LoggedInRoom.objects.all().filter(user=user,room_chat=room_chat).exists():
        logged_room = LoggedInRoom.objects.all().filter(user=user,room_chat=room_chat)
        if logged_room.delete():
            data['is_valid'] = True
        else:
            data['is_valid'] = False
    return JsonResponse(data)


@csrf_exempt
def create_reply_of_room_chat(request):
    user_id= request.POST.get('user_id', False)
    user = User.objects.all().filter(id=user_id).first()
    id = request.POST.get('id', False)
    room_chat = RoomChat.objects.all().filter(id=id).first()
    reply = request.POST.get('reply', False)

    RoomChatReply.objects.create(user=user, room_chat=room_chat, reply_message=reply)
    data = {
        'is_valid': 'Success',
    }

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.publish('chat', user.username+" "+request.POST.get('reply', False))
    return JsonResponse(data)


@csrf_exempt
def create_conversation_reply(request):
    request_user_id = request.POST.get("request_user_id", False)
    page_user_id = request.POST.get("page_user_id", False)
    reply = request.POST.get("reply", False)

    request_user = User.objects.get(id=request_user_id)
    page_user = User.objects.get(id=page_user_id)

    if Conversation.objects.all().filter(user1=request_user, user2=page_user).exists():
        conversation = Conversation.objects.all().filter(user1=request_user, user2=page_user).first()
        conversation_reply = ConversationReply(user=request_user, conversation=conversation, reply_message=reply)
        conversation_reply.save()
    else:
        conversation = Conversation(user1=request_user, user2=page_user)
        conversation.save()

        conversation_reply = ConversationReply(user=request_user, conversation=conversation, reply_message=reply)
        conversation_reply.save()

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.publish('conversation_chat', request_user.username + " " + reply)

    data ={
        'is_valid': 'Success',
    }
    return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def show_personal_page(request, username):
    user = User.objects.get(username=username)
    conversation1 = Conversation.objects.all().filter(user1=user, user2=request.user).first()
    conversation2 = Conversation.objects.all().filter(user1=request.user, user2=user).first()

    conversation_replies1 = ConversationReply.objects.all().filter(conversation=conversation1)[0:100]
    conversation_replies2 = ConversationReply.objects.all().filter(conversation=conversation2)[0:100]

    result_list = sorted(chain(conversation_replies1, conversation_replies2), key=attrgetter('time_send'))

    return render(request, 'pages/personal_page.html', {'user': user,
                                                        'result_list': result_list})


def signup_account(request):
    form = RegistationForm()
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    return render(request, 'pages/sign_up.html', {'form': form})


def login_account(request):
    form = LoginForm()
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],
                                 password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('/home/')
        else:
            return render(request, 'pages/login.html',
                          {'errors': 'Sorry, your password was incorrect.Please double-check your password.',
                           'form': form})
    return render(request, 'pages/login.html', {'form': form})