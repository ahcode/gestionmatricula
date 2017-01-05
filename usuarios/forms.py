#from django.forms import ModelForm
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm

class RegistroAlumForm(UserCreationForm):
	class Meta:
		model = Usuario
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'carrera')
	def save(self, commit=True):
		user = super(RegistroAlumForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class RegistroProfForm(UserCreationForm):
	class Meta:
		model = Usuario
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'imparte')
	def save(self, commit=True):
		user = super(RegistroProfForm, self).save()
		user.email = self.cleaned_data["email"]
		user.imparte = self.cleaned_data["imparte"]
		user.profesorSinVerificar = True
		if commit:
			user.save()
		return user