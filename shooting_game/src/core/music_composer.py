"""Original high-energy arcade music renderer.

The score is intentionally composed from general arcade-rock conventions rather
than copying any identifiable composer or existing song.  It renders a portable
WAV cache so the game uses a real music asset after the first launch.
"""

from __future__ import annotations

from pathlib import Path
import wave

import numpy as np


SAMPLE_RATE = 44_100


def _osc(freq: float, length: int, kind: str) -> np.ndarray:
    t = np.arange(length, dtype=np.float64) / SAMPLE_RATE
    phase = (freq * t) % 1.0
    if kind == "saw":
        return 2.0 * phase - 1.0
    if kind == "square":
        return np.sign(np.sin(np.pi * 2 * freq * t))
    return np.sin(np.pi * 2 * freq * t)


def render_combat_theme() -> np.ndarray:
    """Render a 16-bar, 154 BPM arcade-rock combat cue in stereo PCM."""
    bpm, bars, beats_per_bar = 154, 16, 4
    beat = 60.0 / bpm
    total = int(SAMPLE_RATE * beat * beats_per_bar * bars)
    left, right = np.zeros(total), np.zeros(total)
    rng = np.random.default_rng(60716)

    def note(freq: float, at_beats: float, length_beats: float, amp: float, voice: str, pan: float = 0.0) -> None:
        start = int(at_beats * beat * SAMPLE_RATE)
        length = min(int(length_beats * beat * SAMPLE_RATE), total - start)
        if length <= 0:
            return
        t = np.arange(length) / SAMPLE_RATE
        env = np.minimum(1.0, t * 80) * np.exp(-t / max(0.035, length_beats * beat * 0.85))
        tone = _osc(freq, length, voice) * env * amp
        left[start:start + length] += tone * (1.0 - pan * 0.35)
        right[start:start + length] += tone * (1.0 + pan * 0.35)

    def noise(at_beats: float, seconds: float, amp: float, pan: float = 0.0) -> None:
        start = int(at_beats * beat * SAMPLE_RATE)
        length = min(int(seconds * SAMPLE_RATE), total - start)
        if length <= 0:
            return
        t = np.arange(length) / SAMPLE_RATE
        env = np.exp(-t * 35)
        tone = rng.uniform(-1, 1, length) * env * amp
        left[start:start + length] += tone * (1.0 - pan * 0.25)
        right[start:start + length] += tone * (1.0 + pan * 0.25)

    # A minor-key progression: A minor / F / G / E.  Repeated motifs with a
    # mid-track lift and turnaround make it feel composed rather than looped.
    roots = [110.0, 87.31, 98.0, 82.41]
    riff_a = [440, 523.25, 659.25, 880, 659.25, 523.25, 493.88, 440]
    riff_b = [659.25, 783.99, 880, 1046.5, 987.77, 880, 783.99, 659.25]
    for bar in range(bars):
        base = bar * 4
        root = roots[bar % 4]
        # Driving bass + distorted octave guitar/synth stabs.
        for eighth in range(8):
            note(root, base + eighth * 0.5, 0.40, 0.145, "square", -0.08)
            if eighth in (1, 3, 5, 7):
                note(root * 2, base + eighth * 0.5, 0.24, 0.055, "saw", 0.12)
        for stab in (0.0, 1.5, 2.5):
            note(root * 2, base + stab, 0.42, 0.052, "saw", -0.42)
            note(root * 2.996, base + stab + 0.012, 0.42, 0.042, "saw", 0.42)

        # Four-on-the-floor kick, backbeat snare and 16th hats.
        for sixteenth in range(16):
            at = base + sixteenth * 0.25
            noise(at, 0.018, 0.022 if sixteenth % 2 else 0.035, -0.18 if sixteenth % 2 else 0.18)
        for b in (0, 1, 2, 3):
            at = base + b
            if b in (0, 2) or (bar >= 8 and b == 3):
                note(72, at, 0.28, 0.19, "sine")
                note(44, at, 0.22, 0.10, "sine")
            else:
                noise(at, 0.11, 0.12)

        # Lead does not enter for the two-bar intro; it then alternates between
        # a hook and a lifted variation before a final octave climax.
        if bar >= 2:
            riff = riff_b if 8 <= bar < 12 else riff_a
            octave = 2 if bar >= 12 else 1
            for i, pitch in enumerate(riff):
                accent = 1.2 if i in (0, 3, 6) else 1.0
                note(pitch * octave, base + i * 0.5, 0.36, 0.070 * accent, "saw", 0.18)
                note(pitch * octave * 2, base + i * 0.5, 0.16, 0.020, "square", -0.1)

    # Gentle saturation and peak protection for cabinet-like presence.
    stereo = np.column_stack((np.tanh(left * 1.28), np.tanh(right * 1.28)))
    return (stereo * 32767 * 0.72).astype(np.int16)


def ensure_combat_wav() -> Path:
    """Create the distributable BGM asset once and return its path."""
    target = Path(__file__).resolve().parents[2] / "assets" / "audio" / "seoyul_arcade_assault.wav"
    if target.exists() and target.stat().st_size > 100_000:
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    pcm = render_combat_theme()
    with wave.open(str(target), "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(SAMPLE_RATE)
        out.writeframes(pcm.tobytes())
    return target
