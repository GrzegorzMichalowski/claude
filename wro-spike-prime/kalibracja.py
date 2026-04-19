"""
SKRYPT KALIBRACJI - uruchom PRZED zawodami na KAŻDEJ nowej macie!
Wyniki wpisz do robot_config.py
"""

from spike_library import *
import time

setup_robot()

print("=" * 40)
print("KALIBRACJA CZUJNIKÓW KOLORU")
print("=" * 40)
print()

# Test 1: Odczyty przez 5 sekund
print("TEST 1: Odczyty bieżące (5s)")
print("Przesuń czujnik nad różne kolory na macie:")
for i in range(25):
    ref = get_reflection(COLOR_FRONT)
    col = get_color(COLOR_FRONT)
    print(f"  Odbicie={ref:3d}%  Kolor={str(col):<10}")
    time.sleep_ms(200)

print()
print("ZALECANE WARTOŚCI DLA robot_config.py:")
print("  BLACK_THRESHOLD = ~30  (gdy czujnik nad czarną linią)")
print("  WHITE_THRESHOLD = ~70  (gdy czujnik nad białym polem)")
print("  LINE_EDGE = 50         (krawędź linii - zwykle środek)")
print()

# Test 2: Sprawdzenie żyroskopu
print("TEST 2: Żyroskop")
reset_gyro()
print(f"  Po resecie: {_get_yaw():.1f}°  (powinno być ~0)")
time.sleep_ms(2000)
print(f"  Po 2s stania: {_get_yaw():.1f}° (drift - im mniej tym lepiej)")
print()
print("GOTOWE! Porównaj wyniki i zaktualizuj robot_config.py")
