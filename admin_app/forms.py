from django import forms

from . models import *
from UserApp.models import *
from UserApp.forms import *
from django.core.files.storage import default_storage


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields





class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm,self).__init__(*args, **kwargs)        
        
    class Meta:
        fields = ['name','fee']
        model = Course
        




class FacultyForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Faculty
        fields = CustomUserForm.Meta.fields + \
            ['fac_id','age','phone','course','joining_date','starting_salary','current_salary']
            
            
class BatchForm(FormSettings):
    class Meta:
        model = Batch
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
            
class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + [
            'reg_no', 'phone1', 'phone2', 'educational_qualification',
            'domain', 'qualified', 'papers_to_pass', 'completion_date',
            'course', 'batch', 'work_experience', 'placement_preferred', 'resume'
        ]
    resume = forms.FileField(required=False)
    # Update the widgets for the optional fields
    widgets = {
        'work_experience': forms.Textarea(attrs={'rows': 3, 'cols': 30}),
    }

    # Make the optional fields not required
    required = {
        'work_experience': False,
        'placement_preferred': False,
        'resume': False,
    }
    
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Handle file upload and storage here
            resume_filename = default_storage.save(f'resumes/{resume.name}', resume)
            # Get the URL for the saved resume file
            resume_url = default_storage.url(resume_filename)
            return resume_url
        return None  # If no resume is provided
    
    
    
    
class AssessmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AssessmentForm,self).__init__(*args, **kwargs)        
        
    class Meta:
        fields = ['name','out_of_marks']
        model = Assessment