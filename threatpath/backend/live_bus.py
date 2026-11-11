import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

class LiveBusEngine:
    """
    Real-Time Virtual Automotive CAN Bus & Intrusion Detection Simulator.
    Simulates high-speed 500 kbps CAN-HS network with live traffic,
    anomaly injection, and AUTOSAR SecOC cryptographic defense.
    """
    def __init__(self):
        self.bus_interface = "vcan0"
        self.baud_rate = "500 kbps (CAN-HS)"
        self.is_attack_active = False
        self.is_secoc_active = False
        self.total_frames_sent = 12480
        self.anomalies_detected = 0
        self.bus_load_pct = 32.4
        self.frames_per_sec = 145
        self.packets_history: List[Dict[str, Any]] = []
        self.max_history = 50
        self.attack_start_time: Optional[float] = None
        self.attack_duration = 12.0 # seconds
        
        # Rolling graph telemetry points (last 15 seconds)
        self.rolling_telemetry: List[Dict[str, Any]] = [
            {"time": "0s", "packets": 138, "load": 31.2, "hazard": 1.2},
            {"time": "2s", "packets": 142, "load": 32.5, "hazard": 1.1},
            {"time": "4s", "packets": 145, "load": 33.1, "hazard": 1.4},
            {"time": "6s", "packets": 140, "load": 32.0, "hazard": 1.0},
            {"time": "8s", "packets": 148, "load": 33.4, "hazard": 1.3},
            {"time": "10s", "packets": 144, "load": 32.8, "hazard": 1.2},
        ]
        
        # Populate initial baseline packets
        for _ in range(12):
            self._generate_single_frame()

    def set_attack(self, active: bool, duration: float = 12.0):
        self.is_attack_active = active
        if active:
            self.attack_start_time = time.time()
            self.attack_duration = duration
        else:
            self.attack_start_time = None

    def toggle_secoc(self, active: Optional[bool] = None) -> bool:
        if active is None:
            self.is_secoc_active = not self.is_secoc_active
        else:
            self.is_secoc_active = active
        return self.is_secoc_active

    def _generate_single_frame(self) -> Dict[str, Any]:
        self.total_frames_sent += 1
        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Auto-timeout attack if duration elapsed
        if self.is_attack_active and self.attack_start_time:
            if time.time() - self.attack_start_time > self.attack_duration:
                self.is_attack_active = False
                self.attack_start_time = None

        # Determine frame type
        if self.is_attack_active and random.random() < 0.65:
            # Malicious Injection: CAN ID 0x020 Brake Override
            if not self.is_secoc_active:
                self.anomalies_detected += 1
                status = "EXPLOIT"
                secoc_tag = "NO_MAC"
                desc = "Brake solenoid forced to 120 bar! Physical deceleration triggered."
            else:
                status = "DEFENDED"
                secoc_tag = "MAC_MISMATCH_DROPPED"
                desc = "SecOC CMAC-AES128 failed. Unauthorized packet discarded by ESC HAL."

            frame = {
                "id": f"pkt_{self.total_frames_sent}",
                "timestamp": now_str,
                "can_id": "0x020",
                "ecu": "ESC_BRAKE",
                "dlc": 8,
                "data": "80 00 00 FF 00 00 00 00",
                "status": status,
                "secoc": secoc_tag,
                "desc": desc,
                "priority": "HIGH (0x020)"
            }
        else:
            # Legitimate ECU Heartbeats & Sensor Broadcasts
            normal_templates = [
                {
                    "can_id": "0x110",
                    "ecu": "ECM_POWERTRAIN",
                    "dlc": 8,
                    "data": f"09 {random.randint(80, 99):02X} B4 00 12 00 00 00",
                    "desc": f"Engine RPM: {random.randint(2300, 2550)} | Torque: 180 Nm",
                    "secoc": "AUTHENTICATED" if self.is_secoc_active else "LEGACY_CLEAR"
                },
                {
                    "can_id": "0x0A0",
                    "ecu": "ADAS_RADAR",
                    "dlc": 8,
                    "data": f"01 {random.randint(60, 90):02X} 26 00 00 00 00 00",
                    "desc": f"Forward Target Distance: {random.uniform(32.0, 48.0):.1f}m",
                    "secoc": "AUTHENTICATED" if self.is_secoc_active else "LEGACY_CLEAR"
                },
                {
                    "can_id": "0x220",
                    "ecu": "TCU_TRANSMISSION",
                    "dlc": 6,
                    "data": "04 55 00 00 00 00",
                    "desc": "Drive Mode: D4 | Clutch Pressure: Nominal",
                    "secoc": "AUTHENTICATED" if self.is_secoc_active else "LEGACY_CLEAR"
                },
                {
                    "can_id": "0x320",
                    "ecu": "BCM_BODY_GATEWAY",
                    "dlc": 4,
                    "data": "01 02 00 00",
                    "desc": "Perimeter Central Lock: SECURED | Hazard: OFF",
                    "secoc": "AUTHENTICATED" if self.is_secoc_active else "LEGACY_CLEAR"
                },
                {
                    "can_id": "0x020",
                    "ecu": "ESC_BRAKE",
                    "dlc": 8,
                    "data": "00 00 00 00 00 00 00 00",
                    "desc": "Hydraulic Baseline: 0 bar | Stability Status: OK",
                    "secoc": "AUTHENTICATED" if self.is_secoc_active else "LEGACY_CLEAR"
                }
            ]
            t = random.choice(normal_templates)
            frame = {
                "id": f"pkt_{self.total_frames_sent}",
                "timestamp": now_str,
                "can_id": t["can_id"],
                "ecu": t["ecu"],
                "dlc": t["dlc"],
                "data": t["data"],
                "status": "VALID",
                "secoc": t["secoc"],
                "desc": t["desc"],
                "priority": f"NORMAL ({t['can_id']})"
            }

        # Update metrics dynamically
        if self.is_attack_active:
            if not self.is_secoc_active:
                self.bus_load_pct = round(random.uniform(84.0, 93.5), 1)
                self.frames_per_sec = random.randint(480, 560)
            else:
                self.bus_load_pct = round(random.uniform(36.0, 42.0), 1)
                self.frames_per_sec = random.randint(160, 185)
        else:
            self.bus_load_pct = round(random.uniform(30.0, 34.5), 1)
            self.frames_per_sec = random.randint(135, 155)

        self.packets_history.insert(0, frame)
        if len(self.packets_history) > self.max_history:
            self.packets_history.pop()

        return frame

    def tick_telemetry(self):
        """Advances telemetry time window by 1 step."""
        now_time = datetime.now().strftime("%H:%M:%S")
        hazard = 9.9 if (self.is_attack_active and not self.is_secoc_active) else (2.4 if self.is_secoc_active and self.is_attack_active else 1.2)
        
        self.rolling_telemetry.append({
            "time": now_time,
            "packets": self.frames_per_sec,
            "load": self.bus_load_pct,
            "hazard": hazard
        })
        if len(self.rolling_telemetry) > 12:
            self.rolling_telemetry.pop(0)

    def get_snapshot(self) -> Dict[str, Any]:
        """Generates 3 new frames and returns immediate state snapshot."""
        for _ in range(3):
            self._generate_single_frame()
        self.tick_telemetry()

        return {
            "bus_interface": self.bus_interface,
            "baud_rate": self.baud_rate,
            "is_attack_active": self.is_attack_active,
            "is_secoc_active": self.is_secoc_active,
            "total_frames_sent": self.total_frames_sent,
            "anomalies_detected": self.anomalies_detected,
            "bus_load_pct": self.bus_load_pct,
            "frames_per_sec": self.frames_per_sec,
            "recent_packets": self.packets_history[:20],
            "rolling_telemetry": self.rolling_telemetry
        }

# Global Singleton Instance
live_bus = LiveBusEngine()
