from django.shortcuts import render, redirect
from forms import *
from django.contrib.auth import login
# Create your views here.

def registro(request, tipo):
	if request.method == 'POST':
		if (tipo == 'profesor'):
			form = RegistroProfForm(request.POST)
		else:
			form = RegistroAlumForm(request.POST)
		if form.is_valid():
			login(request, form.save())
			return redirect('/')
	else:
		if (tipo == 'profesor'):
			form = RegistroProfForm()
		else:
			form = RegistroAlumForm()
	context = {'form':form, 'tipo':tipo}
	return render(request, 'usuarios/registro.html',  context)