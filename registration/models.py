from django.db import models
from django.forms import ModelForm, TextInput, RadioSelect

from datetime import datetime

class Delegate(models.Model):
    """Create delegate model."""
    delegate = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    accessory = models.BooleanField(
        choices=((True, 'Yes'), (False, 'No')),
        default=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    timestamp_issue = models.DateTimeField('Issued', auto_now_add=True)
    timestamp_return = models.DateTimeField('Returned', default=datetime.min)
    class Meta:
        # Sort alphabetically by delegate barcode.
        ordering = ['delegate']
    def __unicode__(self):
        return self.delegate

class IssueForm(ModelForm):
    """Create form model for issuing items."""
    class Meta:
        model = Delegate
        fields = ['delegate', 'item', 'accessory', 'notes']
        # Customise widgets.
        widgets = {
            'delegate': TextInput(attrs={'autofocus': True}),
            'accessory': RadioSelect()}

class ReturnForm(ModelForm):
    """Create form model for returning items."""
    class Meta:
        model = Delegate
        fields = ['item']
        # Customise widgets.
        widgets = {
            'item': TextInput(attrs={'autofocus': True})}
