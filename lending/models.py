from django.db import models
from django.forms import ModelForm, TextInput

class User(models.Model):
    """Create user model."""
    name = models.CharField('Full Name', max_length=50)
    class Meta:
        # Sort users alphabetically.
        ordering = ['name']
    def __unicode__(self):
        return self.name

class Item(models.Model):
    """Create generic item model."""
    name = models.CharField('Item Name', max_length=50)
    barcode = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    class Meta:
        # Sort items alphabetically by name then barcode.
        ordering = ['name', 'barcode']
    def __unicode__(self):
        return self.name

class History(models.Model):
    """Create history model."""
    item = models.ForeignKey(Item)
    time_stamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=50)
    current_user = models.CharField(max_length=50)
    current_user_pk = models.IntegerField()

class Tablet(Item):
    """Create tablet item model."""
    serial = models.CharField('Serial No.', max_length=50)
    tablet_solution = models.BooleanField('Tablet Solution 1.6')
    message_manager = models.BooleanField('Message Manager')
    honey_hide = models.BooleanField('Honey Hide')
    firefox = models.BooleanField()
    full_screen = models.BooleanField('FS Add On')
    join_in = models.BooleanField('Join In')
    fundraiser = models.BooleanField('Fundraiser 2.4')
    def __unicode__(self):
        return self.name

class BugsFeatures(models.Model):
    """Create bug submission / feature request model."""
    bug_feature = models.TextField('Bug / Feature')
    user = models.ForeignKey(User)
    status = models.CharField(max_length=50)
    def __unicode__(self):
        return str(self.id)

class BorrowForm(ModelForm):
    """Create form model for borrowing items."""
    class Meta:
        model = Item
        fields = ['user', 'barcode']
        # Set focus on barcode field upon page load.
        widgets = {'barcode': TextInput(attrs={'autofocus': True})}

class ReturnForm(ModelForm):
    """Create form model for returning items."""
    class Meta:
        model = Item
        fields = ['barcode']
        # Set focus on barcode field upon page load.
        widgets = {'barcode': TextInput(attrs={'autofocus': True})}

class BugsFeaturesForm(ModelForm):
    """Create form model for submitting a bug / feature request."""
    class Meta:
        model = BugsFeatures
        fields = ['user', 'bug_feature']
