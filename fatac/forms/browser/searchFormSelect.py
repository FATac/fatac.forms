import deform
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class searchFormSelect(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/search.pt')
    
    def isSelect(self):
        return self.request.get('objectSelect', None) or self.request.form.get('objectSelect', None)
        
    def isSearch(self):
        return not self.isSelect()
    
    def classSelection(self):
        try:
            return self.request.form['classSelect']
        except KeyError:
            try:
                return self.request['classSelect']
            except KeyError:
                return ''
    

    def render(self):
        class Schema(colander.Schema):
                text = colander.SchemaNode(
                    colander.String(),
                    validator=colander.Length(max=100),
                    widget=deform.widget.TextInputWidget(size=60),
                    description='Enter some text')
                color = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.SelectWidget(values=[("","---"),("green","verd"),("yellow","groc"),("orange","taronja"),("red","vermell"),("gray","gris")]),
                    name="Color",
                    missing=u''
                    )

        schema = Schema()
        
        if self.isSelect():
            schema.add(colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    name='objectSelect',
                    default='true'
                    ))
            
        try:
            classSelection = self.request.form['classSelect']
        except KeyError:
            try:
                classSelection = self.request['classSelect']
            except KeyError:
                classSelection = None
        
        if classSelection is not None:
            schema.add(colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    name='classSelect',
                    default=classSelection
                    ))
        
        form = deform.Form(schema, action='selectObject', buttons=('submit',))
        return form.render()

    class resultItem:
        name = None
        value = None
        link = None
        legalLink = None

        def __init__(self, name, value, link, legalLink):
            self.name = name
            self.value = value
            self.link = link
            self.legalLink = legalLink

    def results(self):
        result = list()
        if self.request.get('submit', None):
            vIsSearch = self.isSearch()

            sdm = self.context.session_data_manager
            session = sdm.getSessionData(create=True)
            if self.request.AUTHENTICATED_USER and (self.request.AUTHENTICATED_USER.getId() is not None):
                usrId = '&u=' + self.request.AUTHENTICATED_USER.getId()
            else:
                usrId = ''

            self.text = self.request['text']
            self.color = self.request['color']
            
            classSelection = ''
            if not vIsSearch:
                classSelection = "&c=" + self.request.form['classSelect']
                
            colorSelection = ''
            if self.color != '' and self.color is not None:
                colorSelection = "&k=" + self.color
            
            resp = request(self.retServidorRest() + '/search?s=' + str.replace(self.text, " ", "+") + classSelection + colorSelection)
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            for s in jsonTree.keys():
                result.append(self.resultItem("ID", s, None, None))
                for k in jsonTree[s].keys():
                    result.append(self.resultItem(k, jsonTree[s][k], None, None))
                    result.append(self.resultItem('', '', 'javascript:opener.setObjectId("'+s+'");' , None))

        return result
