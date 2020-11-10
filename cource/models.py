from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField('Название организации', max_length=100)
    email = models.CharField('Электронный адрес', max_length=100)
    web_site = models.CharField('Адрес сайта', max_length=100)
    document_series = models.CharField('Серия документа', max_length=100)
    document_number = models.IntegerField('Номер документа')
    document_type = models.CharField('Вид документа', max_length=100)

    def __str__(self):
        return self.name

class Cource(models.Model):
    TYPE_OF_COURCE_CHOICES = [
        ('Груповые', 'Груповые'),
        ('Индивидуальные', 'Индивидуальные'),
    ]

    ATTENDANCE_CHOICES = [
        ('Очные', 'Очные'),
        ('Заочные', 'Заочные'),
    ]

    BASE_EDUCATION_CHOICES = [
        ('Среднее', 'Среднее'),
        ('Высшее', 'Высшее'),
    ]

    GRADUATE_CONTROL_CHOICES = [
        ('Квалификационная работа', 'Квалификационная работа'),
        ('Экзамен', 'Экзамен'),
        ('Собеседование', 'Собеседование'),
    ]

    GRADUATE_DOCUMENT_CHOICES = [
        ('Документ государственного образца', 'Документ государственного образца'),
        ('Сертификат', 'Сертификат'),
    ]

    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    type_of_cource = models.CharField('Тип проведения', choices=TYPE_OF_COURCE_CHOICES, max_length=100)  
    attendance = models.CharField('Вид проведения', choices=ATTENDANCE_CHOICES, max_length=100)
    start_date = models.DateField('Дата начала курсов')
    end_date = models.DateField('Дата окончания курсов')
    study_hours = models.IntegerField('Колличество часов обучения')
    base_education = models.CharField('Базовое образование', choices=BASE_EDUCATION_CHOICES, max_length=100)
    graduate_control = models.CharField('Вид выпускного контроля', choices=GRADUATE_CONTROL_CHOICES, max_length=100)
    graduate_document = models.CharField('Вид выдаваемого документа', choices=GRADUATE_DOCUMENT_CHOICES, max_length=100)
    price = models.IntegerField('Стоимость обучения')
    organization = models.ForeignKey(Organization, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    
class Topic(models.Model):
    cource = models.ForeignKey(Cource, on_delete = models.CASCADE)
    name = models.CharField('Название', max_length=100)
    hours = models.IntegerField('Колличество часов')

    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAY_CHOICES = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]

    cource = models.ForeignKey(Cource, on_delete = models.CASCADE)
    day = models.CharField('День', choices=DAY_CHOICES, max_length=100)
    from_time = models.TimeField('Начало занятия')
    to_time = models.TimeField('Конец занятия')

    def __str__(self):
        return self.day

class UserCource(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    cource = models.ForeignKey(Cource, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username
