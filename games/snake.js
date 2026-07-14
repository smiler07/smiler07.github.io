const DEFAULT_GRID_SIZE = 20;
const STEP_MS = 120;

const DIRECTIONS = {
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
};

export function spawnFood(gridSize, snake, random = Math.random) {
  const occupied = new Set(snake.map(({ x, y }) => `${x},${y}`));
  const free = [];

  for (let y = 0; y < gridSize; y += 1) {
    for (let x = 0; x < gridSize; x += 1) {
      if (!occupied.has(`${x},${y}`)) {
        free.push({ x, y });
      }
    }
  }

  if (free.length === 0) {
    return null;
  }

  const index = Math.min(free.length - 1, Math.floor(random() * free.length));
  return free[index];
}

export function createSnakeState({ gridSize = DEFAULT_GRID_SIZE, random = Math.random } = {}) {
  const center = Math.floor(gridSize / 2);
  const snake = [
    { x: center, y: center },
    { x: center - 1, y: center },
    { x: center - 2, y: center },
  ];

  return {
    gridSize,
    snake,
    direction: { ...DIRECTIONS.right },
    nextDirection: { ...DIRECTIONS.right },
    food: spawnFood(gridSize, snake, random),
    score: 0,
    status: "idle",
  };
}

export function setSnakeDirection(state, direction) {
  const current = state.direction;
  const isReverse = current.x + direction.x === 0 && current.y + direction.y === 0;

  if (isReverse) {
    return false;
  }

  state.nextDirection = { ...direction };
  return true;
}

export function stepSnake(state, random = Math.random) {
  if (state.status === "gameover") {
    return state;
  }

  const direction = { ...state.nextDirection };
  const head = {
    x: state.snake[0].x + direction.x,
    y: state.snake[0].y + direction.y,
  };
  const hitWall = head.x < 0 || head.y < 0 || head.x >= state.gridSize || head.y >= state.gridSize;
  const ate = state.food && head.x === state.food.x && head.y === state.food.y;
  const bodyToCheck = ate ? state.snake : state.snake.slice(0, -1);
  const hitSelf = bodyToCheck.some(({ x, y }) => x === head.x && y === head.y);

  if (hitWall || hitSelf) {
    return { ...state, direction, status: "gameover" };
  }

  const snake = [head, ...state.snake];
  if (!ate) {
    snake.pop();
  }

  return {
    ...state,
    snake,
    direction,
    food: ate ? spawnFood(state.gridSize, snake, random) : state.food,
    score: state.score + (ate ? 10 : 0),
    status: ate && snake.length === state.gridSize ** 2 ? "gameover" : state.status,
  };
}

function directionFromKey(key) {
  const normalized = key.toLowerCase();
  const mapping = {
    arrowup: DIRECTIONS.up,
    w: DIRECTIONS.up,
    arrowdown: DIRECTIONS.down,
    s: DIRECTIONS.down,
    arrowleft: DIRECTIONS.left,
    a: DIRECTIONS.left,
    arrowright: DIRECTIONS.right,
    d: DIRECTIONS.right,
  };
  return mapping[normalized] || null;
}

export function mountSnakeGame(root, { random = Math.random } = {}) {
  const canvas = root.querySelector("canvas");
  const scoreNode = root.querySelector("[data-score]");
  const statusNode = root.querySelector("[data-status]");
  const startButton = root.querySelector("[data-action='start']");
  const pauseButton = root.querySelector("[data-action='pause']");
  const restartButton = root.querySelector("[data-action='restart']");

  if (!canvas || !scoreNode || !statusNode || !startButton || !pauseButton || !restartButton) {
    throw new Error("Snake game markup is incomplete.");
  }

  const context = canvas.getContext("2d");
  let state = createSnakeState({ random });
  let frameId = null;
  let lastTime = 0;
  let accumulator = 0;
  let destroyed = false;

  function updateHud() {
    const labels = {
      idle: "시작 대기",
      running: "플레이 중",
      paused: "일시정지",
      gameover: "게임 오버",
    };
    scoreNode.textContent = String(state.score);
    statusNode.textContent = labels[state.status];
    pauseButton.textContent = state.status === "paused" ? "계속" : "일시정지";
    pauseButton.disabled = state.status === "idle" || state.status === "gameover";
  }

  function draw() {
    const size = canvas.width;
    const cell = size / state.gridSize;
    context.clearRect(0, 0, size, size);
    context.fillStyle = "#06131f";
    context.fillRect(0, 0, size, size);

    context.strokeStyle = "rgba(255,255,255,.035)";
    context.lineWidth = 1;
    for (let index = 1; index < state.gridSize; index += 1) {
      const point = index * cell;
      context.beginPath();
      context.moveTo(point, 0);
      context.lineTo(point, size);
      context.moveTo(0, point);
      context.lineTo(size, point);
      context.stroke();
    }

    if (state.food) {
      context.fillStyle = "#ff6b78";
      context.beginPath();
      context.arc((state.food.x + 0.5) * cell, (state.food.y + 0.5) * cell, cell * 0.32, 0, Math.PI * 2);
      context.fill();
    }

    state.snake.forEach((segment, index) => {
      context.fillStyle = index === 0 ? "#b4ffe9" : `hsl(${158 - index * 1.3} 68% ${58 - Math.min(index, 18)}%)`;
      context.beginPath();
      context.roundRect(segment.x * cell + 2, segment.y * cell + 2, cell - 4, cell - 4, cell * 0.25);
      context.fill();
    });

    if (state.status === "idle" || state.status === "paused" || state.status === "gameover") {
      context.fillStyle = "rgba(3, 10, 18, .64)";
      context.fillRect(0, 0, size, size);
      context.fillStyle = "#f5f7fb";
      context.textAlign = "center";
      context.font = "700 24px system-ui";
      const message = state.status === "gameover" ? "게임 오버" : state.status === "paused" ? "일시정지" : "Snake";
      context.fillText(message, size / 2, size / 2);
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
    accumulator += Math.min(250, time - lastTime);
    lastTime = time;

    while (accumulator >= STEP_MS && state.status === "running") {
      state = stepSnake(state, random);
      accumulator -= STEP_MS;
    }
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
      state = createSnakeState({ random });
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
    state = createSnakeState({ random });
    state.status = "running";
    accumulator = 0;
    render();
    ensureLoop();
  }

  function onKeyDown(event) {
    const direction = directionFromKey(event.key);
    if (direction) {
      event.preventDefault();
      setSnakeDirection(state, direction);
    } else if (event.key.toLowerCase() === "p") {
      togglePause();
    }
  }

  function onControl(event) {
    const button = event.target.closest("[data-direction]");
    if (button && DIRECTIONS[button.dataset.direction]) {
      event.preventDefault();
      setSnakeDirection(state, DIRECTIONS[button.dataset.direction]);
    }
  }

  function onVisibilityChange() {
    if (document.hidden && state.status === "running") {
      state.status = "paused";
      render();
    }
  }

  startButton.addEventListener("click", start);
  pauseButton.addEventListener("click", togglePause);
  restartButton.addEventListener("click", restart);
  root.addEventListener("pointerdown", onControl);
  window.addEventListener("keydown", onKeyDown, { passive: false });
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
      root.removeEventListener("pointerdown", onControl);
      window.removeEventListener("keydown", onKeyDown);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    },
    getState: () => state,
  };
}
