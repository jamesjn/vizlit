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
      imDim1 = form.cleaned_data['imDim1']
      imDim2 = form.cleaned_data['imDim2']
      imDim3 = form.cleaned_data['imDim3']
      rotation_azimuth = form.cleaned_data['rotation_azimuth']
      rotation_elevation = form.cleaned_data['rotation_elevation']
      os.system("cd /home/jchiang/dev/django/vizlit/generator/images;rm -f *")
      os.system("cd /home/jchiang/dev/django/vizlit/generator/vtk_scripts;./prep_xvfb")
      os.environ["DISPLAY"]=":100"
      f = Figure()
      f.generate(name,imDim1,imDim2,imDim3, rotation_azimuth, rotation_elevation)
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
  imDim1 = forms.IntegerField()
  imDim2 = forms.IntegerField()
  imDim3 = forms.IntegerField()
  rotation_azimuth = forms.IntegerField()
  rotation_elevation = forms.IntegerField()
 
