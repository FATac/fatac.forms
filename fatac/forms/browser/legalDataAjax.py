import json
from Products.Five.browser import BrowserView
from restkit import request


class legalDataAjax(BrowserView):

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self):
        keyName = self.request['keyName']
        keyValue = self.request['keyValue']
        userId = self.request['userId']

        resp = request('http://localhost:8080/ArtsCombinatoriesRest/legal/restore?key=' + keyName + '&value=' + keyValue + '&userId=' + userId)
        jsonResult = resp.tee().read()

        if jsonResult == 'error':
            return ""

        jsonTree = json.loads(jsonResult)

        result = '<script>'
        for s in jsonTree:
            val = ''
            if 'defaultValue' in s:
                val = s['defaultValue']
            result = result + 'setFormValue("' + s['name'] + '","' + val + '"); '

        result = result + ' </script>'
        return result
