from typing import Any
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password



# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extra_fields):
        email  =  self.normalize_email(email)
        user   =  CustomUser(email=email,**extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        
        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email,password,**extra_fields)
    
    
        

class CustomUser(AbstractUser):
    USER_TYPE  =  ((1,'Admin'),(2,'Faculty'),(3,'Staff'),(4,'Student'))
    GENDER     =  (('M','Male'),('F','Female')) 
    
    username   =  None #Using Email INstead
    email      =  models.EmailField(unique=True)
    user_type  = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender     =  models.CharField(choices=GENDER,max_length=1)
    profile_pic    =  models.ImageField(upload_to='Profile_pics/',blank=True, null=True)
    address    =  models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects    = CustomUserManager()
    
    def __str__(self) -> str:
        return self.first_name+" "+self.last_name
    
    
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    
class Course(models.Model):
    name = models.CharField(max_length=200)
    fee = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Faculty(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fac_id = models.CharField(max_length=20, unique=True, default=' ')
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    joining_date = models.DateField(null=True, blank=True)  # Set default to None
    starting_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    

class Batch(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course,on_delete=models.DO_NOTHING, null=True, blank=False)
    faculty = models.ForeignKey(Faculty,on_delete=models.DO_NOTHING,null=True, blank=False,related_name='batches_faculty')
    timing = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name
    

class Student(models.Model):
    EDUCATION_CHOICES = [
        ('+2', '+2'),('Diploma', 'Diploma'),
        ('BA ', 'BA'),('BSc','BSc'),('BCom','BCom'),('BCA','BCA'),
        ('BBA','BBA'),('B.Tech','B.Tech'),('B.Ed','B.Ed'),('BFA','BFA'),
        
        ('MA', 'MA'),('MSc','MSc'),('Mcom','Mcom'),('MCA','MCA'),
        ('MBA','MBA'),('M.Tech','M.Tech'),('M.Ed','M.Ed'),('MFA','MFA'),
        ('Ph.D', 'Ph.D'),
    ]
    
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20, blank=False)
    phone1=models.CharField(max_length=255,null=True)
    phone2=models.CharField(max_length=255,null=True)
    educational_qualification = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    domain = models.CharField(max_length=100)
    qualified = models.BooleanField(null=True)
    papers_to_pass = models.IntegerField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    batch = models.ForeignKey(Batch, on_delete=models.DO_NOTHING, null=True)
    work_experience = models.CharField(max_length=100,blank=True)
    placement_preferred = models.BooleanField(null=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    def __str__(self):
        return   self.admin.first_name+" "+self.admin.last_name





class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    date = models.DateField()
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} - {self.date}"
    
    

class Assessment(models.Model):
    name = models.CharField(max_length=50)
    out_of_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Faculty.objects.create(admin=instance)
        if instance.user_type == 4:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.faculty.save()
    if instance.user_type == 4:
        instance.student.save()
