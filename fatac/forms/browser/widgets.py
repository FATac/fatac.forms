from deform.widget import Widget
from colander import null

class GenericInputWidget(Widget):
    
    def __init__(self, objectClass=None, **kw):
        Widget.__init__(self, **kw)
        self.objectClass = objectClass

    def serialize(self, field, cstruct, readonly=False):
        ""
        ""
        
class ObjectInputWidget(GenericInputWidget):
    objectClass = ""

    def __init__(self, objectClass=None, **kw):
        Widget.__init__(self, **kw)
        self.objectClass = objectClass

    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = u''

        js = "<script> var seek = function f(c) { var seekWin = window.open('./selectObject?c='+c); } </script>"
        js += "<script> var setObjectId = function f(id) { document.getElementById(currField).value = id; } </script>"

        try:
            val = field.default
        except AttributeError:
            val = u''

        if cstruct is not None and cstruct != u'':
            link = '&nbsp;<a href="./updateExisting?id=' + cstruct + '">[Edit]</a>'
        else:
            link = ''

        html = '<input readonly="true" type="text" value="' + cstruct + '" alt="' + self.objectClass + '" name="' + field.name + '" id="' + field.name + '"><input type="button" name="btn" value="Seek" onclick="seek(\'' + self.objectClass + '\'); currField=\'' + field.name + '\' " >' + link
        return js + html

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        return pstruct

    def handle_error(self, field, error):
        if field.error is None:
            field.error = error
        for e in error.children:
            for num, subfield in enumerate(field.children):
                if e.pos == num:
                    subfield.widget.handle_error(subfield, e)


class LegalResultWidget(Widget):

    def __init__(self, **kw):
        Widget.__init__(self, **kw)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = u''

        js = "<script> var legal = function f() { var legalWin = window.open('./legalSelectObjectsAux'); } </script>"
        js += "<script> var setLegalResult = function f(color) { var res = 'green'; if (color=='#ffff00') res = 'yellow'; else if (color=='#ffa500') res = 'orange'; else if (color=='#ff0000') res = 'red'; document.getElementById(currField).value = res; } </script>"

        html = '<input readonly="true" type="text" name="' + field.name + '" id="' + field.name + '"><input type="button" name="btn" value="Legal" onclick="legal(); currField=\'' + field.name + '\' " >'
        return js + html

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        return pstruct

    def handle_error(self, field, error):
        if field.error is None:
            field.error = error
        for e in error.children:
            for num, subfield in enumerate(field.children):
                if e.pos == num:
                    subfield.widget.handle_error(subfield, e)
