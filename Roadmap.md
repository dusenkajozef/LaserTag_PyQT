# Laser Tag System Software Roadmap

This roadmap outlines the planned development phases and features for the laser tag system software.

## Phase 1: Core Functionality

*   **Goal:** Implement the basic structure, UI, and database connectivity.
*   **Tasks:**
    *    Set up the project environment (Python, PyQt, MVVM, SQLite).
    *   Create splash screen.
    *   Design and implement the Player Entry Screen UI.
    *   Connect to the local SQLite database.
    *   Implement database query and update functionality for player information.
    *   Implement the ability to add two players via the application and save to the database.
    *   Set up UDP sockets (transmit and receive).
    *   Transmit equipment codes after each player addition.
    *   Implement the option to select a different network address for UDP sockets.
    *   Implement hardware ID input for each player on the Player Entry Screen.
    *   Design and implement the basic Play Action Display UI (no dynamic events yet).
        *   Show the players in their respective team windows.
    *   Code the F5 key (or equivalent) to switch to the Play Action Display and start the game (initial setup, no timers yet).
    *   Code the F12 key (or equivalent) to clear all player entries on the Player Entry Screen.
    *   Code up the game start count-down timer.

## Phase 2: Game Logic and Scoring

*   **Goal:** Implement the core game logic, scoring rules, and dynamic updates to the Play Action Screen.
*   **Tasks:**
    *   Add random music track selection.
    *   Implement the 6-minute game play timer (activated after the 30-second game start timer).
    *   Implement base scoring logic:
        *   Add stylized "B" to any player hitting a base (persists for the rest of the game).

## Phase 3: Network Communication and Events

*   **Goal:**  Implement the network communication logic for tracking hits and base scores.
*   **Tasks:**
    *   Handle received UDP data (hit events, base scores).
    *   Update player scores based on hit events.
    *   Transmit equipment ID of player who was hit via UDP.
    *   Implement logic for transmitting own equipment ID when tagging a teammate.
    *   Implement game start (202) and game end (221 x3) transmission.

## Phase 4: Unit Testing

*   **Goal:**  Test the core functionality of the application.
*   **Tasks:**
    *   Test the Player Entry Screen UI.
    *   Test the Play Action Display UI.
    *   Test the database connectivity.
    *   Test the UDP sockets.
    *   Test the game logic.
    *   Test the network communication logic.