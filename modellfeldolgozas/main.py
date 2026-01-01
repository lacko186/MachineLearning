from dataset import Aibo, Edison, CodeandGorobotegér, Robotkar, Vr, LegoSpikePrime, LegoEssential, Microbit, RVRSphero, Spherookoslabda, Nev
from dataset import Bemutatkozás
import time
import sys
import pyttsx3
import threading
import os
from gtts import gTTS
from ollama import chat
from ollama import ChatResponse


def hang(szoveg):
    try:
        python_hang = pyttsx3.init()
        python_hang_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Katalin-Beta"
        python_hang.setProperty('voice', python_hang_id)
        python_hang.setProperty('rate', 150)
        python_hang.say(szoveg)
        python_hang.runAndWait()
    except Exception as e:
        print(f" Hang történt: {e}")
      
        try:
            python_hang = pyttsx3.init()
            python_hang.setProperty('rate', 150)
            python_hang.say(szoveg)
            python_hang.runAndWait()
        except:
            print("sikertelen")


def pontos_kereses(product_name):
    products = {
        'Aibo': Aibo,
        'Edison': Edison,
        'CodeandGorobotegér': CodeandGorobotegér,
        'Robotkar': Robotkar,
        'Vr': Vr,
        'LegoSpikePrime': LegoSpikePrime,
        'LegoEssential': LegoEssential,
        'Microbit': Microbit,
        'RVRSphero': RVRSphero,
        'Spherookoslabda': Spherookoslabda
    }
    return products.get(product_name, None)


def mondatszures(mondat):
    """Kulcsszavak alapján termék keresés"""
    kulcsszavak = {
        'aibo': Aibo,
        'robotkutya': Aibo,
        'programozható': Aibo,
        'mesterséges intelligencia': Aibo,
        'kiskutya': Aibo,
        'padlórobot': Edison,
        'vonalkövető': Edison,
        'robot egér': CodeandGorobotegér,
        'robotkar': Robotkar,
        'vr szemüveg': Vr,
        'lego spike prime': LegoSpikePrime,
        'lego essential': LegoEssential,
        'micro:bit': Microbit,
        'rvr sphero': RVRSphero,
        'sphero okoslabda': Spherookoslabda,
        'labda': Spherookoslabda,
        'emelő': Robotkar,
        'forgató': Robotkar,
        '3d-s környezet': Vr,
        'essential': LegoEssential,
        'spike': LegoSpikePrime,
        'kicsiknek legó': LegoEssential,
        'egérke': CodeandGorobotegér,
        'marsjáró': RVRSphero,
        'robotegér': CodeandGorobotegér,
        'code&go': CodeandGorobotegér,
        'micro usb': Microbit,
        'microbit': Microbit,
        'led kijelző': Microbit,
        'golyó': Spherookoslabda,
        'edison': Edison,
        'szumó': Edison,
        'szumó bírkózás': Edison,
        'vonalkövetés': Edison,
        'fénykövetés': Edison,
        'tapsra mozog': Edison,
        'taps': Edison,
        'japán': Aibo,
        'szimuláció': Vr,
        'szemüveg': Vr,
        'rvr': RVRSphero,
        'sphero': Spherookoslabda,
        'okoslabda': Spherookoslabda,
        'robot jármű': RVRSphero,
        'programozható számítógép': Microbit,
        'kicsi számítógép': Microbit,
        'vonalhatárok': Edison,
        'vr': Vr,
        'hivnak': Nev,
        'neved': Nev,
        'mi a neved': Nev,
        'Ki vagy te': Nev,
        'hogy hívnak': Nev,
        'hogy szólítanak': Nev,
        'hogy szólíthatlak': Nev
    }
    
    mondat_lower = mondat.lower()
    
    for kulcs, termek in kulcsszavak.items():
        if kulcs in mondat_lower:
            return termek
    
    return None


def ollama_valasz(kerdes):
    try:
        system_prompt = """Te Blinky vagy, a Digitális Tudásközpont AI asszisztense. 
        A tudásközpontban különböző technológiákkal ismerkedhetnek meg a látogatók: 
        Aibo robotkutya, Edison padlórobotok, Code&Go robot egér, robotkar, VR szemüveg, 
        Lego Spike Prime és Essential, Micro:bit, RVR Sphero, Sphero okoslabda.
        
        Válaszolj röviden, barátságosan és érthetően magyarul. 
        Ha a kérdés nem kapcsolódik a tudásközponthoz vagy robotikához, akkor is segítőkész vagy."""
        
        response: ChatResponse = chat(
            model='tinyllama', 
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': kerdes,
                },
            ]
        )
        
        
        return response.message.content
    except Exception as e:
        return f"Sajnos nem tudok válaszolni erre a kérdésre. Hiba: {str(e)}"


def irás_effect(szoveg, kesleltet=0.05):
    """Begépelés effektus"""
    for betuk in szoveg:
        sys.stdout.write(betuk)
        sys.stdout.flush()
        time.sleep(kesleltet)
    print()


def hang_mentes(szoveg, fajlnev="audio"):
    try:
        audio_mappa = "audio"
        if not os.path.exists(audio_mappa):
            os.makedirs(audio_mappa)
        
        szoveg_tiszta = szoveg.replace('\n', ' ').strip()
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        fajl_utvonal = os.path.join(audio_mappa, f"{fajlnev}_{timestamp}.mp3")
        
        tts = gTTS(text=szoveg_tiszta, lang='hu', slow=False)
        tts.save(fajl_utvonal)
        
        return True
    except Exception as e:
        print(f"sikertelen mentés: {e}")
        return False


def irás_effect_hang(szoveg, kesleltet=0.05):
    szoveg_tiszta = szoveg.replace('\n', ' ').strip()
    
    hang_thread = threading.Thread(target=hang, args=(szoveg_tiszta,))
    hang_thread.start()
    
    try:
        hang_mentes(szoveg_tiszta, "valasz")
    except Exception as e:
        print(f"Hiba: {e}")

    irás_effect(szoveg, kesleltet)
    hang_thread.join()


def kerdes_feldolgozas(felhasznalo_valasz):
  
    info = pontos_kereses(felhasznalo_valasz)
    
    if info:
        return info[0], "static"

    reszleges = mondatszures(felhasznalo_valasz)
    if reszleges:
        if isinstance(reszleges[0], list):
            return reszleges[0], "static"
        else:
            return [reszleges[0]], "static"
    

    ollama_response = ollama_valasz(felhasznalo_valasz)
    return [ollama_response], "ollama"


if __name__ == "__main__":

    irás_effect_hang(Bemutatkozás[0])

    vege = True
    while vege:
        kerdes = '\n\nMelyik technológiáról szeretnél többet tudni, vagy kérdezz bátran:'
        irás_effect_hang(kerdes)
        
        felhasznalo_valasz = input()
        
        if felhasznalo_valasz.lower() in ['vége', 'kilépés', 'kilép', 'end', 'exit', 'quit']:
            viszlat = "Viszlát! Várunk vissza a Digitális Tudásközpontban!"
            irás_effect_hang(viszlat)
            vege = False
            break
        
        valaszok, forrás = kerdes_feldolgozas(felhasznalo_valasz)
        
        if isinstance(valaszok, list):
            for szoveg in valaszok:
                irás_effect_hang(szoveg)
        else:
            irás_effect_hang(valaszok)
        
        # if forrás == "ollama":
        #    print("\n(ollama által generált válasz)")
        #else:
        #   print("\n(Statikus adatbázisból)")