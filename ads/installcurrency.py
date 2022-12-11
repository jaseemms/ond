from cities_light.models import Country, Region, City
import os
from django.db.models import Q
from ads.models import Currency

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def installcurrency():
	f = open(os.path.join(BASE_DIR, "ads/country.txt"),"w+")
	fr = open(os.path.join(BASE_DIR, "ads/money.txt"),"r")
	if fr.mode == 'r':
		fr = fr.readlines()
	else:
		fr = None

	f.write("name not exist in database\n")
	for fline in fr:
		country = Country.objects.filter(Q(name=fline[:-1].split("\t")[0])|Q(name_ascii=fline[:-1].split("\t")[0]))
		if not country.exists():
			f.write("%s\n" %fline[:-1].split("\t")[0])
				
	f.write("\nname not exit in text file \n\n")

	countries = Country.objects.all()

	for country in countries:
		exist = False
		for fline in fr:
			name = str(fline[:-1].split("\t")[0])
			if str(country.name_ascii) == name or str(country.name) == name:
				exist = True
				code = str(fline[:-1].split("\t")[3])
				if code == "(none)":
					code = None
				if not Currency.objects.filter(country=country,name=name,ISO_Code=code).exists():
					Currency.objects.create(country=country,name=name,ISO_Code=code)
		if exist == False:
			f.write("%s - %s\n" %(country.name_ascii,country.name))


		
		 
