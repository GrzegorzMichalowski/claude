"""
=================================================
KONFIGURACJA ROBOTA - ZMIEŃ TUTAJ ZANIM ZACZNIESZ
=================================================
Dopasuj porty i parametry do swojego robota.
"""

from hub import port

# ── PORTY SILNIKÓW ─────────────────────────────
LEFT_MOTOR  = port.A   # lewy silnik napędowy
RIGHT_MOTOR = port.B   # prawy silnik napędowy
AUX_MOTOR   = port.C   # silnik dodatkowy (ramię, chwytak)

# ── PORTY CZUJNIKÓW ────────────────────────────
COLOR_LEFT  = port.D   # lewy czujnik koloru (do wyrównania)
COLOR_RIGHT = port.E   # prawy czujnik koloru (do wyrównania)
COLOR_FRONT = port.F   # przedni czujnik koloru (do jazdy po linii)

# ── PARAMETRY MECHANICZNE ─────────────────────
WHEEL_DIAMETER_MM = 56.0   # średnica kół SPIKE (standardowe = 56mm)
WHEELBASE_MM      = 112.0  # rozstaw kół (mierz od środka do środka)

# ── PROGI CZUJNIKA KOLORU (kalibracja!) ────────
# Uruchom skrypt kalibracji żeby znaleźć swoje wartości
BLACK_THRESHOLD = 30   # poniżej = czarny
WHITE_THRESHOLD = 70   # powyżej = biały
LINE_EDGE       = 50   # krawędź linii (punkt środkowy)

# ── PRĘDKOŚCI DOMYŚLNE ────────────────────────
SPEED_SLOW   = 200    # [deg/s] - precyzyjne manewry
SPEED_NORMAL = 400    # [deg/s] - jazda standardowa
SPEED_FAST   = 600    # [deg/s] - szybka jazda po prostej

# ── STAŁE PID (dostrajaj eksperymentalnie!) ────
# Jazda prosto
STRAIGHT_KP = 1.5
STRAIGHT_KI = 0.0     # zacznij od 0, dodaj jeśli robot dryfuje
STRAIGHT_KD = 0.8

# Skręt
TURN_KP = 2.0
TURN_KD = 0.5

# Jazda po linii
LINE_KP = 1.2
