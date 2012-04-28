# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect
from generator.libraries import Figure
import os
import vtk
import time
import os.path

def index(request):
  return render_to_response('index.html', {'hi':'hi'})

def results(request):
  return render_to_response('results.html', {'hi':'hi'})

def generate(request):
  if request.method == 'POST':
    form = GenerateForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['figureName'] 
      os.system("cd /home/jchiang/dev/django/vizlit/generator/images;rm -f *")
      os.system("cd /home/jchiang/dev/django/vizlit/generator/vtk_scripts;./prep_xvfb")
      os.environ["DISPLAY"]=":100"
      f = Figure()
      f.generate(name)
      os.system("killall Xvfb > /dev/null")
      os.system("cd /home/jchiang/dev/django/vizlit/generator/images;tar cvf images.tar *")
      return render_to_response('results.html', {'name':name})
  else:
    form = GenerateForm()

  return render_to_response('generate.html', {
    'form': form,
  })

class GenerateForm(forms.Form):
  figureName = forms.CharField(max_length=100)
 
