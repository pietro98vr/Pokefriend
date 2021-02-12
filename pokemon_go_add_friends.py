import requests
from bs4 import BeautifulSoup
import os
import time
import subprocess

numero_pagina = 1
found_codes = []
initial_volume = ((subprocess.check_output("adb shell media volume --get", shell=True)).decode()).removeprefix("[v] will get volume\r\n[v] Connecting to AudioService\r\n[v] volume is ")
initial_volume = initial_volume[:2]

try:
    #set the screen resolution to 1080x1920, the density to 390 and the volume to 0
    os.system("adb shell wm size 1080x1920")
    os.system("adb shell wm density 390")
    os.system("adb shell media volume --set 0")
    os.system("adb shell am force-stop com.nianticlabs.pokemongo") #chiudo pokemon go se era già aperto


    #opening Pokemon Go on the phone
    os.system("adb shell monkey -p com.nianticlabs.pokemongo -c android.intent.category.LAUNCHER 1 > NUL")
    print("\n")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("Inizio ad aprire l'app di Pokemon Go")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("\n")
    print("Ho avviato Pokemon Go, attendo il suo caricamento")
    time.sleep(15)

    #clicking on the alert right after the app's loading screen
    os.system("adb shell input tap 550 1472")
    print("Ho cliccato sull'avviso di sicurezza dopo il login!")
    time.sleep(3)

    #clicking on the profile icon
    os.system("adb shell input tap 140 1764")
    print("Ho cliccato sull'icona del profilo!")
    time.sleep(5)

    #perform a swipe to reach the friends tab
    os.system("adb shell input touchscreen swipe 945 1332 191 1332")
    print("Ho swipato nella scheda amici!")
    time.sleep(3)

    #open the "Add a friend" section
    os.system("adb shell input tap 560 530")
    print("Ho cliccato su aggiungi un amico")
    time.sleep(3)

    #gather information about friend codes from the choosen site
    while numero_pagina <= 10:
        url = "https://pokemongo.gishan.net/friends/friend-codes/?c=all&t=all&g=all&p="+ str(numero_pagina)
        get_html= requests.get(url)
        soup = BeautifulSoup(get_html.text, 'html.parser')
        found_div = soup.find_all("div", class_="code-12")
        for x in found_div:
            code = x.find('p').contents[0]
            code = code.replace(" ", "")
            found_codes.append(code)

        numero_pagina += 1


    print("Ho trovato " + str(len(found_codes)) +" codici amico!")
    print("\n")
    print("Sono pronto per iniziare!")

    #let's start inserting friend codes
    count = 1
    for codice_amico in found_codes:
        inizio_timer = time.perf_counter()
        print("\n")
        print("-------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("Interazione numero " + str(count))
        print("-------------------------------------------------------------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")
        print("Inizio l'inserimento del codice amico")
        os.system("adb shell input tap 572 1391")
        print("Ho cliccato sullo spazio per inserire un amico")
        time.sleep(2)
        os.system("adb shell input keyboard text " + '"' + codice_amico + '"' + "\n")
        print("Ho copiato il codice amico nell'inputBox")
        time.sleep(2)
        #la prima volta è per uscire dall'input della tastiera
        os.system("adb shell input tap 167 1079")
        print("Ho chiuso la tastiera")
        time.sleep(0.5)
        os.system("adb shell input tap 526 915")
        print("Ho cliccato su invia")
        time.sleep(2)
        os.system("adb shell input tap 536 1039")
        print("Ho dato la conferma dell'invio")
        time.sleep(4)
        os.system("adb shell input tap 547 1100")
        print("Ho confermato la richiesta, passo a quella successiva!")
        time.sleep(3)
        count = count +1
        fine_timer = time.perf_counter()
        print(f"L'interazione ha richesto: {fine_timer - inizio_timer:0.0f} secondi")

    #reset the resolution and the density when ended
    os.system("adb shell wm size reset  && adb shell wm density reset && adb shell media volume --set " + initial_volume)

#if the user interrupts the task reset resolution and density to default
except KeyboardInterrupt:
    print("\n")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("L'utente ha interrotto l'esecuzione del codice")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("\n")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("Ripristino la risoluzione e il volume a quelli iniziali")
    print("-------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------")
    os.system("adb shell wm size reset  && adb shell wm density reset && adb shell media volume --set " + initial_volume)
