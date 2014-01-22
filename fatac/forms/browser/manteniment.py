# -*- encoding: utf-8 -*-
import json
import urllib
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("fatac.forms")

class manteniment(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/manteniment.pt')
    
    def action(self):
        result = _("SeleccionaTasca",default="Selecciona una tasca a realitzar")
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
                        result = _("ResetFaltaConfirmar",default="Reset: Falta confirmar")
                else:
                    resp = _("ResetFaltaConfirmar",default="Reset: Falta confirmar")
            elif action == 'thumbnail':
                if 'parametre' in self.request.form:
                    classeThumbnail = self.request.form['parametre']
                    if classeThumbnail != '':
                        call = self.retServidorRest() + '/generateAllThumbnails?c=' + urllib.quote_plus(classeThumbnail)
                        resp = request(call)
                        result = resp.tee().read()
                        result = "Reset: " + result
                    else:
                        resp = _("GenerarMiniaturesFaltaClasse",default="Generar miniatures: Falta escollir la classe")
                else:
                    resp = _("GenerarMiniaturesFaltaClasse",default="Generar miniatures: Falta escollir la classe")
            elif action == 'update':
                if 'parametre' in self.request.form:
                    time = self.request.form['parametre']
                    if time != '':
                        call = self.retServidorRest() + '/solr/update?time='+time
                        resp = request(call)
                        result = resp.tee().read()
                        result = _("IndexarRecents",default="Indexar dades recents") + ": " + result
                    else:
                        resp = _("IndexarRecentsFaltaTemps",default="Indexar dades recents: cal indicar el temps ")
                else:
                    resp = _("IndexarRecentsFaltaTemps",default="Indexar dades recents: cal indicar el temps ")
            elif action == 'replace':
                if 'parametre' in self.request.form:
                   
                    replaceParams = self.request.form['parametre']
                    pl = replaceParams.split(";")
                    if replaceParams != '' or len(pl)< 3:
                        call = self.retServidorRest() + '/replaceUri?uriField='+pl[0]+'&oldUri='+pl[1]+'&newUri='+pl[2]
                        resp = request(call)
                        result = resp.tee().read()
                        result = _("Substitueix",default="Substitueix") + ": " + result
                    else:
                        result = _("SubstitueixFaltenParams",default="Substitueix: falten paràmetres per indicar ")
                else:
                    result = _("SubstitueixFaltenTotsParams",default="Substitueix: cal indicar els paràmetres ")
            elif action == 'ontology':
                resp = request(self.retServidorRest() + '/reset?option=ontology')
                result = resp.tee().read()
                result = _('Ontologies',default='Ontologies') + ': ' + result
            elif action == 'oai':
                resp = request(self.retServidorRest() + '/oai')
                result = resp.tee().read()
                result = 'OAI: ' + result
            elif action == 'index':
                resp = request(self.retServidorRest() + '/solr/reload')
                result = resp.tee().read()
                result = _('IndexAll',default='Indexar tot') +': ' + result
            elif action == 'roles':
                resp = request(self.retServidorRest() + '/reset?option=roles')
                result = resp.tee().read()
                result = _('RestartRoles',default='Reiniciar rols') + ': ' + result
        
        return result
                
