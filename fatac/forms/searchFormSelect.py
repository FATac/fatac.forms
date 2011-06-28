import deform 
import colander
import json
from Products.Five.browser import BrowserView
from restkit import request
from deform import Form

class searchFormSelect(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self):

        class Schema(colander.Schema):
            text = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.TextInputWidget(size=60))
            c = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.HiddenWidget())
            if self.request.has_key('c'): c.default = self.request['c']
            elif self.request.form.has_key('c'): c.default = self.request.form['c']

        schema = Schema()
        form = deform.Form(schema, action='selectObject', buttons=('submit',))
        r1 = form.render()

        r2 = ''
        if 'submit' in self.request:
            clause = "";
            if self.request.has_key('c'): clause = "&c=" + self.request['c']
            elif self.request.form.has_key('c'): clause = "&c=" + self.request.form['c']
            
            sdm = self.context.session_data_manager
            session = sdm.getSessionData(create=True)
            if session.has_key('userType'):
                usrTyp = session['userType']
            else:
                usrTyp = '1'

            resp = request('http://localhost:8080/ArtsCombinatoriesRest/search?s='+self.request['text']+clause+'&r='+usrTyp);
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            r2 = '<table>'
            for s in jsonTree.keys():
                for k in jsonTree[s].keys():
                    r2 = r2 + '<tr><td>' + k + '</td><td>' + jsonTree[s][k] + '</td></tr>'
                r2 = r2 + '<tr><td>&nbsp;</td><td><a href=\"javascript:window.opener.setObjectId(\''+s+'\'); window.close();\">[Seleccionar]</a></tr>'
                r2 = r2 + '<tr><td>&nbsp;</td></tr>'
            r2 = r2 + '</table>'

        return r1 + r2
