from django.contrib import admin
from django import forms
from .models import ScheduledTask
import os
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
    days = forms.IntegerField(required=False, min_value=0, label='Days')
    hours = forms.IntegerField(required=False, min_value=0, max_value=23, label='Hours')
    minutes = forms.IntegerField(required=False, min_value=0, max_value=59, label='Minutes')

    class Meta:
        model = ScheduledTask
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScheduledTaskForm, self).__init__(*args, **kwargs)
        available_commands = get_available_commands()
        self.fields['name'].choices = [(cmd, cmd) for cmd in available_commands]

        if self.instance and self.instance.max_time:
            # If there's an existing max_time, prepopulate days, hours, and minutes
            total_minutes = self.instance.max_time
            self.fields['days'].initial = total_minutes // 1440  # 1 day = 1440 minutes
            total_minutes %= 1440
            self.fields['hours'].initial = total_minutes // 60  # 1 hour = 60 minutes
            self.fields['minutes'].initial = total_minutes % 60  # remaining minutes

    def clean(self):
        cleaned_data = super().clean()
        days = cleaned_data.get('days', 0)
        hours = cleaned_data.get('hours', 0)
        minutes = cleaned_data.get('minutes', 0)

        # Convert the total time into minutes
        total_minutes = (days * 1440) + (hours * 60) + minutes
        cleaned_data['max_time'] = total_minutes
        return cleaned_data

@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    form = ScheduledTaskForm
    list_display = ('name', 'get_days', 'get_hours', 'get_minutes', 'last_run_at', 'last_run_status')
    search_fields = ('name',)
    readonly_fields = ('max_time',)

    def get_days(self, obj):
        return obj.max_time // 1440  # Calculate days from max_time
    get_days.admin_order_field = 'max_time'  # Allow sorting by max_time
    get_days.short_description = 'Days'

    def get_hours(self, obj):
        return (obj.max_time % 1440) // 60  # Calculate hours from remaining minutes
    get_hours.admin_order_field = 'max_time'
    get_hours.short_description = 'Hours'

    def get_minutes(self, obj):
        return obj.max_time % 60  # Get remaining minutes
    get_minutes.admin_order_field = 'max_time'
    get_minutes.short_description = 'Minutes'
