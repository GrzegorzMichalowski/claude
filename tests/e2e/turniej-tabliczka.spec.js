const { test, expect } = require('@playwright/test');

const firebaseMockJs = `
(() => {
  if (window.firebase) return;

  const clone = (v) => (v === undefined ? undefined : JSON.parse(JSON.stringify(v)));
  const listeners = new Map();
  const data = {
    '.info': { connected: true },
    tournaments: {},
    tournamentHistory: {}
  };

  const normalize = (path) => (path || '').replace(/^\\/+|\\/+$/g, '');
  const parts = (path) => {
    const p = normalize(path);
    return p ? p.split('/') : [];
  };
  const getAt = (path) => {
    const p = parts(path);
    let cur = data;
    for (const key of p) {
      if (cur == null || typeof cur !== 'object' || !(key in cur)) return null;
      cur = cur[key];
    }
    return clone(cur);
  };
  const setAt = (path, value) => {
    const p = parts(path);
    if (p.length === 0) return;
    let cur = data;
    for (let i = 0; i < p.length - 1; i++) {
      const key = p[i];
      if (cur[key] == null || typeof cur[key] !== 'object') cur[key] = {};
      cur = cur[key];
    }
    cur[p[p.length - 1]] = clone(value);
  };
  const mergeAt = (path, value) => {
    const existing = getAt(path) || {};
    setAt(path, { ...existing, ...clone(value) });
  };
  const removeAt = (path) => {
    const p = parts(path);
    if (p.length === 0) return;
    let cur = data;
    for (let i = 0; i < p.length - 1; i++) {
      const key = p[i];
      if (!cur[key] || typeof cur[key] !== 'object') return;
      cur = cur[key];
    }
    delete cur[p[p.length - 1]];
  };

  const makeSnapshot = (path) => {
    const value = getAt(path);
    return {
      exists: () => value !== undefined && value !== null,
      val: () => clone(value),
      forEach: (cb) => {
        if (!value || typeof value !== 'object') return;
        Object.entries(value).forEach(([k, v]) => {
          cb({
            key: k,
            val: () => clone(v),
            exists: () => v !== null && v !== undefined
          });
        });
      }
    };
  };

  const shouldNotify = (listenerPath, changedPath) => {
    const lp = normalize(listenerPath);
    const cp = normalize(changedPath);
    if (!lp || !cp) return true;
    return lp === cp || cp.startsWith(lp + '/') || lp.startsWith(cp + '/');
  };

  const notify = (changedPath) => {
    listeners.forEach((arr, key) => {
      if (!shouldNotify(key, changedPath)) return;
      const snap = makeSnapshot(key);
      arr.forEach((cb) => cb(snap));
    });
  };

  const makeRef = (path = '') => ({
    _path: normalize(path),
    on: (event, cb) => {
      if (event !== 'value') return;
      const key = normalize(path);
      if (!listeners.has(key)) listeners.set(key, []);
      listeners.get(key).push(cb);
      cb(makeSnapshot(path));
    },
    off: (event, cb) => {
      if (event && event !== 'value') return;
      const key = normalize(path);
      if (!listeners.has(key)) return;
      if (!cb) {
        listeners.delete(key);
        return;
      }
      listeners.set(key, listeners.get(key).filter(fn => fn !== cb));
    },
    once: () => Promise.resolve(makeSnapshot(path)),
    set: (value) => {
      setAt(path, value);
      notify(path);
      return Promise.resolve();
    },
    update: (value) => {
      mergeAt(path, value);
      notify(path);
      return Promise.resolve();
    },
    remove: () => {
      removeAt(path);
      notify(path);
      return Promise.resolve();
    },
    push: (value) => {
      const key = 'mock_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
      const nextPath = normalize(path) ? normalize(path) + '/' + key : key;
      if (value !== undefined) {
        setAt(nextPath, value);
        notify(path);
      }
      return Promise.resolve({ key });
    },
    orderByChild: () => makeRef(path),
    endAt: () => makeRef(path),
    limitToLast: () => makeRef(path)
  });

  window.firebase = {
    initializeApp: () => {},
    database: () => ({ ref: (path = '') => makeRef(path) })
  };
  window.firebase.database.ServerValue = { TIMESTAMP: Date.now() };
})();
`;

async function installMocks(page) {
  await page.route('https://www.gstatic.com/firebasejs/**', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/javascript',
      body: firebaseMockJs
    });
  });

  await page.route('https://*.goatcounter.com/**', async route => {
    await route.fulfill({ status: 204, body: '' });
  });
}

test('pokazuje ekran startowy i pomoc', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  await expect(page.getByRole('heading', { name: 'Turniej Tabliczki Mnożenia' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Pomoc i instrukcja' })).toBeVisible();

  await page.getByRole('button', { name: 'Pomoc i instrukcja' }).click();
  await expect(page.getByRole('heading', { name: 'Pomoc i instrukcja' })).toBeVisible();
  await expect(page.getByText('Gdy mecz się zawiesi')).toBeVisible();
});

test('ma przycisk powrotu do listy i reset meczu w modalu', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  await expect(page.locator('#closeMatchBtnInline')).toBeAttached();
  await expect(page.locator('#resetMatchBtnInline')).toBeAttached();
});

test('host moze zasymulowac puchar do konca', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  await page.getByRole('button', { name: 'Utwórz nowy turniej' }).click();
  await page.locator('#tournamentName').fill('Test puchar');
  await page.locator('#tournamentMode').selectOption('knockout');
  await page.getByRole('button', { name: 'Utwórz turniej' }).click();

  const code = (await page.locator('#lobbyCode').innerText()).trim();
  expect(code).toHaveLength(6);

  await page.evaluate((tournamentCode) => {
    return firebase.database().ref('tournaments/' + tournamentCode + '/participants').set({
      p1: { name: 'Ala', joinedAt: Date.now() },
      p2: { name: 'Bartek', joinedAt: Date.now() }
    });
  }, code);

  await expect(page.locator('#startTournamentBtn')).toBeEnabled();
  await page.locator('#startTournamentBtn').click();

  await expect(page.locator('#tournamentPanel')).toBeVisible();
  await expect(page.locator('#simulateKnockout')).toBeVisible();
  await page.locator('#simulateKnockout').click();

  await expect(page.locator('#championPanel')).toBeVisible();
  await expect(page.locator('#championName')).not.toHaveText('---');
});

test('host moze zasymulowac lige i final do konca', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  await page.getByRole('button', { name: 'Utwórz nowy turniej' }).click();
  await page.locator('#tournamentName').fill('Test liga');
  await page.locator('#tournamentMode').selectOption('league');
  await page.getByRole('button', { name: 'Utwórz turniej' }).click();

  const code = (await page.locator('#lobbyCode').innerText()).trim();
  expect(code).toHaveLength(6);

  await page.evaluate((tournamentCode) => {
    return firebase.database().ref('tournaments/' + tournamentCode + '/participants').set({
      p1: { name: 'Ala', joinedAt: Date.now() },
      p2: { name: 'Bartek', joinedAt: Date.now() },
      p3: { name: 'Celina', joinedAt: Date.now() }
    });
  }, code);

  await expect(page.locator('#startTournamentBtn')).toBeEnabled();
  await page.locator('#startTournamentBtn').click();

  await expect(page.locator('#leagueStagePanel')).toBeVisible();
  await page.evaluate(() => { isHost = true; });
  await page.evaluate(() => simulatePendingMatches(3));

  await expect(page.locator('#leagueFinalPanel')).toBeVisible();
  await page.evaluate(() => { isHost = true; });
  await page.evaluate(() => simulatePendingMatches(1));

  await expect(page.locator('#championPanel')).toBeVisible();
  await expect(page.locator('#championName')).not.toHaveText('---');
});

test('remote 1v1: autorytet X + intencje O synchronizują mecz do wygranej', async ({ page }) => {
  await installMocks(page);
  // Ta przeglądarka ma stałą tożsamość P1 (= gracz X, autorytet)
  await page.addInitScript(() => {
    try { localStorage.setItem('turniej_tabliczka_client_id', 'P1'); } catch (e) {}
  });
  await page.goto('/turniej-tabliczka.html');

  const code = 'REMOTE';
  const KEY = 'b_0_m0';

  // Turniej pucharowy z gotowym meczem P1 vs P2
  await page.evaluate((code) => {
    const bracket = [[{
      id: 'm0',
      player1: { id: 'P1', name: 'Ala', points: 0, wins: 0, played: 0 },
      player2: { id: 'P2', name: 'Bartek', points: 0, wins: 0, played: 0 },
      score1: 0, score2: 0, winner: null, status: 'ready'
    }]];
    return firebase.database().ref('tournaments/' + code).set({
      code, name: 'Remote', mode: 'knockout', groupCount: 0, level: 'medium',
      pointsToWin: 1, timePressure: false, status: 'knockout',
      participants: { P1: { name: 'Ala', joinedAt: 1 }, P2: { name: 'Bartek', joinedAt: 1 } },
      bracket, host: 'host_x', createdAt: 1
    });
  }, code);

  // Wejście jako gracz P1 → auto-wejście do meczu, autorytet inicjalizuje live
  await page.evaluate((code) => {
    isHost = false;
    currentPlayer = { id: 'P1', name: 'Ala' };
    return firebase.database().ref('tournaments/' + code).once('value').then(s => {
      currentTournament = { ...s.val(), code };
      listenToTournament(code);
    });
  }, code);

  await expect(page.locator('#gameModal')).toHaveClass(/active/);
  await expect(page.locator('#gamePlayerX')).toHaveText('Ala');
  await expect(page.locator('#gameStatusLine')).toHaveText('➡️ Twoja tura');

  // X (autorytet): wybór komórki + poprawna odpowiedź
  async function xPlay(cell) {
    await page.locator('.game-cell[data-index="' + cell + '"]').click();
    await expect(page.locator('#questionPanel')).toBeVisible();
    const correct = await page.evaluate(() => liveState.question.correct);
    await page.locator('.answer-btn[data-answer="' + correct + '"]').first().click();
  }
  // O (przeciwnik): ruch przez intencje w Firebase
  async function oPlay(cell) {
    await page.evaluate(({ cell, code, KEY }) =>
      firebase.database().ref('tournaments/' + code + '/matches/' + KEY + '/intent')
        .set({ type: 'select', cell, by: 'P2', seq: Date.now() }), { cell, code, KEY });
    await page.waitForFunction(() => liveState && liveState.phase === 'question');
    const correct = await page.evaluate(() => liveState.question.correct);
    await page.evaluate(({ correct, code, KEY }) =>
      firebase.database().ref('tournaments/' + code + '/matches/' + KEY + '/intent')
        .set({ type: 'answer', value: correct, by: 'P2', seq: Date.now() }), { correct, code, KEY });
    await page.waitForFunction(() => liveState && liveState.phase === 'playing');
  }

  await xPlay(0);
  await page.waitForFunction(() => liveState.turn === 'O');
  await oPlay(3);
  await page.waitForFunction(() => liveState.turn === 'X');
  await xPlay(1);
  await page.waitForFunction(() => liveState.turn === 'O');
  await oPlay(4);
  await page.waitForFunction(() => liveState.turn === 'X');
  await xPlay(2); // X: górny rząd 0,1,2 → wygrana

  await expect(page.locator('#matchResult')).toBeVisible();
  await expect(page.locator('#matchResultText')).toContainText('Ala wygrywa mecz');
  // Plansza zsynchronizowana: X@0,1,2 oraz O@3,4
  const board = await page.evaluate(() => liveState.board);
  expect(board.slice(0, 3)).toEqual(['X', 'X', 'X']);
  expect(board[3]).toBe('O');
  expect(board[4]).toBe('O');
});

test('harmonogram round-robin: każda para raz, brak gracza dwa razy w rundzie (nieparzyste)', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  const res = await page.evaluate(() => {
    const ids = ['A', 'B', 'C', 'D', 'E']; // 5 = nieparzyste
    const rounds = computeRoundRobinRounds(ids);
    // Zbierz pary i sprawdź duplikaty w rundzie
    const seenPairs = {};
    let dupInRound = false;
    rounds.forEach(pairs => {
      const used = new Set();
      pairs.forEach(([a, b]) => {
        if (used.has(a) || used.has(b)) dupInRound = true;
        used.add(a); used.add(b);
        const k = a < b ? a + b : b + a;
        seenPairs[k] = (seenPairs[k] || 0) + 1;
      });
    });
    return {
      roundCount: rounds.length,
      totalPairs: Object.keys(seenPairs).length,
      anyPairTwice: Object.values(seenPairs).some(c => c > 1),
      dupInRound
    };
  });

  expect(res.roundCount).toBe(5);   // n=6 (z bye) → 5 rund
  expect(res.totalPairs).toBe(10);  // C(5,2)
  expect(res.anyPairTwice).toBe(false);
  expect(res.dupInRound).toBe(false);
});

test('auto-wejście ligi respektuje rundy (nie wchodzi do rundy 2 przed końcem rundy 1)', async ({ page }) => {
  await installMocks(page);
  await page.addInitScript(() => {
    try { localStorage.setItem('turniej_tabliczka_client_id', 'P1'); } catch (e) {}
  });
  await page.goto('/turniej-tabliczka.html');

  const mk = (id, round, a, b, status) => ({
    id, round, player1: { id: a, name: a }, player2: { id: b, name: b },
    score1: 0, score2: 0, winner: null, status
  });

  // Runda 1: P1-P2, P3-P4 ; Runda 2: P1-P3
  const r1 = await page.evaluate(({ mkArgs }) => {
    isHost = false;
    isModalOpen = false;
    lastClosedMatchKey = null;
    currentTournament = {
      code: 'L', status: 'league', pointsToWin: 1, level: 'medium',
      leagueMatches: mkArgs
    };
    const m = findMyPlayableMatch();
    return m ? { id: m.id } : null;
  }, {
    mkArgs: [
      mk('lm0', 1, 'P1', 'P2', 'pending'),
      mk('lm1', 1, 'P3', 'P4', 'pending'),
      mk('lm2', 2, 'P1', 'P3', 'pending')
    ]
  });
  expect(r1?.id).toBe('lm0'); // moja gra rundy 1

  // P1-P2 zakończony, ale P3-P4 (runda 1) wciąż trwa → P1 czeka (brak meczu rundy 1)
  const r2 = await page.evaluate(({ mkArgs }) => {
    currentTournament.leagueMatches = mkArgs;
    const m = findMyPlayableMatch();
    return m ? { id: m.id } : null;
  }, {
    mkArgs: [
      mk('lm0', 1, 'P1', 'P2', 'completed'),
      mk('lm1', 1, 'P3', 'P4', 'pending'),
      mk('lm2', 2, 'P1', 'P3', 'pending')
    ]
  });
  expect(r2).toBeNull(); // NIE wchodzi do rundy 2

  // Cała runda 1 zakończona → P1 wchodzi do meczu rundy 2
  const r3 = await page.evaluate(({ mkArgs }) => {
    currentTournament.leagueMatches = mkArgs;
    const m = findMyPlayableMatch();
    return m ? { id: m.id } : null;
  }, {
    mkArgs: [
      mk('lm0', 1, 'P1', 'P2', 'completed'),
      mk('lm1', 1, 'P3', 'P4', 'completed'),
      mk('lm2', 2, 'P1', 'P3', 'pending')
    ]
  });
  expect(r3?.id).toBe('lm2');
});

// Wspólny helper: wejście do meczu pucharowego P1 vs P2 (P1 = ta przeglądarka)
async function enterKnockoutMatch(page, { timePressure = false } = {}) {
  const code = 'STAB';
  await page.evaluate(({ code, timePressure }) => {
    const bracket = [[{
      id: 'm0',
      player1: { id: 'P1', name: 'Ala', points: 0, wins: 0, played: 0 },
      player2: { id: 'P2', name: 'Bartek', points: 0, wins: 0, played: 0 },
      score1: 0, score2: 0, winner: null, status: 'ready'
    }]];
    return firebase.database().ref('tournaments/' + code).set({
      code, name: 'Stab', mode: 'knockout', groupCount: 0, level: 'medium',
      pointsToWin: 1, timePressure, status: 'knockout',
      participants: { P1: { name: 'Ala', joinedAt: 1 }, P2: { name: 'Bartek', joinedAt: 1 } },
      bracket, host: 'host_x', createdAt: 1
    });
  }, { code, timePressure });
  await page.evaluate((code) => {
    isHost = false; currentPlayer = { id: 'P1', name: 'Ala' };
    return firebase.database().ref('tournaments/' + code).once('value').then(s => {
      currentTournament = { ...s.val(), code };
      listenToTournament(code);
    });
  }, code);
  return code;
}

test('timer tury: brak odpowiedzi = utrata tury (timeout)', async ({ page }) => {
  await installMocks(page);
  await page.addInitScript(() => { try { localStorage.setItem('turniej_tabliczka_client_id', 'P1'); } catch (e) {} });
  await page.goto('/turniej-tabliczka.html');
  await enterKnockoutMatch(page, { timePressure: true });

  await expect(page.locator('#gameModal')).toHaveClass(/active/);
  await page.locator('.game-cell[data-index="0"]').click();
  await expect(page.locator('#questionPanel')).toBeVisible();
  await expect(page.locator('#timerDisplay')).toBeVisible();

  // Nie odpowiadamy — po deadline (final: 3s) autorytet odbiera turę
  await page.waitForFunction(() => liveState && liveState.turn === 'O' && liveState.phase === 'playing', null, { timeout: 8000 });
  const board = await page.evaluate(() => liveState.board);
  expect(board[0]).toBe(''); // po timeoucie znacznik nie jest stawiany
});

test('presence: wskaźnik rozłączenia przeciwnika i jego powrót', async ({ page }) => {
  await installMocks(page);
  await page.addInitScript(() => { try { localStorage.setItem('turniej_tabliczka_client_id', 'P1'); } catch (e) {} });
  await page.goto('/turniej-tabliczka.html');
  const code = await enterKnockoutMatch(page);

  await expect(page.locator('#gameModal')).toHaveClass(/active/);
  // P2 nieobecny → ostrzeżenie
  await expect(page.locator('#gameConnLine')).toContainText('rozłączony');
  // Symuluj obecność P2 → ostrzeżenie znika
  await page.evaluate((code) => firebase.database().ref('tournaments/' + code + '/matches/b_0_m0/presence/P2').set(true), code);
  await expect(page.locator('#gameConnLine')).toHaveText('');
});

test('wznowienie: wejście do trwającego meczu nie resetuje stanu', async ({ page }) => {
  await installMocks(page);
  await page.addInitScript(() => { try { localStorage.setItem('turniej_tabliczka_client_id', 'P1'); } catch (e) {} });
  await page.goto('/turniej-tabliczka.html');
  const code = 'RESUME';

  await page.evaluate((code) => {
    const bracket = [[{
      id: 'm0',
      player1: { id: 'P1', name: 'Ala' }, player2: { id: 'P2', name: 'Bartek' },
      score1: 0, score2: 0, winner: null, status: 'ready'
    }]];
    return firebase.database().ref('tournaments/' + code).set({
      code, name: 'Resume', mode: 'knockout', groupCount: 0, level: 'medium',
      pointsToWin: 1, timePressure: false, status: 'knockout',
      participants: { P1: { name: 'Ala', joinedAt: 1 }, P2: { name: 'Bartek', joinedAt: 1 } },
      bracket, host: 'host_x', createdAt: 1,
      // Trwający mecz zapisany w Firebase (jak po rozłączeniu)
      matches: { b_0_m0: { live: {
        board: ['X', '', '', '', 'O', '', '', '', ''],
        turn: 'O', phase: 'playing', score1: 0, score2: 0,
        selectedCell: null, question: null, deadline: null,
        roundWinnerRole: null, matchWinnerRole: null, seq: 5, updatedAt: 1
      } } }
    });
  }, code);

  await page.evaluate((code) => {
    isHost = false; currentPlayer = { id: 'P1', name: 'Ala' };
    return firebase.database().ref('tournaments/' + code).once('value').then(s => {
      currentTournament = { ...s.val(), code };
      listenToTournament(code);
    });
  }, code);

  await expect(page.locator('#gameModal')).toHaveClass(/active/);
  // Stan wczytany, NIE zresetowany do początkowego
  const state = await page.evaluate(() => ({ turn: liveState.turn, board: liveState.board, seq: liveState.seq }));
  expect(state.turn).toBe('O');
  expect(state.board[0]).toBe('X');
  expect(state.board[4]).toBe('O');
  expect(state.seq).toBe(5);
});

test('awaryjny reset meczu zwraca mecz do listy w pucharze', async ({ page }) => {
  await installMocks(page);
  await page.goto('/turniej-tabliczka.html');

  await page.getByRole('button', { name: 'Utwórz nowy turniej' }).click();
  await page.locator('#tournamentName').fill('Reset test');
  await page.locator('#tournamentMode').selectOption('knockout');
  await page.getByRole('button', { name: 'Utwórz turniej' }).click();

  const code = (await page.locator('#lobbyCode').innerText()).trim();
  expect(code).toHaveLength(6);

  await page.evaluate((tournamentCode) => {
    return firebase.database().ref('tournaments/' + tournamentCode + '/participants').set({
      p1: { name: 'Ala', joinedAt: Date.now() },
      p2: { name: 'Bartek', joinedAt: Date.now() }
    });
  }, code);

  await expect(page.locator('#startTournamentBtn')).toBeEnabled();
  await page.locator('#startTournamentBtn').click();

  await expect(page.locator('#tournamentPanel')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Graj!' }).first()).toBeVisible();
  await page.getByRole('button', { name: 'Graj!' }).first().click();

  await expect(page.locator('#gameModal')).toHaveClass(/active/);
  await page.evaluate(async () => {
    isHost = true;
    const originalConfirm = window.confirm;
    window.confirm = () => true;
    try {
      await resetCurrentMatch();
    } finally {
      window.confirm = originalConfirm;
    }
  });

  await expect(page.locator('#gameModal')).not.toHaveClass(/active/);
  await expect(page.getByRole('button', { name: 'Graj!' }).first()).toBeVisible();
});
