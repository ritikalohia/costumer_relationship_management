from django import forms
from django.contrib.auth import get_user_model
from django.contrib
from leads.models import Agent

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = (
            'user',
        )



