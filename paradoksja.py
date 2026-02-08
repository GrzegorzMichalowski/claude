#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARADOKSJA: Część I - Uciekająca Motywacja
Edukacyjna gra tekstowa dla uczniów klas 5-6
Autor: Claude AI
Wersja: 1.0
"""

import os
import sys
import time
from typing import Dict, List, Optional, Callable

# ============================================================================
# KONFIGURACJA
# ============================================================================

WIDTH = 60  # Szerokość tekstu
DELAY_CHAR = 0.02  # Opóźnienie przy pisaniu (efekt maszyny do pisania)
DELAY_FAST = 0.01
DELAY_SLOW = 0.04

# Kolory ANSI (opcjonalne - działają w większości terminali)
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @staticmethod
    def disable():
        """Wyłącz kolory jeśli terminal nie wspiera"""
        Colors.RESET = ''
        Colors.BOLD = ''
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''

# Sprawdź czy terminal wspiera kolory
if os.name == 'nt':  # Windows
    try:
        os.system('color')
    except:
        Colors.disable()

# ============================================================================
# ASCII ART
# ============================================================================

ASCII_TITLE = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗  █████╗ ██████╗  █████╗ ██████╗  ██████╗      ║
║   ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗     ║
║   ██████╔╝███████║██████╔╝███████║██║  ██║██║   ██║     ║
║   ██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║  ██║██║   ██║     ║
║   ██║     ██║  ██║██║  ██║██║  ██║██████╔╝╚██████╔╝     ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝      ║
║                    K S J A                               ║
║                                                          ║
║        ~ Część I: Uciekająca Motywacja ~                 ║
║                                                          ║
║   ╭─────────────────────────────────────────────────╮    ║
║   │  Gra edukacyjna dla uczniów klas 5-6           │    ║
║   │  Polski • Matematyka • Angielski                │    ║
║   ╰─────────────────────────────────────────────────╯    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

ASCII_BOOK = """
        ___________
       /          /|
      /  KSIĘGA  / |
     /  WIEDZY  /  |
    /__________/   |
    |   ~~~~   |   |
    |  ~~~~~~  |   /
    |   ~~~~   |  /
    |__________|/
"""

ASCII_HUB = """
    ·  ✦  ·    ·  ✦  ·    ·  ✦  ·
         ╭──────────────╮
    ·    │  BIBLIOTECZNY │    ·
  ✦      │     LIMBO     │      ✦
         ╰──────────────╯
    ·  ·  ·  ·  ·  ·  ·  ·  ·  ·

   [1]           [2]           [3]
  ┌───┐        ┌───┐        ┌───┐
  │ P │        │ M │        │ A │
  │ O │        │ A │        │ N │
  │ L │        │ T │        │ G │
  └───┘        └───┘        └───┘
"""

ASCII_NOTKA = """
   ┌─────┐
   │ ^_^ │  ← Notka
   │     │
   └──┬──┘
      │
"""

ASCII_LAS = """
    🌲    ,🌲,   🌲    ,🌲
  ,  🌲  🌲  ,🌲,  🌲  ,
    ,🌲,    🌲    ,🌲,  🌲
  🌲    🌲,    ,🌲    🌲
  ════════════════════════
      LAS PRZECINKOWY
"""

ASCII_GERALT = """
       ⚔️
      (·_·)   ← Geralt z Ortografii
      /|█|\\
       / \\
"""

ASCII_JASKINIA = """
      /\\     /\\
     /  \\___/  \\
    /           \\
   |   JASKINIA  |
   |  ORTOGRAFII |
    \\___________/
"""

ASCII_YENNEFER = """
       ✨✨
      (◠‿◠)  ← Yennefer
      /|█|\\
       / \\
"""

ASCII_ROWNINA = """
    x + y = ?     2x = 10
         \\  /
    ══════════════════════
    ░░░░░░░░░░░░░░░░░░░░░░
    RÓWNINA RÓWNAŃ
"""

ASCII_PITAGORAS = """
       💪💪
      (ಠ益ಠ)  ← Pitagoras Maximus
      /|█|\\
      _/ \\_
"""

ASCII_PIRAMIDA = """
          /\\
         /  \\
        / a² \\
       /──────\\
      / b² + c²\\
     /──────────\\
    PIRAMIDA PITAGORASA
"""

ASCII_ZERO = """
      (╥_╥)   ← Zero Bohater
      /(0)\\
       / \\
"""

ASCII_SLANG = """
   ╔═══════════════════╗
   ║  S L A N G   ST  ║
   ╠═══════════════════╣
   ║ COOL! AWESOME!   ║
   ║  DOPE! SICK!     ║
   ╚═══════════════════╝
"""

ASCII_ZOSIA = """
       📱
      (^◡^)  ← Zosia ze Słownika
      /|█|\\
       / \\
"""

ASCII_TENSES = """
   PAST ←── NOW ──→ FUTURE
     │       │        │
    was    is/am    will be
   ═══════════════════════
      TOWN OF TENSES
"""

ASCII_SHAKESPEARE = """
       🎭
      (˵ ͡° ͜ʖ ͡°˵)  ← Sir Shakespire
      /|█|\\
       / \\
"""

ASCII_VICTORY = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║                    🎉 GRATULACJE! 🎉                       ║
║                                                            ║
║         Ukończyłeś PARADOKSJĘ: Część I                     ║
║                                                            ║
║   ════════════════════════════════════════════════════     ║
║                                                            ║
║         ⭐ MOTYWACJA ODZYSKANA! ⭐                         ║
║                                                            ║
║         🪶 Polski:      ✓ ZALICZONY                        ║
║         🔢 Matematyka:  ✓ ZALICZONA                        ║
║         🏴 Angielski:   ✓ ZALICZONY                        ║
║                                                            ║
║   ════════════════════════════════════════════════════     ║
║                                                            ║
║         Kolejna część wkrótce...                           ║
║         (Geografia, Fizyka, Informatyka)                   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

ASCII_MOTIVATION = """
        ✨  ✨  ✨

    🪶  +  🔢  +  🏴
         ║
         ▼
    ╔═══════════╗
    ║ MOTYWACJA ║
    ║  ⭐⭐⭐   ║
    ╚═══════════╝
"""

# ============================================================================
# KLASY GRY
# ============================================================================

class Puzzle:
    """Reprezentuje zagadkę w grze"""

    def __init__(self, question: str, options: List[str], correct: int,
                 hints: List[str], points: int = 10):
        self.question = question
        self.options = options  # Lista opcji lub None dla odpowiedzi otwartej
        self.correct = correct  # Indeks poprawnej odpowiedzi lub string
        self.hints = hints
        self.points = points
        self.attempts = 0
        self.solved = False

    def check_answer(self, answer: str) -> bool:
        """Sprawdź odpowiedź"""
        self.attempts += 1

        if isinstance(self.correct, int):
            # Odpowiedź wielokrotnego wyboru
            try:
                choice = answer.lower().strip()
                if choice in ['a', '1']:
                    return self.correct == 0
                elif choice in ['b', '2']:
                    return self.correct == 1
                elif choice in ['c', '3']:
                    return self.correct == 2
                elif choice in ['d', '4']:
                    return self.correct == 3
            except:
                return False
        else:
            # Odpowiedź otwarta
            return answer.lower().strip() == str(self.correct).lower().strip()

        return False

    def get_hint(self) -> str:
        """Pobierz wskazówkę na podstawie liczby prób"""
        if self.attempts <= len(self.hints):
            return self.hints[self.attempts - 1]
        return self.hints[-1]


class NPC:
    """Reprezentuje postać niezależną"""

    def __init__(self, name: str, ascii_art: str, dialogues: List[str],
                 puzzle: Optional[Puzzle] = None):
        self.name = name
        self.ascii_art = ascii_art
        self.dialogues = dialogues
        self.puzzle = puzzle
        self.dialogue_index = 0
        self.talked = False

    def talk(self) -> str:
        """Zwróć następną linię dialogu"""
        if self.dialogue_index < len(self.dialogues):
            text = self.dialogues[self.dialogue_index]
            self.dialogue_index += 1
            self.talked = True
            return text
        return self.dialogues[-1] if self.dialogues else ""

    def reset_dialogue(self):
        """Zresetuj dialog"""
        self.dialogue_index = 0


class Location:
    """Reprezentuje lokację w grze"""

    def __init__(self, name: str, description: str, ascii_art: str,
                 npcs: List[NPC] = None, exits: Dict[str, str] = None):
        self.name = name
        self.description = description
        self.ascii_art = ascii_art
        self.npcs = npcs or []
        self.exits = exits or {}
        self.visited = False
        self.completed = False

    def get_npc(self, name: str) -> Optional[NPC]:
        """Znajdź NPC po nazwie"""
        name_lower = name.lower()
        for npc in self.npcs:
            if name_lower in npc.name.lower():
                return npc
        return None


class Player:
    """Reprezentuje gracza"""

    def __init__(self):
        self.inventory: List[str] = []
        self.motivations: Dict[str, bool] = {
            'polski': False,
            'matematyka': False,
            'angielski': False
        }
        self.score: int = 0
        self.start_time: float = 0

    def add_item(self, item: str):
        """Dodaj przedmiot do ekwipunku"""
        self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        """Sprawdź czy gracz ma przedmiot"""
        return item.lower() in [i.lower() for i in self.inventory]

    def get_motivation(self, subject: str):
        """Zdobądź motywację z przedmiotu"""
        self.motivations[subject.lower()] = True

    def motivation_count(self) -> int:
        """Policz zdobyte motywacje"""
        return sum(1 for v in self.motivations.values() if v)


class Game:
    """Główna klasa gry"""

    def __init__(self):
        self.player = Player()
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[Location] = None
        self.running = True
        self.game_started = False

        self._setup_world()

    def _setup_world(self):
        """Utwórz świat gry"""

        # ==================== HUB ====================
        notka = NPC(
            name="Notka",
            ascii_art=ASCII_NOTKA,
            dialogues=[
                "Hej! Jestem Notka, asystentka Księgi Wiedzy!",
                "Widzę, że jesteś nowy tutaj. Ok, no to tl;dr:",
                "Musisz odzyskać kawałki MOTYWACJI z trzech krain.",
                "Każda kraina = jeden przedmiot szkolny.",
                "Zaczynaj od POLSKIEGO [1], to najłatwiejsze!",
                "Potem MATMA [2], a na końcu ANGIELSKI [3].",
                "Wpisz 'idź 1', 'idź 2' lub 'idź 3' żeby wybrać krainę.",
                "Powodzenia, bestie! No cap, dasz radę! 💪"
            ]
        )

        hub = Location(
            name="Biblioteczny Limbo",
            description="Przestrzeń między stronami Księgi Wiedzy. "
                       "Wokół unoszą się kartki, litery i cyfry. "
                       "Widzisz trzy portale do różnych krain.",
            ascii_art=ASCII_HUB,
            npcs=[notka],
            exits={'1': 'las_przecinkowy', '2': 'rownina_rownan', '3': 'slang_street',
                   'polski': 'las_przecinkowy', 'matma': 'rownina_rownan',
                   'angielski': 'slang_street'}
        )

        # ==================== POLSKI ====================
        geralt_puzzle = Puzzle(
            question='Gdzie wstawić przecinek?\n"Ala ma kota psa i papugę"',
            options=[
                'a) Ala ma, kota psa i papugę',
                'b) Ala ma kota, psa i papugę',
                'c) Ala ma kota psa, i papugę'
            ],
            correct=1,  # odpowiedź B
            hints=[
                "Hmm, pomyśl o wyliczeniu. Co Ala ma?",
                "Przecinek oddziela elementy wyliczenia: kota, psa, papugę",
                "Poprawna odpowiedź to B - 'Ala ma kota, psa i papugę'"
            ]
        )

        geralt = NPC(
            name="Geralt z Ortografii",
            ascii_art=ASCII_GERALT,
            dialogues=[
                "Witaj, wędrowcze. Jestem Geralt z Ortografii.",
                "Widzę, że szukasz Motywacji. Cóż, najpierw pomóż mi.",
                "Te drzewa rosną przecinki, ale nie każdy jest na miejscu.",
                "Rozwiąż zagadkę, a przepuszczę cię dalej.",
                "Wpisz 'rozwiąż' aby zobaczyć zadanie."
            ],
            puzzle=geralt_puzzle
        )

        las = Location(
            name="Las Przecinkowy",
            description="Lekko creepy las. Z drzew zwisają... przecinki? "
                       "Tak, dosłownie znaki interpunkcyjne rosną na gałęziach.",
            ascii_art=ASCII_LAS,
            npcs=[geralt],
            exits={'hub': 'hub', 'powrót': 'hub', 'dalej': 'jaskinia_ortografii'}
        )

        # Zagadki Yennefer
        yen_puzzle1 = Puzzle(
            question='Które słowo jest napisane POPRAWNIE?',
            options=[
                'a) wogule',
                'b) w ogule',
                'c) w ogóle'
            ],
            correct=2,  # odpowiedź C
            hints=[
                "To słowo pisze się rozłącznie...",
                "Zwróć uwagę na 'ó' - to nie jest 'u'!",
                "Poprawna odpowiedź to C - 'w ogóle'"
            ]
        )

        yen_puzzle2 = Puzzle(
            question='Wstaw RZ lub Ż w słowach:\np_ecinki, mo_e, _aba\n\n'
                    'Wpisz odpowiedzi oddzielone przecinkami (np: rz,ż,rz)',
            options=None,  # odpowiedź otwarta
            correct='rz,rz,ż',
            hints=[
                "Pierwsza: pRZecinki - po 'p' często jest 'rz'",
                "Druga: moRZe - morze to duży zbiornik wody",
                "Trzecia: Żaba - żaba to zwierzę, zaczyna się od Ż"
            ]
        )

        yennefer = NPC(
            name="Yennefer",
            ascii_art=ASCII_YENNEFER,
            dialogues=[
                "Witajże, młodzieńcze. Jestem Yennefer, strażniczka ortografii.",
                "Widzę, że pokonałeś Geralta. Impressive!",
                "Lecz by zdobyć Motywację z Polskiego, musisz pokonać MNIE.",
                "Mam dla ciebie DWA wyzwania. Gotowy?",
                "Wpisz 'rozwiąż' aby rozpocząć."
            ],
            puzzle=yen_puzzle1  # Pierwsza zagadka
        )
        yennefer.puzzle2 = yen_puzzle2  # Druga zagadka
        yennefer.current_puzzle = 1

        jaskinia = Location(
            name="Jaskinia Ortografii",
            description="Ciemna jaskinia. Na ścianach świecą napisy - niektóre "
                       "błyszczą zielono (poprawne), inne czerwono (błędy).",
            ascii_art=ASCII_JASKINIA,
            npcs=[yennefer],
            exits={'powrót': 'las_przecinkowy', 'hub': 'hub'}
        )

        # ==================== MATEMATYKA ====================
        pita_puzzle = Puzzle(
            question='Rozwiąż równanie:\nx + 5 = 12\n\nx = ?',
            options=None,
            correct='7',
            hints=[
                "Zastanów się: co plus 5 daje 12?",
                "Przenieś 5 na drugą stronę: x = 12 - 5",
                "Odpowiedź to 7 (bo 7 + 5 = 12)"
            ]
        )

        pitagoras = NPC(
            name="Pitagoras Maximus",
            ascii_art=ASCII_PITAGORAS,
            dialogues=[
                "WITAJ, WOJOWNIKU LICZB! 💪",
                "Jestem Pitagoras Maximus, strażnik Mathlandu!",
                "Tu rządzą RÓWNANIA! Aby przejść dalej...",
                "...musisz pokonać Równanie Strażnika!",
                "Wpisz 'rozwiąż' i pokaż co potrafisz!"
            ],
            puzzle=pita_puzzle
        )

        rownina = Location(
            name="Równina Równań",
            description="Rozległa równina. Wszędzie latają cyfry i znaki "
                       "matematyczne. Gigantyczne równania wiszą w powietrzu.",
            ascii_art=ASCII_ROWNINA,
            npcs=[pitagoras],
            exits={'hub': 'hub', 'powrót': 'hub', 'dalej': 'piramida'}
        )

        zero_puzzle = Puzzle(
            question='Twierdzenie Pitagorasa:\na² + b² = c²\n\n'
                    'Jeśli a = 3 i b = 4, ile wynosi c?\n'
                    '(Podpowiedź: 3² = 9, 4² = 16)',
            options=None,
            correct='5',
            hints=[
                "Podstaw do wzoru: 3² + 4² = c²",
                "Oblicz: 9 + 16 = 25 = c²",
                "c² = 25, więc c = √25 = 5"
            ]
        )

        zero = NPC(
            name="Zero Bohater",
            ascii_art=ASCII_ZERO,
            dialogues=[
                "Hej... jestem Zero. Nic nie znaczę... dosłownie.",
                "*wzdycha* Ale może pomogę ci, jeśli...",
                "...jeśli udowodnisz, że matematyka ma sens?",
                "Oto trójkąt prostokątny. Znasz twierdzenie Pitagorasa?",
                "Wpisz 'rozwiąż' i oblicz przeciwprostokątną!"
            ],
            puzzle=zero_puzzle
        )

        piramida = Location(
            name="Piramida Pitagorasa",
            description="Gigantyczna piramida zbudowana z trójkątów prostokątnych. "
                       "Na wejściu wielki napis: 'a² + b² = c²'",
            ascii_art=ASCII_PIRAMIDA,
            npcs=[zero],
            exits={'powrót': 'rownina_rownan', 'hub': 'hub'}
        )

        # ==================== ANGIELSKI ====================
        zosia_puzzle = Puzzle(
            question='Przetłumacz na polski:\n"I have a cat and a dog."',
            options=[
                'a) Mam kota i pies',
                'b) Ja mam kot i psa',
                'c) Mam kota i psa'
            ],
            correct=2,  # odpowiedź C
            hints=[
                "Pamiętaj o poprawnej odmianie w języku polskim!",
                "'have' = 'mam', 'cat' = 'kot', 'dog' = 'pies'",
                "Poprawna odpowiedź to C - 'Mam kota i psa'"
            ]
        )

        zosia = NPC(
            name="Zosia ze Słownika",
            ascii_art=ASCII_ZOSIA,
            dialogues=[
                "Yo, bestie! Widzę, że jesteś new here! 📱",
                "This quest is giving main character energy, no cap fr fr!",
                "Ale żeby przejść dalej, musisz rozumieć English.",
                "It's not that hard, trust me!",
                "Wpisz 'rozwiąż' and let's gooo! 🚀"
            ],
            puzzle=zosia_puzzle
        )

        slang = Location(
            name="Slang Street",
            description="Ulica pełna neonów z angielskimi napisami. "
                       "Wszędzie słychać 'COOL!', 'AWESOME!', 'NO CAP!'",
            ascii_art=ASCII_SLANG,
            npcs=[zosia],
            exits={'hub': 'hub', 'powrót': 'hub', 'dalej': 'town_of_tenses'}
        )

        shakespeare_puzzle = Puzzle(
            question='Uzupełnij czasownik "to be" w czasie teraźniejszym:\n\n'
                    'I ___\nYou ___\nHe/She ___\n\n'
                    'Wpisz odpowiedzi oddzielone przecinkami (np: am,are,is)',
            options=None,
            correct='am,are,is',
            hints=[
                "I AM, You ARE, He/She IS - pamiętasz?",
                "AM dla 'I', ARE dla 'You', IS dla 'He/She/It'",
                "Odpowiedź: am,are,is"
            ]
        )

        shakespeare = NPC(
            name="Sir Shakespire",
            ascii_art=ASCII_SHAKESPEARE,
            dialogues=[
                "To learn or not to learn, that IS the question! 🎭",
                "Welcome, young scholar! I am Sir Shakespire!",
                "Thou must prove thy knowledge of English grammar!",
                "The verb 'to be' - the foundation of all!",
                "Type 'rozwiąż' and show me what you know!"
            ],
            puzzle=shakespeare_puzzle
        )

        tenses = Location(
            name="Town of Tenses",
            description="Miasto podzielone na strefy czasowe: PAST, NOW, FUTURE. "
                       "Ludzie chodzą między nimi zmieniając formy czasowników.",
            ascii_art=ASCII_TENSES,
            npcs=[shakespeare],
            exits={'powrót': 'slang_street', 'hub': 'hub'}
        )

        # Dodaj wszystkie lokacje do gry
        self.locations = {
            'hub': hub,
            'las_przecinkowy': las,
            'jaskinia_ortografii': jaskinia,
            'rownina_rownan': rownina,
            'piramida': piramida,
            'slang_street': slang,
            'town_of_tenses': tenses
        }

    # ==================== WYŚWIETLANIE ====================

    def clear_screen(self):
        """Wyczyść ekran"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def slow_print(self, text: str, delay: float = DELAY_CHAR):
        """Drukuj tekst z efektem maszyny do pisania"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def print_separator(self):
        """Drukuj separator"""
        print(Colors.CYAN + "═" * WIDTH + Colors.RESET)

    def print_box(self, text: str, color: str = Colors.YELLOW):
        """Drukuj tekst w ramce"""
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        print(color + "╭" + "─" * (max_len + 2) + "╮" + Colors.RESET)
        for line in lines:
            print(color + "│ " + line.ljust(max_len) + " │" + Colors.RESET)
        print(color + "╰" + "─" * (max_len + 2) + "╯" + Colors.RESET)

    def print_ascii(self, art: str):
        """Drukuj ASCII art"""
        print(Colors.CYAN + art + Colors.RESET)

    def print_dialogue(self, speaker: str, text: str):
        """Drukuj dialog"""
        print(f"\n{Colors.YELLOW}{speaker}:{Colors.RESET}")
        self.slow_print(f'  "{text}"', DELAY_FAST)

    def print_location(self):
        """Wyświetl aktualną lokację"""
        loc = self.current_location
        self.clear_screen()
        self.print_separator()
        print(f"{Colors.BOLD}{Colors.GREEN}📍 {loc.name}{Colors.RESET}")
        self.print_separator()
        print()
        self.print_ascii(loc.ascii_art)
        print()
        self.slow_print(loc.description, DELAY_FAST)
        print()

        if loc.npcs:
            npcs_names = [npc.name for npc in loc.npcs]
            print(f"{Colors.MAGENTA}Widzisz: {', '.join(npcs_names)}{Colors.RESET}")

        if loc.exits:
            exits_str = ', '.join(loc.exits.keys())
            print(f"{Colors.BLUE}Wyjścia: {exits_str}{Colors.RESET}")

        print()

    # ==================== KOMENDY ====================

    def show_help(self):
        """Pokaż pomoc"""
        help_text = """
╔══════════════════════════════════════════════════════════╗
║                    📖 POMOC                              ║
╠══════════════════════════════════════════════════════════╣
║  idź [kierunek]    - idź w podanym kierunku             ║
║  rozmawiaj [kto]   - porozmawiaj z postacią             ║
║  rozwiąż           - rozwiąż zagadkę                     ║
║  plecak            - zobacz ekwipunek                    ║
║  mapa              - pokaż mapę świata                   ║
║  pomoc             - ta pomoc                            ║
║  wyjdź             - zakończ grę                         ║
╚══════════════════════════════════════════════════════════╝
        """
        print(Colors.CYAN + help_text + Colors.RESET)

    def show_map(self):
        """Pokaż mapę"""
        print(Colors.CYAN + """
╔══════════════════════════════════════════════════════════╗
║                    🗺️  MAPA ŚWIATA                       ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║                  ┌─────────────────┐                     ║
║                  │ BIBLIOTECZNY    │                     ║
║                  │     LIMBO       │                     ║
║                  └────────┬────────┘                     ║
║           ┌───────────────┼───────────────┐              ║
║           │               │               │              ║
║           ▼               ▼               ▼              ║
║    ┌────────────┐  ┌────────────┐  ┌────────────┐        ║
║    │ POLSZCZYZNA│  │  MATHLAND  │  │  ANGLOLAD  │        ║
║    │  PRZEKLĘTA │  │            │  │            │        ║
║    │    ⭐      │  │    ⭐⭐    │  │   ⭐⭐⭐   │        ║
║    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘        ║
║          │               │               │               ║
║          ▼               ▼               ▼               ║
║    ┌──────────┐    ┌──────────┐    ┌──────────┐          ║
║    │   Las    │    │ Równina  │    │  Slang   │          ║
║    │Przecink. │    │ Równań   │    │  Street  │          ║
║    └────┬─────┘    └────┬─────┘    └────┬─────┘          ║
║         │               │               │                ║
║         ▼               ▼               ▼                ║
║    ┌──────────┐    ┌──────────┐    ┌──────────┐          ║
║    │ Jaskinia │    │ Piramida │    │  Town of │          ║
║    │Ortografii│    │Pitagorasa│    │  Tenses  │          ║
║    └──────────┘    └──────────┘    └──────────┘          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """ + Colors.RESET)

        # Pokaż status motywacji
        print("\n📊 Status Motywacji:")
        for subject, obtained in self.player.motivations.items():
            status = "✅" if obtained else "❌"
            print(f"  {status} {subject.capitalize()}")

    def show_inventory(self):
        """Pokaż ekwipunek"""
        print(f"\n{Colors.YELLOW}🎒 PLECAK:{Colors.RESET}")
        if self.player.inventory:
            for item in self.player.inventory:
                print(f"  • {item}")
        else:
            print("  (pusty)")

        print(f"\n{Colors.GREEN}⭐ MOTYWACJE:{Colors.RESET}")
        for subject, obtained in self.player.motivations.items():
            status = "✅" if obtained else "⬜"
            print(f"  {status} {subject.capitalize()}")

        print(f"\n{Colors.CYAN}💰 Punkty: {self.player.score}{Colors.RESET}")

    def go_to(self, direction: str):
        """Idź do innej lokacji"""
        if not direction:
            print("Gdzie chcesz iść? Wpisz 'idź [kierunek]'")
            return

        direction = direction.lower().strip()
        exits = self.current_location.exits

        if direction in exits:
            next_loc_id = exits[direction]

            # Sprawdź czy można przejść (czy rozwiązano zagadki)
            if self.current_location.name == "Las Przecinkowy" and direction == 'dalej':
                geralt = self.current_location.get_npc("Geralt")
                if geralt and geralt.puzzle and not geralt.puzzle.solved:
                    print("\n⚠️ Geralt blokuje przejście! Najpierw rozwiąż jego zagadkę.")
                    return

            if self.current_location.name == "Równina Równań" and direction == 'dalej':
                pita = self.current_location.get_npc("Pitagoras")
                if pita and pita.puzzle and not pita.puzzle.solved:
                    print("\n⚠️ Pitagoras nie przepuści cię bez rozwiązania równania!")
                    return

            if self.current_location.name == "Slang Street" and direction == 'dalej':
                zosia = self.current_location.get_npc("Zosia")
                if zosia and zosia.puzzle and not zosia.puzzle.solved:
                    print("\n⚠️ Zosia chce najpierw sprawdzić twój angielski!")
                    return

            self.current_location = self.locations[next_loc_id]
            self.print_location()
        else:
            print(f"Nie możesz tam iść. Dostępne kierunki: {', '.join(exits.keys())}")

    def talk_to(self, npc_name: str):
        """Porozmawiaj z NPC"""
        if not npc_name:
            if self.current_location.npcs:
                npc = self.current_location.npcs[0]
            else:
                print("Z kim chcesz rozmawiać?")
                return
        else:
            npc = self.current_location.get_npc(npc_name)

        if not npc:
            print(f"Nie widzisz tutaj nikogo o imieniu '{npc_name}'")
            return

        self.print_ascii(npc.ascii_art)
        dialogue = npc.talk()
        self.print_dialogue(npc.name, dialogue)

        # Kontynuuj dialog jeśli jest więcej
        while npc.dialogue_index < len(npc.dialogues):
            input(f"\n{Colors.CYAN}[Naciśnij ENTER aby kontynuować...]{Colors.RESET}")
            dialogue = npc.talk()
            self.print_dialogue(npc.name, dialogue)

    def solve_puzzle(self):
        """Rozwiąż zagadkę"""
        # Znajdź NPC z zagadką
        puzzle_npc = None
        for npc in self.current_location.npcs:
            if npc.puzzle and not npc.puzzle.solved:
                puzzle_npc = npc
                break
            # Sprawdź drugą zagadkę Yennefer
            if hasattr(npc, 'puzzle2') and hasattr(npc, 'current_puzzle'):
                if npc.current_puzzle == 2 and not npc.puzzle2.solved:
                    puzzle_npc = npc
                    break

        if not puzzle_npc:
            print("Nie ma tu żadnej zagadki do rozwiązania.")
            return

        # Pobierz aktualną zagadkę
        if hasattr(puzzle_npc, 'current_puzzle') and puzzle_npc.current_puzzle == 2:
            puzzle = puzzle_npc.puzzle2
        else:
            puzzle = puzzle_npc.puzzle

        print(f"\n{Colors.YELLOW}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}🧩 ZAGADKA od {puzzle_npc.name}:{Colors.RESET}")
        print(f"\n{puzzle.question}\n")

        if puzzle.options:
            for opt in puzzle.options:
                print(f"  {opt}")
            print()

        answer = input(f"{Colors.GREEN}Twoja odpowiedź: {Colors.RESET}").strip()

        if puzzle.check_answer(answer):
            print(f"\n{Colors.GREEN}✅ BRAWO! Poprawna odpowiedź!{Colors.RESET}")
            puzzle.solved = True
            self.player.score += puzzle.points

            # Specjalna logika dla Yennefer (2 zagadki)
            if hasattr(puzzle_npc, 'current_puzzle'):
                if puzzle_npc.current_puzzle == 1:
                    print(f"\n{Colors.YELLOW}{puzzle_npc.name}:{Colors.RESET} Świetnie! Ale to nie koniec...")
                    puzzle_npc.current_puzzle = 2
                    print("Mam jeszcze jedno zadanie! Wpisz 'rozwiąż' ponownie.")
                    return

            # Sprawdź czy to była ostatnia zagadka w krainie
            self._check_realm_complete()
        else:
            hint = puzzle.get_hint()
            print(f"\n{Colors.RED}❌ Niestety, to nie jest poprawna odpowiedź.{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 Wskazówka: {hint}{Colors.RESET}")

            if puzzle.attempts >= 3:
                print(f"\n{Colors.MAGENTA}Nie poddawaj się! Spróbuj jeszcze raz.{Colors.RESET}")

    def _check_realm_complete(self):
        """Sprawdź czy ukończono krainę"""
        loc_name = self.current_location.name

        # Polski - Jaskinia Ortografii
        if loc_name == "Jaskinia Ortografii":
            yen = self.current_location.get_npc("Yennefer")
            if yen and yen.puzzle.solved and hasattr(yen, 'puzzle2') and yen.puzzle2.solved:
                if not self.player.motivations['polski']:
                    self.player.motivations['polski'] = True
                    self.player.add_item("🪶 Motywacja Polskiego")
                    print(f"\n{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    print(f"{Colors.BOLD}🎉 ZDOBYŁEŚ MOTYWACJĘ Z POLSKIEGO! 🪶{Colors.RESET}")
                    print(f"{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    self._check_victory()

        # Matematyka - Piramida
        elif loc_name == "Piramida Pitagorasa":
            zero = self.current_location.get_npc("Zero")
            if zero and zero.puzzle.solved:
                if not self.player.motivations['matematyka']:
                    self.player.motivations['matematyka'] = True
                    self.player.add_item("🔢 Motywacja Matematyki")
                    print(f"\n{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    print(f"{Colors.BOLD}🎉 ZDOBYŁEŚ MOTYWACJĘ Z MATEMATYKI! 🔢{Colors.RESET}")
                    print(f"{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    # Zero jest szczęśliwy
                    print(f"\n{Colors.YELLOW}Zero:{Colors.RESET} Wow... matematyka NAPRAWDĘ ma sens! Dziękuję! 😊")
                    self._check_victory()

        # Angielski - Town of Tenses
        elif loc_name == "Town of Tenses":
            shakespeare = self.current_location.get_npc("Sir Shakespire")
            if shakespeare and shakespeare.puzzle.solved:
                if not self.player.motivations['angielski']:
                    self.player.motivations['angielski'] = True
                    self.player.add_item("🏴 Motywacja Angielskiego")
                    print(f"\n{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    print(f"{Colors.BOLD}🎉 ZDOBYŁEŚ MOTYWACJĘ Z ANGIELSKIEGO! 🏴{Colors.RESET}")
                    print(f"{Colors.GREEN}{'═' * 50}{Colors.RESET}")
                    print(f"\n{Colors.YELLOW}Sir Shakespire:{Colors.RESET} Excellent! Thou art a true scholar! 🎭")
                    self._check_victory()

    def _check_victory(self):
        """Sprawdź czy gracz wygrał"""
        if self.player.motivation_count() == 3:
            self._show_ending()

    def _show_ending(self):
        """Pokaż zakończenie gry"""
        input(f"\n{Colors.CYAN}[Naciśnij ENTER aby kontynuować...]{Colors.RESET}")
        self.clear_screen()

        print(Colors.YELLOW + ASCII_MOTIVATION + Colors.RESET)
        time.sleep(2)

        print(f"\n{Colors.BOLD}Księga Wiedzy:{Colors.RESET}")
        self.slow_print('"YOOO! Masz wszystkie trzy kawałki! Poskładajmy je!"')
        time.sleep(1)

        print("\n⭐ Składanie Motywacji... ⭐\n")
        for i in range(3):
            time.sleep(0.5)
            print("▓" * ((i + 1) * 15))

        time.sleep(1)
        self.clear_screen()
        print(Colors.GREEN + ASCII_VICTORY + Colors.RESET)

        # Statystyki
        elapsed = time.time() - self.player.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        print(f"\n{Colors.CYAN}📊 STATYSTYKI:{Colors.RESET}")
        print(f"  ⏱️  Czas gry: {minutes}:{seconds:02d}")
        print(f"  💰 Punkty: {self.player.score}")
        print(f"  🎒 Przedmioty: {len(self.player.inventory)}")

        print(f"\n{Colors.YELLOW}Księga Wiedzy:{Colors.RESET}")
        self.slow_print('"Dzięki, ziomek! Motywacja wraca! Czuję się jak nowo narodzony!"')
        self.slow_print('"Ale to dopiero początek. Są jeszcze inne przedmioty..."')
        self.slow_print('"Geografia, Fizyka, Informatyka... TO BE CONTINUED!"')

        print(f"\n{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}Dziękujemy za grę w PARADOKSJĘ!{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")

        input("\n[Naciśnij ENTER aby zakończyć...]")
        self.running = False

    # ==================== PĘTLA GRY ====================

    def parse_command(self, command: str):
        """Parsuj komendę gracza"""
        parts = command.lower().strip().split(maxsplit=1)
        if not parts:
            return

        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ['pomoc', 'help', '?']:
            self.show_help()
        elif cmd in ['mapa', 'map']:
            self.show_map()
        elif cmd in ['plecak', 'ekwipunek', 'inventory', 'i']:
            self.show_inventory()
        elif cmd in ['idź', 'idz', 'go', 'id']:
            self.go_to(arg)
        elif cmd in ['rozmawiaj', 'talk', 'gadaj', 'r']:
            self.talk_to(arg)
        elif cmd in ['rozwiąż', 'rozwiaz', 'solve', 'zagadka']:
            self.solve_puzzle()
        elif cmd in ['patrz', 'look', 'l', 'rozejrzyj']:
            self.print_location()
        elif cmd in ['wyjdź', 'wyjdz', 'quit', 'exit', 'q']:
            if input("Czy na pewno chcesz wyjść? (t/n): ").lower() in ['t', 'tak', 'y', 'yes']:
                self.running = False
        else:
            print(f"Nie rozumiem komendy '{cmd}'. Wpisz 'pomoc' aby zobaczyć listę komend.")

    def show_intro(self):
        """Pokaż intro gry"""
        self.clear_screen()
        print(Colors.YELLOW + ASCII_TITLE + Colors.RESET)

        print(f"\n{Colors.CYAN}Naciśnij ENTER aby rozpocząć przygodę...{Colors.RESET}")
        input()

        self.clear_screen()
        print(f"\n{Colors.BOLD}📍 Szkoła, godzina 16:30{Colors.RESET}")
        print("═" * 40)

        self.slow_print("\nJesteś sam w pustej szkole po lekcjach.")
        time.sleep(0.5)
        self.slow_print("Masz napisać poprawkę z polskiego, ale...")
        time.sleep(0.5)
        self.slow_print("...nie możesz znaleźć właściwej sali.")
        time.sleep(0.5)

        self.slow_print("\nBłądzisz korytarzami gdy nagle...")
        time.sleep(0.5)
        self.slow_print("...zauważasz dziwne światło z pokoju nauczycielskiego.")

        input(f"\n{Colors.CYAN}[ENTER aby zajrzeć do środka...]{Colors.RESET}")

        self.clear_screen()
        print(Colors.MAGENTA + ASCII_BOOK + Colors.RESET)

        self.slow_print("\nNa stole leży WIELKA KSIĘGA WIEDZY.")
        self.slow_print("Świeci neonowym światłem jak telefon w nocy.")
        self.slow_print("Księga otwiera się sama...")

        time.sleep(1)
        print(f"\n{Colors.YELLOW}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}Księga Wiedzy:{Colors.RESET}")
        self.slow_print('"LOL, w końcu ktoś przyszedł!"')
        self.slow_print('"Mam problem, mordo. Uciekła mi MOTYWACJA."')
        self.slow_print('"Rozpierzchła się po trzech Krainach Przedmiotów."')
        self.slow_print('"Bez niej wiedza to dead content, rozumiesz?"')
        self.slow_print('"Masz 40 minut, zanim zjawi się pani od polskiego."')
        print(f"{Colors.YELLOW}{'═' * 50}{Colors.RESET}")

        while True:
            choice = input(f"\n{Colors.GREEN}Pomożesz Księdze? (tak/nie): {Colors.RESET}").lower()
            if choice in ['tak', 't', 'yes', 'y']:
                break
            elif choice in ['nie', 'n', 'no']:
                print("\nKsięga: 'No dobra, to idź na tę poprawkę... boring.'")
                print("(Ale tak naprawdę musisz pomóc, to gra edukacyjna! 😉)")
            else:
                print("Wpisz 'tak' lub 'nie'")

        self.slow_print("\nKsięga: 'Wiedziałem! No to jedziemy z tym koksem!'")
        self.slow_print("*Świat wiruje... wciąga cię do środka księgi...*")

        time.sleep(1)
        self.game_started = True
        self.player.start_time = time.time()

    def run(self):
        """Główna pętla gry"""
        self.show_intro()

        if not self.game_started:
            return

        # Rozpocznij w Hubie
        self.current_location = self.locations['hub']
        self.print_location()

        # Automatyczna rozmowa z Notką na start
        notka = self.current_location.get_npc("Notka")
        if notka:
            print(f"\n{Colors.MAGENTA}Ktoś do ciebie podchodzi...{Colors.RESET}")
            time.sleep(1)
            self.talk_to("Notka")

        # Główna pętla
        while self.running:
            try:
                command = input(f"\n{Colors.GREEN}> {Colors.RESET}").strip()
                if command:
                    self.parse_command(command)
            except KeyboardInterrupt:
                print("\n\nDo zobaczenia!")
                break
            except EOFError:
                break


# ============================================================================
# URUCHOMIENIE
# ============================================================================

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        print("Jeśli problem się powtarza, zgłoś go nauczycielowi.")
        input("\n[Naciśnij ENTER aby zamknąć...]")
