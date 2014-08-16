from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from lending.models import (User, Item, History, Tablet, BugsFeatures,
    BorrowForm, ReturnForm, BugsFeaturesForm)

class UserList(ListView):
    """Create list of users. Use default template 'user_list.html'."""
    model = User

class ItemList(ListView):
    """Create list of items. Use default template 'item_list.html'."""
    model = Item

class HistoryList(ListView):
    """Create history list. Use default template 'history_list.html'."""
    model = History

class TabletDetail(DetailView):
    """Display detailed tablet attributes. Use default template
    'tablet_detail.html'.
    """
    model = Tablet
    def get_context_data(self, **kwargs):
        """Override default 'get_context_data' method to add context."""
        # Call the base implementation to obtain default context.
        context = super(TabletDetail, self).get_context_data()
        # Add further context.
        context['history'] = History.objects.filter(item__pk = self.object.pk)
        return context

class UserDetail(DetailView):
    """Display detailed user attributes. Use default template
    'user_detail.html'.
    """
    model = User
    def get_context_data(self, **kwargs):
        """Override default 'get_context_data' method to add context."""
        # Call the base implementation to obtain default context.
        context = super(UserDetail, self).get_context_data()
        # Add further context.
        context['history'] = History.objects.filter(
            current_user_pk = self.object.pk)
        return context

class TabletList(ListView):
    """Create list of tablets."""
    model = Tablet
    # Specify template, as using custom queryset.
    template_name = 'lending/tablet_list.html'
    context_object_name = 'tablet_list'
    # def get_context_data(self):
    #     """Override default 'get_context_data' method to add context."""
    #     # Call the base implementation to obtain default context.
    #     context = super(TabletList, self).get_context_data()
    #     # Add further context.
    #     stock_total = context['stock_total'] = len(Tablet.objects.all())
    #     stock_in = context['stock_in'] = len(Tablet.objects.filter(
    #         user__name = 'None'))
    #     context['stock_out'] = stock_total - stock_in
    #     return context
    def get_queryset(self):
        """Split tablets by in and out of stock."""
        stock_in = Tablet.objects.filter(user__name = 'None')
        stock_out = Tablet.objects.exclude(user__name = 'None')
        # Include counts in returned list.
        tablets = [
            [len(stock_in), len(stock_out), len(stock_in) + len(stock_out)],
            stock_in, stock_out]
        return tablets

class LentList(ListView):
    """Create list of lent items."""
    # Currently, only concerned with tablets, so use Tablet model.
    model = Tablet
    # Specify template, as using custom queryset.
    template_name = 'lending/lent_list.html'
    context_object_name = 'lent_list'
    def get_queryset(self):
        """Create list of users and associated items."""
        # Create list of items associated with users other than 'None'.
        items = Tablet.objects.exclude(user__name = 'None').order_by('user')
        lent = []
        for item in items:
            item_details = [item.pk, item.barcode, item.name, item.serial,
                item.tablet_solution, item.message_manager, item.honey_hide,
                item.firefox, item.full_screen, item.join_in, item.fundraiser]
            # Upon first iteration, 'lent' is empty, so 'added' must be 'False'.
            added = False
            for entry in lent:
                # Check if user is already in 'lent' and append item details
                # under their entry if so.
                if item.user.pk == entry[0]:
                    entry.append(item_details)
                    # Set 'added' to 'True' to prevent adding user to 'lent'
                    # more than once.
                    added = True
                    break
            # If user is not yet in 'lent', add them and first item details.
            if not added:
                lent.append([item.user.pk, item.user.name, item_details])
        return lent

def borrow_item(request, current_user=None):
    """Associate an item with a user."""
    user_lent = None
    # If data has been submitted, process it.
    if request.method == 'POST':
        # Select the appropriate form.
        form = BorrowForm(request.POST)
        # If submitted data is valid, continue.
        if form.is_valid():
            # Compare submitted barcode with item barcodes. If a match is found,
            # set the item's user to submitted user and record transaction
            # history.
            for item in Item.objects.all():
                if item.barcode == form.cleaned_data['barcode']:
                    item.user = form.cleaned_data['user']
                    item.save()
                    history = History(item=item, transaction_type='Borrow',
                        current_user=item.user, current_user_pk=item.user.pk)
                    history.save()
                    # Reload the page, passing current user with request.
                    return HttpResponseRedirect(reverse(
                        'lending:borrow_item', args=[item.user.pk]))
    else:
        # If a user has been passed with the page request, preselect them on the
        # appropriate form and create a list of their associated items.
        if current_user:
            form = BorrowForm(initial={'user': User(pk=current_user)})
            user_lent = create_user_lent(current_user)
        else:
            form = BorrowForm()
    return render(
        request, 'lending/borrow.html', {'form': form, 'user_lent': user_lent})

def return_item(request, current_user = None):
    """Disassociate an item with a user."""
    user_lent = None
    # If data has been submitted, process it.
    if request.method == 'POST':
        # Select the appropriate form.
        form = ReturnForm(request.POST)
        # If submitted data is valid, continue.
        if form.is_valid():
            # Compare submitted barcode with item barcodes. If a match is found,
            # record transaction history, store current user then set the item's
            # user to 'None' (pk=3).
            for item in Item.objects.exclude(user__name = 'None'):
                if item.barcode == form.cleaned_data['barcode']:
                    history = History(item=item, transaction_type='Return',
                        current_user=item.user, current_user_pk=item.user.pk)
                    history.save()
                    user_pk = item.user.pk
                    item.user = User(pk=3)
                    item.save()
                    # Reload the page, passing current user with request.
                    return HttpResponseRedirect(reverse(
                        'lending:return_item', args=[user_pk]))
    else:
        # If a user has been passed with the page request, create a list of
        # their associated items.
        if current_user:
            user_lent = create_user_lent(current_user)
        form = ReturnForm()
    return render(
        request, 'lending/return.html', {'form': form, 'user_lent': user_lent})

def create_user_lent(current_user):
    """Create a list of the current user's associated items."""
    # Create a list containing any items associated with the current user.
    user_items = Tablet.objects.filter(user__pk = current_user)
    # If there are items associated with the current user, create a list
    # containing the user's pk and name followed by the details of each item.
    if user_items:
        user_lent = [current_user, user_items[0].user.name]
        for item in user_items:
            user_lent.append(
                [item.pk, item.barcode, item.name, item.serial,
                 item.tablet_solution, item.message_manager, item.honey_hide,
                 item.firefox, item.full_screen, item.join_in, item.fundraiser])
    else:
        # If there aren't any items associated with the current user, simply
        # create a list containing the user's pk and name.
        user_lent = [current_user, User.objects.filter(pk = current_user)[0]]
    return user_lent

def submit_bug_feature(request):
    """Log a bug or feature request."""
    bug_feature_list = None
    # If data has been submitted, process it.
    if request.method == 'POST':
        # Select the appropriate form.
        form = BugsFeaturesForm(request.POST)
        # If submitted data is valid, continue.
        if form.is_valid():
            # Create a new database entry.
            submission = BugsFeatures(user=form.cleaned_data['user'],
                bug_feature=form.cleaned_data['bug_feature'],
                status='Submitted')
            submission.save()
            # Reload the page.
            return HttpResponseRedirect(reverse('lending:submit_bug_feature'))
    else:
        form = BugsFeaturesForm()
        # Create list of all submitted bugs and feature requests.
        bug_feature_list = BugsFeatures.objects.all()
    return render(request, 'lending/bugs_features.html',
        {'form': form, 'bug_feature_list': bug_feature_list})
