import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request


class viewObject(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/viewObject.pt')

    class resultItem:
        name = None
        value = None
        link = None

        def __init__(self, name, value, link):
            self.name = name
            self.value = value
            self.link = link

    def isAdmin(self):
        return True

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)

        usrTyp = None
        if 'userType' in session:
            usrTyp = session['userType']

        if usrTyp == '4':
            return True
        else:
            return False

    def editLink(self):
        return "window.location='./updateExisting?id=" + self.getOid() + "'"

    def mediaLink(self):
        return self.mLink

    def getOid(self):
        return self.request.form['id']

    def results(self):
        oid = self.getOid()

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        if self.request.AUTHENTICATED_USER and self.request.AUTHENTICATED_USER.getId() is not None:
            usrId = '?u=' + self.request.AUTHENTICATED_USER.getId()
        else:
            usrId = ''

        resp = request('http://localhost:8080/ArtsCombinatoriesRest/objects/' + oid + usrId)
        jsonResult = resp.tee().read()
        obj = json.loads(jsonResult)

        try:
            className = obj['type']
        except KeyError:
            className = None

        resp = request('http://localhost:8080/ArtsCombinatoriesRest/classes/' + className + '/form')
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)

        result = list()
        self.mLink = None

        for s in jsonTree['inputList']:
            if s['controlType'] == 'fileInput':
                self.mLink = 'http://stress.upc.es:8080/ArtsCombinatoriesRest/objects/' + oid + '/file' + usrId

            try:
                currValue = obj[s['name']]
                if s['controlType'] == 'objectInput':
                    try:
                        result.append(self.resultItem(s['name'], currValue, './viewObject?id=' + currValue))
                    except TypeError:
                        for v in currValue:
                            result.append(self.resultItem(s['name'], v, './viewObject?id=' + v))
                else:
                    result.append(self.resultItem(s['name'], currValue, None))
            except KeyError:
                currValue = None

        return result
