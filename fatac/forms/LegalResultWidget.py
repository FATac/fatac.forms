from deform.widget import Widget
from colander import null
import cgi

class LegalResultWidget(Widget):
    
    def __init__(self, **kw):
        Widget.__init__(self, **kw)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct is null:
            cstruct = u''

        js = "<script> var legal = function f() { var legalWin = window.open('./legalSelectObjectsAux'); } </script>";
        js += "<script> var setLegalResult = function f(color) { var res = 'green'; if (color=='#ffff00') res = 'yellow'; else if (color=='#ffa500') res = 'orange'; else if (color=='#ff0000') res = 'red'; document.getElementById(currField).value = res; } </script>";

        html =  '<input readonly="true" type="text" name="'+field.name+'" id="'+field.name+'"><input type="button" name="btn" value="Legal" onclick="legal(); currField=\''+field.name+'\' " >'
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
