# -*- coding: utf-8 -*-

import deform
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from widgets import LegalResultWidget
from fatac.theme.browser.funcionsCerca import funcionsCerca
from Products.CMFCore.utils import getToolByName


class legalValidation(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def retIds(self):
        """
        """
        if 'objectIdsVal' in self.request:
            return self.request['objectIdsVal']
        return None

    def retIdsObjectes(self):
        """ retorna una llista amb els ids dels objectes sobre els que estem
        treballant
        """
        if 'objectIdsVal' in self.request:
            return self.request['objectIdsVal'].split(",")
        return None

    def retLegalDocuments(self):
        """ retorna una llista de dicionaris amb l'id i l'html de la visualitzacio
        'fitxa_home' dels objectes sobre els que estem treballant
        """
        portal = getToolByName(self, 'portal_url')
        portal = portal.getPortalObject()
        dades_resultats = []
        for id_objecte in self.retIdsObjectes():
            self.request.set('idobjecte', id_objecte)
            self.request.set('visualitzacio', 'fitxa_home')
            html = portal.restrictedTraverse('@@genericView')()
            dades_resultats.append({'id': id_objecte, 'html': html})
        return dades_resultats

    def render(self):
        userId = ''
        if 'objectIdsVal' in self.request:
            objectIdsVal = self.request['objectIdsVal']

        if 'userId' in self.request:
            userId = self.request['userId']

        if userId == '':
            resp = request(self.retServidorRest() + '/legal/start',
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

        resp = request(self.retServidorRest() + '/legal/next',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonData))

        jsonResult = resp.tee().read()
        if jsonResult == 'success':
            crida = self.retServidorRest() + '/resource/' + objectIdsVal.split(",")[0] + '/color'
            resp = request(crida)
            return "<div style='width:150px;height:150px;background-color:" + resp.tee().read() + "'> &nbsp;</div>"
        elif jsonResult == 'error':
            return "<br/>Error: unexpected termination of legal flow.<br/>"

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
                    missing=u'',
                    required=False
                    )
            elif s['type'] == 'date':
                import datetime
                from colander import Range
                inputField = colander.SchemaNode(
                    colander.Date(),
                    validator=Range(
                        min=datetime.date(2010, 5, 5)
                        ),
                    name=s['name'],
                    missing=u''
                    )
            elif s['type'] == 'boolean':
                inputField = colander.SchemaNode(
                    colander.Boolean(),
                    widget=deform.widget.CheckboxWidget(),
                    name=s['name'],
                    default=s['defaultValue'],
                    missing=False
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

                if 'autodata' in s:
                    autodataKey = s['name']
                    inputField.id = 'autodataField'
                else:
                    inputField.missing = u''

            schema.add(inputField)

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
            ajaxLink = "<span>(*) Recupera dades de processos anteriors d'acord amb la referencia</span><script> function getKeyVal() { return document.getElementById('deform')." + autodataKey + ".value; } $(\"input[name='"+autodataKey+"']\").blur(function() { $('#legalDataAjax').load('legalDataAjax?keyName=" + autodataKey + "&keyValue='+getKeyVal()+'&userId=" + userId + "') }); </script>"

        return form.render() + ajaxLink


class legalValidationAux(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def retIdsObjectes(self):
        """ retorna una llista amb els ids dels objectes sobre els que estem
        treballant
        """
        if 'objectIdsVal' in self.request:
            return self.request['objectIdsVal'].split(",")
        return None

    def retLegalDocuments(self):
        """ retorna una llista de dicionaris amb l'id i l'html de la visualitzacio
        'fitxa_home' dels objectes sobre els que estem treballant
        """
        portal = getToolByName(self, 'portal_url')
        portal = portal.getPortalObject()
        dades_resultats = []
        for id_objecte in self.retIdsObjectes():
            self.request.set('idobjecte', id_objecte)
            self.request.set('visualitzacio', 'fitxa_home')
            html = portal.restrictedTraverse('@@genericView')()
            dades_resultats.append({'id': id_objecte, 'html': html})
        return dades_resultats

    def render(self):
        userId = ''
        if 'objectIdsVal' in self.request:
            objectIdsVal = self.request['objectIdsVal']

        if 'userId' in self.request:
            userId = self.request['userId']

        if userId == '':
            resp = request(self.retServidorRest() + '/legal/start',
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

        resp = request(self.retServidorRest() + '/legal/next',
                                method='POST',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonData))

        jsonResult = resp.tee().read()
        if jsonResult == 'success':
            crida = self.retServidorRest() + '/resource/' + objectIdsVal.split(",")[0] + '/color'
            resp = request(crida)
            return "<script> window.opener.setLegalResult('" + resp.tee().read() + "'); window.close(); </script>"
        elif jsonResult == 'error':
            return "Error: unexpected termination of legal flow."

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
                    missing=u'',
                    required=False
                    )
            elif s['type'] == 'date':
                import datetime
                from colander import Range
                inputField = colander.SchemaNode(
                    colander.Date(),
                    validator=Range(
                        min=datetime.date(2010, 5, 5)
                        ),
                    name=s['name'],
                    missing=u''
                    )
            elif s['type'] == 'boolean':
                inputField = colander.SchemaNode(
                    colander.Boolean(),
                    widget=deform.widget.CheckboxWidget(),
                    name=s['name'],
                    default=s['defaultValue'],
                    missing=False
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

                if 'autodata' in s:
                    autodataKey = s['name']
                    inputField.id = 'autodataField'
                else:
                    inputField.missing = u''

            schema.add(inputField)

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
            ajaxLink = "<span>(*) Recupera dades de processos anteriors d'acord amb la referencia</span><script> function getKeyVal() { return document.getElementById('deform')." + autodataKey + ".value; } $(\"input[name='"+autodataKey+"']\").blur(function() { $('#legalDataAjax').load('legalDataAjax?keyName=" + autodataKey + "&keyValue='+getKeyVal()+'&userId=" + userId + "') }); </script>"

        return form.render() + ajaxLink
