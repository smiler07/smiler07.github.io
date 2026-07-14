const LOGICAL_WIDTH = 384;
const LOGICAL_HEIGHT = 448;
const PLAYER_SPEED = 230;
const FIRE_COOLDOWN = 0.16;

const DIFFICULTY = {
  easy: { lives: 5, enemySpeed: 0.72, spawnInterval: 1.35, scoreMultiplier: 1 },
  normal: { lives: 3, enemySpeed: 1, spawnInterval: 1.05, scoreMultiplier: 1 },
  hard: { lives: 2, enemySpeed: 1.28, spawnInterval: 0.72, scoreMultiplier: 2 },
};

export const PLANES = {
  p38: { name: "P-38", speed: 230, fireRate: 0.16, color: "#63f3d1" },
  spitfire: { name: "Spitfire", speed: 245, fireRate: 0.12, color: "#ffe45e" },
  shinden: { name: "Shinden", speed: 275, fireRate: 0.19, color: "#b983ff" },
};

export function getShootingConfig(difficulty = "normal") {
  return { ...(DIFFICULTY[difficulty] || DIFFICULTY.normal) };
}

function cloneState(state) {
  return {
    ...state,
    player: { ...state.player },
    bullets: state.bullets.map((item) => ({ ...item })),
    enemyBullets: state.enemyBullets.map((item) => ({ ...item })),
    enemies: state.enemies.map((item) => ({ ...item })),
    effects: (state.effects || []).map((item) => ({ ...item })),
  };
}

export function createShootingState({ difficulty = "normal", planeId = "p38" } = {}) {
  const config = getShootingConfig(difficulty);
  const plane = PLANES[planeId] || PLANES.p38;
  return {
    width: LOGICAL_WIDTH,
    height: LOGICAL_HEIGHT,
    status: "idle",
    score: 0,
    difficulty,
    scoreMultiplier: config.scoreMultiplier,
    spawnInterval: config.spawnInterval,
    enemySpeedMultiplier: config.enemySpeed,
    elapsed: 0,
    spawnTimer: 0.65,
    fireCooldown: 0,
    playerInvulnerable: 0,
    bombs: 3,
    bombWave: 0,
    effects: [],
    player: {
      x: LOGICAL_WIDTH / 2,
      y: LOGICAL_HEIGHT - 54,
      width: 26,
      height: 28,
      lives: config.lives,
      speed: plane.speed,
      fireRate: plane.fireRate,
      color: plane.color,
      planeId,
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
    speed: (66 + random() * 35) * (state.enemySpeedMultiplier || 1),
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
  state.fireCooldown = state.player.fireRate || FIRE_COOLDOWN;
  return true;
}

export function useBomb(state) {
  if (state.status !== "running" || state.bombs <= 0) {
    return false;
  }
  state.bombs -= 1;
  state.bombWave = 0.75;
  state.effects.push(...state.enemies.map((enemy, index) => ({
    x: enemy.x,
    y: enemy.y,
    life: 0.65,
    radius: 8 + (index % 4) * 3,
    color: index % 2 ? "#ffe45e" : "#ff5d8f",
  })));
  state.enemies = [];
  state.enemyBullets = [];
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
  const playerSpeed = state.player.speed || PLAYER_SPEED;
  state.player.x += dx * playerSpeed * dt;
  state.player.y += dy * playerSpeed * dt;
  state.player.x = Math.max(state.player.width / 2, Math.min(state.width - state.player.width / 2, state.player.x));
  state.player.y = Math.max(state.player.height / 2, Math.min(state.height - state.player.height / 2, state.player.y));

  if (input.fire) {
    fireShot(state);
  }
  if (input.bomb) {
    useBomb(state);
  }

  state.bombWave = Math.max(0, state.bombWave - dt);
  state.effects.forEach((effect) => {
    effect.life -= dt;
    effect.radius += 48 * dt;
  });
  state.effects = state.effects.filter((effect) => effect.life > 0);

  state.spawnTimer -= dt;
  if (state.spawnTimer <= 0) {
    state.enemies.push(spawnEnemy(state, random));
    state.spawnTimer = Math.max(0.34, state.spawnInterval - state.elapsed * 0.006);
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
        state.score += 100 * state.scoreMultiplier;
        state.effects.push({ x: enemy.x, y: enemy.y, life: 0.55, radius: 8, color: "#ffe45e" });
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

export function mountShootingGame(root, { random = Math.random, difficulty = "normal" } = {}) {
  const canvas = root.querySelector("canvas");
  const scoreNode = root.querySelector("[data-score]");
  const livesNode = root.querySelector("[data-lives]");
  const bombsNode = root.querySelector("[data-bombs]");
  const statusNode = root.querySelector("[data-status]");
  const startButton = root.querySelector("[data-action='start']");
  const pauseButton = root.querySelector("[data-action='pause']");
  const restartButton = root.querySelector("[data-action='restart']");
  const bombActionButton = root.querySelector("[data-action='bomb']");
  const planeButtons = [...root.querySelectorAll("[data-plane]")];

  if (!canvas || !scoreNode || !livesNode || !bombsNode || !statusNode || !startButton || !pauseButton || !restartButton || !bombActionButton) {
    throw new Error("Shooting game markup is incomplete.");
  }

  const context = canvas.getContext("2d");
  const input = { up: false, down: false, left: false, right: false, fire: false, bomb: false };
  let selectedPlane = planeButtons.find((button) => button.getAttribute("aria-checked") === "true")?.dataset.plane || "p38";
  let state = createShootingState({ difficulty, planeId: selectedPlane });
  let frameId = null;
  let lastTime = 0;
  let destroyed = false;

  function updateHud() {
    const labels = { idle: "시작 대기", running: "플레이 중", paused: "일시정지", gameover: "게임 오버" };
    scoreNode.textContent = String(state.score);
    livesNode.textContent = String(state.player.lives);
    bombsNode.textContent = String(state.bombs);
    statusNode.textContent = labels[state.status];
    pauseButton.textContent = state.status === "paused" ? "계속" : "일시정지";
    pauseButton.disabled = state.status === "idle" || state.status === "gameover";
    bombActionButton.disabled = state.status !== "running" || state.bombs <= 0;
  }

  function draw() {
    const gradient = context.createLinearGradient(0, 0, 0, state.height);
    gradient.addColorStop(0, "#071235");
    gradient.addColorStop(0.48, "#483d9b");
    gradient.addColorStop(1, "#ff6f61");
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

    state.effects.forEach((effect) => {
      context.globalAlpha = Math.max(0, effect.life / 0.65);
      context.strokeStyle = effect.color;
      context.lineWidth = 4;
      context.beginPath();
      context.arc(effect.x, effect.y, effect.radius, 0, Math.PI * 2);
      context.stroke();
    });
    context.globalAlpha = 1;

    if (state.bombWave > 0) {
      const progress = 1 - state.bombWave / 0.75;
      context.strokeStyle = `rgba(255, 228, 94, ${state.bombWave / 0.75})`;
      context.lineWidth = 12;
      context.beginPath();
      context.arc(state.player.x, state.player.y, 24 + progress * state.width, 0, Math.PI * 2);
      context.stroke();
    }

    if (state.playerInvulnerable <= 0 || Math.floor(state.playerInvulnerable * 12) % 2 === 0) {
      context.fillStyle = state.player.color;
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
      state = createShootingState({ difficulty, planeId: selectedPlane });
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
    state = createShootingState({ difficulty, planeId: selectedPlane });
    state.status = "running";
    render();
    ensureLoop();
  }

  function actionFromKey(key) {
    const mapping = {
      arrowup: "up", w: "up", arrowdown: "down", s: "down",
      arrowleft: "left", a: "left", arrowright: "right", d: "right",
      " ": "fire", z: "fire", x: "bomb",
    };
    return mapping[key.toLowerCase()] || null;
  }

  function onKeyDown(event) {
    if (event.target instanceof Element && event.target.closest("[data-plane]")) return;
    const action = actionFromKey(event.key);
    if (action) {
      event.preventDefault();
      if (action === "bomb") {
        if (!event.repeat) useBomb(state);
        render();
      } else {
        input[action] = true;
      }
    } else if ((event.key === "Escape" || event.key.toLowerCase() === "p") && !event.repeat) {
      event.preventDefault();
      togglePause();
    }
  }

  function onKeyUp(event) {
    const action = actionFromKey(event.key);
    if (action) {
      event.preventDefault();
      if (action !== "bomb") input[action] = false;
    }
  }

  function setPointerAction(event, value) {
    const button = event.target.closest("[data-control]");
    if (!button) return;
    event.preventDefault();
    const action = button.dataset.control;
    if (action !== "bomb") input[action] = value;
    if (value && action === "fire") fireShot(state);
    if (value && action === "bomb") useBomb(state);
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

  function onBombAction() {
    useBomb(state);
    render();
  }

  function onPlaneSelect(event) {
    const button = event.target.closest("[data-plane]");
    if (!button || state.status === "running") return;
    selectedPlane = button.dataset.plane;
    planeButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-checked", String(selected));
    });
    state = createShootingState({ difficulty, planeId: selectedPlane });
    render();
  }

  function onPlaneKeyDown(event) {
    const button = event.target.closest("[data-plane]");
    if (!button || !["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    event.stopPropagation();
    const index = planeButtons.indexOf(button);
    let nextIndex = index;
    if (["ArrowLeft", "ArrowUp"].includes(event.key)) nextIndex = (index - 1 + planeButtons.length) % planeButtons.length;
    if (["ArrowRight", "ArrowDown"].includes(event.key)) nextIndex = (index + 1) % planeButtons.length;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = planeButtons.length - 1;
    planeButtons[nextIndex].click();
    planeButtons[nextIndex].focus();
  }

  startButton.addEventListener("click", start);
  pauseButton.addEventListener("click", togglePause);
  restartButton.addEventListener("click", restart);
  bombActionButton.addEventListener("click", onBombAction);
  root.addEventListener("click", onPlaneSelect);
  root.addEventListener("keydown", onPlaneKeyDown);
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
      bombActionButton.removeEventListener("click", onBombAction);
      root.removeEventListener("click", onPlaneSelect);
      root.removeEventListener("keydown", onPlaneKeyDown);
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
