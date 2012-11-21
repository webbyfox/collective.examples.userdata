Introduction
============

The registration and personal information forms are z3c.form forms. These
can be extended to allow any additional data to be collected on the forms.

This product aims to show how you could extend or modify the default schema
provided by plone.app.users, and add new fields to the registration form.

Adding custom fields
--------------------

Adding fields to the memberdata properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To store the values alongside default fields, we need to add fields to
``profiles/default/memberdata_properties.xml``. For example::

    <?xml version="1.0"?>
    <object name="portal_memberdata" meta_type="Plone Memberdata Tool">
      <property name="country" type="string"></property>
    </object>

We don't define the "accept" field here, since that is only for signup.

Creating a schema
~~~~~~~~~~~~~~~~~

We create a schema for our fields in the same manner as any other schema::

    class IEnhancedUserDataSchema(model.Schema):
        country = schema.TextLine(
            title=_(u'label_country', default=u'Country'),
            description=_(u'help_country',
                          default=u"Fill in the country you live in."),
            required=False,
            )

Defining FormExtenders
~~~~~~~~~~~~~~~~~~~~~~

We need to define a form extender for both ``UserDataPanel`` and 
``BaseRegistrationForm``. This allows us to register our fields onto either the
userdata or registration form respectively::

    class UserDataPanelExtender(extensible.FormExtender):
        adapts(Interface, IDefaultBrowserLayer, UserDataPanel)
        def update(self):
            fields = field.Fields(IEnhancedUserDataSchema)
            fields = fields.omit('accept') # Users have already accepted.
            self.add(fields, prefix="IEnhancedUserDataSchema")

    class RegistrationPanelExtender(extensible.FormExtender):
        adapts(Interface, IDefaultBrowserLayer, BaseRegistrationForm)
        def update(self):
            fields = field.Fields(IEnhancedUserDataSchema)
            self.add(fields, prefix="IEnhancedUserDataSchema")

And register these in configure.zcml::

    <adapter
      factory=".userdataschema.UserDataPanelExtender"
      provides="plone.z3cform.fieldsets.interfaces.IFormExtender" />

    <adapter
      factory=".userdataschema.RegistrationPanelExtender"
      provides="plone.z3cform.fieldsets.interfaces.IFormExtender" />

Defining data manager
~~~~~~~~~~~~~~~~~~~~~

Before values can be read and written, there needs to be a data manager to
fetch the values. This can inherit from the default one, so most of the work is
done for you::

    from plone.app.users.browser.z3cpersonalpreferences import AccountPanelSchemaAdapter

    class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
        schema = IEnhancedUserDataSchema

And register this in ZCML::

    <adapter
      provides=".userdataschema.IEnhancedUserDataSchema"
      for="plone.app.layout.navigation.interfaces.INavigationRoot"
      factory=".adapter.EnhancedUserDataSchemaAdapter"
      />

By default anything defined in your schema will be read out of the property
sheets. If you don't want to do that, or want to do more processing beforehand,
then define getters and setters (the example does this).

Various other field examples
----------------------------

There are various other extra fields with which you could extend your users'
profile. In ``userdataschema.py`` you will find examples for:

- a Date field (``birthdate``)
- a Boolean field (``newsletter``)
- a Choice field (``gender``)

The "Accept Terms" field
~~~~~~~~~~~~~~~~~~~~~~~~

A special case is the ``accept`` field. This is a Boolean field which is
required for signup. We implement it by adding a ``constraint`` to the schema::

    def validateAccept(value):
        if not value == True:
            return False
        return True

    class IEnhancedUserDataSchema(IUserDataSchema):
        # ...
        accept = schema.Bool(
            title=_(u'label_accept', default=u'Accept terms of use'),
            description=_(u'help_accept',
                          default=u"Tick this box to indicate that you have found,"
                          " read and accepted the terms of use for this site. "),
            required=True,
            constraint=validateAccept,
            )

Because this field can be ignored once registration is complete, we don't add
it to the memberdata properties (see below).

Default settings for registration fields
----------------------------------------

We can automatically select some fields to go on the registration form. The
fields we define in ``profiles/default/propertiestool.xml`` will be on the form
once the product is installed.

Of course, the site manager can modify this after installation.

.. _plone.app.users: http://pypi.python.org/pypi/plone.app.users
.. _formlib: http://pypi.python.org/pypi/zope.formlib
.. _plone.app.controlpanel: http://pypi.python.org/pypi/plone.app.controlpanel
 