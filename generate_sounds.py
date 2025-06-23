import numpy as np
from scipy.io import wavfile
import os

def generate_sine_wave(freq, duration, sample_rate=44100, volume=0.5):
    """Generate a sine wave tone"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * freq * t) * volume * 32767
    return tone.astype(np.int16)

def generate_hit_sound():
    """Generate a hit sound effect"""
    # Short beep at 800Hz
    hit = generate_sine_wave(800, 0.1, volume=0.3)
    wavfile.write('assets/sounds/hit.wav', 44100, hit)

def generate_base_hit_sound():
    """Generate a base hit sound effect"""
    # Lower pitched beep at 500Hz
    base_hit = generate_sine_wave(500, 0.2, volume=0.5)
    wavfile.write('assets/sounds/base_hit.wav', 44100, base_hit)

def generate_warning_sound():
    """Generate a warning sound effect"""
    # Two quick beeps
    beep1 = generate_sine_wave(1000, 0.1, volume=0.4)
    beep2 = generate_sine_wave(1200, 0.1, volume=0.4)
    silence = np.zeros(2205, dtype=np.int16)  # 50ms of silence
    warning = np.concatenate([beep1, silence, beep2])
    wavfile.write('assets/sounds/warning.wav', 44100, warning)

def generate_tick_sound():
    """Generate a tick sound effect for the countdown"""
    tick = generate_sine_wave(1500, 0.05, volume=0.3)
    wavfile.write('assets/sounds/tick.wav', 44100, tick)

def generate_game_over_sound():
    """Generate a game over sound effect"""
    # Descending tone
    t = np.linspace(0, 1.5, int(44100 * 1.5), False)
    freq = np.linspace(1000, 200, len(t))
    tone = np.sin(2 * np.pi * freq * t) * 0.5 * 32767
    wavfile.write('assets/sounds/game_over.wav', 44100, tone.astype(np.int16))

if __name__ == "__main__":
    # Create sounds directory if it doesn't exist
    os.makedirs('assets/sounds', exist_ok=True)
    
    # Generate all sound effects
    print("Generating sound effects...")
    generate_hit_sound()
    generate_base_hit_sound()
    generate_warning_sound()
    generate_tick_sound()
    generate_game_over_sound()
    print("Sound effects generated in assets/sounds/")
