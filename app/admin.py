from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class warehouseuserAdmin(ImportExportModelAdmin):
    pass
admin.site.register(warehouseuser, warehouseuserAdmin)

class GeneralAdmin(ImportExportModelAdmin):
    pass
admin.site.register(General, GeneralAdmin)

class GstdetailsAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Gstdetails, GstdetailsAdmin)

class AdditemAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Additem, AdditemAdmin)

class InventoryAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Inventory, InventoryAdmin)
