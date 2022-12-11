from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from django.core.urlresolvers import reverse
from ond.functions import generate_form_errors,superuser
from django.contrib.auth.decorators import login_required,user_passes_test
from ads.forms import AdvertisementForm, FilterAdvertisementForm
from ads.models import Advertisement, LabelValue, PropertyValue, Currency,\
    Category, SubCategory, Price
from users.models import RegionName,CityName
from cities_light.models import Country
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from ond.functions import generate_form_errors,superuser


@login_required(login_url='/login')
def create_advertisement(request):     
    if request.method == "POST":
        form = AdvertisementForm(request.POST,request.FILES)

        if form.is_valid():
            subcategory = form.cleaned_data['subcategory']

            property_value_list = []
            for property_obj in subcategory.property_ptr.all():
                property_value = request.POST.get(property_obj.property_name)
                property_value = PropertyValue.objects.get(pk=property_value)
                property_value_list.append(property_value)

            label_value_list = []
            for label in subcategory.label.all():
                label_value = request.POST.get(label.label_name)
                label_value = LabelValue.objects.get(pk=label_value)
                label_value_list.append(label_value)

            data = form.save(commit=False)
            if request.user.is_authenticated:
                data.user = request.user

            data.save()
            data.property_value.set(property_value_list)
            data.label_value.set(label_value_list)
            
            request.session['success'] = True
            return HttpResponseRedirect(reverse('ads:create_advertisement'))
        
        else:
            context = {
	            "form" : form,
	            "title" : "Create Advertisement",
	        }          

    else: 
        form = AdvertisementForm()
        form.fields['region'].queryset = form.fields['region'].queryset.none()
        form.fields['city'].queryset = form.fields['city'].queryset.none()
        form.fields['subcategory'].queryset = form.fields['subcategory'].queryset.none()
        form.fields['currency'].queryset = form.fields['currency'].queryset.none()

        try:
            success = request.session['success']
            del request.session['success']
        except:
            success = False
        
        context = {
            "form" : form,
            "success": success,
            "title" : "Create Advertisement",
        }
    return render(request, 'ads/create_advertisement.html', context)


@login_required(login_url='/login')
def edit_advertisement(request,pk):
    instance = get_object_or_404(Advertisement.objects.filter(pk=pk))

    if (request.user == instance.user) or request.user.is_superuser :
        pass
    else:
        raise PermissionDenied
    
    if request.method == "POST":
        form = AdvertisementForm(request.POST,request.FILES,instance=instance)
        
        if form.is_valid(): 
            subcategory = form.cleaned_data['subcategory']

            property_value_list = []
            for property_obj in subcategory.property_ptr.all():
                property_value = request.POST.get(property_obj.property_name)
                property_value = PropertyValue.objects.get(pk=property_value)
                property_value_list.append(property_value)

            label_value_list = []
            for label in subcategory.label.all():
                label_value = request.POST.get(label.label_name)
                label_value = LabelValue.objects.get(pk=label_value)
                label_value_list.append(label_value)


            data = form.save(commit=False)
            if request.user.is_authenticated:
                data.user = request.user
            data.save()
            data.property_value.set(property_value_list)
            data.label_value.set(label_value_list)
            
            request.session['success'] = True
            return HttpResponseRedirect(reverse('ads:view_advertisement', kwargs = {'pk' : data.pk}))
        else:
            form.fields['region'].queryset = form.fields['region'].queryset.filter(country_id=instance.country.pk)
            form.fields['city'].queryset = form.fields['city'].queryset.filter(region_id=instance.region.pk)
            form.fields['subcategory'].queryset = form.fields['subcategory'].queryset.filter(category_id=instance.category.pk)
            currency = form.fields['currency'].queryset.filter(country_id=instance.country.pk)
            if not currency.exists():
                currency = form.fields['currency'].queryset.filter(country_id='234')
            form.fields['currency'].queryset = currency
            context = {
                "form" : form,
                "title" : "Edit Advertisement",
            }          
            
    else: 
        form = AdvertisementForm(instance=instance)
        form.fields['region'].queryset = form.fields['region'].queryset.filter(country_id=instance.country.pk)
        form.fields['city'].queryset = form.fields['city'].queryset.filter(region_id=instance.region.pk)
        form.fields['subcategory'].queryset = form.fields['subcategory'].queryset.filter(category_id=instance.category.pk)
        currency = form.fields['currency'].queryset.filter(country_id=instance.country.pk)
        if not currency.exists():
            currency = form.fields['currency'].queryset.filter(country_id='234')
        form.fields['currency'].queryset = currency

        try:
            success = request.session['success']
            del request.session['success']
        except:
            success = False
        
        context = {
            "form" : form,
            "title" : "Edit Advertisement : " + instance.name,
            "instance" : instance,
            "success" : success
        }
    return render(request, 'ads/create_advertisement.html', context)

      

def view_advertisements(request):

    subcategory_obj = None
    property_value_list = []
    label_value_list = []
    prices = None
    price_id = None
    category_list_items = None
    subcategory_list_items = None
    category_obj = None

    if request.method == 'POST':
        country_id = request.POST.get('country')
        region_id = request.POST.get('region')
        city_id =  request.POST.get('city')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        price_id = request.POST.get('price','')
        list_option = request.POST.get('list_option')
        search = request.POST.get('search')

        form = FilterAdvertisementForm(request.POST)
        
        if list_option == 'true':
            category_list_items = Category.objects.all()
            subcategory_list_items=SubCategory.objects.filter(category_id=category_id)
            instances = Advertisement.objects.none()
        else:
            if request.user.is_superuser:
                instances = Advertisement.objects.all()
            else:
                instances = Advertisement.objects.filter(active=True)
        if search:
            instances = instances.filter(Q(title__icontains=search)|Q(description__icontains=search)|
                Q(id__icontains=search))

        if country_id != '':
            form.fields['region'].queryset = RegionName.objects.filter(country_id=country_id)
            instances = instances.filter(country_id=country_id)
        else:
            form.fields['region'].queryset = RegionName.objects.none()

        if region_id != '':
            form.fields['city'].queryset = CityName.objects.filter(region_id=region_id)
            instances = instances.filter(region_id=region_id)
        else:
            form.fields['city'].queryset = CityName.objects.none()

        if category_id != '':
            form.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            instances = instances.filter(category_id=category_id)
            category_obj = Category.objects.get(pk=category_id)
        else:
            form.fields['subcategory'].queryset = SubCategory.objects.none()

        if price_id !='':
            price = Price.objects.get(pk=price_id)
            if price == Price.objects.first():
                instances = instances.filter(price__lt=price.price)
            elif price == Price.objects.last():
                instances = instances.filter(price__gte=price.price)
            else:
               instances = instances.filter(price__lt=price.price)
               pre_price_obj = Price.objects.filter(price__lt=price.price).last()
               if pre_price_obj:
                    instances = instances.filter(price__gte=pre_price_obj.price)

        if subcategory_id !='':
            subcategory_obj = SubCategory.objects.get(id=subcategory_id)
            instances = instances.filter(subcategory_id=subcategory_id)

            for property_obj in subcategory_obj.property_ptr.all():
                property_value = request.POST.get(property_obj.property_name)
                if property_value:
                    property_value_obj = PropertyValue.objects.get(pk=property_value)
                    if property_value_obj is PropertyValue.objects.last():
                        instances = instances.filter(property_value__property_value__gte=property_value_obj.property_value)
                    elif property_value_obj is PropertyValue.objects.first():
                        instances = instances.filter(property_value__property_value__lt=property_value_obj.property_value)
                    else:
                        instances = instances.filter(property_value__property_value__lt=property_value_obj.property_value)
                        pre_value_obj = PropertyValue.objects.filter(property_value__lt=
                            property_value_obj.property_value).last()
                        if pre_value_obj:
                            instances = instances.filter(property_value__property_value__gte=pre_value_obj.property_value)

                    property_value_list.append(property_value)

            for label in subcategory_obj.label.all():
                label_value = request.POST.get(label.label_name)
                if label_value:
                    instances = instances.filter(label_value=label_value)
                    label_value_list.append(label_value)

            if subcategory_obj.has_price or subcategory_obj.is_job:
                prices = Price.objects.all()

        paginator = Paginator(instances,100)

        page = request.POST.get('page')

        try:
            instances = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            instances = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            instances = paginator.page(paginator.num_pages)


    else:
        form = FilterAdvertisementForm()
        form.fields['region'].queryset = RegionName.objects.none()
        form.fields['city'].queryset = CityName.objects.none()
        form.fields['subcategory'].queryset = SubCategory.objects.none()
        instances = Advertisement.objects.none()
        category_list_items = Category.objects.all()


    title = "Home"

    try:
        message = request.session['message']
        del request.session['message']
    except:
        message = None

    context = {
        'title' : title,
        'form' : form,
        'subcategory_obj': subcategory_obj,
        "instances" : instances,
        "message" : message,
        "label_value_list": label_value_list,
        "property_value_list":property_value_list,
        "prices": prices,
        "price_id": price_id,
        "category_list_items":category_list_items,
        "subcategory_list_items":subcategory_list_items,
        "category_obj": category_obj

    }
    return render(request,'ads/view_advertisements.html',context) 



@login_required(login_url='/login')
def my_advertisements(request):
    instances = Advertisement.objects.filter(user=request.user)

    paginator = Paginator(instances,100)

    page = request.GET.get('page')

    try:
        instances = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        instances = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        instances = paginator.page(paginator.num_pages)

    context ={
        'instances':instances,
        'title': 'My Advertisement'
    }
    return render(request,'ads/my_advertisements.html',context)


def view_advertisement(request,pk):
    instance = get_object_or_404(Advertisement.objects.filter(pk=pk))

    context = {
        "instance" : instance,
        "title" : str(instance.title),
    }
    return render(request,'ads/view_advertisement.html',context)


@login_required(login_url='/login')
def delete_advertisement(request,pk):
    instance = get_object_or_404(Advertisement.objects.filter(pk=pk))

    if (request.user == instance.user) or request.user.is_superuser :
        pass
    else:
        raise PermissionDenied

    instance.delete()   
    request.session['message'] = 'Successfully Deleted'
    return HttpResponseRedirect(reverse('ads:view_advertisements'))


@login_required(login_url='/login')
@user_passes_test(superuser)
def ad_activate(request,pk):
    ad = get_object_or_404(Advertisement.objects.filter(pk=pk))

    if ad.active:
        ad.active = False
    else:
        ad.active = True

    ad.save()
    return HttpResponseRedirect(reverse('ads:view_advertisement',kwargs={'pk':pk}))


@login_required(login_url='/login')
@user_passes_test(superuser)
def premium(request,pk):
    ad = get_object_or_404(Advertisement.objects.filter(pk=pk))

    if ad.premium:
        ad.premium = False
    else:
        ad.premium = True

    ad.save()
    return HttpResponseRedirect(reverse('ads:view_advertisement',kwargs={'pk':pk}))

def get_ajax(request):

    id_value = request.GET.get('id')
    selector = request.GET.get('selector')
    instance = request.GET.get('instance','')

    if not instance == '':
        instance = get_object_or_404(Advertisement.objects.filter(pk=instance))
    else:
        instance = None
    
    currency_list = []
    value_list = []
    label_list = []
    property_list = []
    has_price = "False"
    is_job = "False"

    if selector == 'id_country':

        if id_value:
            value_list = list(RegionName.objects.filter(country_id=id_value).values_list('id','name_ascii'))
            currency_list = list(Currency.objects.filter(country_id=id_value).values_list('id','ISO_Code'))
            if currency_list == []:
                currency_list = list(Currency.objects.filter(country_id='234').values_list('id','ISO_Code'))

    if selector == 'id_region':
        if id_value:
            value_list = list(CityName.objects.filter(region_id=id_value).values_list('id','name_ascii'))

    if selector == 'id_category':
        if id_value:
            values = SubCategory.objects.filter(category_id=id_value)
            value_list =[]
            for i,value in enumerate(values):
                value_list.append((str(value.id),value.subcategory_name))

    if selector == 'id_subcategory':
        if id_value:
            subcategory = get_object_or_404(SubCategory,pk=id_value)
            if subcategory.has_price == True:
                has_price = "True"
            if subcategory.is_job == True:
                is_job = "True"
            labels = subcategory.label.all()
            label_list =[]
            for label in labels:
                label_values = label.labelvalue_set.all()
                label_value_list = []
                for label_value in label_values:
                    if instance:
                        if instance.label_value.filter(pk=label_value.id).exists():
                            label_value_list.append([str(label_value.id),label_value.label_value,'selected'])
                        else:
                            label_value_list.append([str(label_value.id),label_value.label_value])
                    else:
                        label_value_list.append([str(label_value.id),label_value.label_value])

                label_list.append([label.label_name,label_value_list])

            properties = subcategory.property_ptr.all()
            property_list =[]
            for property_obj in properties:
                property_values = property_obj.propertyvalue_set.all()
                property_value_list = []
                for property_value in property_values:
                    if instance:
                        if instance.property_value.filter(pk=property_value.id).exists():
                            property_value_list.append([str(property_value.id),
                                str(property_value.property_value),'selected'])
                        else:
                            property_value_list.append([str(property_value.id),
                                str(property_value.property_value)])
                    else:
                        property_value_list.append([str(property_value.id),
                            str(property_value.property_value)])

                property_list.append([property_obj.property_name,property_obj.property_symbol,
                    property_value_list])

    response_data = {
        'value_list': value_list,
        'currency_list':currency_list,
        'label_list': label_list,
        'property_list': property_list,
        'has_price':has_price,
        'is_job':is_job
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')