from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import datetime
import numpy as np
import pandas as pd
import json, string
from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import *
from chats.models import Chat,Feedback

# Create your views here.


#loading trained_model





def home(request):

    if request.user.is_authenticated:
        type = ""
        user = request.user
        if patient.objects.filter(user = user).exists() == True:
            type = "patient"
        elif doctor.objects.filter(user = user).exists() == True:
            type = "doctor"
        else:
            type="admin"

        if type == "patient":
            return redirect('patient_ui')
        elif type == "doctor":
            return redirect('doctor_ui')
        else:
            return redirect('admin_ui')
    else:
        return render(request,'homepage/index.html')

def admin_ui(request):

    doctor_obj = doctor.objects.all()
    patient_obj = patient.objects.all()
    female = patient_obj.filter(gender="Female").count()
    male = patient_obj.filter(gender="Male").count()
    context = {
    "patient_obj":patient_obj,
    "female":female,
    "male":male,
    "doctor_obj":doctor_obj
    }

    return render(request,'admin/admin_ui/admin_ui.html' , context)


def manage_patient(request):

    patient_obj = patient.objects.all()

    context = {
    "patient_obj":patient_obj
    }

    return render(request,'admin/admin_ui/manage_patient.html' , context)

@csrf_exempt
def add_patient(request):
     fname =  request.POST.get('fname')
     lname =  request.POST.get('lname')
     mname =  request.POST.get('mname')
     birthday =  request.POST.get('birthday')
     gender =  request.POST.get('gender')
     civilstatus =  request.POST.get('civilstatus')
     address =  request.POST.get('address')
     birth_place =  request.POST.get('birth_place')
     contact = request.POST.get('contact')
     guardian = request.POST.get('guardian')
     guardian_two = request.POST.get('guardian_two')
     username = lname.lower() + birthday.replace('/', '')
     password = "root"+birthday.replace('/', '')
     date = datetime.datetime.strptime(birthday, "%m/%d/%Y").strftime("%Y-%m-%d")
     try:
         user = User.objects.create_user(username=username,password=password)
         user.save()

         patient_obj = patient(user=user,first_name=fname,last_name=lname,middle_name=mname,dob = date,gender = gender ,contact_number = contact,civil_status = civilstatus, guardian= guardian, other_guardian = guardian_two, address=address, birth_place=birth_place)
         patient_obj.save()
         return JsonResponse({'status':'success','message':'Patient Account & Information saved!'})
     except Exception as e:
         print(e)
         return JsonResponse({'status':'error','message':'Patient Account & Information Failed!'})

@csrf_exempt
def get_patient(request):

    patient_obj = patient.objects.all()
    data = []
    for p in patient_obj:
        data_small = {"id": p.user.id, "fname": p.first_name, "mname":p.middle_name, "lname":p.last_name, "dob":str(p.dob), "gender":p.gender, "username": p.user.username}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)
@csrf_exempt
def delete_patient(request):

    id = request.POST.get('id')

    try:

        user = User.objects.get(id=id)
        patient_obj = patient.objects.get(user=user)
        patient_obj.delete()
        user.delete()
        return JsonResponse({'status':'success','message':'Patient Account & Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Patient Account & Information Failed to Delete!'})


def manage_doctor(request):

    doctor_obj = doctor.objects.all()

    context = {
    "doctor_obj":doctor_obj
    }

    return render(request,'admin/admin_ui/manage_doctor.html' , context)

@csrf_exempt
def add_doctor(request):
    fname =  request.POST.get('fname')
    lname =  request.POST.get('lname')
    mname =  request.POST.get('mname')
    birthday =  request.POST.get('birthday')
    gender =  request.POST.get('gender')
    civilstatus =  request.POST.get('civilstatus')
    address =  request.POST.get('address')
    specialization =  request.POST.get('specialization')
    contact = request.POST.get('contact')
    username = lname.lower() + birthday.replace('/', '')
    password = "root"+birthday.replace('/', '')
    date = datetime.datetime.strptime(birthday, "%m/%d/%Y").strftime("%Y-%m-%d")
    try:
         user = User.objects.create_user(username=username,password=password)
         user.save()

         doctor_obj = doctor(user=user,first_name=fname,last_name=lname,middle_name=mname,dob = date,gender = gender ,contact = contact,civil_status = civilstatus, specialization= specialization, address=address)
         doctor_obj.save()
         return JsonResponse({'status':'success','message':'Doctor Account & Information Saved!'})
    except Exception as e:
         user.delete()
         print(e)
         return JsonResponse({'status':'error','message':'Doctor Account & Information Failed to save!'})
@csrf_exempt
def get_doctor(request):

    doctor_obj = doctor.objects.all()
    data = []
    for p in doctor_obj:
        data_small = {"id": p.user.id, "fname": p.first_name, "mname":p.middle_name, "lname":p.last_name, "dob":str(p.dob), "gender":p.gender, "username": p.user.username}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def delete_doctor(request):
    id = request.POST.get('id')

    try:
        user = User.objects.get(id=id)
        doctor_obj = doctor.objects.get(user=user)
        doctor_obj.delete()
        user.delete()
        return JsonResponse({'status':'success','message':'Doctor Account & Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Doctor Account & Information Failed to Delete!'})


@csrf_exempt
def edit_profile_doctor(request):
    id = request.POST.get('id')
    fname =  request.POST.get('fname')
    lname =  request.POST.get('lname')
    mname =  request.POST.get('mname')
    email =  request.POST.get('email')
    address =  request.POST.get('address')
    contact = request.POST.get('contact')
    user_obj = User.objects.get(id=id)
    doctor_obj = doctor.objects.get(user=user_obj)

    try:
         doctor_obj.first_name = fname
         doctor_obj.last_name = lname
         doctor_obj.middle_name = mname
         doctor_obj.address = address
         doctor_obj.contact = contact
         user_obj.email = email
         doctor_obj.save()
         user_obj.save()
         return JsonResponse({'status':'success','message':'Doctor Account & Information Saved!'})
    except Exception as e:
         print(e)
         return JsonResponse({'status':'error','message':'Doctor Account & Information Failed to save!'})

@csrf_exempt
def edit_profile_patient(request):
    id = request.POST.get('id')
    fname =  request.POST.get('fname')
    lname =  request.POST.get('lname')
    mname =  request.POST.get('mname')
    email =  request.POST.get('email')
    address =  request.POST.get('address')
    contact = request.POST.get('contact')
    user_obj = User.objects.get(id=id)
    patient_obj = patient.objects.get(user=user_obj)

    try:
         patient_obj.first_name = fname
         patient_obj.last_name = lname
         patient_obj.middle_name = mname
         patient_obj.address = address
         patient_obj.contact_number = contact
         user_obj.email = email
         patient_obj.save()
         user_obj.save()
         return JsonResponse({'status':'success','message':'Patient Account & Information Saved!'})
    except Exception as e:
         print(e)
         return JsonResponse({'status':'error','message':'Patient Account & Information Failed to save!'})

@csrf_exempt
def update_password(request):
    id = request.POST.get('id')
    password = request.POST.get('password')

    try:
        user = User.objects.get(id=id)
        user.set_password(password)
        user.save()
        return JsonResponse({'status':'success','message':'Account & Information Updated!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Account & Information Failed to Update!'})

@csrf_exempt
def update_balance(request):
    id = request.POST.get('id')
    balance = request.POST.get('balance')
    user_obj = User.objects.get(id=id)
    patient_obj = patient.objects.get(user=user_obj)
    try:
        patient_obj.balance = balance
        patient_obj.save()
        return JsonResponse({'status':'success','message':'Account & Information Updated!'})
    except Exception as e:
        return JsonResponse({'status':'error','message':'Account & Information Failed to Update!'})

def manage_symptoms(request):
    symptoms_obj = symptoms.objects.all()

    context = {
    "symptoms_obj": symptoms_obj
    }

    return render(request,'admin/admin_ui/manage_symptoms_checker.html' , context)

@csrf_exempt
def add_symp(request):
    name = request.POST.get('symp')
    try:
        symp_obj = symptoms(symptoms_name=name)
        symp_obj.save()
        return JsonResponse({'status':'success','message':'Symptoms Added Successfully!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Error adding information!'})

@csrf_exempt
def get_symp(request):
    symp_obj = symptoms.objects.all()
    data = []
    for p in symp_obj:
        data_small = {"id": p.id, "symp_name": p.symptoms_name}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def delete_symp(request):
    id = request.POST.get('id')

    try:
        sym_obj = symptoms.objects.get(id=id)
        sym_obj.delete()
        return JsonResponse({'status':'success','message':'Symptoms Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Symptoms Information Failed to Delete!'})

def manage_single(request, id):
    symptoms_obj = symptoms.objects.get(id=id)
    question_obj = symptoms_obj.question_id.all()
    possible_obj = possible.objects.all()

    context = {
    "symptoms_obj": symptoms_obj,
    "question_obj": question_obj,
    "possible_obj": possible_obj
    }

    return render(request,'admin/admin_ui/manage_single.html' , context)

@csrf_exempt
def get_question(request):
    id = request.POST.get('id')
    symptoms_obj = symptoms.objects.get(id=id)
    question_obj = symptoms_obj.question_id.all()
    data = []
    for p in question_obj:
        data_small = {"id": p.id, "q_body": p.question_body, "possible": p.possible_id.name, "possible_id": p.possible_id.id}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def delete_question(request):
    id = request.POST.get('id')

    question_obj = question.objects.get(id=id)

    try:
        question_obj.delete()
        return JsonResponse({'status':'success','message':'Question Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Question Information Failed to Delete!'})

@csrf_exempt
def add_question(request):
    id = request.POST.get('id')
    question_body = request.POST.get('body')
    symptoms_obj = symptoms.objects.get(id=id)
    check = symptoms_obj.question_id.all()
    p = request.POST.get('possible')
    possible_obj = possible.objects.get(id=p)
    r = check.filter(question_body=question_body).exists()

    if r == False:
        try:
            q = question(question_body=question_body, possible_id=possible_obj)
            q.save()
            symptoms_obj.question_id.add(q)
            return JsonResponse({'status':'success','message':'Question Added Successfully!'})
        except Exception as e:
            print(e)
            return JsonResponse({'status':'error','message':'Error adding question!'})
    else:
        return JsonResponse({'status':'error','message':'Question exist allready!'})


def manage_possible_cause(request):

    return render(request,'admin/admin_ui/manage_possible_cause.html')

@csrf_exempt
def get_possible_cause(request):
    possible_obj = possible.objects.all()

    data = []
    for p in possible_obj:
        data_small = {"id": p.id, "name": p.name}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def add_possible_cause(request):
    name = request.POST.get('name')
    info = request.POST.get('info')
    self_care = request.POST.get('self')

    try:
        possible_obj = possible(name=name, info=info, self_care=self_care)
        possible_obj.save()
        return JsonResponse({'status':'success','message':'Possible Cause Information Saved!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Possible Cause Information Failed to Save!'})

@csrf_exempt
def update_possible_cause(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    info = request.POST.get('info')
    self_care = request.POST.get('self')
    possible_obj = possible.objects.get(id=id)

    try:
        possible_obj.name = name
        possible_obj.info = info
        possible_obj.self_care = self_care
        possible_obj.save()
        return JsonResponse({'status':'success','message':'Possible Cause Information Saved!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Possible Cause Information Failed to Save!'})

@csrf_exempt
def delete_possible(request):
    id = request.POST.get('id')

    possible_obj = possible.objects.get(id=id)

    try:
        possible_obj.delete()
        return JsonResponse({'status':'success','message':'Possible Cause Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Possible Cause Information Failed to Delete!'})

def manage_single_cause(request, id):
    possible_obj = possible.objects.get(id=id)
    video_obj = video.objects.filter(possible_id=possible_obj.id)
    context= {
    "possible_obj":possible_obj,
    "video_obj":video_obj
    }

    return render(request,'admin/admin_ui/manage_single_cause.html', context)

@csrf_exempt
def get_diagnosis(request):
    id = request.POST.get('id')

    p = possible.objects.get(id=id)
    video_obj = video.objects.filter(possible_id=p.id)

    data = []
    data_vid = []

    data_small = {"id": p.id, "name": p.name, "info": p.info, "self_care": p.self_care}
    data.append(data_small)

    for v in video_obj:
        data_small = {"url":v.video_file.url}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

def add_video(request, id):
    file = request.FILES['vid']
    possible_obj = possible.objects.get(id=id)
    try:
        v = video(video_file=file, possible_id=possible_obj)
        v.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def delete_video(request):
    id = request.POST.get('id')

    video_obj = video.objects.get(id=id)

    try:
        video_obj.delete()
        return JsonResponse({'status':'success','message':'Video Information Deleted!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Possible Cause Information Failed to Delete!'})

def preview(request):
    symptoms_obj = symptoms.objects.all()

    context = {
    "symptoms_obj": symptoms_obj
    }

    return render(request,'admin/admin_ui/preview.html', context)

def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/view_profile/view_profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')




def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})

def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient

      consultationnew = consultation.objects.filter(patient = patient_obj)


      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):
     doctorusername = request.session['doctorusername']
     duser = User.objects.get(username=doctorusername)
     doctor_obj = duser.doctor
     consultation_obj = consultation.objects.filter(doctor = doctor_obj)
     for c in consultation_obj:
         print(c.id)
     return render(request,'doctor/consultation_history/consultation_history.html',{"consultation_obj":consultation_obj})



def doctor_ui(request):

    doctorid = request.session['doctorusername']
    duser = User.objects.get(username=doctorid)
    r = rating_review.objects.filter(doctor=duser.doctor)
    schedule = schedule_consultation.objects.filter(doctor=duser.doctor, status = 1)
    schedule_a = schedule_consultation.objects.filter(doctor=duser.doctor, status = 3)
    consultation_obj = consultation.objects.filter(doctor=duser.doctor, status = 'active')
    patient_obj = patient.objects.all()
    female = patient_obj.filter(gender="Female").count()
    male = patient_obj.filter(gender="Male").count()
    context = {
    "duser":duser,
    "rate":r,
    "patient_obj":patient_obj,
    "female":female,
    "male":male,
    "schedule":schedule,
    "schedule_a":schedule_a,
    "consultation_obj":consultation_obj
    }

    return render(request,'doctor/doctor_ui/profile.html',context)



def dviewprofile(request, doctorusername):

    if request.method == 'GET':


         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)

         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )


def consult_a_doctor(request):
        dobj = doctor.objects.all()
        consultation_obj = consultation.objects.filter(patient=request.user.patient)
        context ={
            "dobj":dobj,
            "consultation_obj":consultation_obj
        }
        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',context)

def make_consultation(request, doctorusername):

    if request.method == 'POST':

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient


        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername

        consultation_date = date.today()
        status = "active"

        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")


        return redirect('consultationview',consultation_new.id)



def consultationview(request,consultation_id):

    request.session['consultation_id'] = consultation_id
    consultation_obj = consultation.objects.get(id=consultation_id)

    context = {
    "consultation_obj":consultation_obj
    }

    return render(request,'consultation/consultation.html', context)





def rate_review(request,consultation_id):
   if request.method == "POST":

         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)


         return redirect('consultationview',consultation_id)



def close_consultation(request,consultation_id):
   if request.method == "POST":

         consultation.objects.filter(pk=consultation_id).update(status="closed")

         return redirect('home')



def doctor_schedule(request):
    schedule = schedule_consultation.objects.filter(doctor_id=request.user.doctor)

    context = {

    "schedule":schedule
    }
    return render(request, 'doctor/schedule/doctor_schedule.html', context)

def doctor_calendar(request):

    schedule = schedule_consultation.objects.filter(doctor_id=request.user.doctor, status=3)

    context = {
    "schedule":schedule
    }

    return render(request, 'doctor/schedule/doctor_calendar.html', context)

def patient_appointment(request):
    schedule = schedule_consultation.objects.filter(patient_id=request.user.patient)
    dobj = doctor.objects.all()
    context = {
    "dobj": dobj,
    "schedule":schedule
    }

    return render(request, 'patient/appointment/appointment.html', context)

def pview_schedule(request, id):
    user = User.objects.get(id=id)
    schedule = schedule_consultation.objects.filter(doctor_id=user.doctor, status=3)
    patient = request.user

    context = {
    "schedule":schedule,
    "user": user,
    "patient":patient
    }
    return render(request, 'patient/appointment/calendar.html', context)

@csrf_exempt
def add_event(request):
    starting = request.POST.get("starting")
    ending = request.POST.get("ending")
    date = request.POST.get("date")
    pid = request.POST.get("pid")
    did = request.POST.get("did")
    user_doc = User.objects.get(id=did)
    doctor_obj = doctor.objects.get(user=user_doc)
    user_patient = User.objects.get(id=pid)
    patient_obj = patient.objects.get(user=user_patient)
    start = date+" "+starting.replace(' AM', 'Z')
    end = date+" "+ending.replace(' AM', 'Z')
    check = schedule_consultation.objects.filter(doctor_id = doctor_obj, status=3)
    existed = False
    date_exist = []
    date_obj = []
    date_check = pd.date_range(start, end, periods=10)
    count_obj = 0
    for s in date_check:
        date_obj.append(date_check)
    for c in check:
        count_obj + 1
        if existed != True:
            s = c.starting_time
            e = c.ending_time
            date_exist = pd.date_range(s, e, periods=10)
            for date in date_check:
                if date in date_exist:
                    existed = True
                else:
                    existed = False
        else:
            break

    if existed == False:
        print(count_obj)
        if count_obj <= 10:
            try:
                sched = schedule_consultation(starting_time=start, ending_time=end, doctor=doctor_obj, patient=request.user.patient, status=1, event_title='Appointment')
                sched.save()
                return JsonResponse({'status':'success','message':'Appointment Request Sent Please Wait for the Confirmation!'})
            except Exception as e:
                print(e)
                return JsonResponse({'status':'error','message':'Error!'})
        else:
            return JsonResponse({'status':'error','message':'Maximum Appointment is Set!'})
    else:
        return JsonResponse({'status':'error','message':'Date is not available!'})

@csrf_exempt
def get_event(request):
    id = request.POST.get('id')
    schedule = schedule_consultation.objects.get(id=id)
    data = {'id':schedule.id, 'starting':str(schedule.starting_time), 'ending':str(schedule.ending_time)}
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def resched_event(request):
    id = request.POST.get('id')
    starting = request.POST.get("starting")
    ending = request.POST.get("ending")
    date = request.POST.get("date")
    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    start = date_obj+" "+starting.replace(' AM', 'Z')
    end = date_obj+" "+ending.replace(' AM', 'Z')

    schedule = schedule_consultation.objects.get(id=id)
    check = schedule_consultation.objects.filter(doctor_id = request.user.doctor, status=3);

    existed = False
    date_exist = []
    date_obj = []
    date_check = pd.date_range(start, end, periods=10)
    for s in date_check:
        print(s)
        date_obj.append(date_check)

    for c in check:
        if existed != True:
            s = c.starting_time
            e = c.ending_time
            date_exist = pd.date_range(s, e, periods=10)
            for date in date_check:
                if date in date_exist:
                    existed = True
                else:
                    existed = False
        else:
            break

    if existed == False:
        try:
            schedule.starting_time = start
            schedule.ending_time = end
            schedule.status = 2
            schedule.save()
            return JsonResponse({'status':'success','message':'Resched save waiting for the confirmation!'})
        except:
            return JsonResponse({'status':'error','message':'Date is not available!'})

    else:
        return JsonResponse({'status':'error','message':'Date is not available!'})

@csrf_exempt
def accept_event(request):
    id = request.POST.get('id')
    schedule = schedule_consultation.objects.get(id=id)
    check = schedule_consultation.objects.filter(doctor_id = schedule.doctor, status=3);
    existed = False
    date_exist = []
    date_obj = []
    date_check = pd.date_range(schedule.starting_time, schedule.ending_time)
    for s in date_check:
        date_obj.append(date_check)
    for c in check:
        if existed != True:
            s = c.starting_time
            e = c.ending_time
            date_exist = pd.date_range(s, e, periods=10)
            for date in date_check:
                if date in date_exist:
                    existed = True
                else:
                    existed = False
        else:
            break

    if existed == False:
        patien_name = schedule.patient.first_name + " " + schedule.patient.last_name
        doctor_name = schedule.doctor.first_name + " " + schedule.doctor.last_name
        patient_obj = patient.objects.get(user=schedule.patient.user)
        try:
            schedule.event_title = "Schedule with patient " + str(patien_name) + " doctor " + str(doctor_name)
            schedule.status = 3
            schedule.save()
            patient_obj.balance = 100.00
            patient_obj.save()
            return JsonResponse({'status':'success','message':'Accept Complete!'})
        except Exception as e:
            print(e)
            return JsonResponse({'status':'error','message':'Error!'})
    else:
        return JsonResponse({'status':'error','message':'Date is not available!'})

@csrf_exempt
def resched_event_patient(request):
    id = request.POST.get('id')
    starting = request.POST.get("starting")
    ending = request.POST.get("ending")
    date = request.POST.get("date")
    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    start = date_obj+" "+starting.replace(' AM', 'Z')
    end = date_obj+" "+ending.replace(' AM', 'Z')

    schedule = schedule_consultation.objects.get(id=id)

    try:
        schedule.starting_time = start
        schedule.ending_time = end
        schedule.status = 1
        schedule.save()
        return JsonResponse({'status':'success','message':'Reschedule save waiting for the confirmation!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Date is not available!'})

@csrf_exempt
def decline_event(request):
    id = request.POST.get('id')

    schedule = schedule_consultation.objects.get(id=id)

    try:
        schedule.delete()
        return JsonResponse({'status':'success','message':'Consultion has been declined!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Failed to decline!'})

@csrf_exempt
def mark_done(request):
    id = request.POST.get('id')

    schedule = schedule_consultation.objects.get(id=id)

    try:
        schedule.status = 4
        schedule.save()
        return JsonResponse({'status':'success','message':'Done!'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'error','message':'Failed!'})
#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id']
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id']

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#-----------------------------chatting system ---------------------------------------------------
