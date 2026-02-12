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
