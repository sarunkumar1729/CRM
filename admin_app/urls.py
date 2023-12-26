from django.urls import path,include
from . import views 

urlpatterns = [
    path('Home/',views.Home,name='Admin_Home'),
    path('UpdateProfile/',views.UpdateProfile,name='Admin_Update_Profile'),
    
    # Course
    
    path('Courses/',views.Courses,name='Courses'),
    path('Add_Course/',views.Add_Course,name='Add_Course'),
    path('Edit_Course/<int:course_id>',views.Edit_Course,name='Edit_Course'),
    path("Delete_Course/<int:course_id>",views.Delete_Course, name='Delete_Course'),
    
    # FACULTY
    path('Manage_Faculty/',views.Manage_Faculty,name='Manage_Faculty'),
    path('Add_Faculty',views.Add_Faculty,name='Add_Faculty'),
    path('Edit_Faculty/<int:faculty_id>',views.Edit_Faculty,name='Edit_Faculty'),
    path('Delete_Faculty/<int:faculty_id>',views.Delete_Faculty,name='Delete_Faculty'),
    
    #BATCH
    path('Batches/',views.Batches,name='Batches'),
    path('Add_Batch/',views.Add_Batch,name='Add_Batch'),
    path('Edit_Batch/<int:batch_id>',views.Edit_Batch,name='Edit_Batch'),
    path('Delete_Batch/<int:batch_id>',views.Delete_Batch,name='Delete_Batch'),
    
    # STUDENT
    path('Students',views.Students,name='Students'),
    path('Add_Student',views.Add_Student,name='Add_Student'),
    path('Edit_Student/<int:student_id>',views.Edit_Student,name='Edit_Student'),
    path('Delete_Student/<int:student_id>',views.Delete_Student,name='Delete_Student'),
    
    #Access Students in a Batch
    path('Batch_Students/<int:batch_id>',views.Batch_Students,name='Batch_Students'),
    
    #Profile Page of Each Student
    path('Student_Profile/<int:student_id>',views.Student_Profile,name='Student_Profile'),
    
    #Profile Page of Each Faculty
    path('Faculty_Profile/<int:faculty_id>',views.Faculty_Profile,name='Faculty_Profile'),
    
    
    #SEARCH
    path('Search_Students/', views.Search_Students, name='Search_Students'),
    path('Search_Faculty/',views.Search_Faculty,name='Search_Faculty'),
    path('Search_Batches/',views.Search_Batches,name='Search_Batches'),
    
    
    #ATTENDANCE
    path('Admin_Select_Attendance/',views.Admin_Select_Attendance,name='Admin_Select_Attendance'),
    
    
    #ASSESSMENTS
    path('Assessments/',views.Assessments,name='Assessments'),
    path('Add_Assessment/',views.Add_Assessment,name='Add_Assessment'),
    path('Edit_Assessment/<int:assessment_id>',views.Edit_Assessment,name='Edit_Assessment'),
    path('Delete_Assessment/<int:assessment_id>',views.Delete_Assessment,name='Delete_Assessment'),
    
    
]