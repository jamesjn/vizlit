# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
  t = loader.get_template('templates/index.html') 
  return HttpResponse(t.render())
