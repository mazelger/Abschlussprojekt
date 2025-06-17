import mysql.connector
import random

def hole_motorrad_daten():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='cdcol'
    )

    cursor = db.cursor()
    cursor.execute("SELECT Marke, Model, `Hubraum(ccm)`, `Leistung(PS)`, `Drehmoment(Nm)`, `Gewicht(kg)`, `Hoechstgeschwindigkeit(km/h)`, `Beschleunigung(m/s)`, `Preis(€)` FROM bikesnotepad")
    daten = cursor.fetchall()
    db.close()
    return daten

def spiel_starten(daten, highscores):
    name = input("Gib deinen Namen ein: ")

    punkte = 0
    print("Willkommen beim Motorrad-Spiel,", name, "!")

    while True:
        bikes = random.sample(daten, 2)
        bike1 = bikes[0]
        bike2 = bikes[1]

        eigenschaften = ['Hubraum(ccm)', 'Leistung(PS)', 'Drehmoment(Nm)', 'Gewicht(kg)', 'Hoechstgeschwindigkeit(km/h)', 'Beschleunigung(m/s)', 'Preis(€)']
        eigenschaft = random.choice(eigenschaften)

        index = ['Marke', 'Model', 'Hubraum(ccm)', 'Leistung(PS)', 'Drehmoment(Nm)', 'Gewicht(kg)', 'Hoechstgeschwindigkeit(km/h)', 'Beschleunigung(m/s)', 'Preis(€)'].index(eigenschaft)

        wert1 = bike1[index]
        wert2 = bike2[index]

        print()
        print(f"Vergleiche: {eigenschaft.upper()}")
        print("1:", bike1[0], bike1[1])
        print("2:", bike2[0], bike2[1])

        while True:
            auswahl = input("Welches ist besser? (1 oder 2, stop zum Beenden): ")
            if auswahl in ["1", "2", "stop"]:
                break
            else:
                print("Ungültige Eingabe! Bitte nur 1, 2 oder q eingeben.")

        if auswahl == "stop":
            break

        if eigenschaft == 'Beschleunigung(m/s)':  
            korrekt = (wert1 <= wert2 and auswahl == "1") or (wert2 <= wert1 and auswahl == "2")
        else:  
            korrekt = (wert1 >= wert2 and auswahl == "1") or (wert2 >= wert1 and auswahl == "2")

        if korrekt:
            print("Richtig!")
            punkte += 1
        else:
            print("Falsch!")

        print("Aktueller Punktestand:", punkte)

    highscores.append((name, punkte))

    print("\n--- Highscores ---")
    for spieler, punkte in sorted(highscores, key=lambda x: x[1], reverse=True):
        print(spieler, ":", punkte, "Punkte")

def main():
    daten = hole_motorrad_daten()
    highscores = []

    while True:
        spiel_starten(daten, highscores)
        nochmal = input("\nMöchtest du nochmal spielen? (ja/nein): ")
        if nochmal.lower() != "ja":
            break

main()

