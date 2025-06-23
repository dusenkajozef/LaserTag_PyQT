# Laser Tag System Software Requirements

## 1. Introduction

This document outlines the requirements for a laser tag system software application. The application will manage player registration, game play, scoring, and network communication with laser tag equipment.

## 2. Goals

*   Provide a user-friendly interface for managing laser tag games.
*   Accurately track player scores and game events.
*   Communicate reliably with laser tag equipment.
*   Create an engaging and enjoyable laser tag experience.

## 3. Functional Requirements

### 3.1. Splash Screen

*   Display a splash screen for 3 seconds upon application startup.

### 3.2. Player Entry Screen

*   Display a player entry screen (refer to screen captures for format).
*   Prompt for player ID number.
*   Query a local PostgreSQL database for player code name based on ID.
*   If the player ID is not found in the database:
    *   Allow the operator to enter a new code name.
    *   Add the new player ID and code name to the database.
*   Prompt for the equipment ID that the player is using (integer).
*   Broadcast the equipment ID through UDP port 7500.
*   Provide tab key navigation between fields.
*   Allow a maximum of 15 players per team (Red and Green).
*   Provide a button (or F12 key equivalent) to clear all player entries.
*   Provide a button (or F5 key equivalent) to move to the Play Action Screen.

### 3.3. Play Action Screen

*   Display a countdown timer for 6-minute games, including a 30-second warning.
*   Display a play-by-play action log in a scrolling window.
*   Display cumulative team scores (Red and Green), constantly updating.
*   Display individual player scores, constantly updating and sorted from highest to lowest within each team.
*   Highlight the high team score (e.g., flashing).
*   Play a random MP3 music file during gameplay, synchronized with the countdown timer.
*   Provide a button to return to the Player Entry Screen after the game ends.

### 3.4. Network Communication

*   Use UDP sockets for communication.
*   Use localhost (127.0.0.1) as the network address by default, with the option to change it.
*   Use port 7500 for broadcasting data.
*   Use port 7501 for receiving data.
*   **Broadcast Format:** Single integer (equipment ID of player who got hit).
*   **Receive Format:** Integer:Integer (equipment ID of player transmitting:equipment ID of player hit).

### 3.5. Scoring and Game Logic

*   Award 10 points per opposing team player tag.
*   Deduct 10 points for same team player tag.
*   When the game starts, transmit code 202.
*   When the game ends, transmit code 221 three times.
*   When data is received:
    *   Transmit the equipment ID of the player who was hit.
    *   If a player tags another player on their own team, transmit their own equipment ID.
*   **Base Scoring:**
    *   If code 53 is received (Red base scored):
        *   If the player is on the Green team, award 100 points.
        *   Add a stylized letter "B" to the left of their code name, persisting for the rest of the game.
    *   If code 43 is received (Green base scored):
        *   If the player is on the Red team, award 100 points.
        *   Add a stylized letter "B" to the left of their code name, persisting for the rest of the game.

### 3.6. Database

*   Use SQLite for local data storage.
*   Store player IDs and names
*   The database will be stored in a single file (`data/laser_tag.db`).
*   Database interaction should be efficient but performance is not critical for the prototype.

## 4. Non-Functional Requirements

*   **Programming Language:** Python
*   **GUI Framework:** PyQt
*   **Structure:** MVVM
*   **Operating System:** Will be developed and tested on Windows. Command line interaction via PowerShell
*   **Security:** No specific security requirements for the prototype.
*   **Performance:** While not critical for the prototype, reasonable performance is expected.
*   **Usability:** The application should be intuitive and easy to use for the laser tag operator.