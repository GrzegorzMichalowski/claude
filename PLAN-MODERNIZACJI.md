# Plan Modernizacji - Narzędzia dla Nauczycieli

**Data utworzenia:** 2026-02-02
**Status:** W trakcie realizacji

---

## Spis treści
1. [Faza 0: Przygotowanie infrastruktury CSS](#faza-0-przygotowanie-infrastruktury-css)
2. [Faza 1: System niepowtarzających się pytań](#faza-1-system-niepowtarzających-się-pytań)
3. [Faza 2: Refaktoryzacja plików - od najprostszych](#faza-2-refaktoryzacja-plików)
4. [Faza 3: Optymalizacje i ulepszenia](#faza-3-optymalizacje)

---

## Faza 0: Przygotowanie infrastruktury CSS

### Zadanie 0.1: Utworzenie styles-common.css
- [x] **Status:** Zakończone (2026-02-02)
- **Plik:** `styles-common.css`
- **Opis:** Wspólny plik CSS z variables, komponentami bazowymi
- **Zawartość:**
  - CSS Variables (kolory, typografia, spacing, breakpointy)
  - Reset i bazowe style
  - Komponenty: .btn, .card, .container, .home-btn
  - Media queries helpers
  - Touch target fixes (min 44x44px)

### Zadanie 0.2: Utworzenie scripts-common.js
- [x] **Status:** Zakończone (2026-02-02)
- **Plik:** `scripts-common.js`
- **Opis:** Wspólne funkcje JS używane w wielu miejscach
- **Zawartość:**
  - QuestionTracker - system śledzenia pytań (localStorage)
  - Timer utilities (clearTimer, safe interval management)
  - DOM helpers (safe element access)
  - Analytics helpers

---

## Faza 1: System niepowtarzających się pytań

### Zadanie 1.1: Implementacja QuestionTracker w scripts-common.js
- [x] **Status:** Zakończone (2026-02-02)
- **Opis:** Klasa/moduł do zarządzania pulą pytań z persystencją
- **Funkcjonalności:**
  ```javascript
  // API:
  QuestionTracker.init(categoryId, allQuestions)
  QuestionTracker.getNext() // Losuje z nieużytych
  QuestionTracker.markAsked(questionId)
  QuestionTracker.getRemainingCount()
  QuestionTracker.reset() // Gdy wszystkie zadane - resetuj i shuffluj
  QuestionTracker.clearStorage() // Ręczny reset
  ```
- **Persystencja:** localStorage z kluczem `questionTracker_{categoryId}`

### Zadanie 1.2: Integracja z mapa-polski.html
- [x] **Status:** Zakończone (2026-02-02)
- **Obecny system:** 16 województw, losowanie `Math.random()`
- **Zmiany:**
  - Import QuestionTracker
  - Śledzenie które województwa były pytane
  - Reset dopiero po przejściu wszystkich 16
  - Osobne śledzenie dla trybu "stolice" vs "województwa"

### Zadanie 1.3: Integracja z tabliczka-kolko-krzyzyk.html
- [ ] **Status:** Do zrobienia
- **Obecny system:** Losowe mnożenie + kategorie quizowe
- **Kategorie do obsłużenia:**
  - Tabliczka mnożenia (dynamiczne generowanie - bez zmian)
  - Stolice Europy (~50 pytań)
  - Stolice Świata (~100+ pytań)
  - Zwierzęta po angielsku (~30 pytań)
  - Kolory po angielsku (~15 pytań)
  - Inne kategorie...
- **Zmiany:**
  - QuestionTracker osobny dla każdej kategorii
  - Pokazanie postępu: "Pytanie 15/50"
  - Opcja resetu w ustawieniach

### Zadanie 1.4: Integracja z turniej-tabliczka.html
- [ ] **Status:** Do zrobienia
- **Opis:** Turniej już ma `askedQuestions` ale tylko per mecz
- **Zmiany:**
  - Rozszerzyć na cały turniej (nie per mecz)
  - Persystencja w localStorage dla dłuższych turniejów

---

## Faza 2: Refaktoryzacja plików

### Kolejność (od najprostszego do najtrudniejszego):
1. progi-ocen.html (prosty, bez JS logiki)
2. termometr-emocji.html (prosty)
3. losowanie-ucznia.html (brak media queries - krytyczne!)
4. timer-kartkowka.html (średni)
5. timer-egzamin.html (średni)
6. stworek.html (średni-złożony)
7. mapa-polski.html (złożony + QuestionTracker)
8. tabliczka-kolko-krzyzyk.html (złożony + QuestionTracker)
9. turniej-tabliczka.html (najbardziej złożony)
10. index.html (na końcu - dostosować do nowego systemu)

---

### Zadanie 2.1: progi-ocen.html
- [x] **Status:** Zakończone (2026-02-02)
- **Problemy:**
  - Inline `onclick` zamiast addEventListener
  - Brak importu common CSS
- **Zmiany:**
  - Import styles-common.css
  - Zamiana onclick na addEventListener
  - Ujednolicenie kolorów na CSS variables
  - Sprawdzenie responsywności (ma media query 500px - OK)

### Zadanie 2.2: termometr-emocji.html
- [x] **Status:** Zakończone (2026-02-02)
- **Problemy:**
  - Własna paleta kolorów
  - Breakpoint 380px (niestandardowy)
- **Zmiany:**
  - Import styles-common.css
  - Dostosowanie do standardowych breakpointów (480px, 768px)
  - Touch targets dla przycisków emocji

### Zadanie 2.3: losowanie-ucznia.html [KRYTYCZNE]
- [x] **Status:** Zakończone (2026-02-02)
- **Problemy:**
  - BRAK media queries - źle na mobile!
  - Historia bez limitu (memory leak)
  - Font-size: 5rem stały
- **Zmiany:**
  - Import styles-common.css
  - Dodanie media queries (480px, 768px)
  - Fluid typography: clamp()
  - Limit historii do 100 wpisów
  - Touch targets dla checkboxów

### Zadanie 2.4: timer-kartkowka.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Font-size timera stały (nie fluid)
  - Własne kolory
- **Zmiany:**
  - Import styles-common.css
  - Fluid typography dla timera
  - Ujednolicenie z timer-egzamin.html

### Zadanie 2.5: timer-egzamin.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Font-size timera stały
  - Własne kolory
- **Zmiany:**
  - Import styles-common.css
  - Fluid typography
  - Lepsze fullscreen support

### Zadanie 2.6: stworek.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Position: fixed może zakrywać na mobile
  - Breakpoint 400px (niestandardowy)
- **Zmiany:**
  - Import styles-common.css
  - Standardowe breakpointy
  - Sprawdzenie fixed elements na mobile

### Zadanie 2.7: mapa-polski.html
- [x] **Status:** Zakończone (2026-02-02)
- **Problemy:**
  - event.target bezpośrednie (bez parametru)
  - SVG 39KB (można zoptymalizować)
  - Brak śledzenia pytań
- **Zmiany:**
  - Import styles-common.css i scripts-common.js
  - QuestionTracker integration
  - Naprawienie event.target
  - Optymalizacja SVG (opcjonalnie)

### Zadanie 2.8: tabliczka-kolko-krzyzyk.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Duży plik (59KB)
  - Niekompletne media queries
  - Brak śledzenia pytań dla kategorii quizowych
- **Zmiany:**
  - Import styles-common.css i scripts-common.js
  - QuestionTracker dla wszystkich kategorii
  - Pełne media queries
  - Pokazanie postępu pytań

### Zadanie 2.9: turniej-tabliczka.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Największy plik (84KB)
  - Pytania śledzne tylko per mecz
- **Zmiany:**
  - Import styles-common.css i scripts-common.js
  - Rozszerzony QuestionTracker (per turniej)
  - Ujednolicenie stylów

### Zadanie 2.10: index.html
- [ ] **Status:** Do zrobienia
- **Problemy:**
  - Własne style (duplikacja)
- **Zmiany:**
  - Import styles-common.css
  - Usunięcie zduplikowanych stylów
  - Ewentualne dodanie nowych narzędzi

---

## Faza 3: Optymalizacje

### Zadanie 3.1: Optymalizacja SVG mapy Polski
- [ ] **Status:** Do zrobienia
- **Cel:** Zmniejszenie z 39KB do ~15KB
- **Metody:**
  - SVGO optimization
  - Usunięcie zbędnych atrybutów
  - Uproszczenie ścieżek

### Zadanie 3.2: Lighthouse audit
- [ ] **Status:** Do zrobienia
- **Cel:** 90+ we wszystkich kategoriach
- **Metryki:**
  - Performance
  - Accessibility
  - Best Practices
  - SEO

### Zadanie 3.3: PWA support (opcjonalnie)
- [ ] **Status:** Do zrobienia
- **Opis:** Service Worker dla offline access
- **Pliki:**
  - manifest.json
  - service-worker.js

---

## Notatki techniczne

### CSS Variables do użycia:
```css
:root {
  /* Colors */
  --color-primary: #667eea;
  --color-primary-dark: #764ba2;
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-danger: #dc3545;
  --color-bg-dark: #1a1a2e;

  /* Typography */
  --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  --font-size-base: 1rem;
  --font-size-sm: 0.875rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Breakpoints (for reference in JS) */
  --bp-mobile: 480px;
  --bp-tablet: 768px;
  --bp-desktop: 1024px;

  /* Touch targets */
  --touch-target-min: 44px;
}
```

### Standardowe breakpointy:
```css
/* Mobile first */
@media (min-width: 481px) { /* Tablet */ }
@media (min-width: 769px) { /* Desktop */ }
@media (min-width: 1025px) { /* Large desktop */ }

/* Alternatywnie max-width */
@media (max-width: 768px) { /* Tablet and below */ }
@media (max-width: 480px) { /* Mobile */ }
```

### QuestionTracker API:
```javascript
class QuestionTracker {
  constructor(categoryId, questions) {
    this.categoryId = categoryId;
    this.allQuestions = questions;
    this.storageKey = `questionTracker_${categoryId}`;
    this.load();
  }

  load() {
    const saved = localStorage.getItem(this.storageKey);
    if (saved) {
      this.askedIds = new Set(JSON.parse(saved));
    } else {
      this.askedIds = new Set();
    }
  }

  save() {
    localStorage.setItem(this.storageKey, JSON.stringify([...this.askedIds]));
  }

  getNext() {
    const remaining = this.allQuestions.filter(q => !this.askedIds.has(q.id));
    if (remaining.length === 0) {
      this.reset();
      return this.getNext();
    }
    const randomIndex = Math.floor(Math.random() * remaining.length);
    return remaining[randomIndex];
  }

  markAsked(questionId) {
    this.askedIds.add(questionId);
    this.save();
  }

  getRemainingCount() {
    return this.allQuestions.length - this.askedIds.size;
  }

  getTotalCount() {
    return this.allQuestions.length;
  }

  reset() {
    this.askedIds = new Set();
    this.save();
  }
}
```

---

## Historia zmian

| Data | Zadanie | Status | Uwagi |
|------|---------|--------|-------|
| 2026-02-02 | Plan utworzony | Zakończone | - |
| | | | |

---

## Jak wznowić prace

1. Otwórz ten plik
2. Znajdź pierwsze zadanie ze statusem `[ ]` (Do zrobienia)
3. Zmień status na `[~]` (W trakcie)
4. Po zakończeniu zmień na `[x]` (Zakończone)
5. Dodaj wpis do "Historia zmian"

**Legenda statusów:**
- `[ ]` - Do zrobienia
- `[~]` - W trakcie
- `[x]` - Zakończone
- `[!]` - Zablokowane/Problem
