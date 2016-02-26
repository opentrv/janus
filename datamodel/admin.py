from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datamodel.models import SensorMetaData
from datamodel.models import SensorLocation
from datamodel.models import Location
from datamodel.models import Address
from datamodel.datamodelquery import SensorLocationQuery

class SensorLocationListFilter(admin.SimpleListFilter):
    title = _('Sensor Location Filter')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'location'

    def lookups(self, request, model_admin):

        return (
            ('unassigned', _('unassigned sensors')),
            ('assigned', _('assigned sensors')),
			('keyunassigned', _('key unassigned sensors')),
			('keyassigned', _('key assigned sensors')),)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either 'unassigned' or 'assigned')
        # to decide how to filter the queryset.
        if self.value() == 'unassigned':
            return SensorLocationQuery().get_unassigned_sensors()
        if self.value() == 'assigned':
            return SensorLocationQuery().get_assigned_sensors()
        if self.value() == 'keyunassigned':
            return SensorLocationQuery().get_key_unassigned_sensors()
        if self.value() == 'keyassigned':
            return SensorLocationQuery().get_key_assigned_sensors()

#display in nice form in admin
class SensorMetaDataAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "type", "value", "timestamp", "updated"]

	class Meta1:
		model = SensorMetaData

class SensorLocationAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "sensor_id", "sensor_ref", "sensor_location", "aes_key", "timestamp_start", "timestamp_finish"]
	list_filter = (SensorLocationListFilter,)
	
	class Meta2:
		model = SensorLocation
		
class LocationAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "location", "location_decription", "latlong", "address", "floor", "room", "wall", "timestamp", "updated"]

	class Meta:
		model = Location
		
class AddressAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "address", "post_code", "timestamp", "updated"]

	class Meta:
		model = Address

admin.site.register(SensorMetaData, SensorMetaDataAdmin)
admin.site.register(SensorLocation, SensorLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Address, AddressAdmin)

# list filter support:


# Register your models here.
