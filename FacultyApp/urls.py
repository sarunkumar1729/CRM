from django.urls import path,include
from . import views

urlpatterns = [
    path('Home/',views.Home,name='Faculty_Home'),
    path('Batches/',views.Batches,name='Faculty_Batches'),
    
    path('Profile/',views.Profile,name='Faculty_Profile'),
    path('Student_Profile/<int:student_id>',views.Student_Profile,name='Student_Profile'),
    
    path('Batch_Students_List/<int:batch_id>',views.Batch_Students_List,name='Batch_Students_List'),
    path('Search_Students/<int:batch_id>/', views.Search_Batch_Students, name='Search_Students'),
    
    
    path('Faculty_Students/',views.Faculty_Students,name='Faculty_Students'),
    path('Search_Faculty_Students/',views.Search_Faculty_Students,name='Search_Faculty_Students'),
    
    path('Attendance_Page/',views.Attendance_Page,name='Attendance_Page'),
    path('Take_Attendance/<int:batch_id>',views.Take_Attendance,name='Take_Attendance'),
    path('View_Attendance_Page/<int:batch_id>/',views.View_Attendance_Page,name='View_Attendance_Page'),
    path('View_Attendance/<int:batch_id>/<str:date_str>/', views.View_Attendance, name='View_Attendance'),
    
    ]