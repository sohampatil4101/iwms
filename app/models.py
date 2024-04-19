from django.db import models

# Create your models here.

def upload_path(instance, filename):
    return '/'.join(['images', str(instance.id), filename])


class warehouseuser(models.Model):
    companyname = models.TextField()
    fullname = models.TextField()
    email = models.TextField()
    password = models.TextField()
    phone_no = models.IntegerField()
    country = models.TextField()
    state = models.TextField()

    def __str__(self):
        return f"{self.companyname}"
    
class Gstdetails(models.Model):
    user = models.ForeignKey(warehouseuser,on_delete=models.CASCADE)
    isbuisness_register_gst = models.BooleanField(default=False,null=False)
    gstin = models.IntegerField(null=True, blank=True)
    gstdate = models.TextField(null=True, blank=True)
    compostion_scheme = models.BooleanField(default=False,null=False)
    compostion_scheme_percent = models.TextField(null=True, blank=True)
    import_export = models.BooleanField(default=False,null=False)
    customduty_tracking = models.TextField(null=True, blank=True)
    digital_service = models.BooleanField(default=False,null=False)
    def __str__(self):
        return f"{self.isbuisness_register_gst}"
    
class Additem(models.Model):
    user = models.ForeignKey(warehouseuser,on_delete=models.CASCADE)
    item_type = models.TextField()
    item_image = models.ImageField(upload_to=upload_path)
    item_name = models.TextField()  
    item_sku = models.TextField()
    item_unit = models.TextField()
    item_sac = models.TextField(null= True, blank=True)
    returnable_item = models.BooleanField(default=False,null=False)
    HSN_code = models.TextField(null= True, blank=True)
    taxable = models.BooleanField(default=False,null=False)
    exemptional_reason = models.TextField(null= True, blank=True)
    sales_info = models.BooleanField(default=False,null=False)
    selling_price = models.IntegerField(null= True, blank= True)
    sales_account = models.TextField(null= True, blank= True)
    sales_description = models.TextField(null= True, blank= True)
    purchase_info = models.BooleanField(default=False,null=False)
    cost_price = models.IntegerField(null= True, blank= True)
    purchase_account = models.TextField(null= True, blank= True)
    purchase_description = models.TextField(null= True, blank= True)
    intrastate_tax = models.TextField()
    interstate_tax = models.TextField()
    track_inventory = models.BooleanField(default=False,null=False)
    inventory_account = models.TextField(null= True, blank= True)
    opening_stock = models.TextField(null= True, blank= True)
    opening_stock_rate_per_unit = models.TextField(null= True, blank= True)
    recorder_level = models.TextField(null= True, blank= True)
    preferred_vendor = models.TextField(null= True, blank= True)
    dimension = models.TextField(null= True, blank= True)
    weight = models.TextField(null= True, blank= True)
    manifacturer = models.TextField(null= True, blank= True)
    brand = models.TextField(null= True, blank= True)
    upc = models.TextField(null= True, blank= True)
    mnp = models.TextField(null= True, blank= True)
    ean = models.TextField(null= True, blank= True)
    isbn = models.TextField(null= True, blank= True)

    
    def __str__(self):
        return f"{self.item_type}"


class Inventory(models.Model):
    user = models.ForeignKey(warehouseuser,on_delete=models.CASCADE)
    inventory_location = models.TextField()
    fiscal_year = models.TextField()
    currency = models.TextField()
    language = models.TextField()
    inventory_startdate = models.TextField()
    


class General(models.Model):
    user = models.ForeignKey(warehouseuser,on_delete=models.CASCADE)
    name = models.TextField()
    image = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return f"{self.name}"