from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class deleteObject(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/deleteObject.pt')

    class resultItem:
        value = None
        link = None

        def __init__(self, value, link):
            self.value = value
            self.link = link

    def locator(self):
        try:
            oid = self.request['objectId']
            loc = self.request['loc']
            loclist = loc.split(",")[:-1]
            if self.request.get('pos', None):
                pos = self.request.form['pos']
                loclist = loclist[:int(pos) + 1]
            else:
                pos = None

            result = []
            idx = 0
            for l in loclist:
                result.append(self.resultItem(l, 'javascript:goToObject("' + l + '","' + str(idx) + '")'))
                idx = idx + 1

            return result
        except KeyError:
            oid = self.request.form['objectId']
            result = [self.resultItem(oid, 'javascript:goToObject("' + oid + '","0")')]
            return result

    def render(self):
        if 'objectId' in self.request:
            oid = self.request['objectId']
            resp = request(self.retServidorRest() + '/resource/' + oid + '/delete', method='DELETE')

            result = resp.tee().read()

            try:
                myformHtml = "<form name='myform'><input type='hidden' name='locator' value='" + self.request.form['loc'] + "'></form> <div id='mydiv'></div>"
            except KeyError:
                myformHtml = ""
            # TODO delete (if exists) dummy object
            return "Object esborrat <br/><br/><a href='./inici'>Inici</a>" + myformHtml
        else:
            return 'Oops!'
