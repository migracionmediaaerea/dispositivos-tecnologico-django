import re

from catalogos_modular.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from unidecode import unidecode

from apps.users.validations import is_anam_mail


class EditProfileForm(forms.ModelForm):
    image = forms.FileField(label='',widget=forms.ClearableFileInput(), required=False, validators=[FileExtensionValidator(['jpg','jpeg','png','svg'])],
		error_messages={'invalid_image': 'Sube una imagen con extensión válida: jpg, jpeg, png, svg. El archivo que cargó no era una imagen o estaba corrupta', 'invalid_extension':'La extensión de archivo “%(extension)s” no está permitida. Las extensiones permitidas son: %(allowed_extensions)s.'})
    # password = forms.CharField(label='Contraseña', required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password','id':'password', 'placeholder': 'Contraseña'}))
    # password2 = forms.CharField(required=False, label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'id': 'verifyPassword'}))
    class Meta:
        model = User

		# Define the fields that will be displayed on the form with their DB column names
        fields = [
			"email", 
			# "password",
			# "password2",
			"image", 
			
		]

		#exclude = ('first_name', 'last_name', 'city', 'state', 'username', 'country', 'address')

		# Modify any labels here if required
        labels = {
			# mark_safe to prevent XSS attacks
			'image': mark_safe(''), # Clean the image label
			'email': mark_safe('<b>Correo electrónico*</b>'),
   			# 'password': mark_safe('<b>Contraseña</b>'),
			# 'password2': mark_safe('<b>Confirmar contraseña</b>'),
			
		}
		
		# Modify the input attributes
        widgets = {
			'email': forms.TextInput(attrs={'class': 'form-control', 'name': 'email','id':'email', 'placeholder': 'Correo electrónico', 'required': ''}),
			
		}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not is_anam_mail(email):
            raise ValidationError('Ingresa un correo electrónico de ANAM')
        return email


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)


        image = self.cleaned_data['image']
        
        try:
            image_name = image.name.replace(" ", '_')
            # Regex that ignores ' and "
            image_name = re.sub(r'[\'"]', '', image_name)
            image_name = unidecode(image_name)
            user.image.name = image_name
        except AttributeError:
            user.image.name = 'profiles/generic/default_profile.jpeg'

        if commit:
            user.save()
        return user





class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'email', 'id':'email'}))

	username = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'username'}))

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'type': 'password',
            'minlength': 8,
			'id':'password'}), required=True, label="Password")

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'type': 'password',
            'minlength': 8,
			'id':'verifyPassword'}), required=True, label="Verify password")

	first_name = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'first name'}))

	last_name = forms.CharField(required=True, 
								widget=forms.TextInput(attrs={'placeholder': 'last name'}))



	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "first_name", "last_name")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def clean_username(self):
		username  = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise ValidationError('This username is already taken')
		return username

	def clean_email(self):
		email  = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise ValidationError('This email is already taken')
		return email
	
	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control form-control-user'


