from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import *
from UserApp.models import *
from UserApp.forms import *
from .forms import *
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import IntegerField,CharField
from django.db.models.functions import Cast
from django.db.models import Q


# Create your views here.
def Home(request):
    # if request.user.is_authenticated:
    #     user_info = {
    #         'username': request.user.username,
    #         'profile_pic': request.user.profile_pic.url if request.user.profile_pic else None,
    #         'address':request.user.address
            
    #     }
    # else:
    #     user_info = None

    # context = {'user_info': user_info}
    return render(request,'Admin/Home.html')






def UpdateProfile(request):
    admin = get_object_or_404(Admin,admin=request.user) #It tries to get an instance of the Admin model where the admin field matches the current user making the request. If no such object is found, it returns a 404 response
    form=AdminForm(request.POST or None, request.FILES or None,instance=admin)
    context = {'form':form,}
    if request.method == 'POST':
        try:
            if form.is_valid():    # is extracting the cleaned data for the 'first_name' field from the form.
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                password = form.cleaned_data.get('password') or None
                pic = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if pic != None:
                    custom_user.profile_pic  = pic
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.address = address
                custom_user.gender = gender
                custom_user.save()
                messages.success(request,'Profile Updated')
                return redirect(reverse('Admin_Update_Profile'))
            else:
                messages.error(request,"Invalid Credentials")
        except Exception as e:
            messages.error(request,"Error Occured while Updating" + str(e))     
    return render(request,'Admin/UpdateProfile.html',context)





# COURSE SECTION


def Courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request,'Admin/Courses.html',context)



def Add_Course(request):
    form = CourseForm(request.POST or None)
    context = {'form':form}
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            fee = form.cleaned_data.get('fee')
            try:
                course = Course()
                course.name = name
                course.fee = fee
                course.save()
                # messages.success(request,"Course Added Successfully")
                return redirect(reverse('Courses'))
            except:
                messages.error(request,"Failed to Add Course, Pls Try Again..")
        else:
            messages.error(request,"Failed to Add Course, Pls Try Again")
    return render (request,'Admin/Add_Course.html',context)


def Edit_Course(request,course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {'form':form,'course_id':course_id}
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            fee = form.cleaned_data.get('fee')
            try:
                course = Course.objects.get(id=course_id)
                course.name = name
                course.fee = fee
                course.save()
                # messages.success(request,"Course Edited Successfully")
                return redirect(reverse('Courses'))
            except:
                messages.error(request,"Failed to Edit Course, Pls Try Again..")
        else:
            messages.error(request,"Failed to Edit Course")
    return render(request,'Admin/Edit_Course.html',context)



def Delete_Course(request,course_id):
    course = get_object_or_404(Course,id=course_id)
    try:
        course.delete()
        messages.success(request, "Course deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some students are assigned to this course already. Kindly change the affected student course and try again")
    return redirect(reverse('Courses'))
                
                
                
    
    
    
# FACULTY SECTION

def Manage_Faculty(request):
    faculty_list = CustomUser.objects.filter(user_type=2).annotate(fac_id_as_int=Cast('faculty__fac_id', output_field=IntegerField())).order_by('fac_id_as_int')

    context = {
        'faculty_list': faculty_list,
    }
    return render(request,'Admin/Manage_Faculty.html',context)


def Add_Faculty(request):
    form = FacultyForm(request.POST or None, request.FILES or None)
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            address=form.cleaned_data.get('address')
            email=form.cleaned_data.get('email')
            gender=form.cleaned_data.get('gender') 
            password=form.cleaned_data.get('password')
            fac_id = form.cleaned_data.get('fac_id')
            age = form.cleaned_data.get('age')
            phone = form.cleaned_data.get('phone')
            course=form.cleaned_data.get('course')
            joining_date = form.cleaned_data.get('joining_date')
            starting_salary = form.cleaned_data.get('starting_salary')      
            current_salary = form.cleaned_data.get('current_salary')      
            profile_pic=request.FILES.get('profile_pic')   
            
            # Save the profile picture using default_storage
            filename = default_storage.save(f'profile_pics/{profile_pic.name}', profile_pic)
            profile_pic_url = default_storage.url(filename)
            
            try:
                user = CustomUser.objects.create_user(
                   user_type=2,email=email,password=password,first_name=first_name, last_name=last_name, profile_pic=profile_pic_url
                )
                user.gender = gender
                user.address = address
                user.faculty.fac_id = fac_id
                user.faculty.age = age
                user.faculty.phone = phone
                user.faculty.course = course
                user.faculty.joining_date= joining_date
                user.faculty.starting_salary = starting_salary
                user.faculty.current_salary = current_salary
                user.save()
                messages.success(request,"Faculty Added")
                return redirect(reverse('Add_Faculty'))
            except Exception as e:
                messages.error(request,"Failed"+ str(e))
        else:
            messages.error(request, "Please fulfil all requirements")
    return render(request,'Admin/Add_Faculty.html',context)
                
                
                
                

def Edit_Faculty(request,faculty_id):
    faculty = get_object_or_404(Faculty,id=faculty_id)
    form = FacultyForm(request.POST or None, instance=faculty)
    context = {
        'form':form,
        'faculty_id':faculty_id
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            fac_id = form.cleaned_data.get('fac_id')
            age = form.cleaned_data.get('age')
            phone = form.cleaned_data.get('phone')
            joining_date = form.cleaned_data.get('joining_date')
            starting_salary = form.cleaned_data.get('starting_salary')      
            current_salary = form.cleaned_data.get('current_salary')      
            profile_pic=request.FILES.get('profile_pic') or None  

            try:
                user =  CustomUser.objects.get(id=faculty.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if profile_pic != None:
                    filename = default_storage.save(f'profile_pics/{profile_pic.name}', profile_pic)
                    profile_pic_url = default_storage.url(filename)
                    user.profile_pic = profile_pic_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                faculty.course=course
                faculty.fac_id = fac_id
                faculty.age = age
                faculty.phone = phone
                faculty.course = course
                faculty.joining_date= joining_date
                faculty.starting_salary = starting_salary
                faculty.current_salary = current_salary
                user.save()
                faculty.save()
                messages.success(request,"Faculty Updated !..")
                return redirect(reverse('Edit_Faculty',args=[faculty_id]))
            except Exception as e:
                messages.error(request,'Updation Failed!..' + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=faculty_id)
        faculty = Faculty.objects.get(id=user.id)
        return render(request, "Admin/Edit_Faculty.html", context)   
                


def Delete_Faculty(request, faculty_id):
    faculty = get_object_or_404(CustomUser, faculty__id=faculty_id)
    faculty.delete()
    messages.success(request, "Faculty deleted successfully!")
    return redirect(reverse('Manage_Faculty'))




#BATCH SECTION



def Add_Batch(request):
    form = BatchForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Batch Created")
                return redirect(reverse('Add_Batch'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "Admin/Add_Batch.html", context)


def Batches(request):
    batches = Batch.objects.all()
    context = {'batches': batches}
    return render(request, "Admin/Batches.html", context)


def Edit_Batch(request, batch_id):
    instance = get_object_or_404(Batch, id=batch_id)
    form = BatchForm(request.POST or None, instance=instance)
    context = {'form': form, 'batch_id': batch_id}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Batch Updated")
                return redirect(reverse('Edit_Batch', args=[batch_id]))
            except Exception as e:
                messages.error(
                    request, "Batch Could Not Be Updated " + str(e))
                return render(request, "Admin/Edit_Batch.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "Admin/Edit_Batch.html", context)

    else:
        return render(request, "Admin/Edit_Batch.html", context)


def Delete_Batch(request,batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    try:
        batch.delete()
        messages.success(request, "Batch deleted successfully!")
    except Exception:
        messages.error(
            request, "There are students assigned to this Batch. Please move them to another Batch.")
    return redirect(reverse('Batches'))





# STUDENTS SECTION

def Students(request):
    student_list = CustomUser.objects.filter(user_type=4).annotate(reg_no_int=Cast('student__reg_no', IntegerField())).order_by('reg_no_int')
    context = {
        'student_list': student_list,
    }
    return render(request,'Admin/Students.html',context)


def Add_Student(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            reg_no = form.cleaned_data.get('reg_no')
            phone1 = form.cleaned_data.get('phone1')
            phone2 = form.cleaned_data.get('phone2')
            educational_qualification = form.cleaned_data.get('educational_qualification')
            domain = form.cleaned_data.get('domain')
            completion_date = form.cleaned_data.get('completion_date')
            course = form.cleaned_data.get('course')
            batch = form.cleaned_data.get('batch')
            work_experience = form.cleaned_data.get('work_experience')
            qualified = form.cleaned_data.get('qualified', False)  # Default to False if not provided
            placement_preferred = form.cleaned_data.get('placement_preferred', False)  # Default to False if not provided
             # Check conditions and update qualified and placement_preferred accordingly
            if not qualified and not placement_preferred:
                qualified = False
                placement_preferred = False
            else:
                qualified = True
                placement_preferred = True
            
            profile_pic=request.FILES.get('profile_pic')  
            filename = default_storage.save(f'profile_pics/{profile_pic.name}', profile_pic)
            profile_pic_url = default_storage.url(filename)
            
            resume = request.FILES.get('resume')
            if resume:
                resume_filename = default_storage.save(f'resumes/{resume.name}', resume)
                resume_url = default_storage.url(resume_filename)
            else:
                resume_url = None
            
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=4, first_name=first_name, last_name=last_name, profile_pic=profile_pic_url)
                user.gender = gender
                user.address = address
                user.student.reg_no = reg_no
                user.student.phone1 = phone1
                user.student.phone2 = phone2
                user.student.educational_qualification = educational_qualification
                user.student.domain = domain
                user.student.qualified = qualified
                user.student.completion_date = completion_date
                user.student.course = course
                user.student.batch = batch
                user.student.work_experience = work_experience
                user.student.placement_preferred = placement_preferred
                if resume_url:
                    user.student.resume = resume_url
                user.student.save()
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('Add_Student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
                
            
            
    return render(request,'Admin/Add_Student.html',context)






def Edit_Student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            reg_no = form.cleaned_data.get('reg_no')
            phone1 = form.cleaned_data.get('phone1')
            phone2 = form.cleaned_data.get('phone2')
            educational_qualification = form.cleaned_data.get('educational_qualification')
            domain = form.cleaned_data.get('domain')
            completion_date = form.cleaned_data.get('completion_date')
            course = form.cleaned_data.get('course')
            batch = form.cleaned_data.get('batch')
            work_experience = form.cleaned_data.get('work_experience') or None
            qualified = form.cleaned_data.get('qualified', False)  # Default to False if not provided
            placement_preferred = form.cleaned_data.get('placement_preferred', False)  # Default to False if not provided
             # Check conditions and update qualified and placement_preferred accordingly
            if not qualified and not placement_preferred:
                qualified = False
                placement_preferred = False
            else:
                qualified = True
                placement_preferred = True
            
            profile_pic=request.FILES.get('profile_pic') or None  
            
            resume = request.FILES.get('resume') or None
            
            
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                user.username = username
                user.email = email
                
                if profile_pic != None:
                    filename = default_storage.save(f'profile_pics/{profile_pic.name}', profile_pic)
                    profile_pic_url = default_storage.url(filename)
                    user.profile_pic = profile_pic_url
                
                
                if password != None:
                    user.set_password(password)
                    
                if resume != None:
                     resume_filename = default_storage.save(f'resumes/{resume.name}', resume)
                     resume_url = default_storage.url(resume_filename)
                else:
                    resume_url = None
                    
            
            
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                student.reg_no = reg_no
                student.phone1 = phone1
                student.phone2 = phone2
                student.educational_qualification = educational_qualification
                student.domain = domain
                student.qualified = qualified
                student.completion_date = completion_date
                student.course = course
                student.batch = batch
                student.work_experience = work_experience
                student.placement_preferred = placement_preferred
                if resume_url:
                    student.resume = resume_url
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('Edit_Student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "Admin/Edit_Student.html", context)
    
    
    
def Delete_Student(request, student_id):
    student = get_object_or_404(CustomUser, student__id=student_id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect(reverse('Students'))



#Access Students of Each Batch

def Batch_Students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    students = Student.objects.filter(batch=batch).annotate(
        reg_no_int=Cast('reg_no', output_field=IntegerField())
    ).order_by('reg_no_int')

    context = {
        'batch': batch,
        'students': students,
    }

    return render(request, 'Admin/Batch_Students.html', context)




#Profile Page of Each Student

def Student_Profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    context = {'student': student}
    return render(request, 'Admin/Student_Profile.html', context)



#Profile Page of Each Faculty

def Faculty_Profile(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    assigned_batches = faculty.batches_faculty.all()
    context = {'faculty': faculty,'assigned_batches':assigned_batches}
    return render(request, 'Admin/Faculty_Profile.html', context)



#SEARCH (FILTER)


def Search_Students(request):
    query = request.GET.get('q')

    if query:
        student_list = CustomUser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(student__reg_no__icontains=query),
            user_type=4
        ).annotate(reg_no_int=Cast('student__reg_no', IntegerField())).order_by('reg_no_int')
    else:
        student_list = CustomUser.objects.filter(user_type=4).annotate(reg_no_int=Cast('student__reg_no', IntegerField())).order_by('reg_no_int')

    context = {
        'student_list': student_list,
    }
    return render(request, 'Admin/Students.html', context)




def Search_Faculty(request):
    query = request.GET.get('q')

    if query:
        faculty_list = CustomUser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(faculty__fac_id__icontains=query),
            user_type=2
        )
    else:
        faculty_list = CustomUser.objects.filter(user_type=2)

    context = {
        'faculty_list': faculty_list,
    }
    return render(request, 'Admin/Manage_Faculty.html', context)




def Search_Batches(request):
    query = request.GET.get('q')

    if query:
        batches = Batch.objects.filter(
            Q(name__icontains=query) | Q(faculty__admin__first_name__icontains=query) | Q(course__name__icontains=query)
        )
    else:
        batches = Batch.objects.all()

    context = {
        'batches': batches,
        'query': query,
    }
    return render(request, "Admin/Batches.html", context)



def Admin_Select_Attendance(request):
    batches = Batch.objects.all()

    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_batch = request.POST.get('batch')

        # Retrieve attendance data for the selected date and batch
        attendance_data = Attendance.objects.filter(
            date=selected_date,
            student__batch=selected_batch
        )
        selected_batch = Batch.objects.filter(id=selected_batch).first()

        #  can pass this attendance_data to the template or perform further actions

        return render(request, 'Admin/View_Attendance.html', {'attendance_data': attendance_data,'selected_date':selected_date,'selected_batch':selected_batch})

    context = {'batches': batches}
    return render(request, 'Admin/Select_Attendance.html', context)
    
    
    


#Assessments Section

    
def Assessments(request):
    assessments = Assessment.objects.all()
    context = {
        'assessments': assessments,
    }
    return render(request, 'Admin/Assessments.html', context)





def Add_Assessment(request):
    form = AssessmentForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            out_of_marks = form.cleaned_data.get('out_of_marks')
            try:
                assessment = Assessment()
                assessment.name = name
                assessment.out_of_marks = out_of_marks
                assessment.save()
                return redirect(reverse('Assessments'))
            except:
                messages.error(request, "Failed to Add Assessment, Please Try Again..")
        else:
            messages.error(request, "Failed to Add Assessment, Please Try Again")
    return render(request, 'Admin/Add_Assessment.html', context)




def Edit_Assessment(request, assessment_id):
    instance = get_object_or_404(Assessment, id=assessment_id)
    form = AssessmentForm(request.POST or None, instance=instance)
    context = {'form': form, 'assessment_id': assessment_id}

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            out_of_marks = form.cleaned_data.get('out_of_marks')
            try:
                assessment = Assessment.objects.get(id=assessment_id)
                assessment.name = name
                assessment.out_of_marks = out_of_marks
                assessment.save()
                return redirect(reverse('Assessments'))
            except:
                messages.error(request, "Failed to Edit Assessment, Please Try Again..")
        else:
            messages.error(request, "Failed to Edit Assessment")
    return render(request, 'Admin/Edit_Assessment.html', context)





def Delete_Assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    try:
        assessment.delete()
        messages.success(request, "Assessment deleted successfully!")
    except Exception:
        messages.error(request, "Sorry, some marks are assigned for this assessment. Kindly change the affected marks and try again")
    return redirect(reverse('Assessments'))