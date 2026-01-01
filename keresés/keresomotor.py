import wikipedia
import pyttsx3


nyelv = 'hu'
wikipedia.set_lang(nyelv)
adatok = []


search = input('\nMiről szeretnél információt: ')
while search == '':
    print("Nem adtál meg keresési kifejezést.")
    search = input('\nMiről szeretnél információt: ')

def info(search, id=id):

    print(f'\nTéma keresése... {search}')

    eredmeny = wikipedia.summary(search, sentences=4)


    print("Találat: ")
    print(eredmeny)      

    try:
        hang = pyttsx3.init()
        hang_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Katalin-Beta"
        hang.setProperty('voice', hang_id)
        hang.setProperty('rate', 150)
        hang.say(eredmeny)
        hang.runAndWait()
    except Exception as e:
        print(f"Hiba történt: {e}")

    azonosító = input("Kérlek, adj meg egy egyedi azonosító számot: ")
    with open('adatok.txt', 'a', encoding='utf-8') as adatgyűjtemény:
        adatgyűjtemény.write(f'{search} = [ID: {azonosító}, Modul: {search}, Result: {eredmeny}]\n')
        

vége = 'kilépés'

while search != vége.lower():
    info(search)
    search = input('\nMiről szeretnél információt: ')
if search == 'kilépés':    
    with open('adatok.txt', 'r', encoding='utf-8') as adatgyűjtemény:
        tartalom = adatgyűjtemény.readlines()
        print("\nMentett adatok:")
        print(tartalom)
        
    adatgyűjtemény.close()
    print("Viszlát!")
    exit()