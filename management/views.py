from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, 
)
from .forms import (
    DownloadForm,
)
from time_logging.models import TimeLog
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Q
import csv
from django.http import HttpResponse
import re
import statistics


def DataGetForAnalysis(year=None, month=None, is_exit=True):
    now = timezone.localtime(timezone.now())
    if year is None or month is None:
        year = now.year
        month = now.month


    data = TimeLog.objects.filter(
        is_exit=is_exit, 
        enter__year=year, 
        enter__month=month,
    )

    weekday_japanese = {
        'Monday': '月',
        'Tuesday': '火',
        'Wednesday': '水',
        'Thursday': '木',
        'Friday': '金',
        'Saturday': '土',
        'Sunday': '日',
    }

    DataForAnalysis = []

    for i in data:
        i.exit = timezone.localtime(i.exit)
        i.enter = timezone.localtime(i.enter)
        if is_exit:
            duration = int((i.exit - i.enter).total_seconds() // 60)
            exit = f"{i.exit.hour}:{i.exit.minute}"
            if duration < 1:
                duration = 1

        else:
            duration = None
            exit = None

        enter = f"{i.enter.hour}:{i.enter.minute}"
        weekday = weekday_japanese.get(i.enter.strftime('%A'), '')

        DataForAnalysis.append({
            'id': i.id,
            'is_exit': i.is_exit,
            'year': i.enter.year,
            'month': i.enter.month,
            'day': i.enter.day,
            'weekday': weekday,
            'faculty': i.faculty,
            'attribute': i.attribute,
            'student_number': i.student_number,
            'name': i.name,
            'duration': duration,
            'enter': enter,
            'exit': exit,
        })

    return DataForAnalysis



def is_number(value):
    result = False
    if (re.match(r'^[0-9]*$', str(value)) != None):
        result = True
    return result

def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True



def index(request):
    return render(request, 'management/index.html')


class Analysis(TemplateView):

    template_name='management/analysis.html'

    def __init__(self):
        now = timezone.localtime(timezone.now())
        month = now.month
        self.param = {
            'error':'',
            'data':None,
            'month':month,
        }

    
    def get(self, request):
        if 'data_set' in request.session:
            data = self.request.session["data_set"]
            self.param['data'] = data
        return self.render_to_response(self.param)
    

    def post(self, request):
        check = request.POST.get('check')
        if check == '分析する':
            data_set = DataGetForAnalysis(is_exit=True)
            data = self.get_result_of_analysis(data_set)
            self.request.session["data_set"] = data
            self.param['data'] = data
        else:
            self.param['error'] = 'もう一度、やり直してください'
        
        return self.render_to_response(self.param)
    

    def get_result_of_analysis(self, data_set):
        student_count = 0
        other_count = 0
        info_faculty_count = 0
        other_faculty_count = 0
        durations = []

        weekdays = ['月', '火', '水', '木', '金']
        weekday_data = {day: {'count': 0, 'total_duration': 0} for day in weekdays}

        for record in data_set:
            # 属性が学生の合計利用者数と、その他の合計利用者数
            if record['attribute'] == '学生':
                student_count += 1
            else:
                other_count += 1

            # 学部が情報学部の合計利用者数、その他の学部の合計利用者数
            if record['faculty'] == '情報':
                info_faculty_count += 1
            else:
                other_faculty_count += 1

            # 利用時間（duration）
            duration = record['duration']
            durations.append(duration)

            # 曜日ごとのデータ集計
            week_day = record['weekday']
            if week_day in weekdays:
                weekday_data[week_day]['count'] += 1
                weekday_data[week_day]['total_duration'] += duration

        # 利用時間の合計、平均、最小値、最大値、中央値などの計算
        total_count = student_count + other_count
        total_duration = sum(durations)
        average_duration = int(statistics.mean(durations)) if durations else 0
        min_duration = min(durations) if durations else 0
        max_duration = max(durations) if durations else 0
        median_duration = statistics.median(durations) if durations else 0

        week_data_set = []

        # 曜日ごとの平均計算
        for day in weekdays:
            total_duration = weekday_data[day]['total_duration']
            week_data_set.append(round(total_duration))

        graph_data = self.data_for_graph(week_data_set)

        all_data = {
            'average_duration': average_duration,
            'total_duration': total_duration,
            'min_duration': min_duration,
            'max_duration': max_duration,
            'median_duration': median_duration,

            'total_count':total_count,
            'student_count': student_count,
            'other_count': other_count,
            'info_faculty_count': info_faculty_count,
            'other_faculty_count': other_faculty_count,

            'weekday_data': weekday_data,
            'graph_data': graph_data,

            'test': None,
        }

        return all_data
    

    def data_for_graph(self, data_set):
        total = sum(data_set)
        week_rates = []
        graph_data={}

        for data in data_set:
            if total != 0 :
                rate = round(data / total *100)
                rate = 10 * round(rate / 10)
            else:
                rate = 0
            week_rates.append(rate)

        for i in range(100, 9, -10):
            week_data = []
            for week_rate in week_rates:
                if week_rate >= i:
                    a = 1
                else:
                    a = 0
                week_data.append(a)
            graph_data[i] = week_data

        return graph_data





class Download(TemplateView):

    template_name='management/download.html'

    def __init__(self):
        self.param = {
            'error':'',
            'forms':DownloadForm,
        }
    
    def get(self, request):
        return self.render_to_response(self.param)
    
    def post(self, request):
        year = request.POST.get('year')
        month = request.POST.get('month')

        error = None

        if year == '' and month == '':
            error = 'ダウンロードする年と月を入力してください。'
        elif is_number(year) == False and is_number(month) == False:
            error = '正しく数字を入力してください'
        elif 1 > int(month) and int(month) > 13:
            error = '正しく月の数字を入力してください'
        elif 2000 > int(year) and int(year) > 2100:
            error = '正しく年の数字を入力してください'

        if error is None:
            titleDate = f"{year}-{month}"

            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="Log-'+ titleDate +'.csv"'},
            )

            response.write('\ufeff'.encode('utf8'))
            writer = csv.writer(response)
            writer.writerow([
                "年", "月", "日", "曜日",
                "学部", "所属", "学籍番号", "氏名", 
                "利用時間(分)", "入室時間", "退出時間", 
            ])

            data = DataGetForAnalysis(year=year, month=month)

            for i in data:
                writer.writerow([
                    i['year'], i['month'], i['day'],
                    i['weekday'], i['faculty'], i['attribute'],
                    i['student_number'], i['name'], i['duration'],
                    i['enter'], i['exit']
                ])

            return response

        self.param['error'] = error
        self.param['forms'] = DownloadForm(request.POST)#前のポスト内容を残す
        return self.render_to_response(self.param)
    


class Manage(TemplateView):

    template_name='management/list.html'

    def __init__(self):
        self.param = {
            'error':'',
            'data': None,
        }
    
    def get(self, request):
        fiter = self.request.GET.get('exit', 'yet')
        if not(fiter == 'yet' or fiter == 'al'):
            fiter = 'yet'

        is_exit=False

        if fiter == 'yet':
            is_exit=False
        else:
            is_exit=True

        self.param['data'] = DataGetForAnalysis(is_exit=is_exit)
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

        if error is None:
            timelog = TimeLog(
                is_exit = True,
                faculty = faculty, attribute = attribute, 
                student_number = student_number, 
                name = name, enter = enter,
                exit = exit,
                )
            timelog.save()
            return redirect(to='management:list')

        self.param['error'] = error
        return self.render_to_response(self.param)


def ManageUpdate(request, log_id):
    if(request.method == "POST"):
        duration = request.POST.get('duration')

        if(duration is not None and is_int(duration) and is_int(log_id)):
            log = get_object_or_404(TimeLog, pk=log_id)
            duration = int(duration)

            if log.is_exit == False:
                log.is_exit = True
                log.exit = timezone.localtime(log.enter) + timedelta(minutes=duration)
                log.save()

    return redirect(to='management:list')



def ManageDelete(request, log_id):
    if(request.method == "POST"):
        if is_number(log_id):
            log = get_object_or_404(TimeLog, pk=log_id)
            log.delete()

    return redirect(to='management:list')