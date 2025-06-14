import sqlite3
import random

class Motorrad:
    def __init__(self, *args):
        self.id, self.marke, self.modell, self.hubraum, self.leistung, self.drehmoment, self.gewicht, self.hoechstgeschwindigkeit, self.beschleunigung_0_100, self.preis = args

class MotorradGame:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.score = 0
        self.player_name = ""
        self.current_bike = None
        self.next_bike = None
        self.properties = [
            ('hubraum', 'Hubraum'),
            ('leistung', 'Leistung'),
            ('drehmoment', 'Drehmoment'),
            ('gewicht', 'Gewicht'),
            ('hoechstgeschwindigkeit', 'Höchstgeschwindigkeit'),
            ('beschleunigung_0_100', '0-100 Zeit'),
            ('preis', 'Preis')
        ]
        self.setup_database()
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
            (25, "Yamaha", "Ténéré 700", 689, 74, 68, 205, 200, 5.5, 10000),
            (26, "Ducati", "Diavel V4", 1158, 168, 120, 236, 270, 3.5, 27000),
            (27, "Honda", "Hebel 1100", 1084, 87, 100, 223, 180, 5.2, 11000),
            (28, "Yamaha", "Tracer 9 GT", 890, 119, 93, 220, 230, 4.9, 13000),
            (29, "Kawasaki", "Versys 1000 SE", 1043, 120, 102, 255, 220, 5.5, 14500),
            (30, "BMW", "F 900 XR", 895, 105, 92, 219, 210, 4.8, 12000),
            (31, "Suzuki", "V-Strom 800 DE", 776, 84, 78, 230, 210, 5.3, 11500),
            (32, "Aprilia", "Tuareg 660", 659, 80, 70, 204, 200, 4.5, 11500),
            (33, "KTM", "890 Adventure R", 889, 105, 100, 210, 210, 4.7, 14000),
            (34, "Triumph", "Tiger 900 GT", 888, 95, 87, 219, 210, 5.0, 13500),
            (35, "MV Agusta", "Turismo Veloce", 798, 110, 83, 199, 240, 5.5, 23000),
            (36, "Harley-Davidson", "Road Glide", 1868, 93, 170, 387, 170, 6.0, 28000),
            (37, "Indian", "Chief Dark Horse", 1890, 95, 170, 315, 170, 5.7, 21000),
            (38, "Zero", "SR/F", 0, 110, 190, 220, 200, 0.0, 20000),  
            (39, "Energica", "Ego+", 0, 171, 260, 260, 240, 0.0, 25000), 
            (40, "CFMOTO", "800MT Touring", 799, 95, 80, 231, 210, 5.0, 10000),
            (41, "Benelli", "TRK 702", 698, 70, 68, 235, 190, 5.2, 8500),
            (42, "Moto Guzzi", "V100 Mandello", 1042, 115, 105, 233, 230, 5.3, 16000),
            (43, "Royal Enfield", "Interceptor 650", 648, 47, 52, 202, 170, 4.0, 7000),
            (44, "Husqvarna", "Vitpilen 701", 692, 75, 72, 158, 210, 4.2, 11000),
            (45, "Bimota", "Tesi H2", 998, 231, 160, 207, 299, 2.9, 60000),
            (46, "Norton", "V4SV", 1200, 185, 125, 193, 300, 3.1, 46000),
        ]
    def setup_database(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE motorraeder (
            id INTEGER, marke TEXT, modell TEXT, hubraum INTEGER, leistung INTEGER, 
            drehmoment INTEGER, gewicht INTEGER, hoechstgeschwindigkeit INTEGER, 
            beschleunigung_0_100 REAL, preis INTEGER)''')
        c.execute('''CREATE TABLE highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, score INTEGER)''')

        c.executemany("INSERT INTO motorraeder VALUES (?,?,?,?,?,?,?,?,?,?)", self.bikes)
        self.conn.commit()

    def get_player_name(self):
        print("\nSpielername eingeben:")
        while True:
            name = input("Name: ").strip()
            if name:
                self.player_name = name
                break

    def save_score(self):
        c = self.conn.cursor()
        c.execute("INSERT INTO highscores (player_name, score) VALUES (?, ?)", (self.player_name, self.score))
        self.conn.commit()

    def show_highscores(self):
        c = self.conn.cursor()
        c.execute("SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT 5")
        print("\n🏆 HIGHSCORES:")
        for i, (name, score) in enumerate(c.fetchall(), 1):
            print(f"{i}. {name} - {score} Punkte")

    def get_random_bike(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM motorraeder ORDER BY RANDOM() LIMIT 1")
        return Motorrad(*c.fetchone())

    def print_bike_info(self, bike, prop, val):
        print(f"\nMotorrad: {bike.marke} {bike.modell}")
        print(f"{prop}: {val}")

    def generate_hint(self, key, value):
        if isinstance(value, (int, float)):
            if key == "beschleunigung_0_100":
                if value < 2.5:
                    return "eine sehr schnelle Beschleunigung (< 2.5s)"
                elif value < 4:
                    return "eine gute Beschleunigung (< 4s)"
                elif value < 5.5:
                    return "eine durchschnittliche Beschleunigung (< 5.5s)"
                else:
                    return "eine eher langsame Beschleunigung (> 5.5s)"
            else:
                if value < 100:
                    return "einen eher niedrigen Wert (< 100)"
                elif value < 200:
                    return "einen mittleren Wert (< 200)"
                else:
                    return "einen hohen Wert (>= 200)"
        return "einen unbekannten Wert"

    def play_round(self):
        if not self.current_bike:
            self.current_bike = self.get_random_bike()

        self.next_bike = self.get_random_bike()
        while self.next_bike.id == self.current_bike.id:
            self.next_bike = self.get_random_bike()

        key, name = random.choice(self.properties)
        val1 = getattr(self.current_bike, key)
        val2 = getattr(self.next_bike, key)

        self.print_bike_info(self.current_bike, name, val1)
        print(f"\nHat das nächste Motorrad bei {name} mehr (h) oder weniger (l)? (Tipp mit '?')")

        used_hint = False
        while True:
            guess = input("Deine Wahl (h/l/?): ").lower()
            if guess == '?':
                hint = self.generate_hint(key, val2)
                print(f"Tipp: Das nächste Motorrad hat {hint}.")
                used_hint = True
            elif guess in ['h', 'l']:
                break

        self.print_bike_info(self.next_bike, name, val2)

        if (guess == 'h' and val2 > val1) or (guess == 'l' and val2 < val1):
            points = 1 if used_hint else 3
            self.score += points
            console.print(f"Richtig! Du bekommst {points} Punkt{'e' if points > 1 else ''}.")
        else:
            print("Falsch! Keine Punkte.")

        print(f"Wertvergleich: {val1} vs {val2}")
        self.current_bike = self.next_bike

        print("\n1 = Weiter, 2 = Beenden")
        while True:
            choice = input("Auswahl: ")
            if choice == '1':
                self.play_round()
                return
            elif choice == '2':
                self.save_score()
                self.show_highscores()
                print("Danke fürs Spielen!")
                exit()

    def start(self):
        print("MOTORRAD HIGHER-LOWER SPIEL")
        self.get_player_name()
        input("Enter zum Start...")
        self.play_round()

if __name__ == "__main__":
    MotorradGame().start()

