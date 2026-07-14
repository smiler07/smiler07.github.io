import test from "node:test";
import assert from "node:assert/strict";

import {
  createSnakeState,
  setSnakeDirection,
  spawnFood,
  stepSnake,
} from "../games/snake.js";
import {
  createShootingState,
  fireShot,
  intersects,
  spawnEnemy,
  updateShooting,
} from "../games/shooting.js";

test("Snake blocks an immediate reverse and moves one grid cell", () => {
  const state = createSnakeState({ random: () => 0 });
  assert.equal(setSnakeDirection(state, { x: -1, y: 0 }), false);
  assert.equal(setSnakeDirection(state, { x: 0, y: -1 }), true);
  const next = stepSnake(state, () => 0);
  assert.deepEqual(next.snake[0], { x: state.snake[0].x, y: state.snake[0].y - 1 });
});

test("Snake grows and scores when it eats", () => {
  const state = createSnakeState({ random: () => 0 });
  state.food = { x: state.snake[0].x + 1, y: state.snake[0].y };
  const next = stepSnake(state, () => 0);
  assert.equal(next.snake.length, state.snake.length + 1);
  assert.equal(next.score, 10);
});

test("Snake food never occupies its body", () => {
  const food = spawnFood(4, [{ x: 0, y: 0 }, { x: 1, y: 0 }], () => 0);
  assert.deepEqual(food, { x: 2, y: 0 });
});

test("Snake reports wall collision", () => {
  const state = createSnakeState({ gridSize: 4, random: () => 0 });
  state.snake = [{ x: 3, y: 1 }];
  state.direction = { x: 1, y: 0 };
  state.nextDirection = { x: 1, y: 0 };
  assert.equal(stepSnake(state, () => 0).status, "gameover");
});

test("Snake reports collision with its own body", () => {
  const state = createSnakeState({ gridSize: 5, random: () => 0 });
  state.snake = [
    { x: 1, y: 1 },
    { x: 1, y: 2 },
    { x: 2, y: 2 },
    { x: 2, y: 1 },
  ];
  state.direction = { x: 0, y: 1 };
  state.nextDirection = { x: 0, y: 1 };
  assert.equal(stepSnake(state, () => 0).status, "gameover");
});

test("Shooting player stays inside the logical canvas", () => {
  const state = createShootingState();
  state.status = "running";
  state.player.x = 2;
  state.player.y = 2;
  const next = updateShooting(state, 1, { left: true, up: true }, () => 1);
  assert.ok(next.player.x >= next.player.width / 2);
  assert.ok(next.player.y >= next.player.height / 2);
});

test("Shooting fire obeys cooldown", () => {
  const state = createShootingState();
  state.status = "running";
  assert.equal(fireShot(state), true);
  assert.equal(fireShot(state), false);
  assert.equal(state.bullets.length, 1);
});

test("Shooting bullet collision removes enemy and increases score", () => {
  const state = createShootingState();
  state.status = "running";
  state.enemies = [{ x: 100, y: 100, width: 28, height: 24, speed: 0, shootTimer: 9 }];
  state.bullets = [{ x: 100, y: 100, width: 4, height: 12, speed: 0 }];
  const next = updateShooting(state, 0.016, {}, () => 1);
  assert.equal(next.enemies.length, 0);
  assert.equal(next.bullets.length, 0);
  assert.equal(next.score, 100);
});

test("Shooting spawn is deterministic and rectangles intersect", () => {
  const enemy = spawnEnemy({ width: 384 }, () => 0);
  assert.equal(enemy.x, enemy.width / 2);
  assert.equal(intersects(enemy, { ...enemy }), true);
});

test("Shooting reaches game over after the final life is lost", () => {
  const state = createShootingState();
  state.status = "running";
  state.player.lives = 1;
  state.enemies = [{
    x: state.player.x,
    y: state.player.y,
    width: 28,
    height: 24,
    speed: 0,
    shootTimer: 9,
  }];
  const next = updateShooting(state, 0.016, {}, () => 1);
  assert.equal(next.player.lives, 0);
  assert.equal(next.status, "gameover");
});

test("Shooting enemy projectile reduces a life", () => {
  const state = createShootingState();
  state.status = "running";
  state.enemyBullets = [{
    x: state.player.x,
    y: state.player.y,
    width: 7,
    height: 10,
    speed: 0,
  }];
  const next = updateShooting(state, 0.016, {}, () => 1);
  assert.equal(next.player.lives, 2);
  assert.equal(next.enemyBullets.length, 0);
});
