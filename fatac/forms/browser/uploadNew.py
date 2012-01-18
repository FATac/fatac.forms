import deform
import colander
import json
import myControls
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from widgets import ObjectInputWidget
from fatac.forms import FatAcMessageFactory as _
from fatac.theme.browser.funcionsCerca import funcionsCerca


class uploadNew(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/uploadNew.pt')

    def className(self):
        return self.request['item']

    def render(self):
        if 'item' in self.request:
            className = self.request['item']
            resp = request(self.retServidorRest() + '/classes/' + className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            
            controlList = []
            
            if jsonTree['className'] == className:
                tmpstore = dict()
                
                if '__relatedObject' in self.request.form and self.request.form['__relatedObject'] == 'true' :
                    controlList.append(myControls.HiddenInputControl('__relatedObject','true'))
                    
                controlList.append(myControls.HiddenInputControl('type', jsonTree['className']))
                controlList.append(myControls.TextControl('About', 'about', '', lang=None, multi=False))
                
                for s in jsonTree['inputList']:
                    if s['controlType'] == 'textInput':
                        controlList.append(myControls.TextControl( _(s['name']), s['name'], ''))
                    elif s['controlType'] == 'textAreaInput':
                        controlList.append(myControls.TextAreaControl(_(s['name']), s['name'], ''))
                    elif s['controlType'] == 'dateInput':
                        controlList.append(myControls.DateControl(_(s['name']), s['name'], ''))
                    elif s['controlType'] == 'objectInput':
                        controlList.append(myControls.ObjectInputControl(_(s['name']), s['name'], '', s['objectClass']))
                    elif s['controlType'] == 'checkInput':
                        controlList.append(myControls.CheckControl(_(s['name']), s['name'], False))
                    elif s['controlType'] == 'fileInput':
                        controlList.append(myControls.FileUrlInput( _(s['name']), s['name'], ''))
                    elif s['controlType'] == 'numericInput':
                        controlList.append(myControls.NumberControl( _(s['name']), s['name'], ''))
                
                form = myControls.Form('uploadObject', controlList)                
                return form.render()
            else:
                return 'Oops!'
