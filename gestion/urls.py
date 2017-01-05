from django.conf.urls import url
from gestion.views import *

urlpatterns = [
	url(r'^$', Index.as_view(), name='index'),
	url(r'^expediente/$', ListaCursosAlumno.as_view(), name='expediente'),
	url(r'^expediente/(?P<curso>\d+)/$', ListaAsignaturasAlumno.as_view(), name='curso'),
	url(r'^expediente/(?P<curso>\d+)/(?P<asig>\d+)/$', DetalleNotas.as_view(), name='asignatura'),
	url(r'^nuevamatricula/$', ListaCursosAlumnoMatricula.as_view(), name='cursosmatricula'),
	url(r'^nuevamatricula/(?P<curso>\d+)/$', NuevaMatricula.as_view(), name='matricula'),
	url(r'^verificarprofesor/$', VerificarProfesor.as_view(), name='verificarprofesor'),
	url(r'^verificarprofesor/v/(?P<prof>\d+)/$', VerificarProfesorA.as_view(verificar=True), name='verificarp'),
	url(r'^verificarprofesor/e/(?P<prof>\d+)/$', VerificarProfesorA.as_view(verificar=False), name='eliminarp'),
	url(r'^gestioncursos/$', ListaGestionCursos.as_view(), name='gestioncursos'),
	url(r'^gestionasignaturas/$', ListaGestionAsignaturas.as_view(), name='gestionasignaturas'),
	url(r'^gestioncarreras/$', ListaGestionCarreras.as_view(), name='gestioncarreras'),
	url(r'^gestioncursos/nuevo/$', NuevoCurso.as_view(), name='nuevocurso'),
	url(r'^gestionasignaturas/nuevo/$', NuevaAsignatura.as_view(), name='nuevaasignatura'),
	url(r'^gestioncarreras/nuevo/$', NuevaCarrera.as_view(), name='nuevacarrera'),
	url(r'^calificar/$', ListaAsigProf.as_view(calificar=True), name='asignaturascalificar'),
	url(r'^calificar/(?P<asig>\d+)/$', ListaAlum.as_view(actual=True), name='alumnoscalificar'),
	url(r'^calificar/(?P<asig>\d+)/(?P<alum>\d+)/$', Calificar.as_view(), name='calificar'),
	url(r'^consultar/$', ListaAsigProf.as_view(), name='asignaturasconsultar'),
	url(r'^consultar/(?P<asig>\d+)/$', ListaCursosProf.as_view(), name='cursosconsultar'),
	url(r'^consultar/(?P<asig>\d+)/(?P<curso>\d+)/$', ListaAlum.as_view(), name='alumnosconsultar'),
	url(r'^consultar/(?P<asig>\d+)/(?P<curso>\d+)/(?P<alum>\d+)/$', DetalleNotas.as_view(profesor=True), name='consultar'),
	url(r'^instrucciones/$', Instrucciones.as_view(), name='instrucciones'),
]