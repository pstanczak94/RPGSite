from django import forms
from django.forms.widgets import TextInput

# Functions

def extend_field_kwargs(**kwargs):

    kwargs.setdefault('widget', TextInput())

    if 'placeholder' in kwargs.keys():
        placeholder = kwargs.pop('placeholder')
        kwargs['widget'].attrs.update({'placeholder': placeholder})

    if 'autofocus' in kwargs.keys():
        kwargs.pop('autofocus')
        kwargs['widget'].attrs.update({'autofocus': ''})

    return kwargs

def set_autofocus_to_fields(form):
    for bound_field in form.visible_fields():
        if bound_field.errors:
            bound_field.field.widget.attrs['autofocus'] = ''
        elif 'autofocus' in bound_field.field.widget.attrs:
            bound_field.field.widget.attrs.pop('autofocus')

# Fields

class CharField(forms.CharField):
    def __init__(self, **kwargs):
        kwargs = extend_field_kwargs(**kwargs)
        super(CharField, self).__init__(**kwargs)

class EmailField(forms.EmailField):
    def __init__(self, **kwargs):
        kwargs = extend_field_kwargs(**kwargs)
        super(EmailField, self).__init__(**kwargs)

# Forms

class CustomModelForm(forms.ModelForm):

    autofocus_post_clean = True

    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'widget_attrs'):
            for key, value in self.Meta.widget_attrs.items():
                self.fields[key].widget.attrs.update(value)

    def _post_clean(self):
        super(CustomModelForm, self)._post_clean()
        if self.autofocus_post_clean:
            set_autofocus_to_fields(self)

class AutoFocusFormMixin(object):

    def _clear_autofocus(self):
        for field in self.fields.values():
            if 'autofocus' in field.widget.attrs:
                field.widget.attrs.pop('autofocus')

    def _set_autofocus(self, field):
        self.fields[field].widget.attrs['autofocus'] = ''

    def set_autofocus(self, field):
        if field:
            self._clear_autofocus()
            self._set_autofocus(field)

    def set_correct_focus(self):
        for field in self.visible_fields():
            if field.errors:
                self.set_autofocus(field.name)
                return

    def _post_clean(self):
        if getattr(self, 'autofocus_post_clean', True):
            self.set_correct_focus()

    def add_form_error(self, message, field_to_focus=None):
        self.set_autofocus(field_to_focus)
        self.add_error(None, message)

# Widgets

class BootstrapTextInput(TextInput):
    def __init__(self, attrs=None):
        super(BootstrapTextInput, self).__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' form-control'
        else:
            self.attrs['class'] = 'form-control'
