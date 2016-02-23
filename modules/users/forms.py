# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


class UserAdminCreationForm(forms.ModelForm):

    """A form for creating new users."""

    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label=_('Password confirmation'), widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'surname')

    def clean_confirm_password(self):
        """Clean passwords."""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(self.PASSWORDS_MUST_MATCH)

        return password

    def save(self, *args, **kwargs):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        return super(UserAdminCreationForm, self).save(*args, **kwargs)


class UserAdminChangeForm(forms.ModelForm):

    """A form for updating users."""

    password = ReadOnlyPasswordHashField(
        label=_('Password'), help_text=_('<a href="../password/">Change</a>')
    )

    class Meta:
        model = get_user_model()
        exclude = tuple()

    def clean_password(self):
        """Clean password."""
        return self.initial['password']
