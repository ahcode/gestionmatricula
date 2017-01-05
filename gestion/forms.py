from django.forms import ModelForm, Form, ModelMultipleChoiceField
from gestion.models import *
from usuarios.models import *
from django.contrib.admin import widgets

class MatriculaForm(Form):
	def __init__(self,*args,**kwargs):
		obj1 = kwargs.pop('obj1')
		obj2 = kwargs.pop('obj2')
		super(MatriculaForm,self).__init__(*args,**kwargs)
		self.fields['cuatrimestre1']=ModelMultipleChoiceField(obj1)
		self.fields['cuatrimestre2']=ModelMultipleChoiceField(obj2)

	class Meta:
		fields = ('cuatrimestre1','cuatrimestre2')

	def save(self, u, c):
		asignaturas=self.cleaned_data["cuatrimestre1"]
		for asig in asignaturas:
			mat=MatriculaAsignatura(alumno=u, curso=c, asignatura=asig)
			mat.save()
		asignaturas=self.cleaned_data["cuatrimestre2"]
		for asig in asignaturas:
			mat=MatriculaAsignatura(alumno=u, curso=c, asignatura=asig)
			mat.save()

class CursoForm(ModelForm):
	class Meta:
		model = Curso
		fields = ['year', 'inicioMatricula', 'finMatricula']

class AsignaturaForm(ModelForm):
	class Meta:
		model = Asignatura
		fields = ['nombre', 'curso', 'cuatrimestre', 'carrera']

class CarreraForm(ModelForm):
	class Meta:
		model = Carrera
		fields = ['nombre',]

class CalificarForm(ModelForm):
	class Meta:
		model = MatriculaAsignatura
		fields = ['nota1','matriculaHonor1','noPresentado1','nota2','matriculaHonor2','noPresentado2']