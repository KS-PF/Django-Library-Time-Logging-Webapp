from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .forms import (
    EnterForm, AddForm, 
)
from django.views.generic import (
    TemplateView, ListView, UpdateView, DeleteView
)
from .models import TimeLog
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Q
from django.http import HttpResponse
import re
from django.urls import reverse


def is_number(value):
    result = False
    if (re.match(r'^[0-9]*$', str(value)) != None):
        result = True
    return result


def message(request, type):
    title = 'もう一度やり直してください'
    text = ''
    label = 'ログインする'
    name = 'accounts:login'

    if type == 'signup':
        title = '登録が完了しました'
        text = 'ユーザーの新規登録が完了しました。以下のボタンからログインしてください。'
    elif type == 'enter':
        title = '入室しました'
        text = '入室の時間が記録されました。以下のボタンからホームに戻ってください'
        label = 'ホームに戻る'
        name = 'time_logging:index'
    elif type == 'exit':
        title = '退室しました'
        text = '退室の時間が記録されました。以下のボタンからホームに戻ってください'
        label = 'ホームに戻る'
        name = 'time_logging:index'
    elif type == 'add':
        title = '時間が記録されました'
        text = '入退室の時間が記録されました。以下のボタンからホームに戻ってください'
        label = 'ホームに戻る'
        name = 'time_logging:index'

    view_url = reverse(name)
    context ={
        "title":title,
        "text":text,
        "label":label,
        "url": view_url,
        }
    return render(request, 'time_logging/message.html', context )



def index(request):
    return render(request, 'time_logging/index.html')


class Enter(TemplateView):

    template_name='time_logging/forms.html'

    def __init__(self):
        self.param = {
            'error':'',
            'back':'time_logging:index',
            'msg':'入室される方は必要な情報を入力し確定を押してください',
            'urlName':'time_logging:enter',
            'forms':EnterForm
        }
    
    def get(self, request):
        return self.render_to_response(self.param)
    
    def post(self, request):
        faculty = request.POST.get('faculty')
        attribute = request.POST.get('attribute')
        student_number = request.POST.get('student_number')
        name = request.POST.get('name')
        enter = timezone.localtime(timezone.now())

        error = None

        if student_number == '' and name == '':
            error = '学籍番号か氏名を入力してください'
        elif is_number(student_number) == False:
            error = '正しく学生番号を入力してください'

        if error is None:
            timelog = TimeLog(
                faculty = faculty, attribute = attribute, 
                student_number = student_number, 
                name = name, enter = enter,
                )
            timelog.save()

            url = reverse('time_logging:message', kwargs={'type': 'enter'})
            
            return redirect(url)

        self.param['error'] = error
        self.param['forms'] = EnterForm(request.POST)#前のポスト内容を残す
        return self.render_to_response(self.param)


class Add(TemplateView):

    template_name='time_logging/forms.html'

    def __init__(self):
        self.param = {
            'error':'',
            'back':'time_logging:index',
            'msg':'あとから時間を記録する方は、必要な情報を入力し確定を押してください',
            'urlName':'time_logging:add',
            'forms':AddForm
        }
    
    def get(self, request):
        return self.render_to_response(self.param)
    
    def post(self, request):
        faculty = request.POST.get('faculty')
        attribute = request.POST.get('attribute')
        student_number = request.POST.get('student_number')
        name = request.POST.get('name')
        enter = request.POST.get('enter')
        exit = request.POST.get('exit')

        error = None

        if exit < enter:
            error = '日時を正しく入力してください'
        elif student_number == '' and name == '':
            error = '学生番号か氏名を入力してください'
        elif is_number(student_number) == False:
            error = '正しく学生番号を入力してください'
        # elif enter.day != exit.day:
        #     error = '同じ日付を入力してください'

        if error is None:
            timelog = TimeLog(
                is_exit = True,
                faculty = faculty, attribute = attribute, 
                student_number = student_number, 
                name = name, enter = enter,
                exit = exit,
                )
            timelog.save()
            url = reverse('time_logging:message', kwargs={'type': 'add'})
            return redirect(url)

        self.param['error'] = error
        self.param['forms'] = AddForm(request.POST)#前のポスト内容を残す
        return self.render_to_response(self.param)


class Exit(ListView):

    template_name = 'time_logging/exit.html'
    
    def get_queryset(self): # 検索機能のために追加
        text = self.request.GET.get('text')
        sort = self.request.GET.get('sort', 'id')
        if not(sort == 'id' or sort == '-id'):
            sort = 'id'

        today = timezone.localtime(timezone.now()).date()

        if text:
            data = TimeLog.objects.filter(
                Q(is_exit=False) & 
                (Q(student_number__contains=text) | Q(name__contains=text))
                & Q(enter__date=today)
            )
        else:
            data = TimeLog.objects.filter(is_exit=False, enter__date=today) 

        return data.order_by(sort)


class ExitExecute(TemplateView):
    template_name='time_logging/exit_do.html'

    def __init__(self):
        self.param = {
            'error':'',
            'data':None,
        }
    
    def get(self, request, pk):
        self.param['data'] = get_object_or_404(TimeLog, pk=pk)
        return self.render_to_response(self.param)
    
    def post(self, request, pk):
        check_id = int(request.POST['id'])
        pk = int(pk)
        log = get_object_or_404(TimeLog, pk=pk)
        self.param['data'] = log

        if check_id == pk:
            log.is_exit = True
            log.exit = timezone.localtime(timezone.now())
            log.save()
            
            url = reverse('time_logging:message', kwargs={'type': 'exit'})
            return redirect(url)

        self.param['error'] = 'もう一度入力してください'
        return self.render_to_response(self.param)

    


def use(request):
    return render(request, 'time_logging/use.html')

