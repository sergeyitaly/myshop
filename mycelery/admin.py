from django.contrib import admin
from django import forms
from .models import ScheduledTask
import os
import importlib
import logging

logger = logging.getLogger(__name__)
def get_available_commands():
    command_dir = os.path.join(os.path.dirname(__file__), 'management', 'commands')
    available_commands = []

    if os.path.isdir(command_dir):
        for filename in os.listdir(command_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                command_name = filename[:-3]  # Remove the '.py' extension
                available_commands.append(command_name)

    return available_commands

class ScheduledTaskForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[])

    class Meta:
        model = ScheduledTask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScheduledTaskForm, self).__init__(*args, **kwargs)
        available_commands = get_available_commands()
        self.fields['name'].choices = [(cmd, cmd) for cmd in available_commands]

@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    form = ScheduledTaskForm
    list_display = ('name', 'max_time', 'last_run_at', 'last_run_status')
    search_fields = ('name',)
