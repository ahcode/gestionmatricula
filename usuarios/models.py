from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

class Carrera(models.Model):
	nombre = models.CharField(max_length=50, unique = True)
	def __str__(self):
		return self.nombre

class Asignatura(models.Model):
	nombre = models.CharField(max_length=50, unique = True)
	CURSO_OPCIONES = ((1, 'Primero'),(2, 'Segundo'),(3, 'Tercero'),(4, 'Cuarto'))
	curso = models.IntegerField(choices=CURSO_OPCIONES)
	CUATRIMESTRE_OPCIONES = ((1, 'Primer Cuatrimestre'),(2, 'Segundo Cuatrimestre'))
	cuatrimestre = models.IntegerField(choices=CUATRIMESTRE_OPCIONES)
	carrera = models.ForeignKey(Carrera)
	def __str__(self):
		return self.nombre

class Usuario(AbstractUser):
	carrera = models.ForeignKey(Carrera, null = True) #Los alumnos deben seleccionar una sola carrera, los profesores ninguna
	imparte = models.ManyToManyField(Asignatura) #Los profesores deben seleccionar una o varias asignaturas, los alumnos ninguna
	profesorSinVerificar = models.BooleanField(default = False) #Un administrador debe verificar a un profesor poniendo este campo a true