import os
import random
from pathlib import Path
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QObject, pyqtSignal

class AudioPlayer(QObject):
    """Handles background music and sound effects"""
    music_ended = pyqtSignal()
    
    def __init__(self, music_dir: str = None):
        if music_dir is None:
            music_dir = str(Path(__file__).parent.parent.parent / "assets" / "sounds")
        super().__init__()
        self.music_dir = music_dir
        self.current_track = None
        self.music_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.music_player.setAudioOutput(self.audio_output)
        self.music_player.playbackStateChanged.connect(self._on_playback_state_changed)
        self.tracks = self._discover_tracks()
    
    def _discover_tracks(self) -> list[str]:
        """Find all audio files in the sounds directory"""
        try:
            if not os.path.exists(self.music_dir):
                print(f"Music directory not found: {self.music_dir}")
                return []
                
            supported_extensions = ('.mp3', '.wav', '.ogg', '.m4a')
            tracks = [
                os.path.join(self.music_dir, f) 
                for f in os.listdir(self.music_dir) 
                if f.lower().endswith(supported_extensions)
            ]
            print(f"Found {len(tracks)} music tracks in {self.music_dir}")
            return tracks
        except Exception as e:
            print(f"Error discovering tracks: {e}")
            return []
    
    def play_random_track(self):
        """Play a random music track from the music directory"""
        if not self.tracks:
            print("No music tracks found in", self.music_dir)
            return
            
        # Don't play the same track twice in a row
        available_tracks = [t for t in self.tracks if t != self.current_track]
        if not available_tracks:
            available_tracks = self.tracks
            
        self.current_track = random.choice(available_tracks)
        self.music_player.setSource(QUrl.fromLocalFile(self.current_track))
        self.audio_output.setVolume(50)  # 50% volume
        self.music_player.play()
    
    def stop(self):
        """Stop the current playback"""
        self.music_player.stop()
    
    def set_volume(self, volume: int):
        """Set the volume (0-100)"""
        self.audio_output.setVolume(volume)
    
    def _on_playback_state_changed(self, state):
        """Handle when a track finishes playing"""
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.music_ended.emit()
    
    def play_sound_effect(self, sound_file: str):
        """Play a sound effect (blocking)"""
        if not os.path.exists(sound_file):
            print(f"Sound file not found: {sound_file}")
            return
            
        effect_player = QMediaPlayer()
        audio_output = QAudioOutput()
        effect_player.setAudioOutput(audio_output)
        effect_player.setSource(QUrl.fromLocalFile(sound_file))
        audio_output.setVolume(100)  # Full volume for sound effects
        effect_player.play()
        
        # Keep the effect player alive until playback finishes
        while effect_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            pass
