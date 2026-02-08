#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARADOKSJA: Część I - Uciekająca Motywacja
Edukacyjna gra tekstowa dla uczniów klas 5-6
Wersja z pełną narracją literacką

Autor: Claude AI
Wersja: 2.0
"""

import os
import sys
import time
import shutil
import textwrap
import re
from typing import Dict, List, Optional

# ============================================================================
# KONFIGURACJA
# ============================================================================

WIDTH = 60
NARRATOR_DELAY = 0.025
FAST_DELAY = 0.015
SLOW_DELAY = 0.045

# ============================================================================
# CENTROWANIE
# ============================================================================

def get_terminal_width() -> int:
    """Pobierz szerokość terminala"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def strip_ansi(text: str) -> str:
    """Usuń kody ANSI z tekstu (do liczenia długości)"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_line(text: str) -> str:
    """Wyśrodkuj pojedynczą linię"""
    term_width = get_terminal_width()
    visible_length = len(strip_ansi(text))
    padding = max(0, (term_width - visible_length) // 2)
    return ' ' * padding + text

def center_block(text: str) -> str:
    """Wyśrodkuj blok tekstu (każdą linię osobno)"""
    lines = text.split('\n')
    centered_lines = [center_line(line) if line.strip() else '' for line in lines]
    return '\n'.join(centered_lines)

def cprint(text: str = ''):
    """Wydrukuj wyśrodkowany tekst"""
    if text:
        print(center_block(text))
    else:
        print()

def cinput(prompt: str = '') -> str:
    """Wyśrodkowany input"""
    if prompt:
        print(center_line(prompt), end='')
    return input()

# Kolory ANSI
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'  # Same as yellow but semantically different

# Windows compatibility
if os.name == 'nt':
    try:
        os.system('color')
    except:
        for attr in dir(C):
            if not attr.startswith('_'):
                setattr(C, attr, '')

# ============================================================================
# ASCII ART
# ============================================================================

TITLE_ART = f"""
{C.GOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     ██████╗  █████╗ ██████╗  █████╗ ██████╗  ██████╗  ║
    ║     ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗ ║
    ║     ██████╔╝███████║██████╔╝███████║██║  ██║██║   ██║ ║
    ║     ██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║  ██║██║   ██║ ║
    ║     ██║     ██║  ██║██║  ██║██║  ██║██████╔╝╚██████╔╝ ║
    ║     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ║
    ║                      K S J A                          ║
    ║                                                       ║
    ║          ~ Przygoda w Krainie Wiedzy ~                ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
{C.RESET}"""

BOOK_ART = f"""
{C.CYAN}
              ⚡ ✨ KSIĘGA ✨ ⚡
                   ___________
                  /           \\
                 /  _________  \\
                /  /         \\  \\
               |  | ◉     ◉ |  |
               |  |    ▼    |  |
               |  |  \\___/  |  |
                \\  \\_______/  /
                 \\___________/
                ╱╱╱╱╱╱╱╱╱╱╱╱╱
               Świeci. Wibruje.
{C.RESET}"""

HUB_ART = f"""
{C.BLUE}
         ✨  📚    📖    📚  ✨
       🗂️                      🗂️
            [ BIBLIOTECZNY ]
            [    LIMBO     ]
       📋                      📋
         ✨  📚    📖    📚  ✨
{C.RESET}"""

PORTAL_ART = f"""
{C.CYAN}
    ╔═════════════════════════════════════════════╗
    ║              PORTALE DO KRAIN               ║
    ╠═════════════════════════════════════════════╣
    ║                                             ║
    ║   🪶 [1] POLSZCZYZNA PRZEKLĘTA    ⭐       ║
    ║       "Tam, gdzie przecinki rosną..."      ║
    ║                                             ║
    ║   🔢 [2] MATHLANDIA               ⭐⭐     ║
    ║       "Kraina, gdzie 2+2=5..."             ║
    ║                                             ║
    ║   🇬🇧 [3] ANGLOLAD                 ⭐⭐⭐   ║
    ║       "Where everything is możliwe..."     ║
    ║                                             ║
    ╚═════════════════════════════════════════════╝
{C.RESET}"""

NOTKA_ART = f"""
{C.YELLOW}
            📄
           (• ‿ •)
             / \\
          ~ NOTKA ~
{C.RESET}"""

GERALT_ART = f"""
{C.CYAN}
            ⚔️
           /|\\
          / | \\
            |
           / \\
    ~ GERALT z POLSZCZYZNY ~
{C.RESET}"""

PITAGORAS_ART = f"""
{C.BLUE}
            📐
           /|\\
          △ | △
            |
           / \\
       ~ PITAGORAS ~
{C.RESET}"""

ZOSIA_ART = f"""
{C.MAGENTA}
            🎧
          (◕‿◕)
          /|📱|\\
            ||
           / \\
      ~ ZOSIA GEN Z ~
{C.RESET}"""

SHAKESPEARE_ART = f"""
{C.RED}
            🎭
          /|\\
         / | \\
        📜 | 🪶
           / \\
      ~ SHAKESPEARE ~
{C.RESET}"""

VICTORY_ART = f"""
{C.GOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║                    🏆 ZWYCIĘSTWO! 🏆                  ║
    ║                                                       ║
    ║         Ukończyłeś PARADOKSJĘ: Część I                ║
    ║                                                       ║
    ║   ═══════════════════════════════════════════════     ║
    ║                                                       ║
    ║         ⭐ MOTYWACJA ODZYSKANA! ⭐                    ║
    ║                                                       ║
    ║         📚 Polski:      ✓ ZDOBYTY                     ║
    ║         🔢 Matematyka:  ✓ ZDOBYTA                     ║
    ║         🇬🇧 Angielski:   ✓ ZDOBYTY                     ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
{C.RESET}"""

MOTIVATION_MERGE_ART = f"""
{C.GOLD}
              ✨  ✨  ✨
           📚  🔢  🇬🇧
              \\  |  /
               \\ | /
                \\|/
             ⚡💎⚡
                |
             📖📖📖
           MOTYWACJA!
{C.RESET}"""

# ============================================================================
# KLASA GRY
# ============================================================================

class Game:
    def __init__(self):
        self.running = True
        self.score = 0
        self.motivations = []
        self.inventory = []
        self.hints_used = 0
        self.puzzles_solved = []
        self.current_location = 'hub'
        self.start_time = 0

    # ======================== WYŚWIETLANIE ========================

    def clear(self):
        """Wyczyść ekran"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self, prompt="[Naciśnij ENTER aby kontynuować...]"):
        """Czekaj na ENTER"""
        cprint(f"\n{C.DIM}{prompt}{C.RESET}")
        input(center_line(""))

    def divider(self, char="═", length=WIDTH):
        """Wyświetl separator"""
        cprint(f"{C.GOLD}{char * length}{C.RESET}")

    def narrator(self, text: str, delay: float = NARRATOR_DELAY):
        """Narracja z efektem maszyny do pisania"""
        term_width = get_terminal_width()

        # Przetwórz tekst - zawiń i wyśrodkuj
        lines = []
        for paragraph in text.split('\n'):
            stripped = paragraph.strip()
            if stripped:
                # Sprawdź czy to kolorowany tekst (zaczyna się od \033)
                if '\033[' in stripped:
                    # Kolorowany tekst - nie zawijaj, wyświetl jako jest
                    lines.append(stripped)
                else:
                    # Zwykły tekst - zawiń do WIDTH
                    wrapped = textwrap.wrap(stripped, width=WIDTH - 4)
                    lines.extend(wrapped)
                lines.append('')
            else:
                lines.append('')

        for line in lines:
            # Oblicz padding dla centrowania
            visible_len = len(strip_ansi(line))
            line_padding = max(0, (term_width - visible_len) // 2)
            print(' ' * line_padding, end='')

            # Efekt maszyny do pisania (pomijamy kody ANSI w opóźnieniu)
            i = 0
            while i < len(line):
                # Sprawdź czy to początek kodu ANSI
                if line[i:i+2] == '\033[':
                    # Znajdź koniec kodu ANSI
                    end = line.find('m', i)
                    if end != -1:
                        print(line[i:end+1], end='', flush=True)
                        i = end + 1
                        continue

                char = line[i]
                print(char, end='', flush=True)
                if char in '.!?':
                    time.sleep(delay * 6)
                elif char in ',;:':
                    time.sleep(delay * 3)
                else:
                    time.sleep(delay)
                i += 1
            print()

    def fast_print(self, text: str):
        """Szybkie wyświetlanie"""
        self.narrator(text, FAST_DELAY)

    def dialog(self, speaker: str, text: str, color: str = C.YELLOW):
        """Wyświetl dialog postaci"""
        cprint(f"\n{color}╭─ {speaker} ─╮{C.RESET}")
        wrapped = textwrap.wrap(text, width=WIDTH-4)
        for line in wrapped:
            cprint(f'{color}│{C.RESET} {C.ITALIC}"{line}"{C.RESET}')
        cprint(f"{color}╰{'─' * (len(speaker) + 4)}╯{C.RESET}")

    def action(self, text: str):
        """Wyświetl akcję/komentarz gracza"""
        cprint(f"\n{C.DIM}[{text}]{C.RESET}")

    def emphasis(self, text: str) -> str:
        """Tekst wyróżniony"""
        return f"{C.GOLD}{text}{C.RESET}"

    def loud(self, text: str) -> str:
        """Tekst głośny/krzyk"""
        return f"{C.RED}{C.BOLD}{text}{C.RESET}"

    def whisper(self, text: str) -> str:
        """Tekst szeptany"""
        return f"{C.DIM}{C.ITALIC}{text}{C.RESET}"

    def meta(self, text: str) -> str:
        """Komentarz meta-narracyjny"""
        return f"{C.MAGENTA}{text}{C.RESET}"

    def thought(self, text: str) -> str:
        """Myśl gracza"""
        return f"{C.BLUE}{C.ITALIC}{text}{C.RESET}"

    # ======================== INTRO ========================

    def show_title(self):
        """Ekran tytułowy"""
        self.clear()
        cprint(TITLE_ART)
        cprint(f"\n{C.DIM}Gra edukacyjna dla uczniów klas 5-6{C.RESET}")
        cprint(f"{C.DIM}Polski • Matematyka • Angielski{C.RESET}")
        self.pause("\n[Naciśnij ENTER aby rozpocząć...]")

    def intro_school(self):
        """Prolog - pusta szkoła"""
        self.clear()
        cprint(f"\n{C.DIM}╔══════════════════════════════════════════════════════╗{C.RESET}")
        cprint(f"{C.GOLD}                        PROLOG{C.RESET}")
        cprint(f"{C.DIM}╚══════════════════════════════════════════════════════╝{C.RESET}")
        cprint()

        self.narrator("Piątek. 16:30.")
        time.sleep(0.5)

        self.narrator(f"\nSzkoła Podstawowa nr 7 jest pusta. Prawie.")
        time.sleep(0.3)

        self.narrator(f"\n{self.emphasis('Ty')} jesteś tutaj. Oczywiście. Bo przecież kto normalny wychodzi ze szkoły o normalnej porze, prawda?")

        self.narrator(f"\nPoprawka ze sprawdzianu z polskiego. Pani Kowalska powiedziała, że {self.thought('to dla twojego dobra')}. Pewnie. Dla dobra. Jak praktycznie wszystko, co dorośli każą ci robić w piątek po lekcjach.")

        self.narrator(f"\nIdziesz korytarzem. Twoje kroki odbijają się echem. Gdzieś kapie woda. Lampy migają.")

        self.narrator(f"\n{self.meta('Normalka. Szkoła po godzinach zawsze przypomina film grozy, tylko zamiast zombi są sterty zeszytów i plakaty o higienie.')}")

        self.pause()

    def intro_door(self):
        """Odkrycie drzwi"""
        self.clear()
        cprint(f"\n{C.DIM}═══════════════════════════════════════════════════════{C.RESET}")
        cprint(f"{C.GOLD}Korytarz - Drugie piętro{C.RESET}")
        cprint(f"{C.DIM}═══════════════════════════════════════════════════════{C.RESET}\n")

        self.narrator("Masz znaleźć salę 217. Ale... czekaj. Nie było sali 217 na drugim piętrze? Jesteś pewien, że była 217, a nie 207...?")

        self.narrator(f"\nBłądzisz. {self.meta('Oczywiście. Bo dlaczego miałoby być łatwo.')}")

        self.narrator("\nI wtedy to widzisz.")
        time.sleep(0.5)

        self.narrator(f"\nDrzwi do {self.emphasis('pokoju nauczycielskiego')} są uchylone.")

        self.narrator(f"\nNigdy nie są uchylone. {self.loud('NIGDY.')}")

        self.narrator(f"\n{self.meta('To jest jak Strefa 51 tej szkoły — wchodzisz tam tylko, jeśli masz przesłuchanie albo jesteś w NAPRAWDĘ dużych tarapatach.')}")

        self.narrator(f"\nAle przez szparę sączy się... {self.emphasis('światło')}. Niebieskie. Pulsujące. Jak ekran telefonu w nocy, tylko... jaśniejsze. Dziwniejsze.")

        self.narrator("\nPodchodzisz.")

        self.narrator(f"\n{self.meta('Oczywiście, że podchodzisz. Bo jesteś ciekawy. Albo głupi. Albo jedno i drugie.')}")

        self.narrator("\nPchniesz drzwi.")
        time.sleep(0.3)
        self.narrator("\nI zamierasz.")

        self.pause()

    def intro_book(self):
        """Odkrycie Księgi"""
        self.clear()
        cprint(BOOK_ART)

        self.narrator("Na biurku leży książka. Ale nie zwykła książka.")

        self.narrator(f"\nTo jest... no, powiedzmy sobie szczerze — to jest {self.loud('GRUBA')} księga. Z tych, które ważą tyle co twój plecak w poniedziałek. Oprawa ze skóry {self.whisper('(przynajmniej masz nadzieję, że to skóra)')}. Złote okucia. Dziwne runy na okładce.")

        self.narrator(f"\nI {self.emphasis('świeci')}. Jasnym, niebieskim światłem.")

        self.narrator("\nPodchodzisz bliżej. Księga... drży? Wibruje jak telefon na wibracji? Co do—")

        time.sleep(0.5)
        self.narrator(f"\nI nagle się {self.loud('OTWIERA')}.")

        cprint(f"\n{C.RED}{C.BOLD}BACH!{C.RESET}")
        time.sleep(0.3)

        self.narrator("\nKartki same się przewracają. Szybko. Coraz szybciej. Litery zlatują ze stron. Dosłownie. Unoszą się w powietrzu.")

        self.narrator(f"\nA potem słyszysz {self.emphasis('GŁOS')}.")

        self.narrator(f"\nNie ma nikogo w pokoju. Ale głos jest. Młody. Męski. Lekko... {self.whisper('znudzony?')}")

        self.pause()

    def intro_dialog(self):
        """Rozmowa z Księgą"""
        self.clear()
        cprint(f"\n{C.GOLD}══════════════ Pokój nauczycielski ══════════════{C.RESET}\n")

        self.dialog("📚 Księga", "Wreszcie. WRESZCIE ktoś przyszedł. Myślałem, że tu zgnuję w tym pokoju pełnym kubków z niedopitą kawą i stosów kartkówek do sprawdzenia.")

        self.action("Milczysz. Bo co masz powiedzieć MÓWIĄCEJ KSIĄŻCE?")

        self.dialog("📚 Księga", "Ok, widzę, że jesteś w szoku. Rozumiem. Mówiąca księga, to niecodzienny widok, wiem. Ale nie mamy czasu na panikę, kolego. Mam problem. DUŻY problem.")

        self.action("Wciąż milczysz. Ale już nie uciekasz. To dobry znak.")

        self.dialog("📚 Księga", "Jestem Wielka Księga Wiedzy. Tak, brzmi pretensjonalnie, wiem. Mieszkam tutaj od... ee... nie pamiętam. Kilkadziesiąt lat? Może więcej? Czas w pokoju nauczycielskim płynie dziwnie.")

        self.pause()

        self.clear()
        cprint(f"\n{C.GOLD}══════════════ Pokój nauczycielski ══════════════{C.RESET}\n")

        self.dialog("📚 Księga", "Moja rola? Przechowuję wiedzę. Całą. No, prawie całą. Od historii dinozaurów po to, dlaczego 'rz' brzmi jak 'ż', ale pisze się inaczej.")

        self.action("Kiwasz głową. Bo pytanie o 'rz' i 'ż' zadajesz sobie od klasy trzeciej.")

        self.dialog("📚 Księga", "Ale jest haczyk. Wiedza bez MOTYWACJI jest bezużyteczna. Możesz mieć w głowie wszystkie wzory i daty, ale jeśli nie masz motywacji do nauki... to co z tego?")

        self.dialog("📚 Księga", "I tu dochodzimy do sedna sprawy. Moja Motywacja... UCIEKŁA.")

        self.action("Mrugasz. Czekaj, CO?")

        self.dialog("📚 Księga", "Tak, UCIEKŁA. Rozpierzchła się po Krainie Przedmiotów. Podzieliła się na kawałki. Polski, Matematyka, Angielski... wszystkie się rozłaziły.")

        self.dialog("📚 Księga", "Bez nich jestem tylko... zbiorem suchych faktów. Nudnych dat. Nijakiej wiedzy, którą i tak wszyscy scrollują na Wikipedii.")

        self.action("Patrzysz na księgę. Ona... wygląda na smutną? Czy księga może być smutna?")

        self.pause()

    def intro_choice(self):
        """Wybór gracza"""
        self.clear()
        cprint(f"\n{C.GOLD}══════════════ Pokój nauczycielski ══════════════{C.RESET}\n")

        self.dialog("📚 Księga", "Potrzebuję pomocy. Twojej pomocy. Musisz wejść do mojego świata — do Paradoksji — i odzyskać kawałki Motywacji.")

        self.dialog("📚 Księga", "Masz może... 40 minut? Zanim tu wpadnie pani Kowalska i zobaczy cię gadającego z książką. A wtedy to dopiero będzie POPRAWKA.")

        self.action("Zastanawiasz się. To brzmi absurdalnie. Ale...")

        self.dialog("📚 Księga", "No to co? Wchodzisz, czy ślisz się na poprawkę?")

        cprint(f"\n{C.GOLD}════════════════ TWÓJ WYBÓR ════════════════{C.RESET}")
        cprint(f"\n  {C.GREEN}[1]{C.RESET} \"Wchodzę.\" {self.whisper('(bo czemu nie)')}")
        cprint(f"  {C.RED}[2]{C.RESET} \"Uciekam stąd!\" {self.whisper('(game over)')}")

        while True:
            choice = cinput(f"\n{C.CYAN}Twój wybór (1/2): {C.RESET}").strip()
            if choice == '1':
                return True
            elif choice == '2':
                self.game_over_escape()
                return False
            else:
                cprint("Wpisz 1 lub 2")

    def game_over_escape(self):
        """Game over - ucieczka"""
        self.clear()
        cprint(f"\n{C.RED}══════════════ GAME OVER ══════════════{C.RESET}\n")

        self.narrator("Uciekasz.")

        self.narrator(f"\n{self.meta('Oczywiście, że uciekasz. To rozsądne. Mówiąca księga? Magiczne światy? Kto by w to wchodził?')}")

        self.narrator("\nWracasz do sali 207 (bo jednak była 207, nie 217). Piszesz poprawkę. Dostajesz trójkę z minusem.")

        self.narrator("\nWracasz do domu. Jesz kolację. Grasz w telefon. Idziesz spać.")

        self.narrator("\nI nigdy, przenigdy nie dowiesz się, co by było, gdybyś jednak wszedł do tej księgi.")

        cprint(f"\n{self.emphasis('Koniec.')}")

        cprint(f"\n{self.whisper('(No dobra, to był głupi wybór. Uruchom grę jeszcze raz, żeby spróbować mądrzej.)')}")

        input(f"\n{C.DIM}[Naciśnij ENTER aby zakończyć...]{C.RESET}")
        self.running = False

    def intro_transport(self):
        """Transport do Paradoksji"""
        self.clear()
        cprint(f"\n{C.GOLD}══════════════ Między światami ══════════════{C.RESET}\n")

        self.narrator("Wybierasz \"wchodzę\".")

        self.narrator(f"\n{self.meta('Oczywiście, że wybierasz.')}")

        self.narrator(f"\nKsięga uśmiecha się. Tak, {self.emphasis('UŚMIECHA SIĘ')}. Rysunki na okładce układają się w coś przypominającego uśmiech.")

        self.dialog("📚 Księga", "Wiedziałem, że nie jesteś frajerem. Trzymaj się!")

        self.narrator("\nI nagle—")

        cprint(f"\n{C.RED}{C.BOLD}SZUUUUUUUUUM!{C.RESET}")
        time.sleep(0.5)

        self.narrator(f"\nŚwiat się {self.loud('KRĘCI')}.")

        self.narrator("\nPokój nauczycielski wiruje jak bęben pralki. Ściany się rozmazują. Podłoga znika pod stopami.")

        self.narrator(f"\n{self.emphasis('Lecisz.')}")

        self.narrator("\nPrzez... kartki? Latające kartki? Litery przelatują obok twojej głowy. Przecinki świszczą jak pociski. Cyfry wirują jak liście w wichurze.")

        self.narrator("\nI nagle...")

        cprint(f"\n{C.RED}{C.BOLD}ŁUBUDU!{C.RESET}")
        time.sleep(0.3)

        self.narrator("\nLądowanie. Twarde. Na tyłku.")

        cprint(f"\n{self.thought('Auć.')}")

        self.narrator("\nWstajesz. Otrzepujesz spodnie. I rozglądasz się.")

        self.pause()

    # ======================== HUB ========================

    def hub_arrival(self):
        """Przybycie do Hubu"""
        self.clear()
        cprint(HUB_ART)

        cprint(f"\n{C.GOLD}═══════ ✨ BIBLIOTECZNY LIMBO ✨ ═══════{C.RESET}\n")

        self.narrator("Jesteś w... przestrzeni.")

        self.narrator("\nNie jest to pokój. Nie jest to korytarz. To jest... no, trudno powiedzieć.")

        self.narrator("\nWiszysz jakby w powietrzu. Pod tobą — biel. Nad tobą — biel. Wokół unoszą się kartki. Powoli. Leniwie. Jak ryby w akwarium.")

        self.narrator(f"\nNiektóre kartki mają notatki: {self.whisper('Sprawdzian - matematyka')}, {self.whisper('Zadanie domowe - angielski')}, {self.whisper('Wypracowanie - 3+')}.")

        self.narrator("\nCzujesz zapach... papieru. Starego papieru. I kurzu. I kredy.")

        self.narrator(f"\n{self.meta('To pachnie jak szkoła. Ale jakoś... inaczej.')}")

        self.narrator(f"\nI wtedy widzisz {self.emphasis('JĄ')}.")

        self.pause()
        self.notka_intro()

    def notka_intro(self):
        """Spotkanie z Notką"""
        self.clear()
        cprint(NOTKA_ART)

        cprint(f"\n{C.GOLD}═══════ Biblioteczny Limbo ═══════{C.RESET}\n")

        self.narrator("To jest... kartka papieru. Z narysowaną buźką. I mówi do ciebie.")

        self.dialog("📄 Notka", "Hej! Ty! Nowy!")

        self.action("Patrzysz na kartkę. Ok. Najpierw mówiąca księga. Teraz mówiąca kartka. Piątek po lekcjach robi się coraz dziwniejszy.")

        self.dialog("📄 Notka", "Jestem Notka. Asystentka Księgi. Prowadzę tutaj interesy, gdy szef śpi. A śpi DUŻO, bo ma już swoje lata.")

        self.dialog("📄 Notka", "Widzę, że jesteś nowy w Paradoksji. No to tl;dr sytuacji:")

        self.action("Notka zaczyna mówić szybciej, jak influenserka nagrywająca TikToka:")

        self.dialog("📄 Notka", "Jesteś w Bibliotecznym Limbo. To jest hub. Central. Baza. Stąd prowadzą portale do różnych Krain Przedmiotów.")

        self.pause()

        self.clear()
        cprint(PORTAL_ART)

        self.dialog("📄 Notka", "Twoja misja: odzyskać kawałki Motywacji. Są trzy:")

        cprint(f"\n  🪶 {self.emphasis('Polszczyzna Przeklęta')} — poziom easy, dla rozgrzewki.")
        cprint(f"  🔢 {self.emphasis('Mathlandia')} — poziom medium, tu już musisz myśleć.")
        cprint(f"  🇬🇧 {self.emphasis('Anglolad')} — poziom hard, bo angielski zawsze hard.")

        self.dialog("📄 Notka", "Radzę iść po kolei. Bo jeśli wpadniesz do Angloladu bez przygotowania, to się pogubisz jak ja w tablicy Excela.")

        self.action("Kiwasz głową.")

        self.dialog("📄 Notka", "Każda kraina ma swojego bossa — NPC, który pilnuje Motywacji. Musisz rozwiązać zagadki, żeby ją dostać. Easy, prawda?")

        self.action("Nie jest easy. Ale kiwasz głową.")

        self.dialog("📄 Notka", "I jeszcze jedno. Uważaj na język. Tutaj język jest... dosłowny. Jeśli coś powiesz, może się spełnić. Jeśli popełnisz błąd ortograficzny... cóż, lepiej nie popełniaj.")

        self.dialog("📄 Notka", "No to powodzenia, bestie! Widzimy się po drugiej stronie!")

        self.action("Notka macha ci na pożegnanie i znika w stosie kartek.")

        self.pause()

    def show_hub(self):
        """Pokaż hub z portalami"""
        self.clear()
        cprint(PORTAL_ART)

        # Status motywacji
        cprint(f"\n{C.GOLD}══════════ Status Motywacji ══════════{C.RESET}")

        statuses = {
            'polski': '📚 Polski',
            'matematyka': '🔢 Matematyka',
            'angielski': '🇬🇧 Angielski'
        }

        for key, name in statuses.items():
            status = f"{C.GREEN}✓ ZDOBYTA{C.RESET}" if key in self.puzzles_solved else f"{C.DIM}○ Brak{C.RESET}"
            cprint(f"  {name}: {status}")

        cprint(f"\n  {C.GOLD}⭐ Punkty: {self.score}{C.RESET}")

        if len(self.puzzles_solved) == 3:
            cprint(f"\n{C.GREEN}{C.BOLD}Wszystkie Motywacje zebrane! Wpisz 'powrót' aby wrócić do Księgi!{C.RESET}")

        # Menu wyboru
        cprint(f"\n{C.CYAN}Dokąd wchodzisz?{C.RESET}")

        if 'polski' not in self.puzzles_solved:
            cprint(f"  {C.GREEN}[1]{C.RESET} Polszczyzna Przeklęta")
        else:
            cprint(f"  {C.DIM}[1] Polszczyzna Przeklęta ✓{C.RESET}")

        if 'matematyka' not in self.puzzles_solved:
            cprint(f"  {C.GREEN}[2]{C.RESET} Mathlandia")
        else:
            cprint(f"  {C.DIM}[2] Mathlandia ✓{C.RESET}")

        if 'angielski' not in self.puzzles_solved:
            cprint(f"  {C.GREEN}[3]{C.RESET} Anglolad")
        else:
            cprint(f"  {C.DIM}[3] Anglolad ✓{C.RESET}")

        if len(self.puzzles_solved) == 3:
            cprint(f"  {C.GOLD}[4]{C.RESET} Wróć do Księgi (zakończ)")

        cprint(f"  {C.RED}[q]{C.RESET} Wyjdź z gry")

    # ======================== POLSZCZYZNA ========================

    def polski_intro(self):
        """Intro do Polszczyzny"""
        self.clear()
        cprint(f"\n{C.GREEN}══════════ 🪶 POLSZCZYZNA PRZEKLĘTA 🪶 ══════════{C.RESET}\n")

        self.narrator("Wchodzisz w portal.")

        self.narrator("\nŚwiat się zmienia. Kolory. Zapachy. Dźwięki.")

        self.narrator(f"\nLas wita cię szmerem, który brzmi jak... {self.emphasis('szelest kartek w podręczniku do gramatyki')}.")

        self.narrator(f"\nDrzewa są {self.emphasis('DZIWNE')}. Na gałęziach zamiast liści wiszą {self.emphasis('przecinki')}. Tak, dosłownie znaki interpunkcyjne. Małe. Czarne. Zwisające jak dziwne owoce.")

        self.narrator(f"\nNiektóre spadają. Miękko. Na mech. {self.whisper('*Plum, plum, plum.*')}")

        self.narrator("\nSłyszysz coś w oddali. Szczęk metalu. Ktoś tu jest.")

        self.narrator(f"\nIdziesz dalej. Mech ścieszy pod stopami. Powietrze pachnie papierem i... tuszem? {self.meta('Dziwne miejsce.')}")

        self.narrator(f"\nI nagle widzisz {self.emphasis('GO')}.")

        self.pause()
        self.polski_geralt()

    def polski_geralt(self):
        """Spotkanie z Geraltem"""
        self.clear()
        cprint(GERALT_ART)

        cprint(f"\n{C.GREEN}══════════ Las Przecinkowy ══════════{C.RESET}\n")

        self.narrator("Mężczyzna. Siwe włosy związane w kucyk. Miecz u boku. Zmęczona mina człowieka, który widział za dużo.")

        self.action("Odwraca się. W ręku trzyma miecz. Na mieczu wygrawerowane: 'ORTOGRAFIA +5'")

        self.dialog("⚔️ Geralt", "Witaj, wędrowcze.")

        self.action("Mierzy cię wzrokiem. Nie wygląda na zachwyconego.")

        self.dialog("⚔️ Geralt", "Widzę, że jesteś nowy w Polszczyźnie. Pozwól, że wyjaśnię zasady. Tu język jest żywy. Dosłownie. Błędy gramatyczne materializują się jako potwory.")

        self.dialog("⚔️ Geralt", "Widziałeś kiedyś Błęda Ortograficznego? Nie? To dobrze. Bo wygląda jak koszmar senny polonistki.")

        self.action("Geralt siada na kamieniu. Wygląda na zmęczonego.")

        self.dialog("⚔️ Geralt", "Pilnuję tutaj Motywacji Polskiego. I nie oddam jej byle komu. Musisz udowodnić, że zasługujesz.")

        self.pause()
        self.polski_puzzle()

    def polski_puzzle(self):
        """Zagadka Polskiego"""
        self.clear()
        cprint(f"\n{C.GREEN}══════════ 🪶 ZAGADKA POLSKIEGO 🪶 ══════════{C.RESET}\n")

        self.dialog("⚔️ Geralt", "Oto twoje wyzwanie. Znajdź błąd. I nie pomyl się. Bo w Polszczyźnie błędy... gryzą.")

        cprint(f"\n{C.CYAN}╔════════════════════════════════════════════════════╗")
        cprint(f"║  Które z poniższych zdań zawiera BŁĄD INTERPUNKCYJNY?  ║")
        cprint(f"╚════════════════════════════════════════════════════╝{C.RESET}")

        cprint(f"\n  {C.GREEN}[A]{C.RESET} Poszedłem na spacer do parku.")
        cprint(f"  {C.GREEN}[B]{C.RESET} Kupiłem nową książkę w księgarni.")
        cprint(f"  {C.GREEN}[C]{C.RESET} Wziąłem parasol bo padał deszcz.")
        cprint(f"  {C.GREEN}[D]{C.RESET} Spotkałem się z przyjacielem.")

        hint_shown = False

        while True:
            answer = cinput(f"\n{C.CYAN}Twoja odpowiedź (A/B/C/D lub 'podpowiedź'): {C.RESET}").strip().lower()

            if answer in ['podpowiedź', 'podpowiedz', 'hint', 'p']:
                if not hint_shown:
                    cprint(f"\n{C.YELLOW}💡 Podpowiedź: Sprawdź znaki interpunkcyjne — po \"parasol\" czegoś brakuje! Przed \"bo\" powinien być...{C.RESET}")
                    hint_shown = True
                    self.hints_used += 1
                else:
                    cprint(f"\n{C.YELLOW}💡 Przed \"bo\" wprowadzającym zdanie podrzędne ZAWSZE stawiamy przecinek!{C.RESET}")
                continue

            if answer in ['c', '3']:
                self.polski_success()
                return
            elif answer in ['a', 'b', 'd', '1', '2', '4']:
                cprint(f"\n{C.RED}❌ Niestety, to nie jest poprawna odpowiedź. Spróbuj jeszcze raz!{C.RESET}")
            else:
                cprint(f"{C.DIM}Wpisz A, B, C lub D{C.RESET}")

    def polski_success(self):
        """Sukces w Polskim"""
        self.puzzles_solved.append('polski')
        self.motivations.append('📚')
        self.inventory.append('📚 Motywacja Polskiego')
        self.score += 100

        self.clear()
        cprint(f"\n{C.GREEN}{'═' * 50}")
        cprint(f"           ✨ BRAWO! POPRAWNA ODPOWIEDŹ! ✨")
        cprint(f"{'═' * 50}{C.RESET}\n")

        self.narrator("Geralt kiwa głową. Po raz pierwszy widzisz cień uśmiechu na jego twarzy.")

        self.dialog("⚔️ Geralt", "Dobrze. Przed 'bo' zawsze stawiamy przecinek, gdy wprowadza zdanie podrzędne przyczynowe. To podstawa.")

        self.dialog("⚔️ Geralt", "Zasłużyłeś.")

        self.narrator(f"\nGeralt wyciąga z kieszeni świecący kryształ. {self.emphasis('Motywacja Polskiego')}.")

        self.narrator("\nBierzesz ją. Jest ciepła. Wibruje lekko w dłoni.")

        cprint(f"\n{C.GREEN}+100 punktów!{C.RESET}")
        cprint(f"{C.GOLD}📚 Zdobyto Motywację Polskiego!{C.RESET}")

        self.dialog("⚔️ Geralt", "Idź. Czekają cię jeszcze dwie krainy. I uważaj na te przecinki... one tu dosłownie spadają z drzew.")

        self.narrator(f"\n{self.emphasis('Jedna Motywacja zdobyta. Zostały dwie.')}")

        self.pause()

    # ======================== MATHLANDIA ========================

    def matma_intro(self):
        """Intro do Matmy"""
        self.clear()
        cprint(f"\n{C.BLUE}══════════ 🔢 MATHLANDIA 🔢 ══════════{C.RESET}\n")

        self.narrator("Portal matematyczny jest... inny.")

        self.narrator(f"\nKiedy przechodzisz, czujesz, jak twój mózg się {self.emphasis('rozciąga')}. Jakby ktoś próbował zmieścić w nim więcej miejsca na liczby.")

        self.narrator(f"\nPo drugiej stronie... {self.loud('WOW')}.")

        self.narrator(f"\nGóry. Ale nie byle jakie góry. Góry w kształcie {self.emphasis('piramid')}. Idealnych, geometrycznych piramid. Niebo jest pokryte wzorami — równania wirują jak chmury.")

        self.narrator("\nŚcieżka pod stopami to linia liczbowa. Dosłownie. Widzisz na niej znaczki: -3, -2, -1, 0, 1, 2, 3...")

        self.narrator(f"\nI chodzisz po niej. {self.meta('Surrealistyczne.')}")

        self.narrator("\nW oddali widzisz postać. Stoi przy ogromnym kamieniu z wyrytym trójkątem.")

        self.pause()
        self.matma_pitagoras()

    def matma_pitagoras(self):
        """Spotkanie z Pitagorasem"""
        self.clear()
        cprint(PITAGORAS_ART)

        cprint(f"\n{C.BLUE}══════════ Mathlandia ══════════{C.RESET}\n")

        self.narrator("Starzec. Długa biała broda. Toga. Sandały. Wygląda jakby wyszedł prosto z... no, z lekcji historii starożytnej.")

        self.narrator("\nW ręku trzyma cyrkiel i linijkę. Jak broń.")

        self.dialog("📐 Pitagoras", "A, kolejny wędrowiec! Witaj w Mathlandii, krainie, gdzie liczby są prawdą, a prawda jest liczbą!")

        self.action("Jest zdecydowanie bardziej entuzjastyczny niż Geralt. Co może być dobre. Lub złe.")

        self.dialog("📐 Pitagoras", "Szukasz Motywacji Matematyki? Ach, oczywiście! Każdy jej szuka! Bo bez motywacji, matematyka jest tylko... torturą. Z motywacją, to MUZYKA WSZECHŚWIATA!")

        self.action("Robi dramatyczny gest ręką. Trochę teatralny ten Pitagoras.")

        self.dialog("📐 Pitagoras", "Ale! Żeby ją zdobyć, musisz udowodnić, że rozumiesz podstawy. Rozwiąż moje równanie. Proste. Eleganckie. Piękne.")

        self.pause()
        self.matma_puzzle()

    def matma_puzzle(self):
        """Zagadka Matematyczna"""
        self.clear()
        cprint(f"\n{C.BLUE}══════════ 🔢 ZAGADKA MATEMATYCZNA 🔢 ══════════{C.RESET}\n")

        self.dialog("📐 Pitagoras", "Oto moje wyzwanie. Równanie proste, ale wymagające MYŚLENIA.")

        cprint(f"\n{C.CYAN}╔════════════════════════════════════════════╗")
        cprint(f"║         Rozwiąż równanie:                  ║")
        cprint(f"║                                            ║")
        cprint(f"║              3x + 7 = 22                   ║")
        cprint(f"║                                            ║")
        cprint(f"║         Ile wynosi x?                      ║")
        cprint(f"╚════════════════════════════════════════════╝{C.RESET}")

        hint_shown = False

        while True:
            answer = cinput(f"\n{C.CYAN}Twoja odpowiedź (lub 'podpowiedź'): {C.RESET}").strip().lower()

            if answer in ['podpowiedź', 'podpowiedz', 'hint', 'p']:
                if not hint_shown:
                    cprint(f"\n{C.YELLOW}💡 Podpowiedź: Najpierw odejmij 7 od obu stron równania (3x = 22 - 7), potem podziel obie strony przez 3.{C.RESET}")
                    hint_shown = True
                    self.hints_used += 1
                else:
                    cprint(f"\n{C.YELLOW}💡 3x = 15, więc x = 15 ÷ 3 = ?{C.RESET}")
                continue

            if answer == '5':
                self.matma_success()
                return
            else:
                cprint(f"\n{C.RED}❌ To nie jest poprawna odpowiedź. Spróbuj jeszcze raz!{C.RESET}")

    def matma_success(self):
        """Sukces w Matmie"""
        self.puzzles_solved.append('matematyka')
        self.motivations.append('🔢')
        self.inventory.append('🔢 Motywacja Matematyki')
        self.score += 100

        self.clear()
        cprint(f"\n{C.GREEN}{'═' * 50}")
        cprint(f"           ✨ BRAWO! POPRAWNA ODPOWIEDŹ! ✨")
        cprint(f"{'═' * 50}{C.RESET}\n")

        self.narrator("Pitagoras klaszcze z zachwytem.")

        self.dialog("📐 Pitagoras", "WSPANIALE! 3x + 7 = 22, więc 3x = 15, więc x = 5! PERFEKCJA!")

        self.action("Podskakuje z radości. Trochę dziwnie wygląda skaczący staruszek w todze, ale ok.")

        self.dialog("📐 Pitagoras", "Widzę, że rozumiesz podstawy algebry. Zasłużyłeś na nagrodę!")

        self.narrator(f"\nPitagoras wyciąga z fałdów togi świecący kryształ. {self.emphasis('Motywacja Matematyki')}.")

        self.narrator("\nJest geometrycznie idealna. Wielościan. Każda ściana pod idealnym kątem.")

        cprint(f"\n{C.GREEN}+100 punktów!{C.RESET}")
        cprint(f"{C.GOLD}🔢 Zdobyto Motywację Matematyki!{C.RESET}")

        self.dialog("📐 Pitagoras", "Idź, młody podróżniku! I pamiętaj — w każdym równaniu jest piękno. Trzeba je tylko zobaczyć!")

        self.narrator(f"\n{self.emphasis('Dwie Motywacje zdobyte. Została jedna.')}")

        self.pause()

    # ======================== ANGLOLAD ========================

    def angielski_intro(self):
        """Intro do Angielskiego"""
        self.clear()
        cprint(f"\n{C.RED}══════════ 🇬🇧 ANGLOLAD 🇬🇧 ══════════{C.RESET}\n")

        self.narrator("Portal angielski jest... czerwony? I niebieski? I ma w sobie trochę bieli?")

        self.narrator(f"\n{self.meta('Ach. Jak flaga. Oczywiście.')}")

        self.narrator("\nPrzechodzisz.")

        self.narrator("\nPo drugiej stronie... ulica. Ale dziwna ulica. Wszystkie szyldy są w dwóch językach jednocześnie. Jakby ktoś nie mógł się zdecydować.")

        cprint(f"\n{self.whisper('TEA SHOP / Sklep z Herbatą')}")
        cprint(f"{self.whisper('FISH AND CHIPS / Ryba i Frytki')}")
        cprint(f"{self.whisper('IRREGULAR VERBS REHABILITATION CENTER / Centrum Rehabilitacji Czasowników Nieregularnych')}")

        self.narrator("\n...to ostatnie brzmi niepokojąco.")

        self.narrator("\nPrzy latarni stoi postać. Młoda dziewczyna. Słuchawki. Telefon w ręce. Żuje gumę.")

        self.pause()
        self.angielski_zosia()

    def angielski_zosia(self):
        """Spotkanie z Zosią"""
        self.clear()
        cprint(ZOSIA_ART)

        cprint(f"\n{C.RED}══════════ Anglolad - Slang Street ══════════{C.RESET}\n")

        self.narrator("Dziewczyna podnosi wzrok znad telefona. Zdejmuje jedną słuchawkę.")

        self.dialog("🎧 Zosia", "Oh, hej. Nowy? Nice. Literally nikt tu nie przychodzi, it's kinda dead here, tbh.", C.MAGENTA)

        self.action("Mówi dziwnym mixem polskiego i angielskiego. Każde drugie słowo w innym języku.")

        self.dialog("🎧 Zosia", "Jestem Zosia. Local guide. Basically siedzę tu i scrolluję TikToka, ale jak ktoś needs help, to pomagam. It's whatever.", C.MAGENTA)

        self.action("Wzrusza ramionami.")

        self.dialog("🎧 Zosia", "Szukasz Motywacji? Ugh, everyone does. It's guarded przez Shakespeare'a. Old guy, bardzo dramatic, mówi w these weird verses. Ale fair warning — his riddles są hard.", C.MAGENTA)

        self.dialog("🎧 Zosia", "Ale spoko, I believe in you. Go talk to him. He's over there, przy the big statue. Good luck, bestie!", C.MAGENTA)

        self.pause()
        self.angielski_shakespeare()

    def angielski_shakespeare(self):
        """Spotkanie z Shakespeare'm"""
        self.clear()
        cprint(SHAKESPEARE_ART)

        cprint(f"\n{C.RED}══════════ Town of Tenses ══════════{C.RESET}\n")

        self.narrator("Przy ogromnym posągu litery \"A\" stoi mężczyzna. Elizabetański strój. Pióro w ręce. Dramatyczna poza.")

        self.dialog("🎭 Shakespeare", "To be or not to be... a challenger! Hark! A young traveler approacheth!", C.RED)

        self.action("Odwraca się dramatycznie. Wszystko co robi jest dramatyczne.")

        self.dialog("🎭 Shakespeare", "Welcome, young soul, to Anglolad! Land of verbs irregular and grammar most peculiar!", C.RED)

        self.dialog("🎭 Shakespeare", "Thou must prove thy knowledge of English grammar! The verb 'to be' - the foundation of all!", C.RED)

        self.action("Robi przerwę dla efektu dramatycznego. Naprawdę lubi dramat ten gość.")

        self.pause()
        self.angielski_puzzle()

    def angielski_puzzle(self):
        """Zagadka Angielskiego"""
        self.clear()
        cprint(f"\n{C.RED}══════════ 🇬🇧 ENGLISH RIDDLE 🇬🇧 ══════════{C.RESET}\n")

        self.dialog("🎭 Shakespeare", "Behold! The question of grammar most vital!", C.RED)

        cprint(f"\n{C.CYAN}╔════════════════════════════════════════════════════╗")
        cprint(f"║       Choose the CORRECT sentence:                 ║")
        cprint(f"╚════════════════════════════════════════════════════╝{C.RESET}")

        cprint(f"\n  {C.GREEN}[A]{C.RESET} She don't like apples.")
        cprint(f"  {C.GREEN}[B]{C.RESET} She doesn't likes apples.")
        cprint(f"  {C.GREEN}[C]{C.RESET} She doesn't like apples.")
        cprint(f"  {C.GREEN}[D]{C.RESET} She not like apples.")

        hint_shown = False

        while True:
            answer = cinput(f"\n{C.CYAN}Your answer (A/B/C/D or 'hint'): {C.RESET}").strip().lower()

            if answer in ['podpowiedź', 'podpowiedz', 'hint', 'p']:
                if not hint_shown:
                    cprint(f"\n{C.YELLOW}💡 Hint: Remember: \"she\" uses \"doesn't\" (does not), and after \"doesn't\" we use the BASE form of the verb.{C.RESET}")
                    hint_shown = True
                    self.hints_used += 1
                else:
                    cprint(f"\n{C.YELLOW}💡 After \"doesn't\" the verb stays in base form: like → like, NOT likes{C.RESET}")
                continue

            if answer in ['c', '3']:
                self.angielski_success()
                return
            elif answer in ['a', 'b', 'd', '1', '2', '4']:
                cprint(f"\n{C.RED}❌ Wrong! Try again!{C.RESET}")
            else:
                cprint(f"{C.DIM}Type A, B, C or D{C.RESET}")

    def angielski_success(self):
        """Sukces w Angielskim"""
        self.puzzles_solved.append('angielski')
        self.motivations.append('🇬🇧')
        self.inventory.append('🇬🇧 Motywacja Angielskiego')
        self.score += 100

        self.clear()
        cprint(f"\n{C.GREEN}{'═' * 50}")
        cprint(f"           ✨ CORRECT! WELL DONE! ✨")
        cprint(f"{'═' * 50}{C.RESET}\n")

        self.narrator("Shakespeare klaszcze z zachwytem i robi ukłon.")

        self.dialog("🎭 Shakespeare", "BRAVO! MAGNIFICO! 'She doesn't like' — the verb returns to its base form after 'doesn't'! You understand the grammar of mine mother tongue!", C.RED)

        self.action("Wyciąga zza pleców świecący kryształ. Ostatnią Motywację.")

        self.dialog("🎭 Shakespeare", "Take it, young hero! The Motivation of English is yours!", C.RED)

        self.narrator("\nKryształ jest lekki. Przezroczysty. W środku widzisz wirujące litery — A, B, C, D...")

        cprint(f"\n{C.GREEN}+100 punktów!{C.RESET}")
        cprint(f"{C.GOLD}🇬🇧 Zdobyto Motywację Angielskiego!{C.RESET}")

        self.dialog("🎭 Shakespeare", "Now go! Return to the Book! Complete your quest! And remember — 'All the world's a stage, and all the men and women merely players!'", C.RED)

        cprint(f"\n{self.loud('WSZYSTKIE TRZY MOTYWACJE ZEBRANE!')}")
        self.narrator(f"\n{self.emphasis('Czas wrócić do Księgi!')}")

        self.pause()

    # ======================== FINAŁ ========================

    def finale(self):
        """Finał gry"""
        self.clear()
        cprint(f"\n{C.GOLD}══════════ Powrót do Księgi ══════════{C.RESET}\n")

        self.narrator("Wracasz przez portal do Bibliotecznego Limbo.")

        self.narrator(f"\nI natychmiast widzisz {self.emphasis('Księgę')}. Unosi się w powietrzu. Świeci jaśniej niż wcześniej.")

        self.dialog("📚 Księga", "WRÓCIŁEŚ! I... czuję to! MOTYWACJE! Masz je wszystkie!")

        self.action("Księga drży z ekscytacji. Kartki trzepoczą jak skrzydła.")

        self.dialog("📚 Księga", "Szybko! Połóż je na moich stronach! Musimy je połączyć!")

        self.narrator("\nWyciągasz trzy kryształy z plecaka. 📚 🔢 🇬🇧")

        self.narrator("\nKładziesz je na otwartych stronach Księgi.")

        self.narrator("\nI wtedy...")

        self.pause()

        # Animacja łączenia
        self.clear()
        cprint(MOTIVATION_MERGE_ART)

        cprint(f"\n{self.loud('ŚWIAAAATŁO!')}")
        time.sleep(1)

        self.narrator("\nTrzy kryształy zaczynają świecić. Wirować. Łączyć się.")

        self.narrator("\nKolory mieszają się — złoty polskiego, niebieski matematyki, czerwony angielskiego...")

        cprint(f"\n{self.loud('FLASH!')}")
        time.sleep(0.5)

        self.narrator(f"\nKiedy otwierasz oczy, nad Księgą unosi się jeden, wielki, {self.emphasis('tęczowy kryształ')}.")

        self.narrator(f"\n{self.emphasis('MOTYWACJA')}. Kompletna. Cała.")

        self.narrator("\nKryształ opada na strony Księgi i... wchłania się. Znika w papierze.")

        self.dialog("📚 Księga", "TAK! CZUJĘ TO! Motywacja wróciła! Jestem znowu... KOMPLETNA!")

        self.action("Księga świeci ciepłym, złotym światłem. Wygląda na... szczęśliwą?")

        self.pause()
        self.epilogue()

    def epilogue(self):
        """Epilog"""
        self.clear()
        cprint(f"\n{C.GOLD}══════════ Pożegnanie ══════════{C.RESET}\n")

        self.dialog("📚 Księga", "Teraz... wracasz do domu. Twoja misja się skończyła. Uratowałeś Paradoksję.")

        self.action("Czujesz ukłucie smutku. To była... fajna przygoda.")

        self.dialog("📚 Księga", "Ale hej! To nie koniec. Wiedza i Motywacja zostają z tobą. Zawsze. I... kto wie? Może jeszcze się spotkamy.")

        self.action("Księga mruga. Czy księga może mrugać?")

        self.dialog("📚 Księga", "A teraz — WRACAJ! Zanim pani Kowalska zauważy, że zniknąłeś!")

        cprint(f"\n{self.loud('SZUUUUUM!')}")

        self.narrator("\nI znowu wirowanie. Lecenie. Kartki. Litery. Cyfry.")

        self.narrator("\nA potem...")

        self.pause()

        # Powrót do szkoły
        self.clear()
        cprint(f"\n{C.GOLD}══════════ Epilog ══════════{C.RESET}\n")

        self.narrator("Stoisz w pokoju nauczycielskim.")

        self.narrator("\nWszystko wygląda normalnie. Biurka. Kubki z kawą. Stosy kartkówek.")

        self.narrator("\nNa biurku leży Księga. Zamknięta. Nie świeci.")

        self.narrator("\nPatrzysz na zegarek. 16:35.")

        cprint(f"\n{self.thought('Pięć minut? Byłem tam tylko pięć minut?')}")

        self.narrator("\nA może... to był tylko sen? Może się zdrzemnąłeś i...")

        self.narrator("\nNie. Sprawdzasz kieszeń.")

        self.narrator("\nJest tam coś małego. Ciepłego.")

        self.narrator("\nWyciągasz. To mały, świecący kamyczek. Wygląda jak... miniaturowy kryształ. Tęczowy.")

        cprint(f"\n{self.emphasis('To się naprawdę wydarzyło.')}")

        self.narrator("\nUśmiechasz się. Chowasz kamyczek do kieszeni.")

        self.narrator("\nI idziesz na poprawkę do sali 207.")

        self.narrator(f"\n{self.meta('Tym razem nie błądzisz.')}")

        self.pause()
        self.victory_screen()

    def victory_screen(self):
        """Ekran zwycięstwa"""
        self.clear()
        cprint(VICTORY_ART)

        # Statystyki
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        cprint(f"\n{C.CYAN}═══════════════ STATYSTYKI ═══════════════{C.RESET}")
        cprint(f"\n  ⏱️  Czas gry: {minutes}:{seconds:02d}")
        cprint(f"  ⭐ Punkty: {self.score}")
        cprint(f"  🧩 Zagadki rozwiązane: {len(self.puzzles_solved)}/3")
        cprint(f"  💡 Użyte podpowiedzi: {self.hints_used}")

        cprint(f"\n{C.DIM}═════════════════════════════════════════════{C.RESET}")

        cprint(f"\n{self.whisper('A może... kiedyś będzie CZĘŚĆ DRUGA?')}")
        cprint(f"{self.whisper('Kto wie, jakie przygody czekają w innych Krainach Przedmiotów...')}")
        cprint(f"\n{self.meta('🔮 Historia? Biologia? Fizyka? Muzyka?')}")

        cprint(f"\n{C.GOLD}Dziękujemy za grę w PARADOKSJĘ!{C.RESET}")

        input(f"\n{C.DIM}[Naciśnij ENTER aby zakończyć...]{C.RESET}")
        self.running = False

    # ======================== GŁÓWNA PĘTLA ========================

    def run(self):
        """Główna pętla gry"""
        # Ekran tytułowy
        self.show_title()

        # Intro
        self.intro_school()
        self.intro_door()
        self.intro_book()
        self.intro_dialog()

        if not self.intro_choice():
            return

        self.intro_transport()
        self.start_time = time.time()

        # Hub
        self.hub_arrival()

        # Główna pętla
        while self.running:
            self.show_hub()

            choice = cinput(f"\n{C.CYAN}Wybór (1/2/3/q): {C.RESET}").strip().lower()

            if choice == '1':
                if 'polski' not in self.puzzles_solved:
                    self.polski_intro()
                else:
                    cprint(f"{C.DIM}Już zdobyłeś Motywację Polskiego!{C.RESET}")
                    self.pause()
            elif choice == '2':
                if 'matematyka' not in self.puzzles_solved:
                    self.matma_intro()
                else:
                    cprint(f"{C.DIM}Już zdobyłeś Motywację Matematyki!{C.RESET}")
                    self.pause()
            elif choice == '3':
                if 'angielski' not in self.puzzles_solved:
                    self.angielski_intro()
                else:
                    cprint(f"{C.DIM}Już zdobyłeś Motywację Angielskiego!{C.RESET}")
                    self.pause()
            elif choice == '4' and len(self.puzzles_solved) == 3:
                self.finale()
            elif choice in ['q', 'quit', 'exit', 'wyjdź']:
                if input(f"\n{C.RED}Czy na pewno chcesz wyjść? (t/n): {C.RESET}").lower() in ['t', 'tak', 'y']:
                    print("\nDo zobaczenia!")
                    self.running = False
            elif choice in ['powrót', 'powrot', '4'] and len(self.puzzles_solved) == 3:
                self.finale()


# ============================================================================
# URUCHOMIENIE
# ============================================================================

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nDo zobaczenia!")
    except Exception as e:
        cprint(f"\n❌ Błąd: {e}")
        print("Jeśli problem się powtarza, zgłoś go nauczycielowi.")
        input("\n[Naciśnij ENTER aby zamknąć...]")
