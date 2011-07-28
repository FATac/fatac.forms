import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form

class searchForm(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/search.pt')
        
    def render(self):
        class Schema(colander.Schema):
                text = colander.SchemaNode(
                    colander.String(),
                    validator=colander.Length(max=100),
                    widget=deform.widget.TextInputWidget(size=60),
                    description='Enter some text')

        schema = Schema()
        form = deform.Form(schema, action='seek', buttons=('submit',))
        return form.render()
    
    class resultItem:
        name = None
        value = None
        link = None
        
        def __init__(self, name, value, link):
            self.name = name
            self.value = value
            self.link = link

    def results(self):
        result = list()
        if self.request.get('submit',None):
            
            sdm = self.context.session_data_manager
            session = sdm.getSessionData(create=True)
            if self.request.AUTHENTICATED_USER and (self.request.AUTHENTICATED_USER.getId() is not None):
                usrId = '&u=' + self.request.AUTHENTICATED_USER.getId()
            else:
                usrId = ''
                
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/search?s='+self.request['text']+usrId);
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            
            for s in jsonTree.keys():
                for k in jsonTree[s].keys():
                    result.append(self.resultItem(k, jsonTree[s][k], None))
                result.append(self.resultItem('','','./viewObject?id='+s))

        return result
