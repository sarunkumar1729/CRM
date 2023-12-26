from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse
from UserApp.models import *
from admin_app.models import *
from .forms import *
from admin_app.forms import *
from UserApp.forms import *
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db.models import Q
from .forms import *
from django.http import JsonResponse
from django.utils import timezone
from django.db import IntegrityError
import datetime

# Create your views here.

def Home(request):
    
    return render(request, 'Faculty/Home.html')

def Profile(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    batches = faculty.batches_faculty.all()
    context = {'faculty':faculty , 'batches':batches}
    return render(request,'Faculty/Profile.html',context)


def Batches(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    batches = faculty.batches_faculty.all()
    context = {'batches':batches}
    return render(request,'Faculty/Batches.html',context)




def Batch_Students_List(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = Student.objects.filter(batch=batch).annotate(
        reg_no_int=Cast('reg_no', output_field=IntegerField())
    ).order_by('reg_no_int')

    context = {
        'batch': batch,
        'students': students,
    }

    return render(request, 'Faculty/Batch_Students_List.html', context)



def Student_Profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = {'student': student}
    return render(request, 'Faculty/Student_Profile.html', context)



def Search_Batch_Students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    
    # Get the batch-specific students
    students_query = Student.objects.filter(batch=batch).annotate(
        reg_no_int=Cast('reg_no', output_field=IntegerField())
    ).order_by('reg_no_int')

    # Get the search query
    query = request.GET.get('q')

    if query:
        # Filter the students based on the search query
        students = students_query.filter(
            Q(admin__first_name__icontains=query) | 
            Q(admin__last_name__icontains=query) | 
            Q(reg_no__icontains=query)
        )
    else:
        # If no search query, display all batch students
        students = students_query

    context = {
        'batch': batch,
        'students': students,
    }

    return render(request, 'Faculty/Batch_Students_List.html', context)




def Faculty_Students(request):
    faculty = get_object_or_404(Faculty, admin=request.user)

    # Retrieve all batches associated with the faculty
    faculty_batches = faculty.batches_faculty.all()

    # Retrieve students from all batches associated with the faculty
    students = Student.objects.filter(batch__in=faculty_batches).annotate(
        reg_no_int=Cast('reg_no', output_field=IntegerField())
    ).order_by('reg_no_int')

    context = {
        'faculty': faculty,
        'students': students,
    }

    return render(request, 'Faculty/Faculty_Students.html', context)



def Search_Faculty_Students(request):
    query = request.GET.get('q')

    faculty = Faculty.objects.get(admin=request.user)  # Assuming you have a Faculty model

    if query:
        students = CustomUser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(student__reg_no__icontains=query),
            user_type=4,
            student__batch__in=faculty.batches_faculty.all()  # Filter by batches associated with the faculty
        ).annotate(reg_no_int=Cast('student__reg_no', IntegerField())).order_by('reg_no_int')
    else:
        students = CustomUser.objects.filter(
            user_type=4,
            student__batch__in=faculty.batches_faculty.all()  # Filter by batches associated with the faculty
        ).annotate(reg_no_int=Cast('student__reg_no', IntegerField())).order_by('reg_no_int')

    context = {
        'students': students,
    }
    return render(request, 'Faculty/Faculty_Students.html', context)






def Attendance_Page(request):
    faculty = get_object_or_404(Faculty, admin=request.user)
    batches = faculty.batches_faculty.all()
    context = {'batch': batches}
    
    return render(request,'Faculty/Attendance.html',context)




def Take_Attendance(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = Student.objects.filter(batch=batch).annotate(
        reg_no_int=Cast('reg_no', output_field=IntegerField())
    ).order_by('reg_no_int')

    # Use the current date for attendance
    date = timezone.now().date()

    # Check if attendance already exists for the specified date
    existing_attendance = Attendance.objects.filter(
        Q(date=date) & Q(student__batch=batch)
    )

    if request.method == 'POST':
        try:
            if existing_attendance.exists():
                messages.warning(request, "Attendance already added for today.")
            else:
                # Iterate through students to record attendance
                for student in students:
                    # Check if the checkbox is present in the form data
                    checkbox_value = f'student_{student.id}'
                    status = checkbox_value in request.POST

                    # Create Attendance object for each student
                    attendance = Attendance.objects.create(
                        student=student,
                        date=date,
                        status=status
                    )

                # Display success message and redirect to the Attendance page for the specific batch
                messages.success(request, "Successfully Added")
                return redirect(reverse('Take_Attendance', args=[batch.id]))

        except IntegrityError as e:
            # Display error message if there's an integrity violation (e.g., duplicate entry)
            messages.error(request, f"Could Not Add: {e}")

    # Prepare context for rendering the template
    context = {'batch': batch, 'students': students, 'existing_attendance': existing_attendance}

    # Render the template with the context
    return render(request, 'Faculty/Take_Attendance.html', context)

   
   
   
   
   
def View_Attendance_Page(request, batch_id):
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        return redirect(reverse('View_Attendance', args=[batch_id, selected_date]))

    return render(request, 'Faculty/View_Attendance_Page.html', {'batch_id': batch_id})



def get_attendance_data(batch_id, selected_date):
    try:
        # Assuming you have a model named Attendance with a foreign key to Student and a date field
        attendance_data = Attendance.objects.filter(student__batch_id=batch_id, date=selected_date).order_by(Cast('student__reg_no', IntegerField()))
    except Attendance.DoesNotExist:
        attendance_data = []

    return attendance_data




def View_Attendance(request, batch_id, date_str):
    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        batch_name = Batch.objects.get(id=batch_id).name
        attendance_data = get_attendance_data(batch_id, selected_date)

        if request.method == 'POST':
            try:
                # Iterate through attendance data to update the status based on checkbox values
                for attendance_record in attendance_data:
                    checkbox_value = f'student_{attendance_record.student.id}'
                    status = checkbox_value in request.POST
                    attendance_record.status = status
                    attendance_record.save()

                messages.success(request, "Attendance updated successfully.")

            except IntegrityError as e:
                messages.error(request, f"Could Not Update: {e}")

        context = {'batch_name': batch_name, 'batch_id': batch_id, 'selected_date': selected_date, 'attendance_data': attendance_data}
        return render(request, 'Faculty/View_Attendance.html', context)

    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect(reverse('View_Attendance_Page'))
    
    
    
    
