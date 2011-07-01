import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class legalValidation(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def render(self):
        responseId = ''
        userId = ''
        if self.request.has_key('objectIdsVal'):
            objectIdsVal = self.request['objectIdsVal']
        
        if 'userId' in self.request:
            userId = self.request['userId']
        
        if userId == '':
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/startLegal', 
                                method='POST', 
                                headers={'Content-Type': 'application/json'}, 
                                body=json.dumps(objectIdsVal.split(",")))
            
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            userId = jsonTree['userId']
        
        jsonData = dict()
        jsonData['userId'] = userId;
        if 'submit' in self.request and 'fieldList' in self.request:
            fl = self.request['fieldList'].split(",")
            for s in fl:
                if self.request.get(s,None):
                    jsonData[s] = self.request[s]
            
        resp = request('http://localhost:8080/ArtsCombinatoriesRest/legalNext', 
                                method='POST', 
                                headers={'Content-Type': 'application/json'}, 
                                body=json.dumps(jsonData))
        
        jsonResult = resp.tee().read()
        if jsonResult == 'error' or jsonResult == 'success':
            crida = 'http://localhost:8080/ArtsCombinatoriesRest/getObjectLegalColor?id='+objectIdsVal.split(",")[0]
            resp = request(crida)
            return "<div style='width:150px;height:150px;background-color: "+resp.tee().read()+"'> &nbsp;</div>";
        
        print jsonResult
        jsonTree = json.loads(jsonResult)
        
        tmpstore = dict()
        class Schema(colander.Schema):
            ""
            ""
        
        schema = Schema()
        fieldList = list()

        for s in jsonTree:
            if s is None: continue
            fieldList.append(s['name'])
            
            if s.has_key('values'):
                L = list()
                for v in s['values']: L.append((v,v))                 
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.SelectWidget(values=L),
                    name=s['name'],
                    required=False
                    )           
            elif s['type'] == 'date':
                import datetime
                from colander import Range
                inputField = colander.SchemaNode(
                    colander.Date(),
                    validator=Range(
                        min=datetime.date(2010, 5, 5)
                        ),
                    name=s['name']
                    )
            elif s['type'] == 'boolean':
                inputField = colander.SchemaNode(
                    colander.Boolean(),
                    widget=deform.widget.CheckboxWidget(),
                    name=s['name']
                    )
            else:
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.TextInputWidget(size=60),
                    name=s['name']
                    )

            schema.add(inputField)
        
        schema.add(colander.SchemaNode(
            colander.String(),
            widget = deform.widget.HiddenWidget(),
            name='fieldList',
            default=",".join(fieldList),)
        )
        
        schema.add(colander.SchemaNode(
            colander.String(),
            widget = deform.widget.HiddenWidget(),
            name='userId',
            default=userId,)
        )
        
        schema.add(colander.SchemaNode(
            colander.String(),
            widget = deform.widget.HiddenWidget(),
            name='objectIdsVal',
            default=objectIdsVal,)
        )
            
        form = deform.Form(schema, action='legalValidation', buttons=('submit',))
        return form.render()
