from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataSchemaAdapter(UserDataPanelAdapter):
    """
    """
    def get_firstname(self):
        return self.context.getProperty('firstname', '')

    def set_firstname(self, value):
        return self.context.setMemberProperties({'firstname': value})

    firstname = property(get_firstname, set_firstname)
