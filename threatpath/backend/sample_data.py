from models import Component, Connection, Threat, AttackPath, AttackStep

SAMPLE_COMPONENTS = [
    Component(
        id="TCU_01",
        name="Telematics Control Unit (TCU)",
        type="TCU",
        trust_zone="EXTERNAL_UNTRUSTED",
        safety_criticality="QM",
        protocols=["CELLULAR_4G", "WIFI", "ETHERNET", "CAN"],
        firmware_version="v2.14.0-tcu-rc3",
        description="Handles external cellular communication, cloud telemetry, remote vehicle diagnostics, and Over-The-Air (OTA) updates.",
        vulnerabilities=["THREAT_001", "THREAT_002"]
    ),
    Component(
        id="OBD_PORT",
        name="OBD-II Diagnostic Port",
        type="INTERFACE",
        trust_zone="DIAGNOSTIC",
        safety_criticality="QM",
        protocols=["CAN", "UDS_ISO_14229", "DoIP"],
        firmware_version="N/A (Physical Port)",
        description="Physical SAE J1962 vehicle service port exposed beneath the dashboard; exposes high-speed diagnostic communication.",
        vulnerabilities=["THREAT_003"]
    ),
    Component(
        id="GW_01",
        name="Central Gateway ECU",
        type="GATEWAY",
        trust_zone="INTERNAL_BUS",
        safety_criticality="ASIL-B",
        protocols=["CAN_FD", "CAN_HS", "ETHERNET", "LIN"],
        firmware_version="v4.8.1-autosar-classic",
        description="AUTOSAR Central Gateway responsible for routing frames across Telematics, Infotainment, Body, and Safety-Critical Chassis buses.",
        vulnerabilities=["THREAT_004"]
    ),
    Component(
        id="IVI_01",
        name="Infotainment Head Unit (IVI)",
        type="ECU",
        trust_zone="INTERNAL_BUS",
        safety_criticality="QM",
        protocols=["ETHERNET", "CAN", "BLUETOOTH"],
        firmware_version="v3.0.2-android-auto",
        description="Multimedia, navigation display, and Bluetooth smartphone integration module.",
        vulnerabilities=["THREAT_005"]
    ),
    Component(
        id="ESC_BRAKE",
        name="Electronic Stability & Braking ECU",
        type="ECU",
        trust_zone="SAFETY_CRITICAL",
        safety_criticality="ASIL-D",
        protocols=["CAN_HS"],
        firmware_version="v1.0.4-safety-asilD",
        description="ASIL-D safety-critical electronic brake booster and dynamic traction modulation unit.",
        vulnerabilities=["THREAT_006"]
    ),
    Component(
        id="ECM_01",
        name="Engine Control Module (Powertrain)",
        type="ECU",
        trust_zone="SAFETY_CRITICAL",
        safety_criticality="ASIL-D",
        protocols=["CAN_HS", "UDS"],
        firmware_version="v5.2.0-powertrain",
        description="Controls fuel injection, throttle drive-by-wire valve, and engine torque regulation.",
        vulnerabilities=["THREAT_007"]
    )
]

SAMPLE_CONNECTIONS = [
    Connection(
        id="CONN_01",
        source="TCU_01",
        target="GW_01",
        protocol="ETHERNET",
        bus_id="ETH_BACKBONE_100T",
        authenticated=False,
        encrypted=False,
        data_rate="100 Mbps"
    ),
    Connection(
        id="CONN_02",
        source="OBD_PORT",
        target="GW_01",
        protocol="CAN",
        bus_id="CAN_DIAG_500K",
        authenticated=False,
        encrypted=False,
        data_rate="500 kbps"
    ),
    Connection(
        id="CONN_03",
        source="GW_01",
        target="ESC_BRAKE",
        protocol="CAN_HS",
        bus_id="CAN_CHASSIS_SAFETY",
        authenticated=False,
        encrypted=False,
        data_rate="500 kbps"
    ),
    Connection(
        id="CONN_04",
        source="GW_01",
        target="ECM_01",
        protocol="CAN_HS",
        bus_id="CAN_POWERTRAIN",
        authenticated=False,
        encrypted=False,
        data_rate="500 kbps"
    ),
    Connection(
        id="CONN_05",
        source="GW_01",
        target="IVI_01",
        protocol="ETHERNET",
        bus_id="ETH_INFOTAINMENT",
        authenticated=True,
        encrypted=False,
        data_rate="100 Mbps"
    )
]

SAMPLE_THREATS = [
    Threat(
        id="THREAT_001",
        target_component_id="TCU_01",
        target_component_name="Telematics Control Unit (TCU)",
        stride_category="Elevation of Privilege",
        cwe_id="CWE-306",
        cwe_title="Missing Authentication for Critical Function",
        title="Unauthenticated Remote Diagnostic & OTA Update Socket",
        description="The telematics firmware listener on UDP port 13400 (DoIP) fails to verify client authorization prior to accepting firmware flash commands.",
        attack_vector="Remote Cellular (4G LTE / Cloud)",
        cvss_score=9.8,
        severity="Critical",
        tara_impact={"Safety": "Severe (ASIL-D)", "Financial": "High", "Operational": "Catastrophic", "Privacy": "Critical"},
        status="Unverified",
        mitigation="Enforce mutual TLS (mTLS) with TPM-backed hardware certificates and enforce cryptographic signature verification on OTA binaries.",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_002",
        target_component_id="TCU_01",
        target_component_name="Telematics Control Unit (TCU)",
        stride_category="Tampering",
        cwe_id="CWE-120",
        cwe_title="Buffer Copy without Checking Size of Input",
        title="Stack Buffer Overflow in Cellular SMS Parser",
        description="A crafted remote binary SMS packet triggers a classic buffer overflow in the modem parsing routine, yielding remote root shell execution on TCU.",
        attack_vector="Cellular SMS / Baseband",
        cvss_score=8.6,
        severity="High",
        tara_impact={"Safety": "Major", "Financial": "Medium", "Operational": "High", "Privacy": "High"},
        status="Unverified",
        mitigation="Implement safe string parsing primitives, enable compile-time ASLR/Stack Canaries, and restrict modem permissions via seccomp.",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_003",
        target_component_id="OBD_PORT",
        target_component_name="OBD-II Diagnostic Port",
        stride_category="Elevation of Privilege",
        cwe_id="CWE-287",
        cwe_title="Improper Authentication in Diagnostic Protocol",
        title="UDS SecurityAccess (0x27) Fixed Seed/Key Vulnerability",
        description="Diagnostic access level 0x01 on UDS Service 0x27 utilizes an easily reverse-engineered static XOR key algorithm without rate-limiting.",
        attack_vector="Physical Diagnostic Port (OBD-II)",
        cvss_score=7.8,
        severity="High",
        tara_impact={"Safety": "Severe", "Financial": "Medium", "Operational": "High", "Privacy": "Low"},
        status="Unverified",
        mitigation="Upgrade to ISO 14229-1:2020 asymmetric PKI challenge-response (Service 0x29) or 256-bit AES cryptographic seed/key negotiation.",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_004",
        target_component_id="GW_01",
        target_component_name="Central Gateway ECU",
        stride_category="Tampering",
        cwe_id="CWE-284",
        cwe_title="Improper Access Control in Bus Routing",
        title="Unrestricted Cross-Bus Routing to Safety Domain",
        description="Gateway forwards raw Ethernet/DoIP diagnostic packets into the high-speed safety chassis CAN bus without validating packet origin or SecOC tokens.",
        attack_vector="Lateral Bus Pivoting",
        cvss_score=9.1,
        severity="Critical",
        tara_impact={"Safety": "Severe (ASIL-D)", "Financial": "High", "Operational": "Catastrophic", "Privacy": "Medium"},
        status="Unverified",
        mitigation="Deploy AUTOSAR Central Gateway Firewall rules, stateful ingress/egress frame filtering, and drop all unauthenticated routing requests.",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_005",
        target_component_id="IVI_01",
        target_component_name="Infotainment Head Unit (IVI)",
        stride_category="Information Disclosure",
        cwe_id="CWE-200",
        cwe_title="Exposure of Sensitive Information to Unauthorized Actor",
        title="GPS Telemetry & Driver Contacts Leakage via Bluetooth",
        description="Bluetooth pairing profile fails to restrict OBEX phonebook access and broadcasts real-time GPS coordinates over open internal socket.",
        attack_vector="Short-Range Wireless (Bluetooth 5.0)",
        cvss_score=6.5,
        severity="Medium",
        tara_impact={"Safety": "None", "Financial": "Low", "Operational": "Medium", "Privacy": "Severe"},
        status="Unverified",
        mitigation="Enforce strict Android permission sandbox isolation and disable insecure legacy pairing modes.",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_006",
        target_component_id="ESC_BRAKE",
        target_component_name="Electronic Stability & Braking ECU",
        stride_category="Spoofing",
        cwe_id="CWE-345",
        cwe_title="Insufficient Verification of Data Authenticity",
        title="Unauthenticated CAN Frame ID 0x020 Brake Override",
        description="The electronic braking controller directly interprets CAN arbitration ID 0x020 for emergency brake actuation without cryptographic SecOC message authentication.",
        attack_vector="CAN Bus Injection (Lateral Pivot via Gateway)",
        cvss_score=9.9,
        severity="Critical",
        tara_impact={"Safety": "Catastrophic (ASIL-D Life Threat)", "Financial": "Catastrophic", "Operational": "Catastrophic", "Privacy": "Low"},
        status="Unverified",
        mitigation="Implement AUTOSAR Secure Onboard Communication (SecOC) with truncated CMAC-AES128 and monotonically incrementing Freshness Value Manager (FVM).",
        mitigation_applied=False
    ),
    Threat(
        id="THREAT_007",
        target_component_id="ECM_01",
        target_component_name="Engine Control Module (Powertrain)",
        stride_category="Denial of Service",
        cwe_id="CWE-400",
        cwe_title="Uncontrolled Resource Consumption",
        title="CAN Bus-Off Flooding & Engine Limp-Home Injection",
        description="Injecting high-frequency dominant bit frames (arbitration ID 0x000) causes transmission error counter saturation, triggering Bus-Off state.",
        attack_vector="Powertrain CAN Bus Injection",
        cvss_score=8.5,
        severity="High",
        tara_impact={"Safety": "Severe (Vehicle Stall)", "Financial": "Medium", "Operational": "Critical", "Privacy": "None"},
        status="Unverified",
        mitigation="Hardware CAN transceiver with dominant bit clamp detection and anomaly-based intrusion detection (CAN IDS).",
        mitigation_applied=False
    )
]

SAMPLE_ATTACK_PATHS = [
    AttackPath(
        id="PATH_01",
        title="Remote Cellular Ingress -> Central Gateway -> ASIL-D Brake Controller Override",
        entry_point="TCU_01",
        target_node="ESC_BRAKE",
        steps=[
            AttackStep(
                step_number=1,
                from_node="External Cellular Network",
                to_node="TCU_01",
                protocol="4G LTE / DoIP UDP 13400",
                exploit_technique="Exploit unauthenticated remote diagnostic socket (CWE-306)",
                cwe="CWE-306",
                stride="Elevation of Privilege",
                severity="Critical"
            ),
            AttackStep(
                step_number=2,
                from_node="TCU_01",
                to_node="GW_01",
                protocol="Automotive Ethernet 100BASE-T1",
                exploit_technique="Pivot laterally across Ethernet backbone without SecOC token (CWE-284)",
                cwe="CWE-284",
                stride="Tampering",
                severity="High"
            ),
            AttackStep(
                step_number=3,
                from_node="GW_01",
                to_node="ESC_BRAKE",
                protocol="High-Speed Chassis CAN (500 kbps)",
                exploit_technique="Inject forged CAN Frame ID 0x020 payload to trigger sudden brake lock (CWE-345)",
                cwe="CWE-345",
                stride="Spoofing",
                severity="Critical"
            )
        ],
        risk_level="CRITICAL (ASIL-D Hazard)",
        overall_score=9.9,
        description="Allows an external adversary without physical access to remotely hijack vehicle braking over cellular networks."
    ),
    AttackPath(
        id="PATH_02",
        title="Physical OBD-II Port -> Gateway Bypass -> Powertrain Denial of Service",
        entry_point="OBD_PORT",
        target_node="ECM_01",
        steps=[
            AttackStep(
                step_number=1,
                from_node="Physical OBD-II Service Port",
                to_node="GW_01",
                protocol="CAN Diagnostic J1939 / ISO 14229",
                exploit_technique="Bypass UDS SecurityAccess (0x27) with static XOR seed/key algorithm",
                cwe="CWE-287",
                stride="Elevation of Privilege",
                severity="High"
            ),
            AttackStep(
                step_number=2,
                from_node="GW_01",
                to_node="ECM_01",
                protocol="Powertrain CAN Bus",
                exploit_technique="Flood dominant bits (ID 0x000) forcing Engine ECU into Bus-Off state",
                cwe="CWE-400",
                stride="Denial of Service",
                severity="High"
            )
        ],
        risk_level="HIGH (Operational / Safety)",
        overall_score=8.5,
        description="Allows an attacker via service port or malicious dongle to force engine shutdown while in motion."
    )
]
