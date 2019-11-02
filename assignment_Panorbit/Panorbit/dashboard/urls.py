from django.urls import path
from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.signup, name='index'),
    url(r'^signup_form/', views.signup_form, name='signup_form'),
    url(r'^signup_test/', views.signup_test, name='signup_test'),
    url(r'^check_if_mail_exist/', views.check_if_mail_exist, name='check_if_mail_exist'),
    url(r'^send_otp_email/', views.send_otp_email, name='send_otp_email'),
    url(r'^send_otp_email_registered/', views.send_otp_email_registered, name='send_otp_email_registered'),
    url(r'^validate_otp/', views.validate_otp, name='validate_otp'),
    url(r'^login/', views.login_sample, name='login_sample'),
    url(r'^login_test/', views.login_test, name='login_test'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^test/', views.test, name='test'),
    url(r'^selected_name/', views.selected_name, name='selected_name'),
    url(r'^country_details/', views.country_details, name='country_details'),
    url(r'^autocompleteModel/', views.autocompleteModel, name='autocompleteModel'),
]