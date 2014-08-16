from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from registration.models import Delegate, IssueForm, ReturnForm

from datetime import datetime

def issue_item(request, last_entry_code = None):
    """Associate delegate and item barcodes."""
    # Initialise values as only one will be set later and both are passed to
    # 'render'.
    issued = None
    item_already_issued = False
    # If data has been submitted, process it.
    if request.method == 'POST':
        # Select the appropriate form.
        form = IssueForm(request.POST)
        # If submitted data is valid, continue.
        if form.is_valid():
            # Check if item is already issued.
            already_issued = False
            for entry in Delegate.objects.all():
                if entry.item == form.cleaned_data['item']:
                    if entry.status == 'Issued':
                        already_issued = True
                        break
            # If item is not already issued, create a new database entry.
            if not already_issued:
                entry = Delegate(
                    delegate=form.cleaned_data['delegate'],
                    item=form.cleaned_data['item'],
                    accessory=form.cleaned_data['accessory'],
                    notes=form.cleaned_data['notes'],
                    status='Issued')
                entry.save()
                # 'entry_code' used to recall processed delegate or indicate
                # that the item is already issued on page reload.
                entry_code = entry.pk
            else:
                entry_code = 0
            # Reload the page.
            return HttpResponseRedirect(reverse(
                'registration:issue_item', args=[entry_code]))
    else:
        if last_entry_code:
            if last_entry_code == '0':
                item_already_issued = True
            else:
                issued = Delegate.objects.get(pk = last_entry_code)
        form = IssueForm()
    return render(request, 'registration/issue.html',
        {'form': form, 'issued': issued,
        'item_already_issued': item_already_issued})

def return_item(request, last_entry_code = None):
    """Disassociate delegate and item barcodes."""
    # Initialise values as only one will be set later and both are passed to
    # 'render'.
    returned = None
    item_not_issued = False
    # If data has been submitted, process it.
    if request.method == 'POST':
        # Select the appropriate form.
        form = ReturnForm(request.POST)
        # If submitted data is valid, continue.
        if form.is_valid():
            # Check if item is issued.
            issued = False
            for entry in Delegate.objects.all():
                if entry.item == form.cleaned_data['item']:
                    if entry.status == 'Issued':
                        issued = True
                        break
            # If item is issued, change 'status' to 'Returned' and update
            # timestamp.
            if issued:
                entry.status = 'Returned'
                entry.timestamp_return = datetime.now()
                entry.save()
                # 'entry_code' used to recall processed delegate or indicate
                # that the item is not issued on page reload.
                entry_code = entry.pk
            else:
                entry_code = 0
            # Reload the page.
            return HttpResponseRedirect(reverse(
                'registration:return_item', args=[entry_code]))
    else:
        if last_entry_code:
            if last_entry_code == '0':
                item_not_issued = True
            else:
                returned = Delegate.objects.get(pk = last_entry_code)
        form = ReturnForm()
    return render(request, 'registration/return.html',
        {'form': form, 'returned': returned,
        'item_not_issued': item_not_issued})
