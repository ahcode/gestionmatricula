from django.shortcuts import render, redirect
from django.views.generic import ListView, View, FormView
from gestion.models import *
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, date
from gestion.forms import *
from usuarios.models import Asignatura
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login

class RequiereLogin(LoginRequiredMixin):
	login_url = '/login/'

class EsAlumno(UserPassesTestMixin):
	def handle_no_permission(self):
		if self.request.user.is_authenticated:
			return render(self.request, 'base.html', {'sinpermiso':True})
		return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

	def test_func(self):
		return (not self.request.user.is_staff and not self.request.user.is_superuser)

class EsProfesor(UserPassesTestMixin):
	def test_func(self):
		return (self.request.user.is_staff and not self.request.user.is_superuser)

class EsAdmin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_superuser

class Index(View):
	template_name = 'gestion/index.html'
	def get(self, request):
		return render(request, self.template_name)

class Instrucciones(View):
	template_name = 'gestion/instrucciones.html'
	def get(self, request):
		return render(request, self.template_name)

class ListaCursosAlumno(RequiereLogin, EsAlumno, ListView):
	model = Curso
	template_name = 'gestion/listacursosexp.html'
	context_object_name = 'lista_de_cursos'
	def get_queryset(self):
		misMatriculas = MatriculaAsignatura.objects.filter(alumno=self.request.user)
		misCursos = [p.curso for p in misMatriculas] #hay elementos duplicados ya que se anade a la lista un curso por cada asignatura
		misCursos = list(set(misCursos)) #se eliminan los elementos duplicados con list y set
		return misCursos

class ListaAsignaturasAlumno(RequiereLogin, EsAlumno, ListView):
	model = MatriculaAsignatura
	template_name = 'gestion/listaasignaturas.html'
	context_object_name = 'lista_de_matriculas'
	def get_queryset(self):
		misMatriculas = MatriculaAsignatura.objects.filter(alumno=self.request.user, curso=self.kwargs['curso'])
		return misMatriculas

class DetalleNotas(RequiereLogin, View):
	template_name = 'gestion/detalle.html'
	profesor = False
	def get(self, request, *args, **kwargs):
		asig = self.kwargs['asig']
		cur = self.kwargs['curso']
		if self.profesor:
			alum = self.kwargs['alum']
		else:
			alum = request.user.id
		matricula = MatriculaAsignatura.objects.get(alumno=alum, asignatura=asig, curso=cur)
		profesores = Usuario.objects.filter(profesorSinVerificar=False, imparte__in=asig)
		return render(request, self.template_name, {'matricula':matricula, 'profesores':profesores, 'profesor':self.profesor})

class ListaCursosAlumnoMatricula(RequiereLogin, EsAlumno, ListView):
	model = Curso
	template_name = 'gestion/listacursosmat.html'
	context_object_name = 'lista_de_cursos'
	def get_queryset(self):
		misCursos = Curso.objects.filter(year__gte=(datetime.now().year-1))
		return misCursos

class NuevaMatricula(RequiereLogin, EsAlumno, View):
	template_name = 'gestion/nuevamatricula.html'
	form_class = MatriculaForm
	def get(self, request, *args, **kwargs):
		misMatriculas = MatriculaAsignatura.objects.filter(alumno=self.request.user)
		misCursos = [p.curso for p in misMatriculas] #hay elementos duplicados ya que se anade a la lista un curso por cada asignatura
		misCursos = list(set(misCursos)) #se eliminan los elementos duplicados con list y set
		curso = Curso.objects.get(id=self.kwargs['curso'])
		if curso in misCursos:
			context = {'error':1} #Ya estas matriculado en este curso
		elif (date.today() < curso.inicioMatricula or date.today() > curso.finMatricula):
			context = {'error':2} #El plazo de matricula esta cerrado
		else:
			asignaturas1 = self.lista(user=request.user, cuatr=1)
			asignaturas2 = self.lista(user=request.user, cuatr=2)
			form = self.form_class(obj1=asignaturas1, obj2=asignaturas2) #Se pasan al formulario las listas de asignaturas que debe mostrar
			context = {'form':form, 'curso':curso}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		asignaturas1 = self.lista(user=request.user, cuatr=1)
		asignaturas2 = self.lista(user=request.user, cuatr=2)
		form = self.form_class(request.POST, obj1=asignaturas1, obj2=asignaturas2)
		curso = Curso.objects.get(id=self.kwargs['curso'])
		if form.is_valid():
			form.save(u=request.user, c=curso)
			return redirect('/')
		else:
			context = {'form':form, 'curso':curso}
			return render(request, self.template_name, context)

	def lista(self, user, cuatr):
		asignaturas = Asignatura.objects.filter(cuatrimestre=cuatr, carrera=user.carrera)
		cursadas = MatriculaAsignatura.objects.filter(alumno=user)
		for asig in asignaturas:
			for curs in cursadas:
				if (asig == curs.asignatura and (curs.nota1 >= 5 or curs.nota2 >= 5)):
					asignaturas = asignaturas.exclude(id=asig.id) #Se excluyen de la lista las asignaturas aprobadas
		return asignaturas

class VerificarProfesor(RequiereLogin, EsAdmin, ListView):
	template_name = 'gestion/verificarprofesor.html'
	model = Usuario
	context_object_name = 'lista_de_profesores'
	def get_queryset(self):
		profesores = Usuario.objects.filter(profesorSinVerificar=True)
		return profesores

class VerificarProfesorA(RequiereLogin, EsAdmin, View):
	verificar = True;
	def get(self, request, *args, **kwargs):
		profid = self.kwargs['prof']
		prof = Usuario.objects.get(id=profid)
		if self.verificar:
			prof.profesorSinVerificar = False
			prof.is_staff = True
			prof.save()
		else:
			prof.delete()
		return redirect('/verificarprofesor/')

class ListaGestionCursos (RequiereLogin, EsAdmin, ListView):
	template_name = 'gestion/gestioncursos.html'
	model = Curso
	context_object_name = 'lista_de_cursos'
	def get_queryset(self):
		cursos = Curso.objects.all()
		return cursos

class ListaGestionAsignaturas (RequiereLogin, EsAdmin, ListView):
	template_name = 'gestion/gestionasignaturas.html'
	model = Asignatura
	context_object_name = 'lista_de_asignaturas'
	def get_queryset(self):
		asignaturas = Asignatura.objects.all()
		return asignaturas

class ListaGestionCarreras (RequiereLogin, EsAdmin, ListView):
	template_name = 'gestion/gestioncarreras.html'
	model = Carrera
	context_object_name = 'lista_de_carreras'
	def get_queryset(self):
		carreras = Carrera.objects.all()
		return carreras

class NuevoCurso (RequiereLogin, EsAdmin, FormView):
	template_name = 'gestion/nuevo.html'
	form_class = CursoForm
	success_url = '/gestioncursos/'
	def form_valid(self, form):
		form.save()
		return super(NuevoCurso, self).form_valid(form)

class NuevaAsignatura (RequiereLogin, EsAdmin, FormView):
	template_name = 'gestion/nuevo.html'
	form_class = AsignaturaForm
	success_url = '/gestionasignaturas/'
	def form_valid(self, form):
		form.save()
		return super(NuevaAsignatura, self).form_valid(form)

class NuevaCarrera (RequiereLogin, EsAdmin, FormView):
	template_name = 'gestion/nuevo.html'
	form_class = CarreraForm
	success_url = '/gestioncarreras/'
	def form_valid(self, form):
		form.save()
		return super(NuevaCarrera, self).form_valid(form)

class ListaAsigProf (RequiereLogin, EsProfesor, View):
	template_name = 'gestion/listaasignaturasprof.html'
	context_object_name = 'lista_de_asignaturas'
	calificar=False
	def get(self, request):
		carreras = request.user.imparte.all()
		return render(request, self.template_name, {self.context_object_name:carreras, 'calificar':self.calificar})

def cursoActual():
	if (date.today().month < settings.FIN_CURSO_MES):
		year=date.today().year-1
	elif (date.today().moth == settings.FIN_CURSO_MES and date.today().day < settings.FIN_CURSO_DIA):
		year=date.today().year-1
	else:
		year=date.today().year
	curso=Curso.objects.get(year=year)
	return curso;

class ListaAlum (RequiereLogin, EsProfesor, View):
	template_name = 'gestion/listaalumnosprof.html'
	context_object_name = 'lista_de_matriculas'
	actual = False
	def get(self, request, *args, **kwargs):
		if self.actual:
			curso = cursoActual()
		else:
			curso = Curso.objects.get(id=self.kwargs['curso'])
		matriculas = MatriculaAsignatura.objects.filter(curso=curso, asignatura=self.kwargs['asig'])
		context = {self.context_object_name:matriculas,}
		if self.actual: context['calificar']=True
		return render(request, self.template_name, context)

class ListaCursosProf (RequiereLogin, EsProfesor, View):
	template_name = 'gestion/listacursosprof.html'
	context_object_name = 'lista_de_cursos'
	def get(self, request, *args, **kwargs):
		cursos = Curso.objects.filter(year__lte=cursoActual().year)
		return render(request, self.template_name, {self.context_object_name:cursos,})

class Calificar(RequiereLogin, EsProfesor, View):
	template_name = 'gestion/calificar.html'
	form_class = CalificarForm
	def get(self, request, *args, **kwargs):
		matricula=MatriculaAsignatura.objects.get(curso=cursoActual(), alumno=self.kwargs['alum'], asignatura=self.kwargs['asig'])
		form = self.form_class(instance=matricula)
		context = {'form':form, 'matricula':matricula}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		matricula=MatriculaAsignatura.objects.get(curso=cursoActual(), alumno=self.kwargs['alum'], asignatura=self.kwargs['asig'])
		if form.is_valid():
			matriculaf = form.save(commit=False)
			matricula.nota1=matriculaf.nota1
			matricula.nota2=matriculaf.nota2
			matricula.matriculaHonor1=matriculaf.matriculaHonor1
			matricula.matriculaHonor2=matriculaf.matriculaHonor2
			matricula.noPresentado1=matriculaf.noPresentado1
			matricula.noPresentado2=matriculaf.noPresentado2
			matricula.save()
			return redirect('/calificar/'+self.kwargs['asig'])
		else:
			context = {'form':form, 'matricula':matricula}
			return render(request, self.template_name, context)