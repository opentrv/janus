from django.contrib import admin
from datamodel.models import SensorMetaData
from datamodel.models import SensorLocation


#display in nice form in admin
class SensorMetaDataAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "type", "value", "timestamp", "updated"]

	class Meta1:
		model = SensorMetaData




class SensorLocationAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "address", "floor", "room", "wall", "timestamp", "updated"]

	class Meta2:
		model = SensorLocation
		

admin.site.register(SensorMetaData, SensorMetaDataAdmin)
admin.site.register(SensorLocation, SensorLocationAdmin)

# Register your models here.
