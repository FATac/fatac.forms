import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class changeUser(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/changeUser.pt')
    
    def userType(self):
        if 'submit' in self.request:
            usrTyp = self.request['userType']
        else:
            usrTyp = None
            
        s = ''
        
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)

        if usrTyp is not None:
            session.set("userType", usrTyp)
            s = '<br>Ok'
        elif session.has_key('userType'):
            usrTyp = session['userType']
            
        return usrTyp
            
    class SelectOption:
        name = None
        value = None
        selected = False
        
        def __init__(self, value, name):
            self.name = name
            self.value = value

    def listUserTypes(self):
        L = [self.SelectOption('1','anonymous'),self.SelectOption('2','registered'),self.SelectOption('3','editor'),self.SelectOption('4','administrator')]
        
        ut = self.userType()
        if ut == '1':
            L[0].selected = True
        elif ut == '2':
            L[1].selected = True
        elif ut == '3':
            L[2].selected = True
        elif ut == '4':
            L[3].selected = True
            
        return L
        
        

