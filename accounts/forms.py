from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from course.models import Department
from .models import User, Student, Parent, RELATION_SHIP, LEVEL, GENDERS


class StaffAddForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.CharField(widget=forms.Select(choices=GENDERS, attrs={"class": "form-control"}))
    address = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    address = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.CharField(widget=forms.Select(choices=GENDERS, attrs={"class": "form-control"}))
    level = forms.CharField(widget=forms.Select(choices=LEVEL, attrs={"class": "form-control"}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Department")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.gender = self.cleaned_data.get("gender")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            Student.objects.create(
                student=user,
                level=self.cleaned_data.get("level"),
                department=self.cleaned_data.get("department"),
            )
        return user


class DepartmentUpdateForm(UserChangeForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Department",
    )

    class Meta:
        model = Student
        fields = ["department"]


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Email Address")
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Last Name")
    gender = forms.CharField(widget=forms.Select(choices=GENDERS, attrs={"class": "form-control"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Phone No.")
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Address / city")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "email", "phone", "address", "picture"]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address."
            self.add_error("email", msg)
        return email


class ParentAddForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Email Address")
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Student")
    relation_ship = forms.CharField(widget=forms.Select(choices=RELATION_SHIP, attrs={"class": "form-control"}))
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Password")
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Password Confirmation")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.email = self.cleaned_data.get("email")
        user.save()
        Parent.objects.create(
            user=user,
            student=self.cleaned_data.get("student"),
            relation_ship=self.cleaned_data.get("relation_ship"),
        )
        return user
