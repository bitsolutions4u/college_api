from django.db import models
from django.conf import settings

from Common.utils import getcode, CompressImage
# from Common.middleware import ErrorMiddleware

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill



class Menu(models.Model):
    code = models.CharField(max_length=30,null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='menuscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='menusupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def __str__(self):
        return self.name


class Submenu(models.Model):
    code = models.CharField(max_length=30,null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    sequence = models.IntegerField(default=100,null=True, blank=True)
    icon = models.CharField(max_length=30,null=True, blank=True)
    click = models.CharField(max_length=50, null=True, blank=True)
    menu = models.ForeignKey('System.Menu', related_name='submenus', on_delete=models.RESTRICT, null=True)
    submenu = models.ForeignKey('System.Submenu', related_name='submenus', on_delete=models.RESTRICT, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submenuscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submenusupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Submenu,'SBM')
        super(Submenu, self).save(*args, **kwargs)

        
class Menuitem(models.Model):
    code = models.CharField(max_length=30,null=True, blank=True, unique=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    icon = models.CharField(max_length=30,null=True, blank=True)
    link = models.CharField(max_length=50,null=True, blank=True)
    sequence = models.IntegerField(default=100,null=True, blank=True)
    click = models.CharField(max_length=50, null=True, blank=True)
    menu = models.ForeignKey('System.Menu', related_name='menuitems', on_delete=models.RESTRICT, null=True)
    submenu = models.ForeignKey('System.Submenu', related_name='menuitems', on_delete=models.RESTRICT, null=True, blank=True)
    permission = models.ForeignKey('auth.Permission', related_name='menuitems', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='menuitemscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='menuitemsupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Menuitem,'MIM')
        super(Menuitem, self).save(*args, **kwargs)

        
NOTE_TYPES_CHOICES = (
    ( 1 , "Message"),
)        
SEEN_CHOICES = (
    ( 0 , "Unseen"),
    ( 1 , "Seen"),
)

class Notification(models.Model):
    subject = models.CharField(max_length=100,null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=25,null=True, blank=True)
    ref = models.IntegerField(default=0,null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.SmallIntegerField(default=1, null=True)

    def __str__(self):
        return str(self.id)



class NotificationUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notificationusers', on_delete=models.RESTRICT, null=True)
    notification = models.ForeignKey(Notification, related_name='notificationusers', on_delete=models.RESTRICT, null=True)
    seen = models.SmallIntegerField(default=0, choices= SEEN_CHOICES, null=True, blank=True)
    seen_time = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(default=1, null=True)

        
class Backup(models.Model):
    code = models.CharField(max_length=30,null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='backupscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='backupsupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Backup,'BAKUP')
        super(Backup, self).save(*args, **kwargs)


class Restore(models.Model):
    code = models.CharField(max_length=30,null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, unique=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restorescreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restoresupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Restore,'RESTR')
        super(Restore, self).save(*args, **kwargs)


class Attachment(models.Model):
    file = models.FileField(upload_to="attachments/", null=True, blank=True)
    file_thumbnail = ImageSpecField(source='file', processors=[ResizeToFill(150, 150)], format='JPEG', options={'quality': 60})
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attachmentscreated', on_delete=models.RESTRICT, null=True)
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file =  CompressImage(self.file)
        super(Attachment, self).save(*args, **kwargs)


    def __str__(self):
        return self.file.path if self.file else ""



class Formula(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=50, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True, )
    formula = models.CharField(max_length=200, null=True, blank=True,)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='formulascreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True,auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='formulasupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True, blank=True)



    def __str__(self):
        return self.name
        


class FormulaVariables(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=30, default=0, null=True, blank=True)
    description = models.TextField(default='', blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, )
    formula = models.ForeignKey(Formula, related_name='formulavariables', on_delete=models.RESTRICT, null=True, blank=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = getcode(FormulaVariables,'FRMV')
        super(FormulaVariables, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name


class FormulaUpdate(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    formula = models.ForeignKey(Formula, related_name='formulaupdates', on_delete=models.RESTRICT, null=True, blank=True)
    formula_txt = models.CharField(max_length=200, null=True, blank=True,)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='formulaupdatescreated', on_delete=models.RESTRICT, null=True)


    def __str__(self):
        return self.formula_txt


ACTION_TYPES_CHOICES = (
    ( 1 , "Create"),
    ( 2 , "Update"),
    ( 3 , "Delete"),
)

class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activitylogs', on_delete=models.RESTRICT, null=True)
    type = models.SmallIntegerField(default=1, choices= ACTION_TYPES_CHOICES, blank=True, null=True, )
    tablename = models.CharField(max_length=100, null=True, blank=True, )
    recordcode = models.CharField(max_length=50, null=True, blank=True, )
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.SmallIntegerField(default=1, null=True, blank=True)



    def __str__(self):
        return self.tablename




class Error(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    errorcode = models.CharField(max_length=50, null=True, blank=True, )
    requestbody = models.TextField( null=True, blank=True, )
    responsecontent = models.TextField( null=True, blank=True, ) 
    error_url = models.URLField(max_length=200,  null=True, blank=True,)


    def __str__(self):
        return self.errorcode
    


class Setting(models.Model):
    pass
    
    class Meta:
        permissions = (
            ("view_masters", "Can View Masters"),
            ("view_trans_approvals", "Can View Transaction Approvals"),
            ("view_import", "Can View Import"),
            ("view_export", "Can View Export "),
            ("view_report", "Can View Reports "),
        )


class TemporaryVerification(models.Model):
    mobile = models.CharField(max_length=15, db_index=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    

    def __str__(self):
        return self.mobile
        
    
