# Sound System and Base Scoring

## Overview
This document describes the sound system and base scoring features implemented in the Laser Tag game.

## Sound Effects

The game includes the following sound effects:

1. **Hit Sound**
   - Played when a player is hit by another player
   - File: `assets/sounds/hit.wav`

2. **Base Hit Sound**
   - Played when a team's base is hit
   - File: `assets/sounds/base_hit.wav`

3. **Warning Sound**
   - Played when there are 30 seconds remaining
   - File: `assets/sounds/warning.wav`

4. **Tick Sound**
   - Played during the last 5 seconds of the game
   - File: `assets/sounds/tick.wav`

5. **Game Over Sound**
   - Played when the game ends
   - File: `assets/sounds/game_over.wav`

## Background Music

The game plays random background music tracks from the `assets/music/` directory. Supported formats include:
- .mp3
- .wav
- .ogg
- .m4a

## Base Scoring System

### Base Hit Mechanics
- Each team has a base that can be hit once per game
- Hitting the base awards 5 points to all players on the team
- A player who has hit the base is marked with a "(B)" next to their name
- Base hits are indicated by special codes:
  - Red base hit: `53`
  - Green base hit: `43`

### Visual Indicators
- Players who have hit the base are marked with "(B)" next to their score
- The score display updates immediately when a base is hit
- Base hits are logged in the game events

## Volume Control

Use the volume slider in the game interface to adjust the music volume. The volume can be adjusted from 0% to 100%.

## Testing with Traffic Generator

You can test the base scoring using the traffic generator:

1. Start the game with at least one player on each team
2. In the traffic generator, select option 6 (Send specific base hit)
3. Choose which base to hit (Red or Green)
4. Verify that all players on that team receive 5 points
5. Verify that the "(B)" indicator appears next to their names

## Adding Custom Sounds

To add custom sounds:

1. Place sound effect files in the `assets/sounds/` directory
2. Update the `sound_effects` dictionary in `play_action_screen.py` to include your new sounds
3. Place music tracks in the `assets/music/` directory - they will be played randomly

## Troubleshooting

- If sounds don't play, check that the files exist in the correct locations
- Make sure the volume is not muted or set to 0
- Check the console for any error messages related to audio playback
- Ensure all audio files are in a supported format
