import deform
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from widgets import LegalResultWidget


class legalValidation(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def render(self):
        userId = ''
        if 'objectIdsVal' in self.request:
            objectIdsVal = self.request['objectIdsVal']

        if 'userId' in self.request:
            userId = self.request['userId']

        if userId == '':
            resp = request('http://stress:8080/ArtsCombinatoriesRest/legal/start',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(objectIdsVal.split(",")))

            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            userId = jsonTree['userId']

        jsonData = dict()
        jsonData['userId'] = userId
        if 'submit' in self.request and 'fieldList' in self.request:
            fl = self.request['fieldList'].split(",")
            for s in fl:
                if self.request.get(s, None):
                    jsonData[s] = self.request[s]

        resp = request('http://stress:8080/ArtsCombinatoriesRest/legal/next',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonData))

        jsonResult = resp.tee().read()
        if jsonResult == 'error' or jsonResult == 'success':
            crida = 'http://stress:8080/ArtsCombinatoriesRest/objects/' + objectIdsVal.split(",")[0] + '/color'
            resp = request(crida)
            return "<div style='width:150px;height:150px;background-color:" + resp.tee().read() + "'> &nbsp;</div>"

        jsonTree = json.loads(jsonResult)

        class Schema(colander.Schema):
            ""
            ""

        schema = Schema()
        fieldList = list()

        autodataKey = None

        for s in jsonTree:
            if s is None:
                continue
            fieldList.append(s['name'])
            if not 'defaultValue' in s:
                s['defaultValue'] = ''

            if 'values' in s and s['type'] == 'string':
                L = list()
                for v in s['values']:
                    L.append((v, v))
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.SelectWidget(values=L),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'date':
                import datetime
                from colander import Range
                inputField = colander.SchemaNode(
                    colander.Date(),
                    validator=Range(
                        min=datetime.date(2010, 5, 5)
                        ),
                    name=s['name']
                    )
            elif s['type'] == 'boolean':
                inputField = colander.SchemaNode(
                    colander.Boolean(),
                    widget=deform.widget.CheckboxWidget(),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'hidden':
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'legal_result':
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=LegalResultWidget(),
                    name=s['name']
                    )
            else:
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.TextInputWidget(size=60),
                    name=s['name'],
                    default=s['defaultValue']
                    )

            schema.add(inputField)

            if 'autodata' in s:
                autodataKey = s['name']

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='fieldList',
            default=",".join(fieldList),)
        )

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='userId',
            default=userId,)
        )

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='objectIdsVal',
            default=objectIdsVal,)
        )

        form = deform.Form(schema, action='legalValidation', buttons=('submit',))

        ajaxLink = ''
        if autodataKey is not None:
            ajaxLink = "<a id='autodataLink'>Autodata</a><script> function getKeyVal() { return document.getElementById('deform')." + autodataKey + ".value; } $('#autodataLink').click(function() { $('#legalDataAjax').load('legalDataAjax?keyName=" + autodataKey + "&keyValue='+getKeyVal()+'&userId=" + userId + "') }); </script>"

        return form.render() + ajaxLink


class legalValidationAux(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def render(self):
        userId = ''
        if 'objectIdsVal' in self.request:
            objectIdsVal = self.request['objectIdsVal']

        if 'userId' in self.request:
            userId = self.request['userId']

        if userId == '':
            resp = request('http://stress:8080/ArtsCombinatoriesRest/legal/start',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(objectIdsVal.split(",")))

            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            userId = jsonTree['userId']

        jsonData = dict()
        jsonData['userId'] = userId
        if 'submit' in self.request and 'fieldList' in self.request:
            fl = self.request['fieldList'].split(",")
            for s in fl:
                if self.request.get(s, None):
                    jsonData[s] = self.request[s]

        resp = request('http://stress:8080/ArtsCombinatoriesRest/legal/next',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonData))

        jsonResult = resp.tee().read()
        if jsonResult == 'error' or jsonResult == 'success':
            crida = 'http://stress:8080/ArtsCombinatoriesRest/objects/' + objectIdsVal.split(",")[0] + '/color'
            resp = request(crida)
            return "<script> window.opener.setLegalResult('" + resp.tee().read() + "'); window.close(); </script>"

        jsonTree = json.loads(jsonResult)

        class Schema(colander.Schema):
            ""
            ""

        schema = Schema()
        fieldList = list()

        autodataKey = None

        for s in jsonTree:
            if s is None:
                continue
            fieldList.append(s['name'])
            if not 'defaultValue' in s:
                s['defaultValue'] = ''

            if 'values' in s and s['type'] == 'string':
                L = list()
                for v in s['values']:
                    L.append((v, v))
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.SelectWidget(values=L),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'date':
                import datetime
                from colander import Range
                inputField = colander.SchemaNode(
                    colander.Date(),
                    validator=Range(
                        min=datetime.date(2010, 5, 5)
                        ),
                    name=s['name']
                    )
            elif s['type'] == 'boolean':
                inputField = colander.SchemaNode(
                    colander.Boolean(),
                    widget=deform.widget.CheckboxWidget(),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'hidden':
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.HiddenWidget(),
                    name=s['name'],
                    default=s['defaultValue']
                    )
            elif s['type'] == 'legal_result':
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=LegalResultWidget(),
                    name=s['name']
                    )
            else:
                inputField = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.TextInputWidget(size=60),
                    name=s['name'],
                    default=s['defaultValue']
                    )

            schema.add(inputField)

            if 'autodata' in s:
                autodataKey = s['name']

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='fieldList',
            default=",".join(fieldList),)
        )

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='userId',
            default=userId,)
        )

        schema.add(colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            name='objectIdsVal',
            default=objectIdsVal,)
        )

        form = deform.Form(schema, action='legalValidationAux', buttons=('submit',))

        ajaxLink = ''
        if autodataKey is not None:
            ajaxLink = "<a id='autodataLink'>Autodata</a><script> function getKeyVal() { return document.getElementById('deform')." + autodataKey + ".value; } $('#autodataLink').click(function() { $('#legalDataAjax').load('legalDataAjax?keyName=" + autodataKey + "&keyValue='+getKeyVal()+'&userId=" + userId + "') }); </script>"

        return form.render() + ajaxLink
