import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class uploadObject(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/uploadObject.pt')

    def render(self):
        if 'submit' in self.request and 'type' in self.request:
            className = self.request['type']
            about = self.request['about']
            resp = request(self.retServidorRest() + '/classes/' + className + '/form')
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            # GestionarLlibre = False

            jsonRequest = {'type': className, 'about': about}
            for s in jsonTree['inputList']:
                nameparts = s['name'].split(":")
                if len(nameparts) > 1:
                    fieldName = nameparts[1]
                else:
                    fieldName = nameparts[0]

                if fieldName in self.request:
                    fieldValue = self.request[fieldName]

                    # Com quan crees el llibre fins que no arriva al solr no es la informacio, ho comentem
                    # if fieldName == u'DisplayScreen' and fieldValue == 'on':
                    #     GestionarLlibre = True 
                    if fieldName + '_lang' in self.request:
                        tmp = []
                        fieldLang = self.request[fieldName + '_lang']
                        if type(fieldValue) == list:
                            for v, l in zip(fieldValue, fieldLang):
                                if l != '':
                                    tmp.append(v + '@' + l)
                                else:
                                    tmp.append(v)
                        else:
                            if fieldLang != '':
                                tmp = fieldValue + '@' + fieldLang
                            else:
                                tmp = fieldValue

                        if tmp == '@':
                            tmp = ''
                        fieldValue = tmp

                    if fieldName + '_prefix' in self.request:
                        fieldPrefix = self.request[fieldName + '_prefix']
                        if type(fieldPrefix) == list:
                            fieldName = fieldPrefix[0] + ":" + fieldName
                        else:
                            fieldName = fieldPrefix + ":" + fieldName

                    jsonRequest[fieldName] = fieldValue

            resp = request(self.retServidorRest() + '/resource/upload',
                                method='PUT',
                                headers={'Content-Type': 'application/json'},
                                body=json.dumps(jsonRequest))

            result = resp.tee().read()

            self.newId = result

            if result != 'error':
                #forcem la visualitzacio del objecte perque no doni error si vas a opcio Gestionar Llibre directament
                #fitxa = request(self.context.portal_url()+'/genericView?idobjecte=%s' % self.request.form['about'])
                if '__relatedObject' in self.request:
                    return "&nbsp;<a href='javascript:opener.setCurrentInputValue(\"" + result + "\"); opener.focus(); window.close();'>[Seleccionar]</a>"
                #Com quan crees el llibre fins que no arriva al solr no es veu peta, per tal ho comentem
                # elif GestionarLlibre:
                #     return "Objecte desat correctament. <br/><br/><a href='./updateExisting?id=" + result + "'>Edita</a><span class='separator'> | </span><a href='./legalValidation?objectIdsVal=" + result + "'>Legal</a><span class='separator'> | </span><a target='_blank' href='./genericView?idobjecte=" + result + "'>Fitxa</a><span class='separator'> | </span><a target='_blank' href='./ac/" + result + '/gestionarLlibre'"'>Gestionar Llibre</a>"
                else:
                    # return "<a href='./genericView?idobjecte=" + result + "' target='_fitaWindow'>Veure fitxa</a>"
                    return "Objecte desat correctament. <br/><br/><a href='./updateExisting?id=" + result + "'>Edita</a><span class='separator'> | </span><a href='./legalValidation?objectIdsVal=" + result + "'>Legal</a><span class='separator'> | </span><a target='_blank' href='./genericView?idobjecte=" + result + "'>Fitxa</a>"
        else:
            return 'Oops!'
