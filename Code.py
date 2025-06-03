import sqlite3
import random
from dataclasses import dataclass

@dataclass
class Motorrad:
    id: int
    marke: str
    modell: str
    hubraum: int
    leistung: int
    drehmoment: int
    gewicht: int
    hoechstgeschwindigkeit: int
    beschleunigung_0_100: float
    preis: int

class MotorradGame:
    def __init__(self):
        self.conn = None
        self.score = 0
        self.player_name = ""
        self.current_bike = None
        self.next_bike = None
        self.properties = [
            ('hubraum', 'Hubraum (ccm)'),
            ('leistung', 'Leistung (PS)'), 
            ('drehmoment', 'Drehmoment (Nm)'),
            ('gewicht', 'Gewicht (kg)'),
            ('hoechstgeschwindigkeit', 'Höchstgeschwindigkeit (km/h)'),
            ('beschleunigung_0_100', 'Beschleunigung 0-100 (s)'),
            ('preis', 'Preis (€)')
        ]
        self.setup_database()
        
    def setup_database(self):
        self.conn = sqlite3.connect(':memory:')
        c = self.conn.cursor()
        
        # Motorrad-Tabelle
        c.execute('''CREATE TABLE motorraeder
                     (id INTEGER PRIMARY KEY,
                      marke TEXT,
                      modell TEXT,
                      hubraum INTEGER,
                      leistung INTEGER,
                      drehmoment INTEGER,
                      gewicht INTEGER,
                      hoechstgeschwindigkeit INTEGER,
                      beschleunigung_0_100 REAL,
                      preis INTEGER)''')
        
        # Highscore-Tabelle
        c.execute('''CREATE TABLE IF NOT EXISTS highscores
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      player_name TEXT,
                      score INTEGER)''')
        
        # Beispieldaten für Motorräder
        bikes = [
            (1, "Ducati", "Panigale V4", 1103, 214, 124, 195, 299, 4.0, 35000),
            (2, "Honda", "CBR 600 RR", 599, 120, 66, 186, 250, 3.5, 12000),
            (3, "Yamaha", "YZF-R1", 998, 200, 112, 201, 299, 3.2, 18000),
            (4, "Kawasaki", "Ninja H2", 998, 310, 165, 238, 340, 2.8, 55000),
            (5, "BMW", "S 1000 RR", 999, 207, 113, 197, 303, 3.1, 19000),
            (6, "Suzuki", "GSX-R 1000", 999, 202, 118, 202, 299, 3.0, 16000),
            (7, "Aprilia", "RSV4", 1099, 217, 125, 193, 299, 3.0, 21000),
            (8, "KTM", "1290 Super Duke R", 1301, 180, 140, 189, 270, 3.5, 19000),
            (9, "Triumph", "Speed Triple", 1160, 150, 125, 198, 250, 3.8, 15000),
            (10, "MV Agusta", "F4 RC", 998, 212, 115, 192, 299, 3.1, 38000),
            (11, "Harley-Davidson", "Sportster S", 1252, 121, 125, 228, 200, 4.5, 15000),
            (12, "Ducati", "Monster", 937, 111, 93, 188, 230, 4.2, 12000),
            (13, "Honda", "CBR 1000 RR", 999, 189, 114, 201, 286, 3.0, 17000),
            (14, "Yamaha", "MT-09", 889, 119, 93, 193, 230, 3.8, 10000),
            (15, "Kawasaki", "Z900", 948, 125, 99, 210, 240, 3.6, 9500),
            (16, "BMW", "R 1250 GS", 1254, 136, 143, 249, 200, 4.5, 18000),
            (17, "Suzuki", "Hayabusa", 1340, 190, 150, 264, 299, 3.2, 19000),
            (18, "Aprilia", "Tuono V4", 1077, 175, 121, 209, 270, 3.5, 15000),
            (19, "KTM", "390 Duke", 373, 44, 37, 149, 170, 5.5, 6000),
            (20, "Triumph", "Street Triple", 765, 123, 79, 189, 240, 3.8, 11000),
            (21, "MV Agusta", "Brutale", 798, 140, 87, 175, 240, 3.5, 15000),
            (22, "Harley-Davidson", "Fat Boy", 1868, 86, 156, 306, 160, 6.5, 21000),
            (23, "Ducati", "Multistrada", 1158, 160, 127, 232, 240, 4.0, 19000),
            (24, "Honda", "Africa Twin", 1084, 102, 105, 236, 200, 5.0, 14000),
            (25, "Yamaha", "Ténéré 700", 689, 74, 68, 205, 200, 5.5, 10000)
        ]
        
        c.executemany("INSERT INTO motorraeder VALUES (?,?,?,?,?,?,?,?,?,?)", bikes)
        self.conn.commit()
    
    def get_player_name(self):
        self.print_header()
        print("\n" + " SPIELERDATEN ".center(50, "~"))
        while True:
            name = input("\nGib deinen Namen ein: ").strip()
            if name:
                self.player_name = name
                break
            print("Bitte gib einen gültigen Namen ein!")
    
    def save_score(self):
        c = self.conn.cursor()
        c.execute("INSERT INTO highscores (player_name, score) VALUES (?, ?)",
                 (self.player_name, self.score))
        self.conn.commit()
    
    def show_highscores(self):
        c = self.conn.cursor()
        c.execute("SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT 5")
        highscores = c.fetchall()
        
        print("\n" + " TOP 5 HIGHSCORES ".center(50, "="))
        if not highscores:
            print("Noch keine Highscores vorhanden!".center(50))
        else:
            for i, (name, score) in enumerate(highscores, 1):
                print(f"{i}. {name:<20} {score} Punkte")
        print("="*50)
    
    def print_header(self):
        print("\n" + "="*50)
        if self.player_name:
            title = f" {self.player_name} | PUNKTE: {self.score} "
            print(title.center(50, "="))
        else:
            print(" MOTORRAD HIGHER-LOWER ".center(50, "="))
        print("="*50 + "\n")
    
    def print_bike_info(self, bike, prop_name, prop_value):
        print(f"\n{' MOTORRAD INFO ':-^50}")
        print(f"Marke/Modell: {bike.marke} {bike.modell}")
        print(f"Vergleichswert: {prop_name}: {prop_value}")
        print("-"*50)
    
    def get_random_bike(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM motorraeder ORDER BY RANDOM() LIMIT 1")
        return Motorrad(*c.fetchone())
    
    def play_round(self):
        if not self.current_bike:
            self.current_bike = self.get_random_bike()
        
        self.next_bike = self.get_random_bike()
        while self.next_bike.id == self.current_bike.id:
            self.next_bike = self.get_random_bike()
        
        prop_key, prop_name = random.choice(self.properties)
        current_val = getattr(self.current_bike, prop_key)
        
        self.print_header()
        self.print_bike_info(self.current_bike, prop_name, current_val)
        
        print("\n" + " VERGLEICH ".center(50, "~"))
        print(f"Wird das nächste Motorrad bei {prop_name}")
        print(f"einen HÖHEREN (h) oder NIEDRIGEREN (l) Wert haben?")
        
        while True:
            guess = input("\nDeine Wahl (h/l): ").lower()
            if guess in ['h', 'l']:
                break
            print("Ungültige Eingabe! Bitte 'h' oder 'l' eingeben.")
        
        next_val = getattr(self.next_bike, prop_key)
        
        self.print_header()
        print("\n" + " ERGEBNIS ".center(50, "~"))
        self.print_bike_info(self.next_bike, prop_name, next_val)
        
        if (guess == 'h' and next_val > current_val) or (guess == 'l' and next_val < current_val):
            self.score += 1
            print("\n✓ Richtig! +1 Punkt")
        else:
            print("\n✗ Falsch! Kein Punkt")
        
        print(f"\nVergleich: {current_val} vs {next_val}")
        
        self.current_bike = self.next_bike
        
        print("\n" + "="*50)
        print(" Was möchtest du tun? ".center(50))
        print("1. Nächste Runde")
        print("2. Beenden")
        
        while True:
            choice = input("\nAuswahl (1-2): ")
            if choice == '1':
                self.play_round()
                return
            elif choice == '2':
                self.save_score()
                self.show_highscores()
                print("\nDanke fürs Spielen! Bis zum nächsten Mal!")
                exit()
            else:
                print("Ungültige Eingabe! Bitte 1 oder 2 wählen.")
    
    def start(self):
        print("\n" + "="*50)
        print(" MOTORRAD HIGHER-LOWER SPIEL ".center(50, "="))
        print("="*50)
        
        self.get_player_name()
        
        print("\nSpielregeln:")
        print("- Es werden zwei Motorräder verglichen")
        print("- Du musst raten, ob das nächste Motorrad")
        print("  einen höheren (h) oder niedrigeren (l) Wert hat")
        print("- Für jede richtige Antwort gibt es einen Punkt")
        
        input("\nDrücke Enter um zu beginnen...")
        self.play_round()

if __name__ == "__main__":
    game = MotorradGame()
    game.start()
