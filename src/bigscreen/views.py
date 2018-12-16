from django.shortcuts import render
from django.views.generic.base import View
from helpers.director.engine import BaseEngine
# Create your views here.

class BigScreen(View):
    #def __init__(self, request = None, **kws):
        #super().__init__(**kws)
        #self.request = request
        
    def get(self,request):
        self.request = request
        ctx = self.get_context()
        template = self.get_template()
        return render(request,template,context=ctx) 
    
    
    def get_context(self):
        baseengine = BaseEngine()
        baseengine.request = self.request    
        
        return {
            'js_config':baseengine.getJsConfig()
        }
    
    def get_template(self):
        return 'bigscreen/chonggu.html'