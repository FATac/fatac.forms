import deform
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from widgets import ObjectInputWidget


class updateExisting(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/updateExisting.pt')

    def className(self):
        self.returnHTML = self.render2()
        return self.className

    def render(self):
        return self.returnHTML

    def render2(self):
        oid = self.request.form['id']

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        if self.request.AUTHENTICATED_USER and self.request.AUTHENTICATED_USER.getId() is not None:
            usrId = '?u=' + self.request.AUTHENTICATED_USER.getId()
        else:
            usrId = ''

        resp = request('http://stress:8080/ArtsCombinatoriesRest/objects/' + oid + usrId)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            self.className = obj['type']
        except KeyError:
            self.className = None

        if self.className != None:
            tmpstore = dict()
            hasFile = False
            resp = request('http://stress:8080/ArtsCombinatoriesRest/classes/' + self.className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            class Schema(colander.Schema):
                className = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    default=jsonTree['className'],
                    )

                objectId = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
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
                        widget=deform.widget.FileUploadWidget(tmpstore),
                        name=s['name']
                        )
                    currValue = None
                    hasFile = True

                if currValue is not None:
                    inputField.default = currValue

                schema.add(inputField)

            form = deform.Form(schema, action='updateObject', buttons=('submit',))
            r1 = form.render()

            if hasFile:
                sdm = self.context.session_data_manager
                session = sdm.getSessionData(create=True)
                if self.request.AUTHENTICATED_USER:
                    usrId = '?u=' + self.request.AUTHENTICATED_USER.getId()
                else:
                    usrId = ''

                r1 += "<div width='100%' height='800px'><iframe width='100%' height='800px' src='http://stress.upc.es:8080/ArtsCombinatoriesRest/objects/" + oid + "/file" + usrId + "'></iframe></div>"

            class Schema(colander.Schema):
                objectId = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    default=oid,
                    )

            form = deform.Form(Schema(), action='deleteObject', buttons=('delete',))
            r1 = r1 + form.render()

            return r1
        else:
            return 'Oops!'
