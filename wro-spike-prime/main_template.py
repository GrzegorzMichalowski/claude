"""
╔══════════════════════════════════════════════════════════╗
║   SZABLON PROGRAMU GŁÓWNEGO - WRO Junior 2026           ║
║   Skopiuj i dostosuj do swoich misji                    ║
╚══════════════════════════════════════════════════════════╝
"""

from spike_library import *

# ─────────────────────────────────────────────
# INICJALIZACJA - ZAWSZE PIERWSZA LINIA
# ─────────────────────────────────────────────
setup_robot()

# ─────────────────────────────────────────────
# MISJA 1 - PRZYKŁAD KOMPLETNEJ SEKWENCJI
# ─────────────────────────────────────────────

def misja_1():
    """Przykład pełnej misji z typowymi manewrami."""

    # Wyjazd z bazy - prosto 40cm
    drive_straight(40)

    # Skręt 90° w prawo
    turn_gyro(90)

    # Jazda do linii wyrównania
    drive_straight(15)
    line_square()           # wyrównaj do czarnej linii

    # Jedź po linii 20cm
    follow_line(20)

    # Wykryj kolor misji
    kolor = get_color()
    print("Wykryty kolor:", kolor)

    if kolor == 'red':
        run_motor(AUX_MOTOR, 360)   # obsłuż czerwoną misję
    elif kolor == 'blue':
        run_motor(AUX_MOTOR, -360)  # obsłuż niebieską misję

    # Powrót do bazy
    turn_gyro(180)
    drive_straight(55)


# ─────────────────────────────────────────────
# MISJA 2 - JAZDA PO LINII DO KOLORU
# ─────────────────────────────────────────────

def misja_2():
    """Misja używająca jazdy po linii do wykrycia celu."""

    drive_straight(10)
    turn_gyro(-45)

    # Jedź po linii aż do czerwonego znacznika
    follow_line_until_color(Color.RED, speed=SPEED_SLOW)

    # Wykonaj zadanie
    run_motor(AUX_MOTOR, 540)
    time.sleep_ms(500)

    # Wróć
    drive_straight(-30)
    turn_gyro(45)
    drive_straight(-10)


# ─────────────────────────────────────────────
# URUCHOMIENIE
# ─────────────────────────────────────────────

misja_1()
misja_2()

print("KONIEC PROGRAMU")
