import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class updateExisting(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/updateExisting.pt')

    def render(self):
        oid = self.request.form['id']
        resp = request('http://localhost:8080/ArtsCombinatoriesRest/getObject?id='+oid)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            className = obj['type']
        except KeyError:
            className = None

        if className != None:
            tmpstore = dict()
            hasFile = False
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/getInsertObjectForm?className='+className)
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            
            class Schema(colander.Schema):
                className = colander.SchemaNode(
                    colander.String(),
                    widget = deform.widget.HiddenWidget(),
                    default=jsonTree['className'],
                    )

                objectId = colander.SchemaNode(
                    colander.String(),
                    widget = deform.widget.HiddenWidget(),
                    default=oid,
                    )

            schema = Schema()

            for s in jsonTree['inputList']:

                try:
                    currValue = obj[s['name']]
                except KeyError:
                    currValue = None

                if s['controlType'] == 'textInput':
                    inputField = colander.SchemaNode(
                        colander.String(),
                        widget=deform.widget.TextInputWidget(size=60),
                        name=s['name'],
                        )
                elif s['controlType'] == 'dateInput':
                    import datetime
                    from colander import Range
                    inputField = colander.SchemaNode(
                        colander.String(),
                        widget=deform.widget.TextInputWidget(size=20),
                        name=s['name'],
                        )
                elif s['controlType'] == 'objectInput':
                    inputField = colander.SchemaNode(
                        colander.String(),
                        widget=ObjectInputWidget(objectClass=s['objectClass']),
                        name=s['name'],
                        )
                elif s['controlType'] == 'checkInput':
                    inputField = colander.SchemaNode(
                        colander.Boolean(),
                        widget=deform.widget.CheckboxWidget(),
                        name=s['name'],
                        )
                elif s['controlType'] == 'fileInput':
                    inputField = colander.SchemaNode(
                        deform.FileData(),
                        widget = deform.widget.FileUploadWidget(tmpstore),
                        name=s['name']
                        )
                    currValue = None;
                    hasFile = True;

                if currValue is not None:
                    inputField.default = currValue

                schema.add(inputField)
                   
            form = deform.Form(schema, action='updateObject', buttons=('submit',))
            r1 = form.render()

            if hasFile:
                r1 += "<div width='100%' height='800px'><iframe width='100%' height='800px' src='http://stress.upc.es:8080/ArtsCombinatoriesRest/getObjectFile?id="+oid+"'></iframe></div>"
                
            class Schema(colander.Schema):
                objectId = colander.SchemaNode(
                    colander.String(),
                    widget = deform.widget.HiddenWidget(),
                    default=oid,
                    )

            form = deform.Form(Schema(), action='deleteObject', buttons=('delete',))
            r1 = r1 + form.render()

            return r1
        else:
            return 'Oops!'
