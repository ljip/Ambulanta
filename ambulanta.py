import os
import json
import sys
import time

pacijenti = {}

def load_data():
    with open("SviPacijenti.json", "r") as dat:
        pacijenti.update(json.load(dat))


def write_data():
    with open("SviPacijenti.json", "w") as dat:
        json.dump(pacijenti, dat)


def inicijalizacija_podataka():
    if not os.path.exists("SviPacijenti.json"):
        print("Nema predpostojećih podataka.")
        time.sleep(1)
        print("Kreiranje nove baze.")
        write_data()
        time.sleep(1)
        print("Baza kreirana.")
        time.sleep(1)
    else:
        print("Predpostojeća baza pronađena.")
        time.sleep(0.5)
        print("Učitavanje baze...")
        load_data()
        time.sleep(1)
        if len(pacijenti) == 0:
            print("Baza je prazna.")
        else:
            print("Baza uspiješno učitana.")
        time.sleep(1)


def start_screen():
    print("""
      \\\\
     c  oo
      | .U        Ambulanta:
    __=__         Filip Lilić     ,,,
    |.  __|___                    oo ;
    ||_/  /  /                    U= _  0
    \_/__/__E   o                 /. .| |
    (___ ||    |~~~~~~~~~~~~~~~~'----'~|
    I---|||    |-----------------------|
    I   |||    |       c(__)           |
    ^   '--''  ^                       ^\n""")
    
    time.sleep(1)
    glavni_izbornik()


def glavni_izbornik():
    """Izbornik"""
    ocisti_ekran()
    unos = int(input("""Unesite broj za odabir opcije:\n
        1. Unos pacijenta
        2. Pregled svih pacijenata
        3. Prikaz pacijenta uz povijest bolesti i propisane terapije
        4. Pregled povijesti bolesti, terapije i kirurske zahvate
        5. Unos anamneze, dijagnoze i terapije za odredenu osobu
        6. Azuriranje dijagnoze
        7. Brisanje dijagnoze
        8. Brisanje pacijenta
        0. Izlaz iz programa

        Unos: """))
    unos_logika(unos)


def unos_pacijenta():
    """Kreiranje profila pacijenta"""
    ocisti_ekran()

    ime = input("Unesite ime pacijenta: ").title()
    prezime = input("Unesite prezime pacijenta: ").title()
    adresa = input("Unesite adresu pacijenta: ").title()
    datum_rodenja = input(
        "Unesite datum rodenja pacijenta u formatu dd-mm-gg: ")
    maticni_broj_osiguranika = mbo()
    lijecnik = input("Unesite nadleznog lijecnika pacijenta: ").title()
    dijagnoza = None
    anamneza = None
    terapija = None
    kirurski_zahvat = input("Je li pacijent imao kirurske zahvate? d/n: ")

    pacijent = {
        "ime": ime,
        "prezime": prezime,
        "adresa": adresa,
        "datum_rodenja": datum_rodenja,
        "maticni_broj_osiguranika": maticni_broj_osiguranika,
        "lijecnik": lijecnik,
        "dijagnoza": dijagnoza,
        "terapija": terapija,
        "kirurski_zahvat": kirurski_zahvat,
        "anamneza": anamneza,
    }

    pacijenti[maticni_broj_osiguranika] = pacijent

    write_data()

    upit_za_dodavanje_novog_pacijenta()


def upit_za_dodavanje_novog_pacijenta():
    upit = input("Zelite li dodati novog pacijenta? d/n \t")

    if upit == "d": 
        unos_pacijenta()
    elif upit == "n":
        write_data()
        glavni_izbornik()
    else:
        upit_za_dodavanje_novog_pacijenta()


def pregled_svih_pacijenata():
    """Prikaz podataka o svim pacijentima"""
    ocisti_ekran()
    for podaci in pacijenti.values():
        print("MBO:", podaci["maticni_broj_osiguranika"],
              "Ime:",podaci["ime"], "Prezime:", podaci["prezime"] + "\n", sep=" | ")
    input("Enter za nastavak")     
    glavni_izbornik()
    

def pregled_pacijenta_povijest_bolesti_terapija():
    """Prikaz pacijenta uz povijest bolesti i propisane terapije"""
    ocisti_ekran()
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        pacijent = pacijenti[maticni_broj_osiguranika]
        
        print("\nPacijent:", pacijent["ime"], pacijent["prezime"], "\n")
        
        if pacijent["dijagnoza"] == None and pacijent["terapija"] == None:
            print("Pacijent nema dijagnozu niti pripisanu terapiju.\n")
        else:
            if pacijent["dijagnoza"] != None:
                print("Dijagnoza:", pacijent["dijagnoza"])
            if pacijent["terapija"] != None:
                print("Terapija:", pacijent["terapija"])
        input("\nPritisnite enter za nastavak...")
    else:
        print("Pacijent ne postoji!")
        time.sleep(1)
    glavni_izbornik()


def pregled_pacijenta_terapija_zahvati():
    """Pregled povijest bolesti, terapije i kirurške zahvate"""
    ocisti_ekran()
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        podaci = pacijenti[maticni_broj_osiguranika]
        if podaci["dijagnoza"] == None and podaci["terapija"] == None and podaci["kirurski_zahvat"] == "n":
            print("Pacijent nema dijagnozu niti pripisanu terapiju niti kirurski zahvat.")
        else:
            if podaci["dijagnoza"] != None:
                print("Dijagnoza:", podaci["dijagnoza"])
            if podaci["terapija"] != None:
                print("Terapija:", podaci["terapija"])
            print("Kirurski zahvat:", podaci["kirurski_zahvat"])
        input("\nPritisnite enter za nastavak...")
    else:
        print("Pacijent s tim maticnim brojem osiguranika ne postoji!")
        input("\nPritisnite enter za nastavak...")
    ocisti_ekran()
    glavni_izbornik()


def postavljanje_anamneze_dijagnoze_terapije():
    """Unos anamneze, dijagnoze i terapije za odredenu osobu"""
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        pacijenti[maticni_broj_osiguranika]["anamneza"] = input("Upišite anamnezu pacijenta: ")
        pacijenti[maticni_broj_osiguranika]["dijagnoza"] = input("Upišite dijagnozu pacijenta: ")
        pacijenti[maticni_broj_osiguranika]["terapija"] = input("Upišite terapiju za pacijenta: ")
        write_data()
        print("Upisali ste anamnezu, dijagnozu i terapiju za pacijenta!\n")
    else:
        print("Osoba s tim oib-om ne postoji!\n")

    ocisti_ekran()
    glavni_izbornik()


def dijagnoza():
    """Azuriranje dijagnoze"""
    ocisti_ekran()
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        nova_dijagnoza = input("Unesite dijagnozu pacijenta: ")
        pacijenti[maticni_broj_osiguranika]["dijagnoza"] = nova_dijagnoza
        write_data()
        print("Ažurirali ste dijagnozu!")
        time.sleep(1)
    else:
        print("Osoba s tim oib-om ne postoji!")
        time.sleep(1)
      
    ocisti_ekran()
    glavni_izbornik()


def brisanje_dijagnoze():
    """Brisanje dijagnoze"""
    ocisti_ekran()
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        pacijenti[maticni_broj_osiguranika]["dijagnoza"] = None
        write_data()
        print("Dijagnoza uspjesno izbrisana!")
        time.sleep(1)
    elif maticni_broj_osiguranika not in pacijenti.keys():
        print("pacijent ne postoji!")
        time.sleep(1)
      
    ocisti_ekran()
    glavni_izbornik()


def brisanje_pacijenta():
    ocisti_ekran()
    maticni_broj_osiguranika = mbo()
    if maticni_broj_osiguranika in pacijenti.keys():
        del pacijenti[maticni_broj_osiguranika]
        write_data()
        print("pacijent uspjesno izbrisan!")
        time.sleep(1)
    else:
        print("pacijent ne postoji")
        time.sleep(1)
    glavni_izbornik()


def izlaz():
    os.system("cls")
    print("Hvala sto ste koristili program!")
    quit()


def ocisti_ekran():
    """os.system("cls") za windowse, os.system("clear") za linux, mac"""
    if sys.platform == "linux" or sys.platform == "darwin":
        os.system('clear')
    else:   
        os.system("cls")


def mbo() -> str:
    maticni_broj_osiguranika = input(
        "Unesite maticni_broj_osiguranika pacijenta: ")
    if len(maticni_broj_osiguranika) != 9:
        print("maticni_broj_osiguranika mora imati 9 znamenki!")
    return maticni_broj_osiguranika


def unos_logika(izbor):
    if izbor == 1:
        unos_pacijenta()
    elif izbor == 2:
        pregled_svih_pacijenata()
    elif izbor == 3:
        pregled_pacijenta_povijest_bolesti_terapija()
    elif izbor == 4:
        pregled_pacijenta_terapija_zahvati()
    elif izbor == 5:
        postavljanje_anamneze_dijagnoze_terapije()
    elif izbor == 6:
        dijagnoza()
    elif izbor == 7:
        brisanje_dijagnoze()
    elif izbor == 8:
        brisanje_pacijenta()
    elif izbor == 0:
        ocisti_ekran()
        print("Hvala što ste koristili program!")
        time.sleep(1)
        ocisti_ekran()
        quit()
    else:
      print("Krivi unos... Izlaz iz programa...")
      quit()


def reset_podataka():
    os.remove("SviPacijenti.json")


def main():
    ocisti_ekran()
    # reset_podataka()
    inicijalizacija_podataka()
    start_screen()
  
  
if __name__ == "__main__":
    main()