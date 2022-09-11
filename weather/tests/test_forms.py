import django.forms.widgets
from django.test import TestCase

from weather.forms import CitySearchForm, UserRegisterForm, UserLoginForm


class CitySearchFormTest(TestCase):

    def test_city_name_label(self):
        field_label = get_field_label_from_form('city_name', CitySearchForm())
        self.assertEqual(field_label, 'City Name')

    def test_city_name_widget_is_text_input(self):
        form = CitySearchForm()
        widget = form.fields['city_name'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.TextInput))


class UserRegisterFormTest(TestCase):

    def test_username_max_length(self):
        form = UserRegisterForm()
        max_length = form.fields['username'].max_length
        self.assertEqual(max_length, 150)

    def test_username_label(self):
        field_label = get_field_label_from_form('username', UserRegisterForm())
        self.assertEqual(field_label, 'User name')

    def test_username_widget_is_text_input(self):
        form = UserRegisterForm()
        widget = form.fields['username'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.TextInput))

    def test_password1_label(self):
        field_label = get_field_label_from_form('password1', UserRegisterForm())
        self.assertEqual(field_label, 'Password')

    def test_password1_widget_is_password_input(self):
        form = UserRegisterForm()
        widget = form.fields['password1'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.PasswordInput))

    def test_password2_label(self):
        field_label = get_field_label_from_form('password2', UserRegisterForm())
        self.assertEqual(field_label, 'Password confirm')

    def test_password2_widget_is_password_input(self):
        form = UserRegisterForm()
        widget = form.fields['password2'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.PasswordInput))

    def test_email_label(self):
        field_label = get_field_label_from_form('email', UserRegisterForm())
        self.assertEqual(field_label, 'E-mail')

    def test_email_widget_is_email_input(self):
        form = UserRegisterForm()
        widget = form.fields['email'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.EmailInput))


class UserLoginFormTest(TestCase):

    def test_username_label(self):
        field_label = get_field_label_from_form('username', UserLoginForm())
        self.assertEqual(field_label, 'User name')

    def test_username_widget_is_text_input(self):
        form = UserLoginForm()
        widget = form.fields['username'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.TextInput))

    def test_password_label(self):
        field_label = get_field_label_from_form('password', UserLoginForm())
        self.assertEqual(field_label, 'Password')

    def test_password_widget_is_password_input(self):
        form = UserLoginForm()
        widget = form.fields['password'].widget
        self.assertTrue(isinstance(widget, django.forms.widgets.PasswordInput))


def get_field_label_from_form(field_label_name, form):
    return form.fields[field_label_name].label
