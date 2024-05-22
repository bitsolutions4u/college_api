from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from Masters.models import State, District, City, Country, Branch, Religion, Caste, SubCaste, Occupation, Education, \
	Language, Source, MemberShip, Agent, Customer, Designation, University, Visa
from Users.serializers import UserCommonSerializer
from Users.models import User
from Masters.models import Staff
from django.contrib.auth.models import AnonymousUser
class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = '__all__'
		# read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class StateSerializer(serializers.ModelSerializer):
	country_name = ReadOnlyField(source='country.name')
	class Meta:
		model = State
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class DistrictSerializer(serializers.ModelSerializer):
	country_name = ReadOnlyField(source='country.name')
	state_name = ReadOnlyField(source='state.name')
	class Meta:
		model = District
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class CitySerializer(serializers.ModelSerializer):
	country_name = ReadOnlyField(source='country.name')
	state_name = ReadOnlyField(source='state.name')
	district_name = ReadOnlyField(source='district.name')
	class Meta:
		model = City
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class BranchSerializer(serializers.ModelSerializer):
	user = UserCommonSerializer()
	class Meta:
		model = Branch
		fields = '__all__'
	def create(self,validate_data):
		user_data = validate_data.pop('user')
		user = User.objects.create(**user_data)
		branch = Branch.objects.create(user=user,**validate_data)
		return branch

	def update(self,validate_data):
		user_data = validate_data.pop('user')
		user=User.objects.update(**user_data)
		branch=Branch.objects.update(user=user,**validate_data)
		return branch

class ReligionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Religion
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class CasteSerializer(serializers.ModelSerializer):
	religion_name = ReadOnlyField(source='religion.name')
	class Meta:
		model = Caste
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class SubCasteSerializer(serializers.ModelSerializer):
	caste_name = ReadOnlyField(source='caste.name')
	class Meta:
		model = SubCaste
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class OccupationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Occupation
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class EducationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Education
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class LanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Language
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class DesignationSerializer(serializers.ModelSerializer):
	profession_name = ReadOnlyField(source='occupation.name')
	class Meta:
		model = Designation
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class UniversitySerializer(serializers.ModelSerializer):
	class Meta:
		model = University
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class VisaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Visa
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs


class SourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Source
		fields = '__all__'
		read_only_fields = ['user']

	def validate(self, attrs):
		attrs['createdby'] = self.context['request'].user
		return attrs

class MemberShipSerializer(serializers.ModelSerializer):
	class Meta:
		model = MemberShip
		fields = '__all__'
		# read_only_fields = ['user']

	# def validate(self, attrs):
	# 	attrs['createdby'] = self.context['request'].user
	# 	return attrs

class StaffSerializer(serializers.ModelSerializer):
	user = UserCommonSerializer()
	education_name = ReadOnlyField(source='education.name')
	source_name = ReadOnlyField(source='source.name')
	branch_name = ReadOnlyField(source='branch.name')
	religion_name = ReadOnlyField(source='religion.name')
	caste_name = ReadOnlyField(source='caste.name')
	class Meta:
		model = Staff
		fields = '__all__'

	def create(self,validate_data):
		user_data = validate_data.pop('user')
		user = User.objects.create(**user_data)
		staff = Staff.objects.create(user=user,**validate_data)
		return staff

class AgentSerializer(serializers.ModelSerializer):
	user = UserCommonSerializer()
	education_name = ReadOnlyField(source='education.name')
	class Meta:
		model = Agent
		fields = '__all__'

	def create(self,validate_data):
		user_data = validate_data.pop('user')
		user = User.objects.create(**user_data)
		agent = Agent.objects.create(user=user,**validate_data)
		return agent

class CustomerSerializer(serializers.ModelSerializer):
	user = UserCommonSerializer()
	createdby_id = serializers.ReadOnlyField(source='createdby.id')
	createdby_username = serializers.ReadOnlyField(source='createdby.username')
	education_name = ReadOnlyField(source='education.name')
	source_name = ReadOnlyField(source='source.name')
	caste_name = ReadOnlyField(source='caste.name')
	# createdby_name = ReadOnlyField(source='user.username')
	class Meta:
		model = Customer
		fields = '__all__'

	def create(self,validate_data):
		user_data = validate_data.pop('user')
		user_data['createdby'] = None
		user_data['modifiedby'] = None
		user = User.objects.create(**user_data)
		customer = Customer.objects.create(user=user,**validate_data)
		return customer

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', None)
		if user_data:
			user_serializer = self.fields['user']
			user_instance = instance.user
			user_serializer.update(user_instance, user_data)

		return super().update(instance, validated_data)