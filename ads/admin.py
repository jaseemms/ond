from __future__ import unicode_literals
from django.contrib import admin
from ads.models import Category,SubCategory,Property,PropertyValue,Label,LabelValue,Price

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name','image']
    list_display =['name','image']
    list_filter =['name']
    search_fields = ['name']



class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['category','subcategory_name','image','property_ptr','label','has_price','is_job']
    list_display =['subcategory_name','category','has_price']
    list_filter =['category','subcategory_name','property_ptr','label']
    search_fields = ['category__name','subcategory_name']


class PropertyInline(admin.TabularInline):
    model = PropertyValue
    extra = 0
    fields = ['property_value',]


class PropertyAdmin(admin.ModelAdmin):
    fields = ['property_name','property_symbol']
    list_display =['property_name','property_symbol']
    list_filter =['property_name','property_symbol']
    search_fields = ['property_name','property_symbol']

    inlines = [PropertyInline]


class LabelInline(admin.TabularInline):
    model = LabelValue
    extra = 1
    fields = ['label_value',]
    

class LabelAdmin(admin.ModelAdmin):
    fields = ['label_name']
    list_display =['label_name']
    list_filter =['label_name',]
    search_fields = ['label_name']

    inlines = [LabelInline]

class PriceAdmin(admin.ModelAdmin):
    fields = ['price']
    list_display = ['price']


admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Property,PropertyAdmin)
admin.site.register(Label,LabelAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.site_header = 'OND'
admin.site.index_title = 'OND Administration'
admin.site.site_title = 'OND'





