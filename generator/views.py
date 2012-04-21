# Create your views here.
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect

def index(request):
  return render_to_response('index.html', {'hi':'hi'})

def results(request):
  return render_to_response('results.html', {'hi':'hi'})

def generate(request):
  if request.method == 'POST':
    form = GenerateForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['figureName']
      return HttpResponseRedirect('/vizlit/results/')
  else:
    form = GenerateForm()

  return render_to_response('generate.html', {
    'form': form,
  })

class GenerateForm(forms.Form):
  figureName = forms.CharField(max_length=100)
 
