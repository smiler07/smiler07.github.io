import { mountSnakeGame } from "./games/snake.js";
import { mountShootingGame } from "./games/shooting.js";

document.documentElement.classList.add("js");

const navToggle = document.querySelector(".nav-toggle");
const navigation = document.querySelector("#primary-navigation");
const year = document.querySelector("#current-year");

function setNavigationOpen(isOpen) {
  if (!navToggle || !navigation) {
    return;
  }

  navToggle.setAttribute("aria-expanded", String(isOpen));
  navigation.classList.toggle("is-open", isOpen);

  const label = navToggle.querySelector(".sr-only");
  if (label) {
    label.textContent = isOpen ? "메뉴 닫기" : "메뉴 열기";
  }
}

if (navToggle && navigation) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    setNavigationOpen(!isOpen);
  });

  navigation.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      setNavigationOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navigation.classList.contains("is-open")) {
      setNavigationOpen(false);
      navToggle.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 768) {
      setNavigationOpen(false);
    }
  });
}

if (year) {
  year.textContent = String(new Date().getFullYear());
}

const gameTabs = [...document.querySelectorAll("[data-game][role='tab']")];
const gamePanels = [...document.querySelectorAll("[data-game-panel]")];
const difficultyButtons = [...document.querySelectorAll("[data-difficulty]")];
const selectionStatus = document.querySelector("#game-selection-status");
const gameFactories = {
  snake: mountSnakeGame,
  shooting: mountShootingGame,
};
let activeGame = null;
let activeController = null;
let activeDifficulty = "normal";

function selectGame(gameName, { focus = false } = {}) {
  if (!gameFactories[gameName] || activeGame === gameName) {
    if (focus) {
      gameTabs.find((tab) => tab.dataset.game === gameName)?.focus();
    }
    return;
  }

  activeController?.destroy();
  activeController = null;
  activeGame = gameName;

  gameTabs.forEach((tab) => {
    const selected = tab.dataset.game === gameName;
    tab.classList.toggle("is-active", selected);
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && focus) tab.focus();
  });

  gamePanels.forEach((panel) => {
    panel.hidden = panel.dataset.gamePanel !== gameName;
  });

  const panel = gamePanels.find((item) => item.dataset.gamePanel === gameName);
  activeController = gameFactories[gameName](panel, { difficulty: activeDifficulty });
  if (selectionStatus) {
    const label = gameName === "snake" ? "Snake" : "Shooting";
    selectionStatus.textContent = `${label} · ${activeDifficulty.toUpperCase()} 모드를 선택했습니다.`;
  }
}

gameTabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectGame(tab.dataset.game));
  tab.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === "ArrowLeft") nextIndex = (index - 1 + gameTabs.length) % gameTabs.length;
    if (event.key === "ArrowRight") nextIndex = (index + 1) % gameTabs.length;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = gameTabs.length - 1;
    selectGame(gameTabs[nextIndex].dataset.game, { focus: true });
  });
});

function chooseDifficulty(button, { focus = false } = {}) {
    activeDifficulty = button.dataset.difficulty;
    difficultyButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-checked", String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    if (focus) button.focus();

    if (activeGame) {
      const gameToRemount = activeGame;
      activeController?.destroy();
      activeController = null;
      activeGame = null;
      selectGame(gameToRemount);
    } else if (selectionStatus) {
      selectionStatus.textContent = `${activeDifficulty.toUpperCase()} 모드입니다. 게임을 선택하세요.`;
    }
}

difficultyButtons.forEach((button, index) => {
  button.addEventListener("click", () => chooseDifficulty(button));
  button.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    event.stopPropagation();
    let nextIndex = index;
    if (["ArrowLeft", "ArrowUp"].includes(event.key)) nextIndex = (index - 1 + difficultyButtons.length) % difficultyButtons.length;
    if (["ArrowRight", "ArrowDown"].includes(event.key)) nextIndex = (index + 1) % difficultyButtons.length;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = difficultyButtons.length - 1;
    chooseDifficulty(difficultyButtons[nextIndex], { focus: true });
  });
});

gamePanels.forEach((panel) => { panel.hidden = true; });
