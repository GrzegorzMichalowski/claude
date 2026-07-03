# Turniej Tabliczki Mnożenia — dziennik pracy

> Ten plik jest naszą "pamięcią" projektu. Jeśli sesja OpenCode się zgubi
> (np. po zamknięciu klapy Maca), wystarczy powiedzieć: "przeczytaj claude/PROGRESS.md",
> a odtworzę kontekst i będziemy kontynuować.

## Jak wracać do pracy
- Uruchom OpenCode z folderu `claude`.
- `opencode -c` kontynuuje ostatnią sesję w tym folderze.
- `ctrl+p` → wybór/lista sesji.
- Na starcie każdej sesji: przeczytaj ten plik.

## Główny plik
- `turniej-tabliczka.html` — gra/turniej tabliczki mnożenia (single-file HTML).

## Wytyczne (ustalenia z użytkownikiem)
- Rozgrywka W PEŁNI ZDALNA: każdy gracz przy swoim komputerze (nie „wielu z jednego urządzenia").
- Gra 1 na 1 (pojedynek dwóch graczy).
- Obsługa min. 6 JEDNOCZESNYCH sesji/turniejów naraz.
- Priorytet: poprawa STABILNOŚCI.
- (2026-07-02) — kierunek ustalony; implementacja do zaplanowania w kolejnym kroku.

## Stan projektu
- Podejście #3. Plik `turniej-tabliczka.html` istnieje z poprzednich prób (~146 KB, 3742 linie).
- PRZEANALIZOWANY (2026-07-02) — patrz sekcja „Analiza turniej-tabliczka.html".

## Analiza turniej-tabliczka.html (2026-07-02)
Kod jest DOJRZAŁY i kompletny (nie szkielet). Gra = kółko-krzyżyk z pytaniami mnożenia.
- Struktura: CSS wewn. (13–867), HTML panele (868–1170), Firebase compat v9.22.0 (1171),
  JS ~2560 linii/~80 funkcji (1174–3738), GoatCounter (3740).
- Firebase: config zgodny z regułami. Dane: `tournaments/{CODE}` (participants, groups,
  groupMatches[], bracket[][], leagueMatches[], leagueFinal), archiwum `tournamentHistory`.
  Transakcje chronią przed race condition (updateMatchInListTransactional, updateBracketMatchTransactional).
- Tryby: WSZYSTKIE 3 w pełni działają — grupy (round-robin→playoff), liga (każdy z każdym+finał top2),
  puchar (drabinka potęgi 2 z bye). Routing wg `status`: lobby|groups|knockout|league|leagueFinal|finished.
- Poziomy: easy 1–5 (Kurczaczek), medium 1–10 (Uczeń), hard 1–12 (Terminator), master 1–20 (Mega Mózg).
  Czas zależy od FAZY meczu (grupa/liga 5s, półfinał 4s, finał 3s), nie od poziomu.
- Kod turnieju: 6 znaków, alfabet bez mylących (bez I/O/0/1). Wielu graczy z 1 urządzenia.
- Odporność: watchdog 8s, sesja w localStorage + resume, recoverFromError, emergencyResetMatch.

### Odstępstwa od konwencji projektu (do decyzji czy poprawiać)
1. ❌ Zmienne CSS `--color-primary` — 0 użyć, kolory hardcode'owane (#ffd700, #1a1a2e…).
2. ❌ Brak breakpointów 768/480px i touch-target 44px — ryzyko UX na mobile/tablet.
3. ❌ Nie używa klasy QuestionTracker (import jest, ale własny system askedQuestions) — martwy import.
4. ⚠️ Przyciski „Symuluj mecze" (debug) WIDOCZNE dla hosta w produkcji — kandydat do ukrycia.
5. ⚠️ Brak semantycznego `<main>` (panele w `.container`); natywne alert()/confirm() zamiast UI.
6. ⚠️ Możliwy relikt: playFinalMatch vs startLeagueFinal — do weryfikacji.
- PWA: `turniej-tabliczka.html` CELOWO poza STATIC_ASSETS (jest w NETWORK_ONLY — wymaga Firebase online).
  service-worker CACHE_NAME = 'nauczyciel-tools-v4'.
- Jakość: brak TODO/FIXME, tylko 1 zbędny console.log (:3628), reszta to uzasadnione error/warn.

## Zrobione
- [x] Ustalono sposób zapisu kontekstu: plik PROGRESS.md + sesje OpenCode.
- [x] Zbudowano „CI" opencode (patrz niżej: Infrastruktura CI).

## ZREALIZOWANE (2026-07-03): etapy 1–3 remote 1v1 — mecz synchronizowany przez Firebase
Plik `turniej-tabliczka.html` przerobiony z hot-seat na zdalny 1v1. Testy E2E: 6/6 (w tym nowy
test remote sync). Składnia OK (node --check). Uruchamianie: `python3 -m http.server 4173`.
- ETAP 1 — tożsamość: stały `myClientId` w localStorage (CLIENT_ID_KEY). Dołączanie = 1 przeglądarka
  = 1 uczestnik (participants/{clientId}); usunięto „+ dodaj kolejną osobę" i addedPlayersFromDevice
  z przepływu. attemptResumeSession używa clientId. Panel dołączania uproszczony.
- ETAP 2 — węzeł live: `tournaments/{code}/matches/{key}/live` { board[9], turn, phase
  (playing|question|roundOver|matchOver), score1/2, selectedCell, question{text,options,correct},
  roundWinnerRole, matchWinnerRole, seq }. Obie przeglądarki renderują z live (onValue). Klucz meczu:
  getMatchKey → g_/l_/final/b_{round}_{id}. Dodano #gameStatusLine (status tury) w oknie meczu.
- ETAP 3 — autorytet = player1 (rola X): buduje pytania (buildQuestion, reużywa generateUniqueQuestion),
  ocenia odpowiedzi, aktualizuje planszę/wynik, wykrywa wygraną (checkWinPure), pisze wynik meczu
  (updateMatchResult z liveState + istniejące transakcje). player2 (O) wysyła intencje
  (matches/{key}/intent {type:select|answer}); autorytet stosuje i czyści. AUTO-WEJŚCIE do meczu:
  findMyPlayableMatch + maybeAutoEnterMatch (wywoływane w show*Stage) — gracze wchodzą automatycznie,
  host obserwuje. closeGame odpina live/intent; reset meczu czyści węzeł (clearLiveNode).
- USUNIĘTO stary hot-seat: resetBoard, handleGameCellClick, showGameQuestion, checkGameAnswer,
  placeGameMarker, checkGameWin, penalizeGamePlayer, showTournamentAnnouncement, show/Round/MatchResult
  (zastąpione silnikiem live). gameState pozostał jako lekki mirror dla watchdog/recover.
- PWA: bez zmian w SW (turniej jest NETWORK_ONLY; styles-common/scripts-common nietknięte).
- DECYZJE v1: brak auth → turę egzekwuje klient; timer/presja czasu (getTimeLimit zachowany) — ETAP 5;
  rozłączenie autorytetu → host „Powtórz mecz" (failover = ETAP 6); reguły Firebase dla live = ETAP 8.

## KLUCZOWE (2026-07-02): obecny mecz był LOKALNY (hot-seat) — PRZEROBIONY (patrz wyżej)
- initializeGame (:2774-2776) WYŁĄCZA listener Firebase na czas meczu.
- gameState (plansza, currentPlayer, wyniki) czysto lokalny (:2778-2788).
- placeGameMarker/checkGameAnswer (:3143-3236) zmieniają tylko lokalny stan + DOM — 0 zapisów do Firebase w grze.
- Do Firebase idzie TYLKO wynik końcowy (updateMatchResult :3349).
- => Dwaj gracze grają w kółko-krzyżyk na TYM SAMYM urządzeniu, na zmianę. Stąd „gracze z jednego urządzenia".
- => Wytyczna „pełny remote 1v1" wymaga PRZEPROJEKTOWANIA warstwy meczu (nie kosmetyka).

## ZREALIZOWANE (2026-07-03 cd.): harmonogram rundowy ligi/grup (automatyczne parowanie)
Problem: przy round-robin (liga/grupy) auto-wejście „pierwszy mój mecz" nie koordynowało par.
Rozwiązanie: harmonogram rundowy metodą koła.
- computeRoundRobinRounds/roundMapFor/pairKey/currentRoundOf — helpery.
- startLeague i startGroupStage przypisują `round` każdemu meczowi (grupy: runda w obrębie grupy,
  więc grupy grają równolegle w tej samej rundzie).
- findMyPlayableMatch dla ligi/grup wybiera TYLKO mecz z bieżącej rundy (currentRoundOf = min
  niezakończona runda). Gracz bez pary w rundzie (nieparzyste/bye) czeka do następnej rundy.
- UI: „Runda X z Y" w lidze (leagueProgress) i grupach (phaseIndicator).
- Nauczyciel klika tylko „Rozpocznij" — mecze startują automatycznie u obu graczy, bez kolizji.
- Nieparzysta liczba: puchar = bye w drabince (już było); liga/grupy = jeden pauzuje w rundzie.
- Testy E2E: 8/8 (dodane: poprawność round-robin nieparzystych + gating rund w auto-wejściu).
- UWAGA (do decyzji): przejścia FAZ nadal ręczne (host: „Rozpocznij fazę pucharową" po grupach,
  „Rozpocznij Wielki Finał" po lidze). Można zautomatyzować — do ustalenia.

## ZREALIZOWANE (2026-07-03 cd.2): auto-przejścia faz + stabilność
- AUTO-PRZEJŚCIA FAZ (wyzwala host, flaga phaseAdvancing + guard na status):
  - grupy → puchar: gdy wszystkie mecze grupowe completed → startPlayoffs() automatycznie
    (renderGroupMatches, komunikat „Przechodzę do fazy pucharowej…”).
  - liga → finał: wszystkie mecze ligowe completed → startLeagueFinal() automatycznie
    (showFinalTransition, zastąpiło ręczny przycisk showStartFinalButton).
- PRESENCE: gracz w meczu zapisuje matches/{key}/presence/{clientId}=true + onDisconnect().remove()
  (guard na brak onDisconnect w mocku). presenceListener liczy obecność przeciwnika →
  #gameConnLine „⚠️ Przeciwnik rozłączony…”. Sprzątane w detachMatchListeners.
- RECONNECT: działa przez attemptResumeSession + auto-wejście + trwałość live w Firebase.
  Autorytet wchodząc do istniejącego live NIE resetuje (init tylko gdy live puste). Sesja zapisywana
  także w trakcie meczu (listener saveSession przed guardem isModalOpen).
- TIMER TURY (presja czasu): applySelect ustawia live.deadline = now + getTimeLimit()*1000.
  manageTurnTimer: odliczanie #timerDisplay u obu (interval 250ms) + egzekwowanie timeoutu tylko
  przez autorytet (turnEnforceTimeout wg seq). applyTimeout = utrata tury (znacznik nie stawiany).
- Testy E2E: 11/11 (dodane: timeout tury, presence, wznowienie trwającego meczu).

## ZREALIZOWANE (2026-07-03 cd.3): reguły Firebase dla węzła matches
- firebase-rules.json (ŹRÓDŁO, format konsoli RTDB z komentarzami + wieloliniowe validate):
  dodano walidację `tournaments/$id/matches/$matchKey`:
  - live: hasChildren(board,turn,phase); board.$i ∈ {'',X,O} + hasChild('8'); turn ∈ {X,O};
    phase ∈ {playing,question,roundOver,matchOver}; score1/2 isNumber. Pozostałe pola wolne.
  - intent: hasChildren(type,by); type ∈ {select,answer}; by isString.
  - presence.$clientId: isBoolean.
- WAŻNE: węzeł matches i tak był dozwolony (kaskada .write:true pod $tournamentId, brak $other:false),
  więc to TWARDNIENIE (walidacja), nie odblokowanie. Zapisy aplikacji (liveRef.set pełnego obiektu,
  intent select/remove, presence set/remove) zgodne z regułami. Transakcja na całym turnieju
  (updateBracketMatchTransactional) re-waliduje matches — dane gry przechodzą.
- firebase-rules-clean.json ZREGENEROWANY ze źródła (ścisły JSON, deployowalny): NAPRAWIONO
  jego przestarzałość — brakowało `league` w mode/status oraz sekcji community/gameResults/adminConfig.
  Teraz jest wiernym, comment-free odpowiednikiem firebase-rules.json.
- WERYFIKACJA: oba pliki to poprawny JSON. Reguł nie dało się przetestować lokalnie (brak firebase-tools/
  emulatora). Do sprawdzenia na deployu (patrz „Wdrożenie reguł”).

## Wdrożenie reguł (do zrobienia ręcznie przez użytkownika)
1. Firebase Console → Realtime Database → Rules → wklej zawartość `firebase-rules.json`
   (konsola akceptuje komentarze) LUB `firebase-rules-clean.json` (ścisły JSON) → Publish.
2. Test po wdrożeniu: rozegrać remote 1v1 (2 przeglądarki) — sprawdzić, że ruchy się zapisują
   (brak PERMISSION_DENIED w konsoli). Sprawdzić też lige/grupy/puchar i community (milionerzy/fiszki).

## ZREALIZOWANE (2026-07-03 cd.4): git push + podpis autora
- Podpis git ustawiony globalnie: `Grzegorz Michałowski <grzegorz.michalowski@zpo-terpentyna.pl>`.
- Commit `ec7aa8f` („Turniej: pelny remote 1v1 (sync przez Firebase) + reguly matches")
  zaktualizowany `--amend --reset-author` (treść bez zmian).
- Push wykonany: `402e732..ec7aa8f main -> main` →
  https://github.com/GrzegorzMichalowski/claude
- Branch: main (aktualny).

## Do zrobienia
- [x] Test po deployu w 2 przeglądarkach — potwierdzony brak PERMISSION_DENIED, 1v1 działa poprawnie.
- [ ] Test manualny wieloosobowy (liga/grupy 4–6 graczy) — rundy, parowanie, auto-finał.
- [ ] (opcja) failover autorytetu, gdy player1 trwale offline (teraz: host „Powtórz mecz”).
- [x] Usunięto debug „Symuluj mecze" z UI (4 przyciski + help-box + JS show/hide; kod funkcji pozostawiony dla konsoli).
- [x] Podbity CACHE_NAME: nauczyel-tools-v4 → v5.
- [ ] Zweryfikować min. 6 jednoczesnych turniejów (izolacja per {code} — architektonicznie OK).

## Infrastruktura CI (opencode) — 2026-07-02
Pliki utworzone:
- `~/.config/opencode/AGENTS.md` — reguły globalne (PROGRESS.md, workflow sesji, Obsidian/RAG, konwencja `#opencode`).
- `claude/AGENTS.md` — reguły projektu (auto-odczyt PROGRESS.md, kontekst „Narzędzia dla Nauczycieli" + turniej).
- `~/.config/opencode/scripts/session-utils.mjs` — tagi (bazowy `opencode`), wikilinki, przebudowa INDEX.
- `~/.config/opencode/scripts/dump-session.mjs` — pełny dump z `opencode.db` (SQLite, node:sqlite).
- `~/.config/opencode/scripts/update-index.mjs` — przebudowa INDEX.md.
- `~/.config/opencode/command/dump-session.md` — komenda `/dump-session`.
- `~/.config/opencode/command/save-session.md` — komenda `/save-session`.

Kluczowe fakty:
- OpenCode trzyma sesje w SQLite (`~/.local/share/opencode/opencode.db`), tabele `session/message/part`
  (inaczej niż Claude Code, który miał JSONL). Dlatego dump napisany od nowa pod tę bazę.
- Notatki opencode: bazowy tag `#opencode`, stopka „przez opencode" (odróżnia od `#claude`, `#codex`).
- Folder notatek sesji (współdzielony): `OB_GM/80_Sesje_Claude_Code/`, tytuł INDEX zachowany.
- WAŻNE: zmiany w konfiguracji opencode działają dopiero po restarcie opencode.

## PLAN TECHNICZNY: remote 1v1 (2026-07-02, do akceptacji przed kodem)
Architektura: authoritative peer = player1 (jego przeglądarka prowadzi „silnik" gry i pisze stan).
Model danych — nowy węzeł `tournaments/{CODE}/matches/{matchId}/`:
  live/ { board[9], turn(X/O), phase, question{a,b,options[4]}, selectedCell, score1, score2, deadline, seq }
  presence/{playerId}: true  (onDisconnect().remove())
  intents/{playerId}: { cell, answer, seq }  // ruch gracza-nie-autorytetu
Zasada: obie przeglądarki renderują z `live` (onValue). player1 ocenia i pisze; player2 wysyła intencje.
Wejście do meczu remote: listener wykrywa mecz z moim udziałem + obaj present → auto-wejście
  (zamiast „host klika Graj!"). player1 inicjalizuje live przy pierwszym wejściu.

Mapa zmian (pliki/linie):
- Tożsamość: stały clientId w localStorage; 1 przeglądarka = 1 uczestnik; myRole X/O per mecz.
- Dołączanie (:1553-1668): domyślnie 1 gracz/urządzenie (multi-add jako opcja demo).
- initializeGame (:2763): NIE odcinać listenera; subskrybować matches/{id}/live; ustalić autorytet.
- placeGameMarker/checkGameAnswer/checkGameWin (:3143-3254): wykonuje autorytet → zapis do live; reszta render.
- showGameQuestion/generateUniqueQuestion (:2998-3141): tylko autorytet generuje pytania.
- timer/getTimeLimit (:2977): oparty o live.deadline; autorytet egzekwuje timeout.
- start*Match (:2126/:2327/:2710): inicjalizacja live + auto-wejście obu.
- updateMatchResult (:3349): tylko autorytet; transakcje bez zmian.
- closeGame (:3435): + odpięcie live/presence.
- Presence/reconnect: onDisconnect, wskaźnik offline, pauza timera; attemptResumeSession (:3691) wraca do live.
- Debug „Symuluj mecze" (:2494-2530): ukryć/usunąć w produkcji.
- Reguły Firebase (firebase-rules.json): dodać walidację live (board len 9, turn X/O).

Ryzyka/decyzje: brak auth → turę egzekwuje klient (stawka niska, OK v1); rozłączenie player1 blokuje
mecz → v1 host robi reset, v2 failover autorytetu; obciążenie zapisów znikome (free tier OK).

Etapy wdrożenia: 1) clientId+dołączanie 2) live+render 3) autorytet player1 4) intencje+tura
5) timer/deadline 6) presence+reconnect 7) auto-wejście+ukrycie debug 8) reguły Firebase 9) testy 2 okna+Playwright.

## Decyzje / notatki techniczne
- Persony z Downloads (personalize.txt, response.txt, wow-custom.gpt) mają cechy „Custom GPT"
  konfliktujące z agentem kodującym (linki Google wszędzie, VERBOSITY, „never minimize").
- DECYZJA (2026-07-02): rdzeń wartościowy (Task Engine 5 kroków, multi-role ekspert,
  proaktywność, brak chain-of-thought) JUŻ jest w globalnym AGENTS.md „Sposób pracy".
  Reszta odrzucona (Google-linki, emoji-prefiksy, tabela Expert/Plan, See also,
  „never minimize", slash-komendy — kolidują z komendami opencode). Do AGENTS.md NIC nie dodano.

## Log sesji
- Sesja 1 (2026-07-02): założono PROGRESS.md, ustalono zasady wracania do pracy;
  zbudowano CI opencode (AGENTS.md ×2, skrypty + komendy dump/save do Obsidiana z tagiem `#opencode`).
  Dump testowy: `80_Sesje_Claude_Code/2026-07-02 [DUMP] Konfiguracja CI opencode...`.
- Sesja 2 (2026-07-02): zamknięto 3 zaległe punkty — (1) decyzja o personie: nic nie dodano do
  globalnego AGENTS.md (rdzeń już był, reszta koliduje); (2) pełna analiza turniej-tabliczka.html;
  (3) wytyczne turnieju: pełny remote 1v1, min. 6 sesji, stabilność. ODKRYCIE: mecz jest lokalny
  (hot-seat) — wymaga przeprojektowania warstwy meczu na sync przez Firebase. Powstał PLAN TECHNICZNY.
  USTALENIE NA JUTRO: zaczynamy od implementacji etapów 1–3 (clientId+dołączanie → live+render →
  autorytet player1), żeby od razu był grywalny remote 1v1 do testu.
