import deform
import colander
import json
from Products.Five.browser import BrowserView
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class searchFormSelect(BrowserView, funcionsCerca):
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
            if 'c' in self.request:
                c.default = self.request['c']
            elif 'c' in self.request.form:
                c.default = self.request.form['c']

        schema = Schema()
        form = deform.Form(schema, action='selectObject', buttons=('submit',))
        r1 = form.render()

        r2 = ''
        if 'submit' in self.request:
            clause = ""
            if 'c' in self.request:
                clause = "&c=" + self.request['c']
            elif 'c' in self.request.form:
                clause = "&c=" + self.request.form['c']

            sdm = self.context.session_data_manager
            session = sdm.getSessionData(create=True)
            if self.request.AUTHENTICATED_USER and self.request.AUTHENTICATED_USER is not None and self.request.AUTHENTICATED_USER.getId() is not None:
                usrId = '&u=' + self.request.AUTHENTICATED_USER.getId()
            else:
                usrId = ''

            resp = request(self.retServidorRest() + '/search?s=' + self.request['text'] + clause + usrId)
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            r2 = '<table>'
            for s in jsonTree.keys():
                for k in jsonTree[s].keys():
                    if type(jsonTree[s][k]) != list:
                        r2 = r2 + '<tr><td>' + k + '</td><td>' + jsonTree[s][k] + '</td></tr>'
                    else:
                        r2 = r2 + '<tr><td>' + k + '</td><td>' + jsonTree[s][k][0] + '</td></tr>'
                r2 = r2 + '<tr><td>&nbsp;</td><td><a href=\"javascript:window.opener.setObjectId(\'' + s + '\'); window.close();\">[Seleccionar]</a></tr>'
                r2 = r2 + '<tr><td>&nbsp;</td></tr>'
            r2 = r2 + '</table>'

        return r1 + r2
