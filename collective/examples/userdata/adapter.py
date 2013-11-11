from .userdataschema import IEnhancedUserDataSchema
from plone.app.users.browser.personalpreferences import AccountPanelSchemaAdapter

class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema

    def get_birthdate(self):
        bd = self._getProperty('birthdate')
        return None if bd == '' else bd

    def set_birthdate(self, value):
        return self._setProperty('birthdate', value)

    birthdate = property(get_birthdate, set_birthdate)
