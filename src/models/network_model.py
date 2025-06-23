import socket
import threading
import json
from typing import Optional, Callable, Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal

class NetworkModel(QObject):
    """Handles network communication for the laser tag system"""
    
    # Signals
    data_received = pyqtSignal(dict)  # Emitted when data is received
    error_occurred = pyqtSignal(str)  # Emitted when an error occurs
    
    def __init__(self, host: str = '127.0.0.1', tx_port: int = 7500, rx_port: int = 7501):
        super().__init__()
        self.host = host
        self.tx_port = tx_port
        self.rx_port = rx_port
        self.running = False
        self.receive_thread: Optional[threading.Thread] = None
        self.sock: Optional[socket.socket] = None
        
        # Callback for processing received data
        self.data_callback: Optional[Callable[[dict], None]] = None
    
    def start(self):
        """Start the network service"""
        if self.running:
            return
            
        try:
            # Create UDP socket for receiving
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.rx_port))
            
            # Start receive thread
            self.running = True
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            self.error_occurred.emit(f"Network service started on port {self.rx_port}")
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to start network service: {e}")
            self.stop()
    
    def stop(self):
        """Stop the network service"""
        self.running = False
        if self.sock:
            try:
                # Send a dummy packet to unblock the receive thread
                temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                temp_sock.sendto(b'', ('127.0.0.1', self.rx_port))
                temp_sock.close()
                
                self.sock.close()
            except:
                pass
            finally:
                self.sock = None
    
    def _receive_loop(self):
        """Main receive loop running in a separate thread"""
        while self.running and self.sock:
            try:
                data, addr = self.sock.recvfrom(1024)  # Buffer size is 1024 bytes
                if not data:
                    continue
                    
                # Process the received data
                self._process_received_data(data.decode('utf-8').strip())
                
            except (socket.timeout, ConnectionResetError):
                continue
            except Exception as e:
                if self.running:  # Only emit error if we're supposed to be running
                    self.error_occurred.emit(f"Receive error: {e}")
                break
    
    def _process_received_data(self, data: str):
        """Process received data and emit appropriate signals"""
        try:
            # Expected format: "shooter_id:target_id" or "202" (game start) or "221" (game end)
            if ':' in data:
                # Player hit another player
                parts = data.split(':')
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    self.data_received.emit({
                        'type': 'player_hit',
                        'shooter_id': int(parts[0]),
                        'target_id': int(parts[1])
                    })
            elif data == '202':
                # Game start
                self.data_received.emit({'type': 'game_start'})
            elif data == '221':
                # Game end
                self.data_received.emit({'type': 'game_end'})
            elif data == '53':
                # Red base hit
                self.data_received.emit({'type': 'base_hit', 'base_team': 'red'})
            elif data == '43':
                # Green base hit
                self.data_received.emit({'type': 'base_hit', 'base_team': 'green'})
                
        except Exception as e:
            self.error_occurred.emit(f"Error processing data: {e}")
    
    def send_data(self, data: str):
        """Send data to the broadcast address"""
        if not self.running or not self.sock:
            self.error_occurred.emit("Network service not running")
            return False
            
        try:
            self.sock.sendto(data.encode('utf-8'), (self.host, self.tx_port))
            return True
        except Exception as e:
            self.error_occurred.emit(f"Send error: {e}")
            return False
    
    def broadcast_hit(self, shooter_id: int, target_id: int):
        """Broadcast a hit event"""
        return self.send_data(f"{shooter_id}:{target_id}")
    
    def broadcast_game_start(self):
        """Broadcast game start signal"""
        return self.send_data("202")
    
    def broadcast_game_end(self):
        """Broadcast game end signal (sends 3 times)"""
        for _ in range(3):
            if not self.send_data("221"):
                return False
        return True
    
    def broadcast_base_hit(self, base_team: str):
        """Broadcast a base hit"""
        code = "53" if base_team.lower() == 'red' else "43"
        return self.send_data(code)
