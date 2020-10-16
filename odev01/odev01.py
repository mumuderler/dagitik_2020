import sys

#print ("this script has the name "+str(sys.argv[0]))

dict = {}

for i in range(int(sys.argv[1])):

	print ("ID,Isim,Soyisim,Yas")
	x = input("Bilgileri sirasiyla giriniz: ")
	data = x.split()
	id = data[0]
	isim = data[1:-2]
	stringisim = "".join(isim)
	soyisim = data[-2]
	yas = data[-1]
#print (data)
	if id.isdigit() and stringisim.isalpha() and soyisim.isalpha() and yas.isdigit():
		thistuple = (stringisim,soyisim,yas)
		dict[id] = thistuple[0],thistuple[1],thistuple[2]
	else:
		print("Yanlis giris yapildi cikis yapılıyor... Programi tekrar calistiriniz")
		sys.exit()
#print (dict.keys())

key = (input("Aranacak ID numarasini giriniz: "))
if key in dict:
	print("Aranilan ID'ye ait kelime bulundu!:" + str(dict[key]))
else:
	print("Aranan kelime bulunamadi")

sorted(dict.keys())

print ("--- Veri tabaninda bulunan veriler ---")
for key in sorted(dict.keys()):
	print (key , "::" , dict[key])
