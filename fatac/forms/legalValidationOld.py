import deform 
import colander
import json
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restkit import request
from deform import Form
import ObjectInputWidget
from ObjectInputWidget import ObjectInputWidget

class legalValidation(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        
    __call__ = ViewPageTemplateFile('templates/legalValidation.pt')

    def render(self):
        responseId = ''
        userId = ''
        objectIds = self.request['objectIdsVal']
        if 'submit' in self.request:
            responseId = self.request['deformField1']
            userId = self.request['userIdVal']
        
        if userId == '':
            resp = request('http://localhost:8080/ArtsCombinatoriesRest/startLegal');
            jsonResult = resp.tee().read()
            jsonTree = json.loads(jsonResult)
            userId = jsonTree['userId']

        if responseId != '':
            jsonRequest = {"responseId":responseId, "userId":userId}
        else:
            jsonRequest = {"userId":userId}

        resp = request('http://localhost:8080/ArtsCombinatoriesRest/legalNext', 
                        method='POST', 
                        headers={'Content-Type': 'application/json'}, 
                        body=json.dumps(jsonRequest))

        jsonResult = resp.tee().read()
        jsonTree = json.loads(jsonResult)

        if not jsonTree.has_key('color'):
            questionId = jsonTree['questionId']
            answerList = jsonTree['answerList']

            choices = ()
            for s in answerList:
                choices += ((s,s), )

            class Schema(colander.Schema):
                deformField1 = colander.SchemaNode(
                    colander.String(),
                    widget=deform.widget.RadioChoiceWidget(values=choices)
                    )
                userIdVal = colander.SchemaNode(
                    colander.String(),
                    widget = deform.widget.HiddenWidget(),
                    default = userId
                    )
                objectIdsVal = colander.SchemaNode(
                    colander.String(),
                    widget = deform.widget.HiddenWidget(),
                    default = objectIds
                    )
                        
            form = deform.Form(Schema(), action='legalValidation', buttons=('submit',))
            return questionId + form.render()
        else:
            objectIdList = objectIds.split(',')
            while objectIdList.count(''): 
                objectIdList.remove('')

            jsonRequest = {'objectIdList':objectIdList, 'color':jsonTree['color']}

            resp = request('http://localhost:8080/ArtsCombinatoriesRest/setRightLevel', 
                        method='POST', 
                        headers={'Content-Type': 'application/json'}, 
                        body=json.dumps(jsonRequest))

            return resp.tee().read()
            
