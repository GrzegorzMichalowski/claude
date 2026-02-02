/**
 * Narzędzia dla Nauczycieli - Wspólne skrypty JS
 * Wersja: 1.0.0
 * Data: 2026-02-02
 */

/* ============================================
   QUESTION TRACKER
   System śledzenia pytań z persystencją w localStorage
   ============================================ */

class QuestionTracker {
    /**
     * @param {string} categoryId - Unikalny identyfikator kategorii (np. 'stolice-europy', 'wojewodztwa')
     * @param {Array} questions - Tablica wszystkich pytań z polem 'id' lub obiektów
     * @param {Object} options - Opcje konfiguracyjne
     * @param {boolean} options.useIndex - Jeśli true, używa indeksów zamiast id (dla prostych tablic)
     * @param {string} options.storagePrefix - Prefix dla klucza localStorage
     */
    constructor(categoryId, questions = [], options = {}) {
        this.categoryId = categoryId;
        this.allQuestions = questions;
        this.useIndex = options.useIndex || false;
        this.storagePrefix = options.storagePrefix || 'questionTracker';
        this.storageKey = `${this.storagePrefix}_${categoryId}`;
        this.askedIds = new Set();
        this.shuffledOrder = [];

        this.load();
    }

    /**
     * Wczytaj stan z localStorage
     */
    load() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) {
                const data = JSON.parse(saved);
                this.askedIds = new Set(data.askedIds || []);
                this.shuffledOrder = data.shuffledOrder || [];

                // Walidacja - jeśli shuffledOrder nie pasuje do questions, resetuj
                if (this.shuffledOrder.length !== this.allQuestions.length) {
                    this.reset(false);
                }
            } else {
                this.reset(false);
            }
        } catch (e) {
            console.warn('QuestionTracker: Błąd wczytywania z localStorage', e);
            this.reset(false);
        }
    }

    /**
     * Zapisz stan do localStorage
     */
    save() {
        try {
            const data = {
                askedIds: [...this.askedIds],
                shuffledOrder: this.shuffledOrder,
                lastUpdated: Date.now()
            };
            localStorage.setItem(this.storageKey, JSON.stringify(data));
        } catch (e) {
            console.warn('QuestionTracker: Błąd zapisywania do localStorage', e);
        }
    }

    /**
     * Pobierz ID pytania (indeks lub pole id)
     */
    getQuestionId(question, index) {
        if (this.useIndex) {
            return index;
        }
        return question.id !== undefined ? question.id : index;
    }

    /**
     * Tasowanie tablicy (Fisher-Yates)
     */
    shuffle(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    /**
     * Resetuj tracker - wszystkie pytania dostępne, nowa kolejność
     * @param {boolean} saveToStorage - Czy zapisać do localStorage
     */
    reset(saveToStorage = true) {
        this.askedIds = new Set();
        // Utwórz nową potasowaną kolejność indeksów
        this.shuffledOrder = this.shuffle(
            Array.from({ length: this.allQuestions.length }, (_, i) => i)
        );
        if (saveToStorage) {
            this.save();
        }
    }

    /**
     * Pobierz następne pytanie (nieużyte)
     * @returns {Object|null} Pytanie lub null jeśli brak pytań
     */
    getNext() {
        if (this.allQuestions.length === 0) {
            return null;
        }

        // Znajdź pierwsze nieużyte pytanie w potasowanej kolejności
        for (const index of this.shuffledOrder) {
            const question = this.allQuestions[index];
            const qId = this.getQuestionId(question, index);

            if (!this.askedIds.has(qId)) {
                return { question, index, id: qId };
            }
        }

        // Wszystkie pytania użyte - resetuj i pobierz pierwsze
        this.reset();
        return this.getNext();
    }

    /**
     * Oznacz pytanie jako zadane
     * @param {*} questionId - ID pytania lub indeks
     */
    markAsked(questionId) {
        this.askedIds.add(questionId);
        this.save();
    }

    /**
     * Pobierz następne pytanie i od razu oznacz jako zadane
     * @returns {Object|null} Pytanie lub null
     */
    getNextAndMark() {
        const result = this.getNext();
        if (result) {
            this.markAsked(result.id);
        }
        return result;
    }

    /**
     * Ile pytań pozostało do zadania
     */
    getRemainingCount() {
        return this.allQuestions.length - this.askedIds.size;
    }

    /**
     * Ile pytań łącznie
     */
    getTotalCount() {
        return this.allQuestions.length;
    }

    /**
     * Ile pytań już zadano
     */
    getAskedCount() {
        return this.askedIds.size;
    }

    /**
     * Procent ukończenia (0-100)
     */
    getProgress() {
        if (this.allQuestions.length === 0) return 0;
        return Math.round((this.askedIds.size / this.allQuestions.length) * 100);
    }

    /**
     * Czy wszystkie pytania zostały zadane (przed automatycznym resetem)
     */
    isComplete() {
        return this.askedIds.size >= this.allQuestions.length;
    }

    /**
     * Sprawdź czy pytanie było już zadane
     * @param {*} questionId - ID pytania
     */
    wasAsked(questionId) {
        return this.askedIds.has(questionId);
    }

    /**
     * Wyczyść całkowicie (usuń z localStorage)
     */
    clear() {
        this.askedIds = new Set();
        this.shuffledOrder = [];
        try {
            localStorage.removeItem(this.storageKey);
        } catch (e) {
            console.warn('QuestionTracker: Błąd usuwania z localStorage', e);
        }
    }

    /**
     * Ustaw nową listę pytań (np. przy zmianie kategorii)
     * @param {Array} questions - Nowa tablica pytań
     * @param {boolean} keepProgress - Czy zachować postęp (jeśli pytania się pokrywają)
     */
    setQuestions(questions, keepProgress = false) {
        this.allQuestions = questions;
        if (!keepProgress) {
            this.reset();
        } else {
            // Zachowaj tylko te asked które istnieją w nowej liście
            const newIds = new Set(
                questions.map((q, i) => this.getQuestionId(q, i))
            );
            this.askedIds = new Set(
                [...this.askedIds].filter(id => newIds.has(id))
            );
            this.shuffledOrder = this.shuffle(
                Array.from({ length: questions.length }, (_, i) => i)
            );
            this.save();
        }
    }

    /**
     * Pobierz statystyki jako obiekt
     */
    getStats() {
        return {
            categoryId: this.categoryId,
            total: this.getTotalCount(),
            asked: this.getAskedCount(),
            remaining: this.getRemainingCount(),
            progress: this.getProgress(),
            isComplete: this.isComplete()
        };
    }
}

/* ============================================
   QUESTION TRACKER MANAGER
   Zarządza wieloma trackerami dla różnych kategorii
   ============================================ */

class QuestionTrackerManager {
    constructor(storagePrefix = 'questionTracker') {
        this.storagePrefix = storagePrefix;
        this.trackers = new Map();
    }

    /**
     * Pobierz lub utwórz tracker dla kategorii
     */
    getTracker(categoryId, questions = [], options = {}) {
        if (!this.trackers.has(categoryId)) {
            this.trackers.set(categoryId, new QuestionTracker(
                categoryId,
                questions,
                { ...options, storagePrefix: this.storagePrefix }
            ));
        }
        return this.trackers.get(categoryId);
    }

    /**
     * Resetuj wszystkie trackery
     */
    resetAll() {
        this.trackers.forEach(tracker => tracker.reset());
    }

    /**
     * Wyczyść wszystkie trackery z localStorage
     */
    clearAll() {
        this.trackers.forEach(tracker => tracker.clear());
        this.trackers.clear();
    }

    /**
     * Pobierz statystyki wszystkich trackerów
     */
    getAllStats() {
        const stats = {};
        this.trackers.forEach((tracker, id) => {
            stats[id] = tracker.getStats();
        });
        return stats;
    }
}

/* ============================================
   TIMER UTILITIES
   Bezpieczne zarządzanie timerami
   ============================================ */

const TimerUtils = {
    intervals: new Map(),
    timeouts: new Map(),

    /**
     * Utwórz bezpieczny interval
     * @param {string} id - Unikalny identyfikator
     * @param {Function} callback - Funkcja do wywołania
     * @param {number} ms - Interwał w milisekundach
     * @returns {number} ID intervalu
     */
    setInterval(id, callback, ms) {
        this.clearInterval(id);
        const intervalId = setInterval(callback, ms);
        this.intervals.set(id, intervalId);
        return intervalId;
    },

    /**
     * Wyczyść interval po ID
     */
    clearInterval(id) {
        if (this.intervals.has(id)) {
            clearInterval(this.intervals.get(id));
            this.intervals.delete(id);
        }
    },

    /**
     * Utwórz bezpieczny timeout
     */
    setTimeout(id, callback, ms) {
        this.clearTimeout(id);
        const timeoutId = setTimeout(() => {
            this.timeouts.delete(id);
            callback();
        }, ms);
        this.timeouts.set(id, timeoutId);
        return timeoutId;
    },

    /**
     * Wyczyść timeout po ID
     */
    clearTimeout(id) {
        if (this.timeouts.has(id)) {
            clearTimeout(this.timeouts.get(id));
            this.timeouts.delete(id);
        }
    },

    /**
     * Wyczyść wszystkie timery
     */
    clearAll() {
        this.intervals.forEach((_, id) => this.clearInterval(id));
        this.timeouts.forEach((_, id) => this.clearTimeout(id));
    }
};

/* ============================================
   DOM UTILITIES
   Bezpieczne operacje na DOM
   ============================================ */

const DOMUtils = {
    /**
     * Bezpieczne pobranie elementu
     * @param {string} selector - Selektor CSS lub ID (bez #)
     * @returns {Element|null}
     */
    get(selector) {
        if (selector.startsWith('#') || selector.startsWith('.')) {
            return document.querySelector(selector);
        }
        return document.getElementById(selector) || document.querySelector(selector);
    },

    /**
     * Bezpieczne pobranie wielu elementów
     */
    getAll(selector) {
        return document.querySelectorAll(selector);
    },

    /**
     * Bezpieczne ustawienie tekstu
     */
    setText(element, text) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) el.textContent = text;
    },

    /**
     * Bezpieczne ustawienie HTML
     */
    setHTML(element, html) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) el.innerHTML = html;
    },

    /**
     * Bezpieczne toggle klasy
     */
    toggleClass(element, className, force) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) el.classList.toggle(className, force);
    },

    /**
     * Bezpieczne dodanie klasy
     */
    addClass(element, ...classNames) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) el.classList.add(...classNames);
    },

    /**
     * Bezpieczne usunięcie klasy
     */
    removeClass(element, ...classNames) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) el.classList.remove(...classNames);
    },

    /**
     * Pokaż element
     */
    show(element) {
        this.removeClass(element, 'hidden');
    },

    /**
     * Ukryj element
     */
    hide(element) {
        this.addClass(element, 'hidden');
    },

    /**
     * Utwórz element z atrybutami
     */
    create(tag, attributes = {}, children = []) {
        const el = document.createElement(tag);

        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                el.className = value;
            } else if (key === 'textContent') {
                el.textContent = value;
            } else if (key === 'innerHTML') {
                el.innerHTML = value;
            } else if (key.startsWith('on') && typeof value === 'function') {
                el.addEventListener(key.slice(2).toLowerCase(), value);
            } else if (key === 'style' && typeof value === 'object') {
                Object.assign(el.style, value);
            } else {
                el.setAttribute(key, value);
            }
        });

        children.forEach(child => {
            if (typeof child === 'string') {
                el.appendChild(document.createTextNode(child));
            } else if (child instanceof Node) {
                el.appendChild(child);
            }
        });

        return el;
    },

    /**
     * Usuń wszystkie dzieci elementu
     */
    clearChildren(element) {
        const el = typeof element === 'string' ? this.get(element) : element;
        if (el) {
            while (el.firstChild) {
                el.removeChild(el.firstChild);
            }
        }
    }
};

/* ============================================
   ANNOUNCEMENT UTILITIES
   Zarządzanie ogłoszeniami/komunikatami
   ============================================ */

const AnnouncementUtils = {
    /**
     * Pokaż ogłoszenie
     * @param {Object} options - Opcje
     * @param {string} options.content - Zawartość HTML
     * @param {number} options.duration - Czas wyświetlania (ms), 0 = bez limitu
     * @param {string} options.className - Dodatkowa klasa CSS
     * @param {Function} options.onClose - Callback po zamknięciu
     */
    show(options = {}) {
        const {
            content = '',
            duration = 1500,
            className = '',
            onClose = null
        } = options;

        // Usuń poprzednie ogłoszenia
        this.clearAll();

        const announcement = DOMUtils.create('div', {
            className: `announcement ${className}`.trim(),
            innerHTML: `<div class="announcement__content">${content}</div>`
        });

        document.body.appendChild(announcement);

        if (duration > 0) {
            setTimeout(() => {
                this.close(announcement, onClose);
            }, duration);
        }

        return announcement;
    },

    /**
     * Zamknij ogłoszenie z animacją
     */
    close(element, callback) {
        if (!element || !element.parentNode) {
            if (callback) callback();
            return;
        }

        element.style.opacity = '0';
        element.style.transition = 'opacity 0.3s';

        setTimeout(() => {
            if (element.parentNode) {
                element.remove();
            }
            if (callback) callback();
        }, 300);
    },

    /**
     * Usuń wszystkie ogłoszenia
     */
    clearAll() {
        document.querySelectorAll('.announcement, .round-announcement, .penalty-message')
            .forEach(el => el.remove());
    }
};

/* ============================================
   STORAGE UTILITIES
   Pomocnicze funkcje dla localStorage
   ============================================ */

const StorageUtils = {
    /**
     * Zapisz obiekt do localStorage
     */
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.warn('StorageUtils: Błąd zapisywania', e);
            return false;
        }
    },

    /**
     * Pobierz obiekt z localStorage
     */
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.warn('StorageUtils: Błąd odczytywania', e);
            return defaultValue;
        }
    },

    /**
     * Usuń z localStorage
     */
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.warn('StorageUtils: Błąd usuwania', e);
            return false;
        }
    },

    /**
     * Wyczyść wszystkie dane z danym prefixem
     */
    clearByPrefix(prefix) {
        try {
            const keys = Object.keys(localStorage).filter(k => k.startsWith(prefix));
            keys.forEach(k => localStorage.removeItem(k));
            return keys.length;
        } catch (e) {
            console.warn('StorageUtils: Błąd czyszczenia', e);
            return 0;
        }
    }
};

/* ============================================
   EXPORT (dla modułów ES6) / GLOBAL (dla zwykłych skryptów)
   ============================================ */

// Dla zwykłych skryptów (bez modułów)
if (typeof window !== 'undefined') {
    window.QuestionTracker = QuestionTracker;
    window.QuestionTrackerManager = QuestionTrackerManager;
    window.TimerUtils = TimerUtils;
    window.DOMUtils = DOMUtils;
    window.AnnouncementUtils = AnnouncementUtils;
    window.StorageUtils = StorageUtils;
}

// Dla ES6 modules (jeśli używane)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        QuestionTracker,
        QuestionTrackerManager,
        TimerUtils,
        DOMUtils,
        AnnouncementUtils,
        StorageUtils
    };
}
