from django.urls import include, path

from . import views

urlpatterns = [

    # path('countryadd/', views.CountryRegisterView.as_view(), name="countryadd"),
    # path('countrylist/', views.CountryRegisterView.as_view(), name="countrylist"),
    # path('countrylist/<int:id>', views.CountryRegisterView.as_view(), name="countrylist"),
    # path('country/update', views.CountryRegisterView.as_view(), name="countryupdatedelete"),
    # path('countrydelete/<int:id>', views.CountryRegisterView.as_view(), name="countrylist"),

    path('country/', views.CountryRegisterView.as_view(), name="countryAddUpdateList"),
    path('country/<int:id>', views.CountryRegisterView.as_view(), name="countryListDelete"),
    path('countries/', views.CountryView.as_view(), name="countryList"),

    path('state/', views.StateRegisterView.as_view(), name="stateAddUpdateList"),
    path('state/<int:id>', views.StateRegisterView.as_view(), name="stateListDelete"),
    path('statecountries/<int:id>', views.StateCountriesView.as_view(), name="stateListCountries"),
    path('findstates/<str:name>', views.StatesView.as_view(), name="statesListIndia"),

    path('district/', views.DistrictRegisterView.as_view(), name="districtAddUpdateList"),
    path('district/<int:id>', views.DistrictRegisterView.as_view(), name="districtListDelete"),
    path('districtstatecountries/<int:id>', views.DistrictStateCountriesView.as_view(), name="districtstateListCountries"),

    path('city/', views.CityRegisterView.as_view(), name="cityAddUpdateList"),
    path('city/<int:id>', views.CityRegisterView.as_view(), name="cityListDelete"),
    path('citydistrictstatecountries/<int:id>', views.CityDistrictStateCountriesView.as_view(),name="citydistrictstateListCountries"),
    path('findcities/<str:name>', views.CitiesView.as_view(), name="citiesListIndia"),

    path('branch/', views.BranchRegisterView.as_view(), name="branchAddUpdateList"),
    path('branch/<int:id>', views.BranchRegisterView.as_view(), name="branchListDelete"),

    path('religion/', views.ReligionRegisterView.as_view(), name="religionAddUpdateList"),
    path('religion/<int:id>', views.ReligionRegisterView.as_view(), name="religionListDelete"),

    path('caste/', views.CasteRegisterView.as_view(), name="casteAddUpdateList"),
    path('caste/<int:id>', views.CasteRegisterView.as_view(), name="casteListDelete"),
    path('castesreligion/<str:name>', views.CasteReligionView.as_view(), name="castereligionsList"),

    path('subcaste/', views.SubCasteRegisterView.as_view(), name="subcasteAddUpdateList"),
    path('subcaste/<int:id>', views.SubCasteRegisterView.as_view(), name="subcasteListDelete"),
    path('subcastecastes/<int:id>', views.SubCasteCasteView.as_view(), name="subcasteListCastes"),

    path('occupation/', views.OccupationRegisterView.as_view(), name="occupationAddUpdateList"),
    path('occupation/<int:id>', views.OccupationRegisterView.as_view(), name="occupationListDelete"),

    path('education/', views.EducationRegisterView.as_view(), name="educationAddUpdateList"),
    path('education/<int:id>', views.EducationRegisterView.as_view(), name="educationListDelete"),

    path('language/', views.LanguageRegisterView.as_view(), name="languageAddUpdateList"),
    path('language/<int:id>', views.LanguageRegisterView.as_view(), name="languageListDelete"),

    path('designation/', views.DesignationRegisterView.as_view(), name="designationAddUpdateList"),
    path('designation/<int:id>', views.DesignationRegisterView.as_view(), name="designationListDelete"),
    path('designationprof/<str:name>', views.DesignationProfView.as_view(), name="designationprofList"),

    path('university/', views.UniversityRegisterView.as_view(), name="universityAddUpdateList"),
    path('university/<int:id>', views.UniversityRegisterView.as_view(), name="universityListDelete"),

    path('visa/', views.VisaRegisterView.as_view(), name="visaAddUpdateList"),
    path('visa/<int:id>', views.VisaRegisterView.as_view(), name="visaListDelete"),

    path('source/', views.SourceRegisterView.as_view(), name="sourcecAddUpdateList"),
    path('source/<int:id>', views.SourceRegisterView.as_view(), name="sourceListDelete"),

    path('membership/', views.MemberShipRegisterView.as_view(), name="membershipAddUpdateList"),
    path('membership/<int:id>', views.MemberShipRegisterView.as_view(), name="membershipListDelete"),
    path('membership/<int:id>/<str:param1>', views.MemberShipRegisterView.as_view(), name="allStatusChange"),

    path('staff/', views.StaffRegisterView.as_view(), name="staffAddUpdateList"),
    path('staff/<int:id>', views.StaffRegisterView.as_view(), name="staffListDelete"),
    path('staffUser/<int:id>', views.StaffUserView.as_view(), name="staffUser"),

    path('agent/', views.AgentRegisterView.as_view(), name="agentAddUpdateList"),
    path('agent/<int:id>', views.AgentRegisterView.as_view(), name="agentListDelete"),
    path('agentUser/<int:id>', views.AgentUserView.as_view(), name="agentUser"),

    path('customer/', views.CustomerRegisterView.as_view(), name="customerAddUpdateList"),
    path('customerUpdate/<int:id>', views.CustomerUserView.as_view(), name="customerUpdate"),
    path('customerUser/<int:id>', views.CustomerUserView.as_view(), name="customerUser"),
    path('customerUser/', views.CustomerUserView.as_view(), name="customerUserAll"),
    path('customerAdd/', views.LoginCustomerRegisterView.as_view(), name="customerAddUpdateList"),
    path('getCustomer/<int:id>', views.LoginCustomerRegisterView.as_view(), name="getCustomer"),
    path('customerUserLogin/<int:id>', views.CustomerUserViewBasedLogin.as_view(), name="customerUser"),
    # path('customer/<int:id>', views.CustomerRegisterView.as_view(), name="customerListDelete"),
    # path('customerUser/<int:id>', views.CustomerUserView.as_view(), name="customerUser"),

]

