from zope.interface import Interface, implements
from zope import schema

from collective.examples.userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add:
    - country
    """
    country = schema.TextLine(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u"Fill in which country you live in."),
        required=False,
        )
