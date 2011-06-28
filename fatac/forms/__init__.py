from zope.i18nmessageid import MessageFactory

FatAcMessageFactory = MessageFactory('fat.demo')  

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
