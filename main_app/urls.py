from django.urls import path , re_path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path('admin_ui', views.admin_ui , name='admin_ui'),
    path('manage_patient', views.manage_patient , name='manage_patient'),
    path('add_patient', views.add_patient , name='add_patient'),
    path('get_patient', views.get_patient , name='get_patient'),
    path('delete_patient', views.delete_patient , name='delete_patient'),
    path('manage_doctor', views.manage_doctor , name='manage_doctor'),
    path('add_doctor', views.add_doctor , name='add_doctor'),
    path('get_doctor', views.get_doctor , name='get_doctor'),
    path('update_password', views.update_password , name='update_password'),
    path('update_balance', views.update_balance , name='update_balance'),
    path('delete_doctor', views.delete_doctor , name='delete_doctor'),
    path('manage_symptoms', views.manage_symptoms , name='manage_symptoms'),
    path('add_symp', views.add_symp , name='add_symp'),
    path('get_symp', views.get_symp , name='get_symp'),
    path('delete_symp', views.delete_symp , name='delete_symp'),
    path('manage_single/<int:id>', views.manage_single , name='manage_single'),
    path('add_question', views.add_question , name='add_question'),
    path('get_question', views.get_question , name='get_question'),
    path('delete_question', views.delete_question , name='delete_question'),
    path('manage_possible_cause', views.manage_possible_cause , name='manage_possible_cause'),
    path('get_possible_cause', views.get_possible_cause , name='get_possible_cause'),
    path('get_diagnosis', views.get_diagnosis , name='get_diagnosis'),
    path('add_possible_cause', views.add_possible_cause , name='add_possible_cause'),
    path('update_possible_cause', views.update_possible_cause , name='update_possible_cause'),
    path('delete_possible', views.delete_possible , name='delete_possible'),
    path('manage_single_cause/<int:id>', views.manage_single_cause , name='manage_single_cause'),
    path('add_video/<int:id>', views.add_video , name='add_video'),
    path('delete_video/', views.delete_video , name='delete_video'),
    path('preview/', views.preview , name='preview'),

    path('patient_ui', views.patient_ui , name='patient_ui'),
    path('patient_appointment', views.patient_appointment , name='patient_appointment'),
    path('pview_schedule/<int:id>', views.pview_schedule , name='pview_schedule'),
    path('pviewprofile/<str:patientusername>', views.pviewprofile , name='pviewprofile'),
    path('pconsultation_history', views.pconsultation_history , name='pconsultation_history'),
    path('consult_a_doctor', views.consult_a_doctor , name='consult_a_doctor'),
    path('make_consultation/<str:doctorusername>', views.make_consultation , name='make_consultation'),
    path('resched_event_patient', views.resched_event_patient, name="resched_event_patient"),
    path('rate_review/<int:consultation_id>', views.rate_review , name='rate_review'),


    path('dconsultation_history', views.dconsultation_history , name='dconsultation_history'),
    path('dviewprofile/<str:doctorusername>', views.dviewprofile , name='dviewprofile'),
    path('doctor_ui', views.doctor_ui , name='doctor_ui'),



    path('consultationview/<int:consultation_id>', views.consultationview , name='consultationview'),
    path('close_consultation/<int:consultation_id>', views.close_consultation , name='close_consultation'),
    path('dschedule', views.doctor_schedule, name="doctor_schedule"),
    path('dcalendar', views.doctor_calendar, name="doctor_calendar"),
    path('add_event', views.add_event, name="add_event"),
    path('get_event', views.get_event, name="get_event"),
    path('resched_event', views.resched_event, name="resched_event"),
    path('accept_event', views.accept_event, name="accept_event"),
    path('decline_event', views.decline_event, name="decline_event"),
    path('mark_done', views.mark_done, name="mark_done"),
    path('edit_profile_doctor', views.edit_profile_doctor, name="edit_profile_doctor"),
    path('edit_profile_patient', views.edit_profile_patient, name="edit_profile_patient"),




    path('post', views.post, name='post'),
    path('chat_messages', views.chat_messages, name='chat_messages'),



]
