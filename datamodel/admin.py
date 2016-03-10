from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datamodel.models import Sensor
from datamodel.models import SensorMetadata
from datamodel.models import SensorLocation
from datamodel.models import Location
from datamodel.models import Address
from datamodel.models import Sensor
from datamodel.models import Measurement
from datamodel.models import Reading
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

class SensorAdmin(admin.ModelAdmin):
	list_display = ["node_id", "created", "updated"]

	class Meta:
		model = Sensor

class SensorMetadataAdmin(admin.ModelAdmin):
	list_display = ["sensor_ref", "sensor_type", "value", "unit","created", "updated"]

	class Meta1:
		model = SensorMetadata

class SensorLocationAdmin(admin.ModelAdmin):
	list_display = ["sensor_ref", "location_ref", "aes_key", "created", "updated", "last_measurement", "finish"]
	list_filter = (SensorLocationListFilter,)
	
	class Meta2:
		model = SensorLocation
		
class LocationAdmin(admin.ModelAdmin):
	list_display = ["parent_ref","description", "address_ref", "created","updated"]

	class Meta3:
		model = Location
		
class AddressAdmin(admin.ModelAdmin):
	list_display = [ "address", "postcode", "created", "updated"]

	class Metai4:
		model = Address

class MeasurementAdmin(admin.ModelAdmin):
	list_display = ["sensor_location_ref","message_counter", "created","packet_timestamp" ]

	class Metai5:
		model = Measurement

class ReadingAdmin(admin.ModelAdmin):
	list_display = ["measurement_ref","measurement_type","value","value_integer","value_float", "unit", "created","updated" ]

	class Metai6:
		model = Measurement

admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorMetadata, SensorMetadataAdmin)
admin.site.register(SensorLocation, SensorLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Reading, ReadingAdmin)

# list filter support:


# Register your models here.
