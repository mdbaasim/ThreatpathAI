import time
from datetime import datetime
from typing import List, Dict, Any
from models import TestExecutionResult, VirtualPacket

class SimulationEngine:
    """Isolated virtual CAN and diagnostic ECU test simulator."""

    def execute_test(self, threat_id: str, apply_mitigation: bool = False) -> TestExecutionResult:
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        if threat_id == "THREAT_006":
            return self._simulate_brake_can_spoof(apply_mitigation, timestamp_str)
        elif threat_id == "THREAT_001":
            return self._simulate_ota_doip_exploit(apply_mitigation, timestamp_str)
        elif threat_id == "THREAT_003":
            return self._simulate_uds_security_access(apply_mitigation, timestamp_str)
        elif threat_id == "THREAT_004":
            return self._simulate_gateway_pivot(apply_mitigation, timestamp_str)
        else:
            return self._simulate_generic_threat(threat_id, apply_mitigation, timestamp_str)

    def _simulate_brake_can_spoof(self, apply_mitigation: bool, timestamp: str) -> TestExecutionResult:
        test_case_id = "TC-CAN-SPOOF-0x020"
        test_title = "Dynamic CAN Frame Injection: Emergency Brake Override (ID: 0x020)"
        
        if not apply_mitigation:
            trace = [
                f"[{timestamp}] [INFO] Initializing isolated Virtual CAN Bus (vcan0) at 500 kbps.",
                f"[{timestamp}] [INFO] Target Node: ESC_BRAKE (ASIL-D Hydraulic Modulation Controller).",
                f"[{timestamp}] [EXPLOIT] Crafting high-priority CAN frame: ID=0x020, DLC=8, Payload=[80 00 00 FF 00 00 00 00] (Force 100% Brake Pressure).",
                f"[{timestamp}] [BUS] Transmitting forged frame onto Chassis Safety CAN...",
                f"[{timestamp}] [RX] ESC_BRAKE received CAN ID 0x020.",
                f"[{timestamp}] [VULN] ESC_BRAKE has NO SecOC profile enabled. Frame processed without cryptographic verification.",
                f"[{timestamp}] [CRITICAL] Brake Booster Solenoid Actuated: 120 bar hydraulic pressure applied!",
                f"[{timestamp}] [VERDICT] EXPLOIT CONFIRMED. Unauthenticated CAN injection allows remote physical actuation."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x020", data_bytes="80 00 00 FF 00 00 00 00", direction="TX", description="Forged Emergency Deceleration Command", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=12, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x120", data_bytes="01 78 4B 00 00 00 00 00", direction="RX", description="ESC Status: HYDRAULIC_PRESSURE_ACTIVE (120 bar)", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=25, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x020", data_bytes="80 00 00 FF 00 00 00 00", direction="TX", description="Replay Deceleration Sustained Command", flag="ATTACK")
            ]
            return TestExecutionResult(
                threat_id="THREAT_006",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="CONFIRMED_EXPLOIT",
                verdict="VULNERABILITY CONFIRMED: Target ECU accepted and executed forged CAN frame.",
                mitigation_active=False,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Implement AUTOSAR SecOC (Specification of Secure Onboard Communication) with CMAC-AES128 and Monotonic Freshness Counter (FVM)."
            )
        else:
            trace = [
                f"[{timestamp}] [INFO] Initializing isolated Virtual CAN Bus (vcan0) with AUTOSAR SecOC active.",
                f"[{timestamp}] [INFO] Security Profile: AES-128-CMAC with 4-byte truncated MAC & 8-byte Freshness Value.",
                f"[{timestamp}] [EXPLOIT] Injecting forged unauthenticated CAN frame: ID=0x020, DLC=8.",
                f"[{timestamp}] [BUS] Transmitting raw frame onto Chassis Safety CAN...",
                f"[{timestamp}] [RX] ESC_BRAKE received CAN ID 0x020.",
                f"[{timestamp}] [DEFENSE] SecOC Verification Failed: Missing Freshness Counter & Valid CMAC tag.",
                f"[{timestamp}] [SECURE] Frame discarded by ECU hardware layer. Hydraulic pressure remained at 0 bar.",
                f"[{timestamp}] [AUDIT] Security Event logged in AUTOSAR IdsM (Intrusion Detection Security Module).",
                f"[{timestamp}] [VERDICT] THREAT MITIGATED. Spoofed frame successfully neutralized by cryptographic verification."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x020", data_bytes="80 00 00 FF 00 00 00 00", direction="TX", description="Forged Emergency Deceleration Command (No MAC)", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=5, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x020", data_bytes="-- DROPPED BY SECOC --", direction="RX", description="SecOC CMAC Mismatch -> Discarded", flag="BLOCKED"),
                VirtualPacket(timestamp_offset_ms=10, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x720", data_bytes="FF 06 35 01 00 00 00 00", direction="RX", description="Security Event: SEC_ERR_SECOC_VERIF_FAIL", flag="DEFENDED")
            ]
            return TestExecutionResult(
                threat_id="THREAT_006",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="VERIFIED_MITIGATED",
                verdict="DEFENSE CONFIRMED: AUTOSAR SecOC successfully dropped spoofed packet with zero impact on braking.",
                mitigation_active=True,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="SecOC configuration verified. Ensure symmetric keys are provisioned in Hardware Security Module (HSM/SHE)."
            )

    def _simulate_ota_doip_exploit(self, apply_mitigation: bool, timestamp: str) -> TestExecutionResult:
        test_case_id = "TC-DOIP-OTA-0x34"
        test_title = "Remote Cellular Ingress: Unauthenticated UDS RequestDownload (0x34)"
        if not apply_mitigation:
            trace = [
                f"[{timestamp}] [INFO] Establishing simulated DoIP (Diagnostics over IP) socket on UDP port 13400.",
                f"[{timestamp}] [EXPLOIT] Transmitting UDS Service 0x34 (RequestDownload) to Telematics (TCU).",
                f"[{timestamp}] [VULN] No mTLS client certificate requested by server socket.",
                f"[{timestamp}] [RX] TCU responded with Service 0x74 (Positive Download Acknowledgement).",
                f"[{timestamp}] [CRITICAL] Arbitrary firmware memory blocks allowed for transfer.",
                f"[{timestamp}] [VERDICT] EXPLOIT CONFIRMED. Remote unauthenticated firmware flashing possible."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="ETH_DOIP", arbitration_id="UDP:13400", data_bytes="02 34 00 44 00 00 10 00", direction="TX", description="UDS RequestDownload (Service 0x34)", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=18, bus="ETH_DOIP", arbitration_id="UDP:13400", data_bytes="04 74 20 00 00 04 00 00", direction="RX", description="Positive Response (Service 0x74 - MaxBlockLength 1024)", flag="ATTACK")
            ]
            return TestExecutionResult(
                threat_id="THREAT_001",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="CONFIRMED_EXPLOIT",
                verdict="VULNERABILITY CONFIRMED: OTA socket accepts arbitrary firmware transfer.",
                mitigation_active=False,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Enforce mutual TLS (mTLS) with IEEE 1609.2 / X.509 device certificates and hardware signature check."
            )
        else:
            trace = [
                f"[{timestamp}] [INFO] Testing DoIP socket with hardware mTLS & Secure Boot enabled.",
                f"[{timestamp}] [EXPLOIT] Transmitting unauthenticated UDS Service 0x34 frame.",
                f"[{timestamp}] [DEFENSE] TLS Handshake rejected: Client certificate not present.",
                f"[{timestamp}] [RX] TCU responded: 0x7F 34 33 (Security Access Denied).",
                f"[{timestamp}] [VERDICT] THREAT MITIGATED. Remote unauthorized download blocked."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="ETH_DOIP", arbitration_id="UDP:13400", data_bytes="02 34 00 44 00 00 10 00", direction="TX", description="Unauthenticated Download Attempt", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=6, bus="ETH_DOIP", arbitration_id="UDP:13400", data_bytes="03 7F 34 33 00 00 00 00", direction="RX", description="Negative Response: SecurityAccessDenied", flag="DEFENDED")
            ]
            return TestExecutionResult(
                threat_id="THREAT_001",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="VERIFIED_MITIGATED",
                verdict="DEFENSE CONFIRMED: Unauthenticated flash rejected by target ECU.",
                mitigation_active=True,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Ensure TPM / HSM root of trust remains locked during runtime."
            )

    def _simulate_uds_security_access(self, apply_mitigation: bool, timestamp: str) -> TestExecutionResult:
        test_case_id = "TC-UDS-0x27-SEEDKEY"
        test_title = "Diagnostic SecurityAccess (0x27) Seed/Key Bypass Test"
        if not apply_mitigation:
            trace = [
                f"[{timestamp}] [INFO] Connecting to Diagnostic CAN at 500 kbps.",
                f"[{timestamp}] [TX] UDS Request Seed: 0x27 0x01.",
                f"[{timestamp}] [RX] Target returned Seed: [AA BB CC DD].",
                f"[{timestamp}] [EXPLOIT] Computing Key using known static XOR mask [55 55 55 55] -> Key: [FF EE 99 88].",
                f"[{timestamp}] [TX] UDS Send Key: 0x27 0x02 [FF EE 99 88].",
                f"[{timestamp}] [RX] Target responded: 0x67 0x02 (Security Access UNLOCKED!).",
                f"[{timestamp}] [VERDICT] EXPLOIT CONFIRMED: Diagnostic privileges unlocked using trivial static algorithm."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="CAN_DIAG", arbitration_id="0x7DF", data_bytes="02 27 01 00 00 00 00 00", direction="TX", description="UDS Service 0x27 01 (Request Seed)", flag="NORMAL"),
                VirtualPacket(timestamp_offset_ms=10, bus="CAN_DIAG", arbitration_id="0x7E8", data_bytes="06 67 01 AA BB CC DD 00", direction="RX", description="Seed Provided: [AA BB CC DD]", flag="NORMAL"),
                VirtualPacket(timestamp_offset_ms=20, bus="CAN_DIAG", arbitration_id="0x7DF", data_bytes="06 27 02 FF EE 99 88 00", direction="TX", description="Calculated Key Sent: [FF EE 99 88]", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=28, bus="CAN_DIAG", arbitration_id="0x7E8", data_bytes="02 67 02 00 00 00 00 00", direction="RX", description="Security Access UNLOCKED (Positive Response)", flag="ATTACK")
            ]
            return TestExecutionResult(
                threat_id="THREAT_003",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="CONFIRMED_EXPLOIT",
                verdict="VULNERABILITY CONFIRMED: Seed/Key security cracked in 28ms.",
                mitigation_active=False,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Migrate to ISO 14229-1:2020 Service 0x29 (Asymmetric Cryptographic Authentication) or 256-bit AES challenge-response."
            )
        else:
            trace = [
                f"[{timestamp}] [INFO] Target running ISO 14229-1:2020 Service 0x29 with AES-256 HSM Seed/Key.",
                f"[{timestamp}] [TX] Sending legacy XOR key.",
                f"[{timestamp}] [RX] Target responded: 0x7F 27 35 (Invalid Key / Access Denied).",
                f"[{timestamp}] [VERDICT] THREAT MITIGATED. Unauthorized diagnostic access blocked."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="CAN_DIAG", arbitration_id="0x7DF", data_bytes="06 27 02 FF EE 99 88 00", direction="TX", description="Legacy XOR Key Attempt", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=12, bus="CAN_DIAG", arbitration_id="0x7E8", data_bytes="03 7F 27 35 00 00 00 00", direction="RX", description="Response: 0x7F 27 35 (Invalid Key)", flag="DEFENDED")
            ]
            return TestExecutionResult(
                threat_id="THREAT_003",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="VERIFIED_MITIGATED",
                verdict="DEFENSE CONFIRMED: Invalid diagnostic key rejected.",
                mitigation_active=True,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Monitor diagnostic attempt thresholds and enforce delay timer upon repeated failures."
            )

    def _simulate_gateway_pivot(self, apply_mitigation: bool, timestamp: str) -> TestExecutionResult:
        test_case_id = "TC-GW-CROSS-ROUTING"
        test_title = "Gateway Lateral Pivot: Cross-Bus Forwarding to Safety Domain"
        if not apply_mitigation:
            trace = [
                f"[{timestamp}] [INFO] Injecting diagnostic frame into Infotainment Ethernet Bus.",
                f"[{timestamp}] [TX] Frame targeted for Chassis Safety CAN (ID 0x020).",
                f"[{timestamp}] [VULN] Central Gateway GW_01 routing table has no domain isolation filter.",
                f"[{timestamp}] [RX] Frame re-transmitted directly onto Chassis CAN without attenuation.",
                f"[{timestamp}] [VERDICT] EXPLOIT CONFIRMED: Gateway allows lateral hop from untrusted domain to safety domain."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="ETH_INFOTAINMENT", arbitration_id="IP_ETH", data_bytes="02 00 20 80 00 00 FF 00", direction="TX", description="Infotainment Cross-Domain Frame", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=15, bus="CAN_CHASSIS_SAFETY", arbitration_id="0x020", data_bytes="80 00 00 FF 00 00 00 00", direction="RX", description="Gateway Forwarded Frame to Safety Bus", flag="ATTACK")
            ]
            return TestExecutionResult(
                threat_id="THREAT_004",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="CONFIRMED_EXPLOIT",
                verdict="VULNERABILITY CONFIRMED: Gateway unrestrictedly routes frames across trust boundaries.",
                mitigation_active=False,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Deploy AUTOSAR Central Gateway Hardware Firewall with ingress/egress message filtering."
            )
        else:
            trace = [
                f"[{timestamp}] [INFO] Testing with Central Gateway Domain Firewall active.",
                f"[{timestamp}] [TX] Frame targeted for Chassis Safety CAN injected on Infotainment bus.",
                f"[{timestamp}] [DEFENSE] Firewall Rule GW_RULE_04 matched: Cross-domain routing to Safety CAN prohibited.",
                f"[{timestamp}] [SECURE] Frame dropped silently at Gateway boundary. Chassis CAN isolated.",
                f"[{timestamp}] [VERDICT] THREAT MITIGATED. Lateral pivot blocked."
            ]
            packets = [
                VirtualPacket(timestamp_offset_ms=0, bus="ETH_INFOTAINMENT", arbitration_id="IP_ETH", data_bytes="02 00 20 80 00 00 FF 00", direction="TX", description="Cross-Domain Routing Attempt", flag="ATTACK"),
                VirtualPacket(timestamp_offset_ms=5, bus="GW_INTERNAL", arbitration_id="GW_FIREWALL", data_bytes="-- DROPPED BY RULE GW_04 --", direction="RX", description="Firewall Filter: REJECT", flag="DEFENDED")
            ]
            return TestExecutionResult(
                threat_id="THREAT_004",
                test_case_id=test_case_id,
                test_title=test_title,
                timestamp=timestamp,
                status="VERIFIED_MITIGATED",
                verdict="DEFENSE CONFIRMED: Cross-domain frame filtered by Gateway firewall.",
                mitigation_active=True,
                execution_trace=trace,
                bus_traffic=packets,
                mitigation_recommendation="Ensure Gateway routing tables are digitally signed during production."
            )

    def _simulate_generic_threat(self, threat_id: str, apply_mitigation: bool, timestamp: str) -> TestExecutionResult:
        return TestExecutionResult(
            threat_id=threat_id,
            test_case_id=f"TC-GEN-{threat_id}",
            test_title=f"Automated Validation Test: {threat_id}",
            timestamp=timestamp,
            status="VERIFIED_MITIGATED" if apply_mitigation else "CONFIRMED_EXPLOIT",
            verdict="DEFENSE CONFIRMED" if apply_mitigation else "EXPLOIT CONFIRMED: Vulnerability verified in simulation.",
            mitigation_active=apply_mitigation,
            execution_trace=[f"[{timestamp}] Simulation test executed for {threat_id}. Status: {'Mitigated' if apply_mitigation else 'Vulnerable'}."],
            bus_traffic=[],
            mitigation_recommendation="Apply standard ISO/SAE 21434 and AUTOSAR SecOC countermeasures."
        )
