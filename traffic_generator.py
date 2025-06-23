import socket
import time
import random
import threading
import argparse
from dataclasses import dataclass
from typing import List, Tuple
import sys

@dataclass
class Player:
    id: int
    name: str
    team: str
    equipment_id: int

class TrafficGenerator:
    def __init__(self, host: str = '127.0.0.1', port: int = 7501):
        self.host = host
        self.port = port
        self.running = False
        self.players = [
            Player(1, "Red-1", "red", 1),
            Player(2, "Red-2", "red", 2),
            Player(3, "Green-1", "green", 3),
            Player(4, "Green-2", "green", 4)
        ]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
    
    def send_hit(self, shooter_id: int, target_id: int):
        """Send a hit message"""
        message = f"{shooter_id}:{target_id}"
        try:
            self.sock.sendto(message.encode('utf-8'), (self.host, self.port))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error sending hit: {e}")
    
    def send_base_hit(self, team: str):
        """Send a base hit message"""
        code = "53" if team.lower() == 'red' else "43"
        try:
            self.sock.sendto(code.encode('utf-8'), (self.host, self.port))
            print(f"Sent base hit: {code} ({'Red' if team.lower() == 'red' else 'Green'})")
        except Exception as e:
            print(f"Error sending base hit: {e}")
    
    def send_game_control(self, command: str):
        """Send game control commands"""
        commands = {
            'start': '202',
            'end': '221'
        }
        if command in commands:
            try:
                self.sock.sendto(commands[command].encode('utf-8'), (self.host, self.port))
                print(f"Sent command: {command.upper()} ({commands[command]})")
                # For game end, send it 3 times as per protocol
                if command == 'end':
                    for _ in range(2):
                        self.sock.sendto(commands[command].encode('utf-8'), (self.host, self.port))
            except Exception as e:
                print(f"Error sending command: {e}")
    
    def random_hit(self):
        """Generate a random hit between players"""
        if len(self.players) < 2:
            return
        
        shooter, target = random.sample(self.players, 2)
        self.send_hit(shooter.equipment_id, target.equipment_id)
    
    def random_base_hit(self):
        """Generate a random base hit"""
        team = random.choice(['red', 'green'])
        self.send_base_hit(team)
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\nLaser Tag Traffic Generator")
        print("==========================")
        print("1. Send random player hit")
        print("2. Send random base hit")
        print("3. Send game start")
        print("4. Send game end")
        print("5. Send specific hit")
        print("6. Send specific base hit")
        print("0. Exit\n")
        
        self.running = True
        while self.running:
            try:
                choice = input("Select an option (or 'h' for help): ").strip().lower()
                
                if choice == '1':
                    self.random_hit()
                elif choice == '2':
                    self.random_base_hit()
                elif choice == '3':
                    self.send_game_control('start')
                elif choice == '4':
                    self.send_game_control('end')
                elif choice == '5':
                    self.send_specific_hit()
                elif choice == '6':
                    self.send_specific_base_hit()
                elif choice == '0' or choice == 'q':
                    self.running = False
                elif choice == 'h':
                    print("\nAvailable commands:")
                    print("1 - Send random player hit")
                    print("2 - Send random base hit")
                    print("3 - Send game start")
                    print("4 - Send game end")
                    print("5 - Send specific hit")
                    print("6 - Send specific base hit")
                    print("0 or q - Exit\n")
                else:
                    print("Invalid option. Try again or 'h' for help.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
    
    def send_specific_hit(self):
        """Send a specific hit between players"""
        print("\nAvailable players:")
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player.name} (ID: {player.equipment_id}, Team: {player.team.capitalize()})")
        
        try:
            shooter_idx = int(input("Select shooter (number): ")) - 1
            target_idx = int(input("Select target (number): ")) - 1
            
            if 0 <= shooter_idx < len(self.players) and 0 <= target_idx < len(self.players):
                self.send_hit(self.players[shooter_idx].equipment_id, self.players[target_idx].equipment_id)
            else:
                print("Invalid player selection")
        except ValueError:
            print("Please enter valid numbers")
    
    def send_specific_base_hit(self):
        """Send a specific base hit"""
        print("\nSelect base to hit:")
        print("1. Red base")
        print("2. Green base")
        
        try:
            choice = input("Select (1-2): ").strip()
            if choice == '1':
                self.send_base_hit('red')
            elif choice == '2':
                self.send_base_hit('green')
            else:
                print("Invalid selection")
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Laser Tag Traffic Generator')
    parser.add_argument('--host', default='127.0.0.1', help='Target host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=7501, help='Target port (default: 7501)')
    
    args = parser.parse_args()
    
    try:
        generator = TrafficGenerator(host=args.host, port=args.port)
        print(f"Traffic Generator started. Sending to {args.host}:{args.port}")
        generator.interactive_mode()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
