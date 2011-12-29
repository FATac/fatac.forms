import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class uploadData(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/uploadData.pt')

    class SelectOption:
        name = None
        value = None

        def __init__(self, value, name):
            self.name = name
            self.value = value
            
    def relatedObject(self):
        if 'r' in self.request:
            return 'true'
        return ''

    def fillLevel(self, str, level):
        while level > 0:
            str = ".        " + str
            level = level - 1
        return str

    def treeToList(self, T, L, level):
        if type(T).__name__ != 'dict':
            L.append(self.SelectOption(T, self.fillLevel(T, level)))
            return

        for node in T:
            L.append(self.SelectOption(node, self.fillLevel(node, level)))
            for branch in T[node]:
                self.treeToList(branch, L, level + 1)

    def listClasses(self):
        if 'c' in self.request.form:
            qs = '?c=' + self.request.form['c']
        else:
            qs = ''

        resp = request(self.retServidorRest() + '/classes/tree' + qs)
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)
        L = list()
        if type(jsonTree) != list: 
            self.treeToList(jsonTree, L, 0)
        else:
            for t in jsonTree:
                self.treeToList(t, L, 0)

        return L
