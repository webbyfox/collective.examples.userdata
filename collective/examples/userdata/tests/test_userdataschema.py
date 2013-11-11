from datetime import datetime
import transaction

from plone.app.testing import TEST_USER_ID, setRoles

from ..testing import FunctionalTestCase


class TestUserDataSchema(FunctionalTestCase):
    def test_personalinformationextended(self):
        """Ensure the fields we wanted were added to @@personal-information
           and @@user-information forms
        """
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        for url in ['/@@personal-information', '/@@user-information']:
            browser = self.getBrowser(url)
            self.assertEquals(
                browser.getControl(name='form.firstname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.lastname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.gender').type,
                'radio')  # Using custom widget
            self.assertEquals(
                browser.getControl(name='form.birthdate-day').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.birthdate-month').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.birthdate-year').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.city').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.country').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.phone').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.newsletter:list').type,
                'checkbox')
            # We hid accept, so shouldn't be here
            with self.assertRaisesRegexp(LookupError, 'form.accept:list'):
                browser.getControl(name='form.accept:list')

    def test_registerextended(self):
        """Ensure the fields we wanted were added to @@register and @@add-user
           forms
        """
        portal = self.layer['portal']
        portal.MailHost.smtp_host = 'localhost'
        setattr(portal, 'email_from_address', 'admin@example.com')
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        for url in ['/@@register', '/@@new-user']:
            browser = self.getBrowser(url)
            self.assertEquals(
                browser.getControl(name='form.firstname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.lastname').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.gender').type,
                'radio')  # Using custom widget
            self.assertEquals(
                browser.getControl(name='form.birthdate-day').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.birthdate-month').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.birthdate-year').type,
                'select')
            self.assertEquals(
                browser.getControl(name='form.city').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.country').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.phone').type,
                'text')
            self.assertEquals(
                browser.getControl(name='form.newsletter:list').type,
                'checkbox')
            if url == '/@@register':
                self.assertEquals(
                    browser.getControl(name='form.accept:list').type,
                    'checkbox')
            else:
                # We hid accept, so shouldn't be here
                with self.assertRaisesRegexp(LookupError, 'form.accept:list'):
                    browser.getControl(name='form.accept:list')

    def test_validateaccept(self):
        """Make sure we have to check the 'accept' box
        """
        # Allow users to set their own passwords when registering
        setRoles(self.layer['portal'], TEST_USER_ID, ['Manager'])
        transaction.commit()
        browser = self.getBrowser('/@@security-controlpanel')
        browser.getControl('Enable self-registration').selected = True
        browser.getControl('Let users select their own passwords').selected \
            = True
        browser.getControl('Save').click()
        self.assertTrue('Changes saved' in browser.contents)

        # Try registering without clicking "accept"
        browser = self.getBrowser('/@@register')
        browser.getControl('User Name').value = 'mrcamel'
        browser.getControl('E-mail').value = 'camel@example.com'
        browser.getControl('Password').value = 'dr0medary'
        browser.getControl('Confirm password').value = 'dr0medary'
        browser.getControl(name='form.gender').value = ['Male']
        browser.getControl('Register').click()
        # Should still be on the form at this point, check the box
        self.assertTrue('@@register' in browser.url)
        browser.getControl('Password').value = 'dr0medary'
        browser.getControl('Confirm password').value = 'dr0medary'
        browser.getControl(name='form.accept:list').value = True
        browser.getControl('Register').click()
        self.assertTrue('You have been registered' in browser.contents)

    def test_setvalues(self):
        """Make sure we can set and retrieve all values
        """
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        transaction.commit()

        yr = str(datetime.now().year - 5)  # widget will only go back 10 years
        browser = self.getBrowser('/@@personal-information')
        browser.getControl('E-mail').value = 'beth@example.com'
        browser.getControl(name='form.firstname').value = 'Beth'
        browser.getControl(name='form.lastname').value = 'Orton'
        browser.getControl(name='form.gender').value = ['Female']
        browser.getControl(name='form.birthdate-day').value = ['15']
        browser.getControl(name='form.birthdate-month').value = ['3']
        browser.getControl(name='form.birthdate-year').value = [yr]
        browser.getControl(name='form.city').value = 'Norwich'
        browser.getControl(name='form.country').value = 'UK'
        browser.getControl(name='form.phone').value = '012345'
        browser.getControl(name='form.newsletter:list').value = ['selected']
        browser.getControl('Save').click()
        self.assertTrue('Changes saved.' in browser.contents)

        # Should be able to retrieve values when page is reloaded
        browser.open(portal.absolute_url() + '/@@personal-information')
        self.assertEquals(
            browser.getControl('E-mail').value,
            'beth@example.com')
        self.assertEquals(
            browser.getControl(name='form.firstname').value,
            'Beth')
        self.assertEquals(
            browser.getControl(name='form.lastname').value,
            'Orton')
        self.assertEquals(
            browser.getControl(name='form.gender').value,
            ['Female'])
        self.assertEquals(
            browser.getControl(name='form.birthdate-day').value,
            ['15'])
        self.assertEquals(
            browser.getControl(name='form.birthdate-month').value,
            ['3'])
        self.assertEquals(
            browser.getControl(name='form.birthdate-year').value,
            [yr])
        self.assertEquals(
            browser.getControl(name='form.city').value,
            'Norwich')
        self.assertEquals(
            browser.getControl(name='form.country').value,
            'UK')
        self.assertEquals(
            browser.getControl(name='form.phone').value,
            '012345')
        self.assertEquals(
            browser.getControl(name='form.newsletter:list').value,
            ['selected'])
