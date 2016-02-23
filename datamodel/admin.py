from django.contrib import admin
from datamodel.models import SensorMetaData
from datamodel.models import SensorLocation
from datamodel.models import Location
from datamodel.models import Address

#display in nice form in admin
class SensorMetaDataAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "type", "value", "timestamp", "updated"]

	class Meta1:
		model = SensorMetaData

class SensorLocationAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "address", "floor", "room", "wall", "aes_key", "timestamp", "updated"]

	class Meta2:
		model = SensorLocation
		
class LocationAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "location", "location_decription", "latlong", "address", "floor", "room", "wall", "timestamp", "updated"]

	class Meta2:
		model = SensorLocation
		
class AddressAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "address", "post_code", "timestamp", "updated"]

	class Meta2:
		model = SensorLocation

admin.site.register(SensorMetaData, SensorMetaDataAdmin)
admin.site.register(SensorLocation, SensorLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Address, AddressAdmin)

# Register your models here.
