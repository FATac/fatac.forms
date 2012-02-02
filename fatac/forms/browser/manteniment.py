# -*- encoding: utf-8 -*-
import json
import urllib
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca

class manteniment(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/manteniment.pt')
    
    def action(self):
        result = "Selecciona una tasca a realitzar"
        if 'action' in self.request.form:
            action = self.request.form['action']
            if action == 'reset':                
                if 'parametre' in self.request.form:
                    confirmReset = self.request.form['parametre']
                    if confirmReset != '':
                        call = self.retServidorRest() + '/reset?confirm=' + urllib.quote_plus(confirmReset)
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Reset: " + result
                    else:
                        result = "Reset: Falta confirmar"
                else:
                    resp = "Reset: Falta confirmar"
            elif action == 'thumbnail':
                if 'parametre' in self.request.form:
                    classeThumbnail = self.request.form['parametre']
                    if classeThumbnail != '':
                        call = self.retServidorRest() + '/generateAllThumbnails?c=' + urllib.quote_plus(classeThumbnail)
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Reset: " + result
                    else:
                        resp = "Generar miniatures: Falta escollir la classe"
                else:
                    resp = "Generar miniatures: Falta escollir la classe"
            elif action == 'update':
                if 'parametre' in self.request.form:
                    time = self.request.form['parametre']
                    if time != '':
                        call = self.retServidorRest() + '/solr/update?time='+time
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Indexar dades recents: " + result
                    else:
                        resp = "Indexar dades recents: cal indicar el temps "
                else:
                    resp = "Indexar dades recents: cal indicar el temps "
            elif action == 'replace':
                if 'parametre' in self.request.form:
                    replaceParams = self.request.form['parametre']
                    pl = replaceParams.split(";")
                    if replaceParams != '' or len(pl)< 3:
                        call = self.retServidorRest() + '/replaceUri?uriField='+pl[0]+'&oldUri='+pl[1]+'&newUri='+pl[2]
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Substitueix: " + result
                    else:
                        result = "Substitueix: falten paràmetres per indicar "
                else:
                    result = "Substitueix: cal indicar els paràmetres "
            elif action == 'ontology':
                resp = request(self.retServidorRest() + '/reset?option=ontology')
                result = resp.tee().read()
                result = 'Ontologies: ' + result
            elif action == 'oai':
                resp = request(self.retServidorRest() + '/oai')
                result = resp.tee().read()
                result = 'OAI: ' + result
            elif action == 'index':
                resp = request(self.retServidorRest() + '/solr/reload')
                result = resp.tee().read()
                result = 'Indexar tot: ' + result
            elif action == 'roles':
                resp = request(self.retServidorRest() + '/reset?option=roles')
                result = resp.tee().read()
                result = 'Reiniciar rols: ' + result
            
        
        return result
                