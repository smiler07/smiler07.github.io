"""Procedural arcade sound generation — no external files needed."""

from __future__ import annotations

import numpy as np
import pygame


SAMPLE_RATE = 44100


def _mix(*waves: np.ndarray) -> np.ndarray:
    max_len = max(len(w) for w in waves)
    out = np.zeros(max_len)
    for w in waves:
        out[: len(w)] += w
    return out


def _to_sound(wave: np.ndarray, volume: float = 0.35) -> pygame.mixer.Sound:
    wave = np.clip(wave * volume, -1.0, 1.0)
    stereo = np.column_stack([wave, wave])
    audio = (stereo * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(audio)


def _sine(freq: float, duration: float, decay: float = 8.0) -> np.ndarray:
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-decay * t)
    return np.sin(2 * np.pi * freq * t) * env


def _square(freq: float, duration: float, decay: float = 10.0) -> np.ndarray:
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-decay * t)
    return np.sign(np.sin(2 * np.pi * freq * t)) * env


def _noise(duration: float, decay: float = 6.0) -> np.ndarray:
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-decay * t)
    return np.random.uniform(-1, 1, n) * env


class AudioManager:
    def __init__(self) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self.enabled = True
        self._shoot_cooldown = 0.0
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._bgm_channel: pygame.mixer.Channel | None = None
        self._current_bgm: str | None = None
        self._build_sounds()
        self._build_bgm()

    def _build_sounds(self) -> None:
        # Shooting variants
        self._sounds["shoot_normal"] = _to_sound(_square(880, 0.05, 30), 0.15)
        self._sounds["shoot_rapid"] = _to_sound(_square(1200, 0.03, 40), 0.12)
        self._sounds["shoot_heavy"] = _to_sound(_square(220, 0.08, 12), 0.25)
        self._sounds["shoot_laser"] = _to_sound(_mix(_sine(1760, 0.04, 35), _sine(880, 0.04, 35)), 0.12)
        self._sounds["shoot_rocket"] = _to_sound(_mix(_noise(0.06, 20), _square(300, 0.06, 15)), 0.18)

        self._sounds["explosion_small"] = _to_sound(_mix(_noise(0.15, 8), _square(120, 0.15, 6)), 0.3)
        self._sounds["explosion_big"] = _to_sound(_mix(_noise(0.4, 4), _square(60, 0.4, 3)), 0.45)

        self._sounds["powerup"] = _to_sound(
            _mix(_sine(523, 0.08, 5), _sine(659, 0.08, 5), _sine(784, 0.12, 4)), 0.3
        )
        self._sounds["bomb"] = _to_sound(_mix(_noise(0.5, 3), _square(80, 0.5, 2)), 0.4)
        self._sounds["bomb_energy"] = _to_sound(_mix(_sine(200, 0.6, 2), _square(400, 0.6, 3)), 0.35)
        self._sounds["bomb_gale"] = _to_sound(_mix(_noise(0.5, 4), _sine(150, 0.5, 3)), 0.35)
        self._sounds["bomb_stuka"] = _to_sound(_mix(_square(180, 0.3, 5), _noise(0.4, 5)), 0.38)
        self._sounds["bomb_phantom"] = _to_sound(_mix(_square(600, 0.4, 8), _sine(300, 0.4, 6)), 0.32)

        self._sounds["boss_warning"] = _to_sound(
            _mix(_square(440, 0.15, 3), _square(330, 0.15, 3)), 0.35
        )
        self._sounds["stage_clear"] = _to_sound(
            _mix(_sine(523, 0.12, 3), _sine(659, 0.12, 3), _sine(784, 0.2, 2), _sine(1047, 0.3, 1.5)),
            0.35,
        )
        self._sounds["select"] = _to_sound(_square(660, 0.06, 20), 0.2)
        self._sounds["confirm"] = _to_sound(_mix(_sine(440, 0.08, 8), _sine(880, 0.12, 6)), 0.25)
        self._sounds["formation"] = _to_sound(_mix(_square(550, 0.2, 6), _noise(0.15, 10)), 0.3)
        self._sounds["charge_shot"] = _to_sound(
            _mix(_sine(440, 0.15, 6), _square(660, 0.12, 10), _noise(0.08, 15)), 0.28
        )
        self._sounds["charge_big"] = _to_sound(
            _mix(_sine(330, 0.25, 4), _square(220, 0.2, 5), _noise(0.15, 8)), 0.35
        )
        self._sounds["charge_loop"] = _to_sound(_sine(520, 0.12, 12), 0.08)

    def _build_bgm(self) -> None:
        """Looping chip-tune BGMs (~6-8 seconds)."""
        self._sounds["bgm_menu"] = self._make_bgm(
            duration=6.0,
            bass_notes=[130.81, 130.81, 146.83, 130.81, 110.0, 110.0, 123.47, 146.83],
            melody=[523, 659, 784, 659, 587, 523, 659, 784],
            volume=0.20,
        )
        self._sounds["bgm_play"] = self._make_bgm(
            duration=8.0,
            bass_notes=[110, 110, 130.81, 110, 98, 98, 110, 130.81],
            melody=[440, 523, 659, 523, 392, 440, 523, 440],
            volume=0.22,
        )

    def _make_bgm(
        self,
        *,
        duration: float,
        bass_notes: list[float],
        melody: list[float],
        volume: float,
    ) -> pygame.mixer.Sound:
        n = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        wave = np.zeros(n)

        steps = len(bass_notes)
        for i, freq in enumerate(bass_notes):
            start = int(i * n / steps)
            end = int((i + 1) * n / steps)
            seg_t = t[start:end] - t[start]
            wave[start:end] += np.sign(np.sin(2 * np.pi * freq * seg_t)) * 0.15 * np.exp(-1.5 * seg_t)

        steps = len(melody)
        for i, freq in enumerate(melody):
            start = int(i * n / steps)
            end = int((i + 1) * n / steps)
            seg_t = t[start:end] - t[start]
            wave[start:end] += np.sin(2 * np.pi * freq * seg_t) * 0.1 * np.exp(-3 * seg_t)

        return _to_sound(wave, volume)

    def play(self, name: str) -> None:
        if not self.enabled:
            return
        snd = self._sounds.get(name)
        if snd:
            snd.play()

    def play_shoot(self, weapon: str) -> None:
        key = {
            "rapid": "shoot_rapid",
            "heavy": "shoot_heavy",
            "laser": "shoot_laser",
        }.get(weapon, "shoot_normal")
        self.play(key)

    def play_bomb(self, bomb_id: str) -> None:
        key = {
            "energy": "bomb_energy",
            "gale": "bomb_gale",
            "stuka": "bomb_stuka",
            "phantom": "bomb_phantom",
        }.get(bomb_id, "bomb")
        self.play(key)

    def play_bgm(self, name: str = "bgm_play") -> None:
        if not self.enabled:
            return
        if self._bgm_channel is None:
            self._bgm_channel = pygame.mixer.Channel(0)
        bgm = self._sounds.get(name)
        if not bgm:
            return
        if self._current_bgm == name and self._bgm_channel.get_busy():
            return
        self._bgm_channel.stop()
        self._bgm_channel.play(bgm, loops=-1)
        self._current_bgm = name

    def start_bgm(self) -> None:
        self.play_bgm("bgm_play")

    def start_menu_bgm(self) -> None:
        self.play_bgm("bgm_menu")

    def stop_bgm(self) -> None:
        if self._bgm_channel:
            self._bgm_channel.stop()
        self._current_bgm = None

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_bgm()
        return self.enabled
