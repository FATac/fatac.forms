from zope.i18nmessageid import MessageFactory

FatAcMessageFactory = MessageFactory('fatac.forms')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
