"""Procedural arcade sound generation — no external files needed."""

from __future__ import annotations

import numpy as np
import pygame

from src.core.music_composer import ensure_combat_wav


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


def _saw(freq: float, duration: float, decay: float = 10.0) -> np.ndarray:
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-decay * t)
    phase = (freq * t) % 1.0
    return (2.0 * phase - 1.0) * env


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
        self._sounds["bomb_launch"] = _to_sound(_mix(_sine(170, 0.18, 6), _saw(95, 0.18, 8)), 0.24)
        self._sounds["bomb_impact"] = _to_sound(_mix(_noise(0.42, 4), _square(62, 0.38, 3), _sine(95, 0.28, 4)), 0.46)
        self._sounds["bomb_energy"] = _to_sound(_mix(_sine(200, 0.6, 2), _square(400, 0.6, 3)), 0.35)
        self._sounds["bomb_gale"] = _to_sound(_mix(_noise(0.5, 4), _sine(150, 0.5, 3)), 0.35)
        self._sounds["bomb_stuka"] = _to_sound(_mix(_square(180, 0.3, 5), _noise(0.4, 5)), 0.38)
        self._sounds["bomb_phantom"] = _to_sound(_mix(_square(600, 0.4, 8), _sine(300, 0.4, 6)), 0.32)
        self._sounds["bomb_nova"] = _to_sound(_mix(_sine(180, 0.5, 2), _saw(420, 0.42, 5), _noise(0.25, 9)), 0.38)

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
        """Two fully layered, deterministic arcade loops (no media files required)."""
        self._sounds["bgm_menu"] = self._make_bgm(
            duration=15.0,
            bass_notes=[130.81, 130.81, 146.83, 164.81, 174.61, 164.81, 146.83, 123.47],
            melody=[659, 784, 880, 1047, 988, 880, 784, 659, 587, 659, 784, 880, 784, 659, 587, 523],
            accent=[988, 1175, 1319, 1175, 1047, 988, 880, 784],
            volume=0.18,
        )
        self._sounds["bgm_play"] = self._make_bgm(
            duration=15.0,
            bass_notes=[110, 110, 123.47, 146.83, 164.81, 146.83, 123.47, 98.0],
            melody=[440, 523, 659, 784, 880, 784, 659, 523, 494, 587, 698, 880, 784, 698, 587, 494],
            accent=[659, 784, 988, 880, 1047, 1175, 988, 784],
            volume=0.22,
        )
        # The combat theme is rendered as a reusable WAV asset, not merely a
        # short runtime beep loop.  Keep the synth fallback if a read-only build
        # environment prevents cache creation.
        try:
            self._sounds["bgm_play"] = pygame.mixer.Sound(str(ensure_combat_wav()))
            self._sounds["bgm_play"].set_volume(0.72)
        except (OSError, pygame.error):
            pass

    def _make_bgm(
        self,
        *,
        duration: float,
        bass_notes: list[float],
        melody: list[float],
        accent: list[float],
        volume: float,
    ) -> pygame.mixer.Sound:
        n = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        wave = np.zeros(n)

        # 128 BPM / 8 bars: tight enough for an arcade cabinet, long enough to avoid
        # the obvious "eight-note ringtone" loop from the prototype.
        beat = duration / 32

        def add_note(freq: float, start_s: float, length: float, amp: float, shape: str, release: float) -> None:
            start = int(start_s * SAMPLE_RATE)
            end = min(n, start + int(length * SAMPLE_RATE))
            if end <= start:
                return
            seg_t = t[start:end] - t[start]
            env = np.exp(-release * seg_t)
            if shape == "square":
                tone = np.sign(np.sin(2 * np.pi * freq * seg_t))
            elif shape == "saw":
                tone = 2.0 * ((freq * seg_t) % 1.0) - 1.0
            else:
                tone = np.sin(2 * np.pi * freq * seg_t)
            wave[start:end] += tone * env * amp

        def add_step(notes: list[float], amp: float, shape: str, decay: float) -> None:
            steps = len(notes)
            for i, freq in enumerate(notes):
                start = int(i * n / steps)
                end = int((i + 1) * n / steps)
                seg_t = t[start:end] - t[start]
                if shape == "square":
                    wave[start:end] += np.sign(np.sin(2 * np.pi * freq * seg_t)) * amp * np.exp(-decay * seg_t)
                elif shape == "saw":
                    phase = (freq * seg_t) % 1.0
                    wave[start:end] += (2.0 * phase - 1.0) * amp * np.exp(-decay * seg_t)
                else:
                    wave[start:end] += np.sin(2 * np.pi * freq * seg_t) * amp * np.exp(-decay * seg_t)

        # Sub bass on every beat, octave pulse on the off-beats, and an arpeggiated
        # chord bed provide the classic 16-bit "stage one" propulsion.
        for step in range(32):
            root = bass_notes[(step // 4) % len(bass_notes)]
            at = step * beat
            add_note(root, at, beat * 0.82, 0.17, "square", 3.2)
            if step % 2:
                add_note(root * 2, at, beat * 0.36, 0.055, "saw", 9.0)
            chord = (root * 2, root * 2.5198, root * 3.0)
            for j, note in enumerate(chord):
                add_note(note, at + (j * 0.045), beat * 0.55, 0.026, "sine", 2.2)

        for step in range(64):
            note = melody[step % len(melody)]
            at = step * beat / 2
            add_note(note, at, beat * 0.44, 0.075, "saw", 8.5)
            if step % 8 in (3, 7):
                add_note(note * 2, at, beat * 0.2, 0.032, "square", 14.0)

        for step in range(16):
            add_note(accent[step % len(accent)], step * beat * 2 + beat * 0.5, beat * 0.3, 0.04, "square", 10.0)

        # Synthesized kick, snare and hi-hats.  The fixed RNG seed makes generated
        # BGM stable across runs while still sounding like sampled arcade percussion.
        rng = np.random.default_rng(1945)
        for sixteenth in range(64):
            at = sixteenth * beat / 2
            start = int(at * SAMPLE_RATE)
            if sixteenth % 8 in (0, 4, 6):
                dur = min(int(SAMPLE_RATE * 0.13), n - start)
                tt = np.arange(dur) / SAMPLE_RATE
                kick = np.sin(2 * np.pi * (120 - 75 * tt) * tt) * np.exp(-22 * tt) * 0.24
                wave[start:start + dur] += kick
            if sixteenth % 8 in (4,):
                dur = min(int(SAMPLE_RATE * 0.09), n - start)
                tt = np.arange(dur) / SAMPLE_RATE
                wave[start:start + dur] += rng.uniform(-1, 1, dur) * np.exp(-30 * tt) * 0.13
            dur = min(int(SAMPLE_RATE * 0.025), n - start)
            tt = np.arange(dur) / SAMPLE_RATE
            hat_amp = 0.045 if sixteenth % 2 == 0 else 0.03
            wave[start:start + dur] += rng.uniform(-1, 1, dur) * np.exp(-55 * tt) * hat_amp

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
        self.play("bomb_launch")
        key = {
            "energy": "bomb_energy",
            "gale": "bomb_gale",
            "stuka": "bomb_stuka",
            "phantom": "bomb_phantom",
            "nova": "bomb_nova",
        }.get(bomb_id, "bomb")
        self.play(key)

    def play_bomb_impact(self) -> None:
        self.play("bomb_impact")

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
