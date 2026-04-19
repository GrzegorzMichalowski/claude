"""
╔══════════════════════════════════════════════════════════╗
║   SPIKE PRIME WRO LIBRARY v2.0                          ║
║   Algorytmy do WRO RoboMission - kategoria Junior       ║
║   LEGO SPIKE Prime 3.x Python                           ║
╚══════════════════════════════════════════════════════════╝

WYMAGANIA:
  - LEGO Education SPIKE app (wersja 3.x)
  - Python mode (nie Word Blocks)
  - Hub SPIKE Prime z wbudowanym żyroskopem (motion sensor)

UŻYCIE:
  1. Wgraj oba pliki (spike_library.py + robot_config.py) do huba
  2. W swoim programie: from spike_library import *
  3. Zawsze zacznij od: setup_robot()
"""

import motor
import motor_pair
from hub import motion_sensor, port as hub_port
from color_sensor import reflection as _reflection, color as _color
from color import Color
import time

from robot_config import *

# ═══════════════════════════════════════════════
# POMOCNICZE - PRZELICZNIKI
# ═══════════════════════════════════════════════

def _cm_to_degrees(cm: float) -> float:
    """Przelicza centymetry na stopnie obrotu silnika."""
    import math
    circumference = math.pi * WHEEL_DIAMETER_MM / 10  # obwód w cm
    return (cm / circumference) * 360

def _clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, value))

# ═══════════════════════════════════════════════
# INICJALIZACJA
# ═══════════════════════════════════════════════

def setup_robot():
    """
    ZAWSZE wywołaj na początku programu!
    Paruje silniki i resetuje żyroskop.
    """
    motor_pair.pair(motor_pair.PAIR_1, LEFT_MOTOR, RIGHT_MOTOR)
    motion_sensor.reset_yaw_angle()
    time.sleep_ms(200)  # daj żyroskopowi chwilę na ustabilizowanie
    print("Robot gotowy. Yaw:", _get_yaw())

def _get_yaw() -> float:
    """Odczyt kąta yaw w stopniach (nie decidegrees)."""
    # SPIKE Prime zwraca decidegrees (dziesiąte stopnia)
    return motion_sensor.tilt_angles()[0] / 10

def reset_gyro():
    """Reset żyroskopu do 0. Wywołuj przed każdym ruchem wymagającym precyzji."""
    motion_sensor.reset_yaw_angle()
    time.sleep_ms(100)

# ═══════════════════════════════════════════════
# 1. JAZDA PROSTO NA ŻYROSKOPIE (PID)
# ═══════════════════════════════════════════════

def drive_straight(distance_cm: float, speed: int = SPEED_NORMAL,
                   Kp: float = STRAIGHT_KP,
                   Ki: float = STRAIGHT_KI,
                   Kd: float = STRAIGHT_KD):
    """
    Jedzie prosto na zadany dystans z korekcją PID.

    Parametry:
        distance_cm : dystans w centymetrach (>0 = do przodu, <0 = do tyłu)
        speed       : prędkość w deg/s (200-700, domyślnie SPEED_NORMAL)
        Kp, Ki, Kd  : stałe PID (zacznij od domyślnych, potem strajaj)

    Strojenie PID:
        1. Ustaw Ki=0, Kd=0. Zwiększaj Kp aż robot jedzie prosto, ale wibruje.
        2. Dodaj Kd żeby wytłumić wibracje (zacznij od Kd = Kp/2).
        3. Dodaj Ki tylko jeśli robot konsekwentnie skręca w jedną stronę.

    Przykład:
        drive_straight(50)          # 50 cm do przodu
        drive_straight(-20, 300)    # 20 cm do tyłu, wolniej
    """
    reset_gyro()
    motor.reset_relative_position(LEFT_MOTOR, 0)

    direction = 1 if distance_cm >= 0 else -1
    target_deg = _cm_to_degrees(abs(distance_cm))
    actual_speed = speed * direction

    integral = 0.0
    last_error = 0.0

    while abs(motor.relative_position(LEFT_MOTOR)) < target_deg:
        error = _get_yaw()

        # Zeruj całkę przy małym błędzie (zapobiega windup)
        if abs(error) < 0.5:
            integral = 0.0
        else:
            integral += error
        integral = _clamp(integral, -30, 30)

        derivative = error - last_error
        correction = int(Kp * error + Ki * integral + Kd * derivative)
        correction = _clamp(correction, -200, 200)

        motor.run(LEFT_MOTOR,  actual_speed - correction)
        motor.run(RIGHT_MOTOR, actual_speed + correction)

        last_error = error

    # Hamowanie
    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


def drive_straight_timed(seconds: float, speed: int = SPEED_NORMAL,
                         Kp: float = STRAIGHT_KP, Kd: float = STRAIGHT_KD):
    """
    Jazda prosto przez zadany czas (gdy nie znasz dystansu).
    Przydatne przy dojechaniu do ściany lub misji bez miarki.
    """
    reset_gyro()
    last_error = 0.0
    end_time = time.ticks_ms() + int(seconds * 1000)

    while time.ticks_ms() < end_time:
        error = _get_yaw()
        correction = int(Kp * error + Kd * (error - last_error))
        correction = _clamp(correction, -200, 200)

        motor.run(LEFT_MOTOR,  speed - correction)
        motor.run(RIGHT_MOTOR, speed + correction)
        last_error = error

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


# ═══════════════════════════════════════════════
# 2. SKRĘT O DOKŁADNY KĄT
# ═══════════════════════════════════════════════

def turn_gyro(angle: float, speed: int = SPEED_SLOW,
              Kp: float = TURN_KP, Kd: float = TURN_KD):
    """
    Skręt w miejscu o zadany kąt z precyzją żyroskopu.

    Parametry:
        angle  : kąt w stopniach (+prawo / -lewo)
        speed  : prędkość obrotu w deg/s (150-400, wolniej = precyzyjniej)
        Kp, Kd : stałe proporcjonalne (PD - zazwyczaj I nie jest potrzebne)

    Zasada:
        Robot zwalnia gdy zbliża się do celu (zone).
        Przy małych kątach (<30°) używaj mniejszego speed.

    Przykład:
        turn_gyro(90)    # skręt 90° w prawo
        turn_gyro(-45)   # skręt 45° w lewo
        turn_gyro(180)   # obrót o 180°
    """
    reset_gyro()
    last_error = 0.0

    while True:
        current = _get_yaw()
        error = angle - current

        # Zatrzymaj gdy blisko celu (tolerancja ±1°)
        if abs(error) <= 1.0:
            break

        # PD correction - płynne dojście do celu
        correction = int(Kp * error + Kd * (error - last_error))
        # Minimalna prędkość żeby robot się poruszał
        correction = _clamp(correction, -speed, speed)
        if 0 < abs(correction) < 80:
            correction = 80 if correction > 0 else -80

        motor.run(LEFT_MOTOR,   correction)
        motor.run(RIGHT_MOTOR, -correction)

        last_error = error

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)
    time.sleep_ms(100)


def turn_one_wheel(angle: float, pivot: str = 'left', speed: int = SPEED_SLOW):
    """
    Skręt na jednym kole (szeroki łuk) - bardziej przewidywalny trajektoria.

    Parametry:
        angle  : kąt do obrotu w stopniach
        pivot  : 'left' = obrót na lewym kole, 'right' = na prawym
        speed  : prędkość aktywnego koła

    Przykład:
        turn_one_wheel(90, 'right')  # łuk 90° z prawym kołem nieruchomym
    """
    reset_gyro()

    while True:
        current = _get_yaw()
        error = angle - current
        if abs(error) <= 1.5:
            break

        spd = _clamp(int(1.5 * error), -speed, speed)
        if 0 < abs(spd) < 60:
            spd = 60 if spd > 0 else -60

        if pivot == 'right':
            motor.run(LEFT_MOTOR, spd)
            motor.stop(RIGHT_MOTOR)
        else:
            motor.stop(LEFT_MOTOR)
            motor.run(RIGHT_MOTOR, -spd)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


# ═══════════════════════════════════════════════
# 3. JAZDA PO LINII
# ═══════════════════════════════════════════════

def follow_line(distance_cm: float, speed: int = SPEED_SLOW,
                sensor_port = None, side: str = 'right',
                Kp: float = LINE_KP):
    """
    Jedzie wzdłuż krawędzi czarnej linii (proportional control).

    Parametry:
        distance_cm : dystans jazdy w cm
        speed       : prędkość bazowa
        sensor_port : port czujnika koloru (domyślnie COLOR_FRONT)
        side        : 'right' = jedź prawą krawędzią, 'left' = lewą krawędzią
        Kp          : czułość korekcji (zacznij od 1.0, zwiększaj ostrożnie)

    Jak to działa:
        Czujnik mierzy odbite światło (0=czarny, 100=biały).
        Target = 50 (krawędź linii).
        Błąd = odczyt - 50. Korekta koryguje oba silniki.

    Strojenie Kp:
        Za małe → robot wężykuje leniwie
        Za duże → robot oscyluje gwałtownie
        Optymalne → płynna jazda wzdłuż krawędzi

    Przykład:
        follow_line(30)                         # 30cm prawą krawędzią
        follow_line(20, side='left', Kp=1.5)    # 20cm lewą krawędzią
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT

    motor.reset_relative_position(LEFT_MOTOR, 0)
    target_deg = _cm_to_degrees(abs(distance_cm))

    while abs(motor.relative_position(LEFT_MOTOR)) < target_deg:
        reflected = _reflection(sensor_port)
        error = reflected - LINE_EDGE

        if side == 'left':
            error = -error

        correction = int(Kp * error)
        correction = _clamp(correction, -300, 300)

        motor.run(LEFT_MOTOR,  speed - correction)
        motor.run(RIGHT_MOTOR, speed + correction)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


def follow_line_until_color(target_color: Color, speed: int = SPEED_SLOW,
                             sensor_port=None, side: str = 'right', Kp: float = LINE_KP):
    """
    Jedzie po linii aż do wykrycia określonego koloru.
    Przydatne gdy nie wiesz dokładnego dystansu do misji.

    Przykład:
        follow_line_until_color(Color.RED)   # jedź po linii aż czerwony
        follow_line_until_color(Color.BLUE)  # jedź aż niebieski
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT

    while True:
        detected = _color(sensor_port)
        if detected == target_color:
            break

        reflected = _reflection(sensor_port)
        error = reflected - LINE_EDGE
        if side == 'left':
            error = -error

        correction = _clamp(int(Kp * error), -300, 300)
        motor.run(LEFT_MOTOR,  speed - correction)
        motor.run(RIGHT_MOTOR, speed + correction)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


# ═══════════════════════════════════════════════
# 4. WYRÓWNYWANIE DO LINII (LINE SQUARING)
# ═══════════════════════════════════════════════

def line_square(speed: int = 150, timeout_ms: int = 3000):
    """
    Wyrównuje robota prostopadle do czarnej linii.
    Używa DWÓCH czujników kolorów (COLOR_LEFT i COLOR_RIGHT).

    Zasada działania:
        1. Oba silniki jadą do przodu.
        2. Gdy lewy czujnik wykryje czerń → zatrzymuje lewy silnik.
        3. Gdy prawy czujnik wykryje czerń → zatrzymuje prawy silnik.
        4. Gdy oba zatrzymane → robot jest wyrównany.

    WAŻNE: Czujniki muszą być symetrycznie po obu stronach robota!
    Odległość czujników od osi kół decyduje o dokładności.

    Przykład:
        drive_straight(20)  # podjazd do okolic linii
        line_square()       # wyrównanie precyzyjne
        drive_straight(5)   # dalszy ruch już po wyrównaniu
    """
    left_locked  = False
    right_locked = False

    start = time.ticks_ms()

    motor.run(LEFT_MOTOR,  speed)
    motor.run(RIGHT_MOTOR, speed)

    while not (left_locked and right_locked):
        # Timeout bezpieczeństwa
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            print("UWAGA: line_square timeout!")
            break

        if not left_locked:
            if _reflection(COLOR_LEFT) < BLACK_THRESHOLD:
                motor.stop(LEFT_MOTOR)
                left_locked = True

        if not right_locked:
            if _reflection(COLOR_RIGHT) < BLACK_THRESHOLD:
                motor.stop(RIGHT_MOTOR)
                right_locked = True

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


def line_square_backward(speed: int = 150, timeout_ms: int = 3000):
    """
    Wyrównanie do linii jadąc DO TYŁU (przydatne po misji).
    Działa identycznie jak line_square() ale w reverse.
    """
    left_locked  = False
    right_locked = False

    start = time.ticks_ms()

    motor.run(LEFT_MOTOR,  -speed)
    motor.run(RIGHT_MOTOR, -speed)

    while not (left_locked and right_locked):
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            break

        if not left_locked:
            if _reflection(COLOR_LEFT) < BLACK_THRESHOLD:
                motor.stop(LEFT_MOTOR)
                left_locked = True

        if not right_locked:
            if _reflection(COLOR_RIGHT) < BLACK_THRESHOLD:
                motor.stop(RIGHT_MOTOR)
                right_locked = True

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


# ═══════════════════════════════════════════════
# 5. OBSŁUGA CZYTNIKA KOLORÓW
# ═══════════════════════════════════════════════

def get_color(sensor_port=None) -> str:
    """
    Wykrywa kolor z czujnika. Zwraca string.
    Kolory: 'red', 'blue', 'green', 'yellow', 'white', 'black', None

    Przykład:
        kolor = get_color()
        if kolor == 'red':
            # zrób coś
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT

    detected = _color(sensor_port)
    color_map = {
        Color.RED:    'red',
        Color.BLUE:   'blue',
        Color.GREEN:  'green',
        Color.YELLOW: 'yellow',
        Color.WHITE:  'white',
        Color.BLACK:  'black',
        Color.CYAN:   'cyan',
        Color.MAGENTA:'magenta',
        Color.ORANGE: 'orange',
    }
    return color_map.get(detected, None)


def get_reflection(sensor_port=None) -> int:
    """
    Odczyt intensywności odbicia (0=czarny, 100=biały).
    Przydatne do kalibracji i śledzenia linii.

    Przykład:
        val = get_reflection()
        print("Odbicie:", val)  # 0-100
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT
    return _reflection(sensor_port)


def calibrate_colors(sensor_port=None):
    """
    NARZĘDZIE KALIBRACJI - uruchom przed zawodami!
    Wyświetla odczyty przez 5 sekund.
    Ustaw czujnik nad czarnym, potem białym, potem linią.
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT

    print("=== KALIBRACJA CZUJNIKA ===")
    print("Obserwuj wartości i zaktualizuj BLACK_THRESHOLD/WHITE_THRESHOLD w robot_config.py")

    end = time.ticks_ms() + 5000
    while time.ticks_ms() < end:
        ref  = _reflection(sensor_port)
        col  = _color(sensor_port)
        print(f"Odbicie: {ref:3d}% | Kolor: {col}")
        time.sleep_ms(300)


def wait_for_color(target_color: Color, sensor_port=None, timeout_ms: int = 10000):
    """
    Czeka aż czujnik wykryje zadany kolor.

    Przykład:
        wait_for_color(Color.RED)   # czeka na czerwony
    """
    if sensor_port is None:
        sensor_port = COLOR_FRONT

    start = time.ticks_ms()
    while _color(sensor_port) != target_color:
        if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
            print("Timeout: nie wykryto koloru!")
            return False
    return True


# ═══════════════════════════════════════════════
# SILNIK POMOCNICZY (ramię, chwytak, pchacz)
# ═══════════════════════════════════════════════

def run_motor(port_id, degrees: int, speed: int = 300):
    """
    Obraca silnik pomocniczy o zadaną liczbę stopni.
    Przydatne do obsługi chwytaka, ramienia, pchacza.

    Przykład:
        run_motor(AUX_MOTOR, 360)    # pełny obrót do przodu
        run_motor(AUX_MOTOR, -180)   # pół obrotu do tyłu
    """
    motor.run_for_degrees(port_id, degrees, speed)
