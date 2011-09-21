import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget
from fat.demo import FatAcMessageFactory as _

class uploadNew(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/uploadNew.pt')
    
    def className(self):
        return self.request['item']

    def render(self):
        if 'submit' in self.request and 'item' in self.request:
            className = self.request['item']
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/classes/'+className+'/form');
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            
            if jsonTree['className'] == className:
                tmpstore = dict()
            
                class Schema(colander.Schema):
                    className = colander.SchemaNode(
                       colander.String(),
                        widget = deform.widget.HiddenWidget(),
                        default=jsonTree['className'],
                        )

                schema = Schema()

                for s in jsonTree['inputList']:
                    if s['controlType'] == 'textInput':
                        inputField = colander.SchemaNode(
                            colander.String(),
                            widget=deform.widget.TextInputWidget(size=60),
                            name=s['name'],
                            title=_(s['name']),
                            )
                    elif s['controlType'] == 'dateInput':
                        import datetime
                        from colander import Range
                        inputField = colander.SchemaNode(
                            colander.Date(),
                            validator=Range(
                                min=datetime.date(2010, 5, 5)
                                ),
                            name=s['name'],
                            title=_(s['name']),
                            )
                    elif s['controlType'] == 'objectInput':
                        inputField = colander.SchemaNode(
                            colander.String(),
                            widget=ObjectInputWidget(objectClass=s['objectClass']),
                            name=s['name'],
                            title=_(s['name']),
                            )
                    elif s['controlType'] == 'checkInput':
                        inputField = colander.SchemaNode(
                            colander.Boolean(),
                            widget=deform.widget.CheckboxWidget(),
                            name=s['name'],
                            title=_(s['name']),
                            )
                    elif s['controlType'] == 'fileInput':
                        inputField = colander.SchemaNode(
                            deform.FileData(),
                            widget = deform.widget.FileUploadWidget(tmpstore),
                            name=s['name'],
                            title=_(s['name']),
                            )

                    schema.add(inputField)
                    
                form = deform.Form(schema, action='uploadObject', buttons=('submit',))
                return form.render()
            else:
                return 'Oops!'
