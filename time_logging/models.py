from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class TimeLog(models.Model):
    is_exit=models.BooleanField(default=False)
    faculty = models.CharField(max_length=20)
    attribute = models.CharField(max_length=20)
    student_number = models.CharField(max_length=10,blank = True,
                                    null=True,
                                    validators=[RegexValidator(r'^[0-9]{8}$')],
                                    )
    name = models.CharField(max_length=50,blank = True,null=True)
    start_date = models.DateTimeField(null=True, blank=True,)
    end_date = models.DateTimeField(null=True, blank=True,)
    enter=models.DateTimeField()
    exit=models.DateTimeField(blank = True,null=True)

    def __str__(self):
        text = f"学部：{self.faculty}、属性：{self.attribute}、入室時間：{timezone.localtime(self.enter)}"
        return text
