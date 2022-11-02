from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.
#user = models.OneToOneField(settings.AUTH_USER_MODEL)

class patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_photo = models.ImageField(upload_to='profile_photo', default="default.jpeg")
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)

    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50, null=True)
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    birth_place = models.CharField(max_length = 100)
    contact_number = models.CharField(max_length = 15, null=True)
    gender = models.CharField(max_length = 10)
    civil_status = models.CharField(max_length = 10)
    guardian = models.CharField(max_length = 255, null=True)
    other_guardian = models.CharField(max_length = 255, null=True)

    balance = models.CharField(max_length = 200, default="0.00")

    @property
    def age(self):
        today = date.today()
        db = self.dob
        age = today.year - db.year
        if today.month < db.month or today.month == db.month and today.day < db.day:
            age -= 1
        return age
    def full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'



class doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_photo = models.ImageField(upload_to='profile_photo', default="default.jpeg")
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)

    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50, null=True)
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    contact = models.CharField(max_length = 15)
    gender = models.CharField(max_length = 10)
    civil_status = models.CharField(max_length = 10)

    specialization = models.CharField(max_length = 30)

    rating = models.IntegerField(default=0)

    @property
    def full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class possible(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    info = models.TextField(max_length=255)
    self_care = models.TextField(max_length=255, null=True)

class video(models.Model):
    id = models.AutoField(primary_key=True)
    possible_id = models.ForeignKey(possible, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='possible_cause_video')

class question(models.Model):
    id = models.AutoField(primary_key=True)
    question_body = models.CharField(max_length=255)
    possible_id = models.ForeignKey(possible, on_delete=models.CASCADE, null=True)

class symptoms(models.Model):
    id = models.AutoField(primary_key=True)
    symptoms_name = models.CharField(max_length=255, unique=True)
    question_id = models.ManyToManyField(question)


class consultation(models.Model):
    patient = models.ForeignKey(patient ,null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.CASCADE)
    consultation_date = models.DateField()
    status = models.CharField(max_length = 20)

class rating_review(models.Model):

    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)

    rating = models.IntegerField(default=0)
    review = models.TextField( blank=True )
    @property
    def rating_is(self):
        new_rating = 0
        rating_obj = rating_review.objects.filter(doctor=self.doctor)
        for i in rating_obj:
            new_rating += i.rating

        new_rating = new_rating/len(rating_obj)
        new_rating = int(new_rating)

        return new_rating

class schedule_consultation(models.Model):
    STATUS_CHOICES = (
        ('1', 'approved_doctor'),
        ('2', 'approved_patient'),
        ('3', 'aggreed'),
        ('4', 'done'),
    )
    patient = models.ForeignKey(patient ,null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(doctor ,null=True, on_delete=models.SET_NULL)
    event_title = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
