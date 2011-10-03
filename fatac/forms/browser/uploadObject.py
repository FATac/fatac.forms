import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request


class uploadObject(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/uploadObject.pt')

    def render(self):
        if 'submit' in self.request and 'className' in self.request:
            className = self.request['className']
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/classes/' + className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            jsonRequest = {'className': className}
            for s in jsonTree['inputList']:
                fieldName = s['name']
                if fieldName in self.request:
                    fieldValue = self.request[fieldName]
                    jsonRequest[fieldName] = fieldValue
                elif fieldName == 'filePath':
                    upload = self.request.get('upload')
                    jsonRequest[fieldName] = upload.filename

            resp = request('http://localhost:8080/ArtsCombinatoriesRest/objects/upload',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonRequest))

            result = resp.tee().read()
            if result == 'error':
                return 'Error'
            else:
                try:
                    resp = request('http://localhost:8080/ArtsCombinatoriesRest/objects/' + result + '/file/upload?fn=' + upload.filename,
                                        method='POST',
                                        headers={'Content-Type': 'multipart/form-data'},
                                        body=upload.read())
                    return result + ' ' + resp.tee().read()
                except NameError:
                    return result
        else:
            return 'Oops!'
