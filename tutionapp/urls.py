from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('teacher_signup', views.teacher_signup, name='teacher_signup'),
    path('student_signup', views.student_signup, name='student_signup'),
    path('teacher_home', views.teacher_home, name='teacher_home'),
    path('student_home', views.student_home, name='student_home'),

    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('approve/<int:d>', views.approve, name='approve'),
    path('disapprove/<int:d>', views.disapprove, name='disapprove'),

    path('add_teacher', views.add_teacher, name='add_teacher'),
    path('add_student', views.add_student, name='add_student'),
    path('log_in', views.log_in, name='log_in'),
    path('logout', views.logout, name='logout'),

    path('teacher_pw_reset', views.teacher_pw_reset, name='teacher_pw_reset'),
    path('teacher_reset', views.teacher_reset, name='teacher_reset'),
    path('student_pw_reset', views.student_pw_reset, name='student_pw_reset'),
    path('student_reset', views.student_reset, name='student_reset'),

    
    
]