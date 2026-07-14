const LOGICAL_WIDTH = 384;
const LOGICAL_HEIGHT = 448;
const PLAYER_SPEED = 230;
const FIRE_COOLDOWN = 0.16;

function cloneState(state) {
  return {
    ...state,
    player: { ...state.player },
    bullets: state.bullets.map((item) => ({ ...item })),
    enemyBullets: state.enemyBullets.map((item) => ({ ...item })),
    enemies: state.enemies.map((item) => ({ ...item })),
  };
}

export function createShootingState() {
  return {
    width: LOGICAL_WIDTH,
    height: LOGICAL_HEIGHT,
    status: "idle",
    score: 0,
    elapsed: 0,
    spawnTimer: 0.65,
    fireCooldown: 0,
    playerInvulnerable: 0,
    player: {
      x: LOGICAL_WIDTH / 2,
      y: LOGICAL_HEIGHT - 54,
      width: 26,
      height: 28,
      lives: 3,
    },
    bullets: [],
    enemyBullets: [],
    enemies: [],
  };
}

export function intersects(a, b) {
  return Math.abs(a.x - b.x) * 2 < a.width + b.width
    && Math.abs(a.y - b.y) * 2 < a.height + b.height;
}

export function spawnEnemy(state, random = Math.random) {
  const width = 28;
  return {
    x: width / 2 + random() * (state.width - width),
    y: -18,
    width,
    height: 24,
    speed: 66 + random() * 35,
    shootTimer: 1.2 + random() * 1.6,
  };
}

export function fireShot(state) {
  if (state.status !== "running" || state.fireCooldown > 0) {
    return false;
  }
  state.bullets.push({
    x: state.player.x,
    y: state.player.y - state.player.height / 2,
    width: 4,
    height: 13,
    speed: 360,
  });
  state.fireCooldown = FIRE_COOLDOWN;
  return true;
}

function hitPlayer(state) {
  if (state.playerInvulnerable > 0) {
    return;
  }
  state.player.lives = Math.max(0, state.player.lives - 1);
  state.playerInvulnerable = 1.1;
  state.player.x = state.width / 2;
  state.player.y = state.height - 54;
  if (state.player.lives === 0) {
    state.status = "gameover";
  }
}

export function updateShooting(current, deltaSeconds, input = {}, random = Math.random) {
  if (current.status !== "running") {
    return current;
  }

  const state = cloneState(current);
  const dt = Math.min(0.05, Math.max(0, deltaSeconds));
  state.elapsed += dt;
  state.fireCooldown = Math.max(0, state.fireCooldown - dt);
  state.playerInvulnerable = Math.max(0, state.playerInvulnerable - dt);

  let dx = Number(Boolean(input.right)) - Number(Boolean(input.left));
  let dy = Number(Boolean(input.down)) - Number(Boolean(input.up));
  if (dx && dy) {
    dx *= Math.SQRT1_2;
    dy *= Math.SQRT1_2;
  }
  state.player.x += dx * PLAYER_SPEED * dt;
  state.player.y += dy * PLAYER_SPEED * dt;
  state.player.x = Math.max(state.player.width / 2, Math.min(state.width - state.player.width / 2, state.player.x));
  state.player.y = Math.max(state.player.height / 2, Math.min(state.height - state.player.height / 2, state.player.y));

  if (input.fire) {
    fireShot(state);
  }

  state.spawnTimer -= dt;
  if (state.spawnTimer <= 0) {
    state.enemies.push(spawnEnemy(state, random));
    state.spawnTimer = Math.max(0.42, 1.05 - state.elapsed * 0.006);
  }

  state.bullets.forEach((bullet) => {
    bullet.y -= bullet.speed * dt;
  });
  state.enemyBullets.forEach((bullet) => {
    bullet.y += bullet.speed * dt;
  });
  state.enemies.forEach((enemy) => {
    enemy.y += enemy.speed * dt;
    enemy.shootTimer -= dt;
    if (enemy.shootTimer <= 0 && enemy.y > 0 && enemy.y < state.height * 0.72) {
      state.enemyBullets.push({ x: enemy.x, y: enemy.y + 12, width: 7, height: 10, speed: 145 });
      enemy.shootTimer = 1.5 + random() * 1.4;
    }
  });

  const removedBullets = new Set();
  const removedEnemies = new Set();
  state.bullets.forEach((bullet, bulletIndex) => {
    state.enemies.forEach((enemy, enemyIndex) => {
      if (!removedBullets.has(bulletIndex) && !removedEnemies.has(enemyIndex) && intersects(bullet, enemy)) {
        removedBullets.add(bulletIndex);
        removedEnemies.add(enemyIndex);
        state.score += 100;
      }
    });
  });

  state.enemies.forEach((enemy, enemyIndex) => {
    if (!removedEnemies.has(enemyIndex) && intersects(enemy, state.player)) {
      removedEnemies.add(enemyIndex);
      hitPlayer(state);
    }
  });
  state.enemyBullets.forEach((bullet, bulletIndex) => {
    if (intersects(bullet, state.player)) {
      removedBullets.add(`enemy-${bulletIndex}`);
      hitPlayer(state);
    }
  });

  state.bullets = state.bullets.filter((bullet, index) => bullet.y > -20 && !removedBullets.has(index));
  state.enemyBullets = state.enemyBullets.filter((bullet, index) => bullet.y < state.height + 20 && !removedBullets.has(`enemy-${index}`));
  state.enemies = state.enemies.filter((enemy, index) => enemy.y < state.height + 36 && !removedEnemies.has(index));
  return state;
}

export function mountShootingGame(root, { random = Math.random } = {}) {
  const canvas = root.querySelector("canvas");
  const scoreNode = root.querySelector("[data-score]");
  const livesNode = root.querySelector("[data-lives]");
  const statusNode = root.querySelector("[data-status]");
  const startButton = root.querySelector("[data-action='start']");
  const pauseButton = root.querySelector("[data-action='pause']");
  const restartButton = root.querySelector("[data-action='restart']");

  if (!canvas || !scoreNode || !livesNode || !statusNode || !startButton || !pauseButton || !restartButton) {
    throw new Error("Shooting game markup is incomplete.");
  }

  const context = canvas.getContext("2d");
  const input = { up: false, down: false, left: false, right: false, fire: false };
  let state = createShootingState();
  let frameId = null;
  let lastTime = 0;
  let destroyed = false;

  function updateHud() {
    const labels = { idle: "시작 대기", running: "플레이 중", paused: "일시정지", gameover: "게임 오버" };
    scoreNode.textContent = String(state.score);
    livesNode.textContent = String(state.player.lives);
    statusNode.textContent = labels[state.status];
    pauseButton.textContent = state.status === "paused" ? "계속" : "일시정지";
    pauseButton.disabled = state.status === "idle" || state.status === "gameover";
  }

  function draw() {
    const gradient = context.createLinearGradient(0, 0, 0, state.height);
    gradient.addColorStop(0, "#071235");
    gradient.addColorStop(0.55, "#263a72");
    gradient.addColorStop(1, "#9e4938");
    context.fillStyle = gradient;
    context.fillRect(0, 0, state.width, state.height);

    context.fillStyle = "rgba(255,255,255,.45)";
    for (let index = 0; index < 22; index += 1) {
      const x = (index * 73) % state.width;
      const y = (index * 109 + state.elapsed * (18 + index % 3)) % state.height;
      context.fillRect(x, y, 2, 2);
    }

    state.bullets.forEach((bullet) => {
      context.fillStyle = "#b8f7ff";
      context.fillRect(bullet.x - bullet.width / 2, bullet.y - bullet.height / 2, bullet.width, bullet.height);
    });
    state.enemyBullets.forEach((bullet) => {
      context.fillStyle = "#ffb45e";
      context.beginPath();
      context.arc(bullet.x, bullet.y, bullet.width / 2, 0, Math.PI * 2);
      context.fill();
    });
    state.enemies.forEach((enemy) => {
      context.fillStyle = "#ed5a63";
      context.beginPath();
      context.moveTo(enemy.x, enemy.y + enemy.height / 2);
      context.lineTo(enemy.x - enemy.width / 2, enemy.y - enemy.height / 2);
      context.lineTo(enemy.x, enemy.y - enemy.height / 4);
      context.lineTo(enemy.x + enemy.width / 2, enemy.y - enemy.height / 2);
      context.closePath();
      context.fill();
    });

    if (state.playerInvulnerable <= 0 || Math.floor(state.playerInvulnerable * 12) % 2 === 0) {
      context.fillStyle = "#7cebd0";
      context.beginPath();
      context.moveTo(state.player.x, state.player.y - state.player.height / 2);
      context.lineTo(state.player.x - state.player.width / 2, state.player.y + state.player.height / 2);
      context.lineTo(state.player.x, state.player.y + state.player.height / 4);
      context.lineTo(state.player.x + state.player.width / 2, state.player.y + state.player.height / 2);
      context.closePath();
      context.fill();
    }

    if (state.status !== "running") {
      context.fillStyle = "rgba(3, 8, 22, .64)";
      context.fillRect(0, 0, state.width, state.height);
      context.fillStyle = "#f5f7fb";
      context.textAlign = "center";
      context.font = "700 24px system-ui";
      const message = state.status === "gameover" ? "게임 오버" : state.status === "paused" ? "일시정지" : "Shooting";
      context.fillText(message, state.width / 2, state.height / 2);
    }
  }

  function render() {
    updateHud();
    draw();
  }

  function loop(time) {
    frameId = null;
    if (destroyed || state.status !== "running") {
      return;
    }
    if (!lastTime) {
      lastTime = time;
    }
    const dt = (time - lastTime) / 1000;
    lastTime = time;
    state = updateShooting(state, dt, input, random);
    render();
    if (state.status === "running") {
      frameId = requestAnimationFrame(loop);
    }
  }

  function ensureLoop() {
    if (frameId === null && state.status === "running") {
      lastTime = 0;
      frameId = requestAnimationFrame(loop);
    }
  }

  function start() {
    if (state.status === "idle" || state.status === "gameover") {
      state = createShootingState();
    }
    state.status = "running";
    render();
    ensureLoop();
  }

  function togglePause() {
    if (state.status === "running") {
      state.status = "paused";
    } else if (state.status === "paused") {
      state.status = "running";
      ensureLoop();
    }
    render();
  }

  function restart() {
    state = createShootingState();
    state.status = "running";
    render();
    ensureLoop();
  }

  function actionFromKey(key) {
    const mapping = {
      arrowup: "up", w: "up", arrowdown: "down", s: "down",
      arrowleft: "left", a: "left", arrowright: "right", d: "right",
      " ": "fire", z: "fire",
    };
    return mapping[key.toLowerCase()] || null;
  }

  function onKeyDown(event) {
    const action = actionFromKey(event.key);
    if (action) {
      event.preventDefault();
      input[action] = true;
    } else if ((event.key === "Escape" || event.key.toLowerCase() === "p") && !event.repeat) {
      event.preventDefault();
      togglePause();
    }
  }

  function onKeyUp(event) {
    const action = actionFromKey(event.key);
    if (action) {
      event.preventDefault();
      input[action] = false;
    }
  }

  function setPointerAction(event, value) {
    const button = event.target.closest("[data-control]");
    if (!button) return;
    event.preventDefault();
    const action = button.dataset.control;
    input[action] = value;
    if (value && action === "fire") fireShot(state);
    if (value && button.setPointerCapture) button.setPointerCapture(event.pointerId);
  }

  function onPointerDown(event) { setPointerAction(event, true); }
  function onPointerUp(event) { setPointerAction(event, false); }
  function onVisibilityChange() {
    if (document.hidden && state.status === "running") {
      state.status = "paused";
      Object.keys(input).forEach((key) => { input[key] = false; });
      render();
    }
  }

  startButton.addEventListener("click", start);
  pauseButton.addEventListener("click", togglePause);
  restartButton.addEventListener("click", restart);
  root.addEventListener("pointerdown", onPointerDown);
  root.addEventListener("pointerup", onPointerUp);
  root.addEventListener("pointercancel", onPointerUp);
  window.addEventListener("keydown", onKeyDown, { passive: false });
  window.addEventListener("keyup", onKeyUp, { passive: false });
  document.addEventListener("visibilitychange", onVisibilityChange);
  render();

  return {
    pause() {
      if (state.status === "running") {
        state.status = "paused";
        render();
      }
    },
    destroy() {
      destroyed = true;
      if (frameId !== null) {
        cancelAnimationFrame(frameId);
        frameId = null;
      }
      startButton.removeEventListener("click", start);
      pauseButton.removeEventListener("click", togglePause);
      restartButton.removeEventListener("click", restart);
      root.removeEventListener("pointerdown", onPointerDown);
      root.removeEventListener("pointerup", onPointerUp);
      root.removeEventListener("pointercancel", onPointerUp);
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    },
    getState: () => state,
  };
}
