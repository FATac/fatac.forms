# -*- encoding: utf-8 -*-

import deform
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from fatac.theme.browser.funcionsCerca import funcionsCerca


class searchForm(BrowserView, funcionsCerca):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    __call__ = ViewPageTemplateFile('templates/search.pt')

    def isSelect(self):
        return self.request.get('objectSelect', None) or self.request.form.get('objectSelect', None)

    def isSearch(self):
        return not self.isSelect()

    def classSelection(self):

        try:
            classSelect = self.request.form['classSelect']
        except KeyError:
            try:
                classSelect = self.request['classSelect']
            except KeyError:
                classSelect = None

        # el primer cop, self.request.form['classSelect'] = 'ac:Media'
        # després: self.request['classSelect'] = ['ac:Media', 'ac:Media']
        if classSelect is not None and type(classSelect).__name__ != 'str':
            classSelect = classSelect[0]

        return classSelect

    def getPagMinus1(self):
        if self.getPag() == 0:
            return None
        return "document.forms['deform'].page.value=" + str(self.getPag() - 1) + ";$(document.forms['deform'].submit).click();"

    def getPagPlus1(self):
        return "document.forms['deform'].page.value=" + str(self.getPag() + 1) + ";$(document.forms['deform'].submit).click();"

    def getPag(self):
        pageValue = self.request.get('page', 0)
        if pageValue == 0:
            pageValue = self.request.form.get('page', 0)
        return int(pageValue)

    def render(self):
        pageValue = self.request.get('page', 0)
        if pageValue == 0:
            pageValue = self.request.form.get('page', 0)

        textValue = self.request.get('text', '')

        choices = self.arbreClasses()

        class Schema(colander.Schema):
            text = colander.SchemaNode(
                    colander.String(),
                    validator=colander.Length(max=100),
                    widget=deform.widget.TextInputWidget(size=60),
                    description='Enter some texit',
                    default=textValue)

            classSelect = colander.SchemaNode(
                           colander.String(),
                           widget=deform.widget.SelectWidget(values=choices),
                           default=self.classSelection())

            page = colander.SchemaNode(
                    colander.Int(),
                    widget=deform.widget.HiddenWidget(),
                    default=pageValue)

        schema = Schema()

        if self.isSelect():
            schema.add(colander.SchemaNode(
                colander.String(),
                widget=deform.widget.HiddenWidget(),
                name='objectSelect',
                default='true'
                ))

        classSelection = self.classSelection()
        if classSelection is not None:
            schema.add(colander.SchemaNode(
                colander.String(),
                widget=deform.widget.HiddenWidget(),
                name='classSelect',
                default=classSelection
                ))

        form = deform.Form(schema, action='seek', buttons=[deform.Button('submit', 'Buscar')])
        return form.render()

    class resultItem:
        name = None
        value = None
        link = None
        legalLink = None
        fitxaLink = None
        gestioLink = None

        def __init__(self, name, value, link, legalLink, fitxaLink, gestioLink):
            self.name = name
            self.value = value
            self.link = link
            self.legalLink = legalLink
            self.fitxaLink = fitxaLink
            self.gestioLink = gestioLink

    def results(self):
        result = list()
        if self.request.get('submit', None):            
            vIsSearch = self.isSearch()     

            sdm = self.context.session_data_manager
            session = sdm.getSessionData(create=True)
            if self.request.AUTHENTICATED_USER and (self.request.AUTHENTICATED_USER.getId() is not None):
                usrId = '&u=' + self.request.AUTHENTICATED_USER.getId()
            else:
                usrId = ''

            self.text = self.request['text']
            self.page = self.getPag()
            classe_aux = self.classSelection()
            classe = ''
            if classe_aux != 'Totes':
                classe = "&c=" + classe_aux

            # GestionarLlibreSolar = False
            # if classe_aux == 'Totes':
            #     querystring_str = self.text
            #     lang = self.getLang()
            #     url = self.retServidorRest() + '/solr/search?rows=9999&f=(id:' + querystring_str + ")&fields=id,Who,What,When,DisplayScreen,class&conf=Explorar&lang=" + lang

            #     read = self.llegeixJson(url)
            #     if read:
            #         resultsolar = {'ordre_filtres': read['llista_claus'], 'dades_json': read['json']}
            #         if 'DisplayScreen' in resultsolar['dades_json']['response']['docs'][0]:  
            #             if resultsolar['dades_json']['response']['docs'][0]['DisplayScreen'] == (u'on'):
            #                 if resultsolar['dades_json']['response']['docs'][0]['id'] == querystring_str:
            #                     GestionarLlibreSolar = True
            #             else:
            #                 GestionarLlibreSolar = False
            #         else:
            #             GestionarLlibreSolar = False
           
            self.context.plone_log('serahcForm.py: ' + self.retServidorRest() + '/search?s=' + str.replace(self.text, " ", "+") + classe + "&page=" + str(self.page))
            resp = request(self.retServidorRest() + '/search?s=' + str.replace(self.text, " ", "+") + classe + "&page=" + str(self.page))
                           
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)

            for s in jsonTree.keys():    
                GestionarLlibre = False                
                result.append(self.resultItem("ID", s, None, None, None, None))
                if u'ac:DisplayScreen' in jsonTree[s].keys():
                    GestionarLlibre = True
                for k in jsonTree[s].keys():
                    result.append(self.resultItem(k, jsonTree[s][k], None, None, None, None))
                    
                if vIsSearch and GestionarLlibre:
                    #forcem la visualitzacio del objecte perque no doni error si vas a opcio Gestionar Llibre directament
                    fitxa = request(self.context.portal_url()+'/genericView?idobjecte=%s' % s)
                    result.append(self.resultItem('', '', './updateExisting?id=' + s, './legalValidation?objectIdsVal=' + s, './genericView?idobjecte=' + s, './ac/' + s + '/gestionarLlibre'))
                elif vIsSearch:
                    result.append(self.resultItem('', '', './updateExisting?id=' + s, './legalValidation?objectIdsVal=' + s, './genericView?idobjecte=' + s, ''))
                else:
                    result.append(self.resultItem('', '', 'javascript:opener.setCurrentInputValue("' + s + '"); window.close();', None, None, None))
        return result

    def llistaClassesPrincipals(self, jsonTree):
        """  parseja l'arbre de classes jsonTree i retorna una llista amb les
        classes principals (presuposant que l'element 'pare' és 'owl:Thing'
        """

        llista_classes = []

        if 'owl:Thing' in jsonTree:
            classes = jsonTree['owl:Thing']
            for classe in classes:
                if type(classe).__name__ == 'dict':
                    for e in classe.keys():
                        llista_classes.append(e)

                        #afegim també les classes de segon nivell
                        for subclasse in classe[e]:
                            if type(subclasse).__name__ == 'dict':
                                for ee in subclasse.keys():
                                    llista_classes.append('###' + ee)
                            else:
                                llista_classes.append('_____' + subclasse)
                else:
                    llista_classes.append(classe)
        return llista_classes

    def arbreClasses(self):
        """ crida el servei self.retServidorRest() + '/classes/tree' i retorna
        el resultat en forma de tupla per passarl-li al widget de deform, afegint
        una primera opció 'Totes'
        """

        resp = request(self.retServidorRest() + '/classes/tree')
        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)

        llista = ['Totes'] + self.llistaClassesPrincipals(jsonTree)
        return tuple([(a.replace('_____', ''), a) for a in llista])
