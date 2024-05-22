from django.db import models

from django.conf import settings
from Common.utils import getcode
import datetime

from Users.models import User


class Country(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='countrycreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='countryupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Country,'COUNTRY')
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class State(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='statescreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='statesupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(State,'STAT')
        super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='districts', on_delete=models.RESTRICT, null=True)
    state = models.ForeignKey(State, related_name='districts', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='districtscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='districtsupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(District,'DIST')
        super(District, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.RESTRICT, null=True)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.RESTRICT, null=True)
    district = models.ForeignKey(District, related_name='cities', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='citiescreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='citiesupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(City,'CITY')
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"



class Area(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, related_name='areas', on_delete=models.RESTRICT, null=True)
    district = models.ForeignKey(District, related_name='areas', on_delete=models.RESTRICT, null=True)
    state = models.ForeignKey(State, related_name='areas', on_delete=models.RESTRICT, null=True)
    pincode = models.CharField(max_length=10, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='areascreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='areasupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Area,'AREA')
        super(Area, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Branch(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    address=models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(User, related_name='branch_users', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='branchcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='branchupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Religion(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='religioncreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='religionupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Religion, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Caste(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    religion = models.ForeignKey(Religion, related_name='religions', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='castecreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='casteupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Caste, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCaste(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    caste = models.ForeignKey(Caste, related_name='subcaste', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subcastecreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subcasteupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)


    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(State,'STAT')
        super(SubCaste, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='occupationcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='occupationupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Occupation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Education(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='educationcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='educationupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Education, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Language(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='languagecreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='languageupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Designation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.ForeignKey(Occupation, related_name='occupation', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='designationcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='designationupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Designation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class University(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='universitycreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='universityupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(University, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Visa(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='visacreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='visaupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Visa, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Source(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sourcecreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sourceupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(Source, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class MemberShip(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    planname = models.CharField(max_length=100, null=True, blank=True)
    plantype = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(default=1, null=True)
    contactsno=models.IntegerField(default=1, null=True)
    amount=models.IntegerField(default=1, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='membershipcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='membershipupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    smsenable = models.SmallIntegerField(default=1, null=True)
    emailenable=models.SmallIntegerField(default=1, null=True)
    personalassistance=models.SmallIntegerField(default=1, null=True)
    photozoom=models.SmallIntegerField(default=1, null=True)
    sendinterest=models.SmallIntegerField(default=1, null=True)
    profilesuggestions=models.SmallIntegerField(default=1, null=True)

    def save(self, *args, **kwargs):
        # if self.id is None and (self.code == "" or self.code == None):
        #     self.code = getcode(Branch,'BRANCH')
        super(MemberShip, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

def images_upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Staff(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    maritalStatus = models.CharField(max_length=15, null=True, blank=True)
    officeMobile = models.CharField(max_length=15, db_index=True, blank=True)
    pemail = models.EmailField(max_length=255, db_index=True, blank=True, null=True)
    branch = models.ForeignKey('Masters.Branch', related_name='staff', on_delete=models.RESTRICT, null=True, blank=True)
    religion = models.ForeignKey('Masters.Religion', related_name='staff', on_delete=models.RESTRICT, null=True, blank=True)
    caste = models.ForeignKey('Masters.Caste', related_name='staff', on_delete=models.RESTRICT, null=True,blank=True)
    education = models.ForeignKey('Masters.Education', related_name='staff', on_delete=models.RESTRICT, null=True,blank=True)
    source = models.ForeignKey('Masters.Source', related_name='staff', on_delete=models.RESTRICT, null=True,blank=True)
    # branch = models.CharField(max_length=100, null=True, blank=True)
    # religion = models.CharField(max_length=100, null=True, blank=True)
    # caste = models.CharField(max_length=100, null=True, blank=True)
    eduType = models.CharField(max_length=100, null=True, blank=True)
    # qual = models.CharField(max_length=100, null=True, blank=True)
    aadharno = models.CharField(max_length=15, null=True, blank=True)
    fname= models.CharField(max_length=50, null=True, blank=True)
    fmobile = models.CharField(max_length=15, db_index=True, blank=True)
    faddress = models.TextField(blank=True, null=True)
    refname = models.CharField(max_length=50, null=True, blank=True)
    refmobile = models.CharField(max_length=15, db_index=True, blank=True)
    refaddress = models.TextField(blank=True, null=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    jdate = models.CharField(max_length=50, null=True, blank=True)
    # source = models.CharField(max_length=50, null=True, blank=True)
    pexp = models.CharField(max_length=5, null=True, blank=True)
    user = models.ForeignKey(User, related_name='staff_users', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staffcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staffupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    photo = models.ImageField(upload_to=images_upload_to,default='bill_pic',  blank=True, null=True)
    def save(self, *args, **kwargs):
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def agents_upload_to(instance, filename):
    return 'images/agents/{filename}'.format(filename=filename)
class Agent(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    maritalStatus = models.CharField(max_length=15, null=True, blank=True)
    education = models.ForeignKey('Masters.Education', related_name='agent', on_delete=models.RESTRICT, null=True,blank=True)
    aadharno = models.CharField(max_length=15, null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    bankaccno= models.CharField(max_length=15, null=True, blank=True)
    bankname = models.CharField(max_length=50,  null=True, blank=True)
    bankifsccode = models.CharField(max_length=15,  null=True, blank=True)
    bankbranchname = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, related_name='agent_users', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='agentcreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='agentupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    photo = models.ImageField(upload_to=agents_upload_to,default='blank_pic',  blank=True, null=True)
    def save(self, *args, **kwargs):
        super(Agent, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def customer_photo_upload_to(instance, filename):
    return 'images/customers/photos/{filename}'.format(filename=filename)
def customer_id_upload_to(instance, filename):
    return 'images/customers/ids/{filename}'.format(filename=filename)
class Customer(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    maritalStatus = models.CharField(max_length=25, null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    applicationFor = models.CharField(max_length=25, null=True, blank=True)
    dateOfMarriage = models.CharField(max_length=50, null=True, blank=True)
    dateOfDivorce = models.CharField(max_length=50, null=True, blank=True)
    reasonDivorce = models.CharField(max_length=50, null=True, blank=True)
    divorceChildren = models.CharField(max_length=5, null=True, blank=True)
    divorcenoofsons= models.CharField(max_length=2, null=True, blank=True)
    divorceSonName_1 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonAge_1 = models.CharField(max_length=2, null=True, blank=True)
    divorceSonMStatus_1 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonName_2  = models.CharField(max_length=50, null=True, blank=True)
    divorceSonAge_2 = models.CharField(max_length=2, null=True, blank=True)
    divorceSonMStatus_2 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonName_3 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonAge_3 = models.CharField(max_length=2, null=True, blank=True)
    divorceSonMStatus_3 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonName_4 = models.CharField(max_length=50, null=True, blank=True)
    divorceSonAge_4 = models.CharField(max_length=2, null=True, blank=True)
    divorceSonMStatus_4 = models.CharField(max_length=50, null=True, blank=True)
    divorcenoofdaughters =models.CharField(max_length=2, null=True, blank=True)
    divorceDaughterName_1 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterAge_1 = models.CharField(max_length=2, null=True, blank=True)
    divorceDaughterMStatus_1 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterName_2 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterAge_2 = models.CharField(max_length=2, null=True, blank=True)
    divorceDaughterMStatus_2 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterName_3 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterAge_3 = models.CharField(max_length=2, null=True, blank=True)
    divorceDaughterMStatus_3 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterName_4 = models.CharField(max_length=50, null=True, blank=True)
    divorceDaughterAge_4 = models.CharField(max_length=2, null=True, blank=True)
    divorceDaughterMStatus_4 = models.CharField(max_length=50, null=True, blank=True)
    dateOfMarriageWidowed = models.CharField(max_length=50, null=True, blank=True)
    dateOfDeath = models.CharField(max_length=50, null=True, blank=True)
    widowedChildren = models.CharField(max_length=5, null=True, blank=True)
    widowednoofsons = models.CharField(max_length=2, null=True, blank=True)
    widowedSonName_1 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonAge_1 = models.CharField(max_length=2, null=True, blank=True)
    widowedSonMStatus_1 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonName_2 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonAge_2 = models.CharField(max_length=2, null=True, blank=True)
    widowedSonMStatus_2 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonName_3 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonAge_3 = models.CharField(max_length=2, null=True, blank=True)
    widowedSonMStatus_3 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonName_4 = models.CharField(max_length=50, null=True, blank=True)
    widowedSonAge_4 = models.CharField(max_length=2, null=True, blank=True)
    widowedSonMStatus_4 = models.CharField(max_length=50, null=True, blank=True)
    widowednoofdaughters = models.CharField(max_length=2, null=True, blank=True)
    widowedDaughterName_1 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterAge_1 = models.CharField(max_length=2, null=True, blank=True)
    widowedDaughterMStatus_1 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterName_2 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterAge_2 = models.CharField(max_length=2, null=True, blank=True)
    widowedDaughterMStatus_2 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterName_3 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterAge_3 = models.CharField(max_length=2, null=True, blank=True)
    widowedDaughterMStatus_3 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterName_4 = models.CharField(max_length=50, null=True, blank=True)
    widowedDaughterAge_4 = models.CharField(max_length=2, null=True, blank=True)
    widowedDaughterMStatus_4 = models.CharField(max_length=50, null=True, blank=True)
    nameofappfilling = models.CharField(max_length=50, null=True, blank=True)
    nameofappmobile = models.CharField(max_length=50, null=True, blank=True)
    nameofapprelation = models.CharField(max_length=50, null=True, blank=True)
    eating = models.CharField(max_length=20, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    bgroup = models.CharField(max_length=10, null=True, blank=True)
    idProofType = models.CharField(max_length=15, null=True, blank=True)
    idProofNumber = models.CharField(max_length=15, null=True, blank=True)
    mtongue = models.CharField(max_length=15, null=True, blank=True)
    birthtime = models.CharField(max_length=50, null=True, blank=True)
    birthplace = models.CharField(max_length=20, null=True, blank=True)
    healthcondition = models.CharField(max_length=20, null=True, blank=True)
    complexion = models.CharField(max_length=20, null=True, blank=True)
    smoke = models.CharField(max_length=20, null=True, blank=True)
    drink = models.CharField(max_length=20, null=True, blank=True)
    altmobile = models.CharField(max_length=15, db_index=True, blank=True)
    altemail = models.EmailField(max_length=30, db_index=True, blank=True, null=True)
    timetocall = models.CharField(max_length=20, null=True, blank=True)
    hobbies = models.CharField(max_length=150, null=True, blank=True)
    # lang = models.CharField(max_length=150, null=True, blank=True)
    lang = models.JSONField(default=dict)
    source = models.ForeignKey('Masters.Source', related_name='customer', on_delete=models.RESTRICT, null=True, blank=True)
    # religion = models.ForeignKey('Masters.Religion', related_name='customer', on_delete=models.RESTRICT, null=True,blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    caste = models.ForeignKey('Masters.Caste', related_name='customer', on_delete=models.RESTRICT, null=True, blank=True)
    subcaste = models.ForeignKey('Masters.SubCaste', related_name='customer', on_delete=models.RESTRICT, null=True,blank=True)
    ccaste = models.CharField(max_length=5, null=True, blank=True)
    gothram = models.CharField(max_length=20, null=True, blank=True)
    star = models.CharField(max_length=20, null=True, blank=True)
    raasi = models.CharField(max_length=20, null=True, blank=True)
    padam = models.CharField(max_length=20, null=True, blank=True)
    dosham = models.CharField(max_length=20, null=True, blank=True)
    fstatus = models.CharField(max_length=20, null=True, blank=True)
    ftype = models.CharField(max_length=20, null=True, blank=True)
    fathername = models.CharField(max_length=20, null=True, blank=True)
    fatherreligion = models.CharField(max_length=20, null=True, blank=True)
    fathercaste = models.CharField(max_length=20, null=True, blank=True)
    fccaste = models.CharField(max_length=5, null=True, blank=True)
    fIsAlive = models.CharField(max_length=10, null=True, blank=True)
    fatherHealth = models.CharField(max_length=20, null=True, blank=True)
    fatherWSector = models.CharField(max_length=20, null=True, blank=True)
    fatherMobile = models.CharField(max_length=20, null=True, blank=True)
    fatherProfession = models.CharField(max_length=20, null=True, blank=True)
    fatherAddress = models.CharField(max_length=20, null=True, blank=True)
    fatherAnnualIncome = models.CharField(max_length=20, null=True, blank=True)
    fatherProperty = models.CharField(max_length=20, null=True, blank=True)
    fatherPension = models.CharField(max_length=20, null=True, blank=True)
    mothername = models.CharField(max_length=20, null=True, blank=True)
    mothermname = models.CharField(max_length=20, null=True, blank=True)
    motherreligion = models.CharField(max_length=20, null=True, blank=True)
    mothercaste = models.CharField(max_length=20, null=True, blank=True)
    mccaste = models.CharField(max_length=5, null=True, blank=True)
    mIsAlive = models.CharField(max_length=10, null=True, blank=True)
    motherHealth = models.CharField(max_length=20, null=True, blank=True)
    motherWSector = models.CharField(max_length=20, null=True, blank=True)
    motherMobile = models.CharField(max_length=20, null=True, blank=True)
    motherProfession = models.CharField(max_length=20, null=True, blank=True)
    motherAddress = models.CharField(max_length=20, null=True, blank=True)
    motherAnnualIncome = models.CharField(max_length=20, null=True, blank=True)
    motherProperty = models.CharField(max_length=20, null=True, blank=True)
    motherPension = models.CharField(max_length=20, null=True, blank=True)
    fperaddress = models.TextField(blank=True, null=True)
    fpreaddress = models.TextField(blank=True, null=True)
    nobrothers = models.CharField(max_length=5, null=True, blank=True)
    nosisters = models.CharField(max_length=5, null=True, blank=True)
    education = models.ForeignKey('Masters.Education', related_name='customer', on_delete=models.RESTRICT, null=True,blank=True)
    edudetail = models.CharField(max_length=20, null=True, blank=True)
    univ = models.CharField(max_length=20, null=True, blank=True)
    employedin = models.CharField(max_length=20, null=True, blank=True)
    property = models.CharField(max_length=20, null=True, blank=True)

    edesignation= models.CharField(max_length=20, null=True, blank=True)
    eprofession= models.CharField(max_length=20, null=True, blank=True)
    eworkinglocation= models.CharField(max_length=20, null=True, blank=True)
    eindiastate= models.CharField(max_length=20, null=True, blank=True)
    eindiacity= models.CharField(max_length=20, null=True, blank=True)
    eindiaaddress= models.CharField(max_length=150, null=True, blank=True)
    eindiacompanyname= models.CharField(max_length=20, null=True, blank=True)
    eindiaworkingsince= models.CharField(max_length=50, null=True, blank=True)
    eindiatotalexperience= models.CharField(max_length=20, null=True, blank=True)
    eindiapassport= models.CharField(max_length=20, null=True, blank=True)
    eabroadcountry= models.CharField(max_length=20, null=True, blank=True)
    eabroadstate= models.CharField(max_length=20, null=True, blank=True)
    eabroadtype= models.CharField(max_length=20, null=True, blank=True)
    eabroadpassport= models.CharField(max_length=20, null=True, blank=True)
    eabroadvalidfrom= models.CharField(max_length=50, null=True, blank=True)
    eabroadvalidto= models.CharField(max_length=50, null=True, blank=True)
    eabroadworkingcompanyname= models.CharField(max_length=20, null=True, blank=True)
    eabroadaddress= models.CharField(max_length=150, null=True, blank=True)
    ecolleguename= models.CharField(max_length=20, null=True, blank=True)
    ecolleguemobileno= models.CharField(max_length=20, null=True, blank=True)
    eannualincome= models.CharField(max_length=20, null=True, blank=True)
    age = models.CharField(max_length=5, null=True, blank=True)
    lheight = models.CharField(max_length=10, null=True, blank=True)
    lweight = models.CharField(max_length=10, null=True, blank=True)
    lfstatus = models.CharField(max_length=20, null=True, blank=True)
    intercaste = models.CharField(max_length=10, null=True, blank=True)
    interreligion = models.CharField(max_length=10, null=True, blank=True)
    ldosham = models.CharField(max_length=10, null=True, blank=True)
    lpassport = models.CharField(max_length=10, null=True, blank=True)
    leducation = models.JSONField(default=dict)
    lemployedin = models.CharField(max_length=10, null=True, blank=True)
    lcomplexion = models.CharField(max_length=10, null=True, blank=True)
    lsmoke = models.CharField(max_length=10, null=True, blank=True)
    ldrink = models.CharField(max_length=20, null=True, blank=True)
    leating = models.CharField(max_length=20, null=True, blank=True)
    lookmaritalStatus= models.JSONField(default=dict)
    lookcaste = models.JSONField(default=dict)
    lookprofession = models.JSONField(default=dict)
    lookdesignation= models.JSONField(default=dict)
    abroadmobileno = models.CharField(max_length=20, null=True, blank=True)
    fatherabroadmobileno = models.CharField(max_length=20, null=True, blank=True)
    motherabroadmobileno = models.CharField(max_length=20, null=True, blank=True)
    stueducation= models.CharField(max_length=20, null=True, blank=True)
    stueducationyears= models.CharField(max_length=20, null=True, blank=True)
    stustudinglocation= models.CharField(max_length=20, null=True, blank=True)
    stuabroadcountry= models.CharField(max_length=20, null=True, blank=True)
    stuabroadstate= models.CharField(max_length=20, null=True, blank=True)
    stuabroadvisatype= models.CharField(max_length=20, null=True, blank=True)
    stuabroadpassport= models.CharField(max_length=20, null=True, blank=True)
    stuabroadvalidfrom= models.CharField(max_length=50, null=True, blank=True)
    stuabroadvalidto= models.CharField(max_length=50, null=True, blank=True)
    stuindiastate= models.CharField(max_length=20, null=True, blank=True)
    stuindiacity= models.CharField(max_length=20, null=True, blank=True)
    stuemployedin= models.CharField(max_length=20, null=True, blank=True)
    studesignation= models.CharField(max_length=20, null=True, blank=True)
    stuprofession= models.CharField(max_length=20, null=True, blank=True)
    stucompanyname= models.CharField(max_length=20, null=True, blank=True)
    stuannualincome= models.CharField(max_length=20, null=True, blank=True)
    # lookmaritalStatus= models.TextField(blank=True, null=True)
    # lookcaste = models.TextField(blank=True, null=True)
    # lookprofession = models.TextField(blank=True, null=True)
    aboutme = models.TextField(blank=True, null=True)
    referencename = models.CharField(max_length=20, null=True, blank=True)
    referencemobile = models.CharField(max_length=20, null=True, blank=True)
    referenceaddress = models.TextField(blank=True, null=True)
    referencerelation = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, related_name='customer_users', on_delete=models.RESTRICT, null=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customercreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customerupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    photo = models.ImageField(upload_to=customer_photo_upload_to, default='blank_pic', blank=True, null=True)
    idproof = models.ImageField(upload_to=customer_id_upload_to, default='blank_pic', blank=True, null=True)
    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomerUserIds(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    customer_id = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_instance = CustomerUserIds.objects.order_by('-id').first()
            if last_instance:
                last_id = last_instance.id
            else:
                last_id = 0
            new_sequence = last_id + 1
            self.customer_id = f"ANPMG{new_sequence:06d}"  # Formats as ANPMG0001, ANPMG0002, ...
        super().save(*args, **kwargs)


















