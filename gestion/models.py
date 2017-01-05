from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from usuarios.models import Usuario, Carrera, Asignatura
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Curso(models.Model):
	YEAR_OPCIONES = []
	for r in range(datetime.now().year-5, datetime.now().year+5):
		YEAR_OPCIONES.append((r,str(r)+'/'+str(r+1)))
	year = models.IntegerField(choices=YEAR_OPCIONES, unique=True)
	inicioMatricula = models.DateField('Inicio matriculacion')
	finMatricula = models.DateField('Fin matriculacion')
	def getCadena(self):
		return str(self.year)+'/'+str(self.year+1)
	def abierto(self):
		if (date.today() >= self.inicioMatricula and date.today() <= self.finMatricula):
			return True
		else:
			return False
	def __str__(self):
		return self.getCadena()

class MatriculaAsignatura(models.Model):
	nota1 = models.DecimalField(validators = [MinValueValidator(0), MaxValueValidator(10)], max_digits=4, decimal_places=2, blank=True, null=True)
	noPresentado1 = models.BooleanField(default = False)
	matriculaHonor1 = models.BooleanField(default = False)
	nota2 = models.DecimalField(validators = [MinValueValidator(0), MaxValueValidator(10)], max_digits=4, decimal_places=2, blank=True, null=True)
	noPresentado2 = models.BooleanField(default = False)
	matriculaHonor2 = models.BooleanField(default = False)
	alumno = models.ForeignKey(Usuario)
	asignatura = models.ForeignKey(Asignatura)
	curso = models.ForeignKey(Curso)
	def __str__(self):
		return self.alumno.__str__() + " - " + self.asignatura.__str__() + " - " + self.curso.__str__()