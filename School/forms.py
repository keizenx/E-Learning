from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class RoleBasedAuthenticationForm(AuthenticationForm):
    """Formulaire d'authentification personnalisé avec sélection de rôle"""
    
    ROLE_CHOICES = [
        ('', _('Select your role')),
        ('ADMIN', _('Administrator')),
        ('ACADEMIC', _('Academic Manager')),
        ('TEACHER', _('Teacher')),
        ('STUDENT', _('Student')),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        label=_('Role'),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': _('Select your role'),
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        role = cleaned_data.get('role')
        
        if username and role:
            user = self.get_user()
            if user and user.role != role:
                raise forms.ValidationError(
                    _("Your account doesn't have the selected role."),
                    code='invalid_role'
                )
        
        return cleaned_data 