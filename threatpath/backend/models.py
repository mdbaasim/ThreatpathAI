from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Component(BaseModel):
    id: str
    name: str
    type: str  # "ECU", "GATEWAY", "TCU", "INTERFACE", "SENSOR", "ACTUATOR"
    trust_zone: str  # "EXTERNAL_UNTRUSTED", "INTERNAL_BUS", "SAFETY_CRITICAL", "DIAGNOSTIC"
    safety_criticality: str  # "ASIL-D", "ASIL-C", "ASIL-B", "ASIL-A", "QM"
    protocols: List[str]
    firmware_version: str
    description: str
    vulnerabilities: List[str] = []

class Connection(BaseModel):
    id: str
    source: str
    target: str
    protocol: str  # "CAN", "CAN-FD", "ETHERNET", "UDS", "CELLULAR_OTA"
    bus_id: str
    authenticated: bool
    encrypted: bool
    data_rate: str

class Threat(BaseModel):
    id: str
    target_component_id: str
    target_component_name: str
    stride_category: str  # Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
    cwe_id: str
    cwe_title: str
    title: str
    description: str
    attack_vector: str
    cvss_score: float
    severity: str  # "Critical", "High", "Medium", "Low"
    tara_impact: Dict[str, str]  # Safety, Financial, Operational, Privacy
    status: str  # "Unverified", "Confirmed Exploit", "Mitigated"
    mitigation: str
    mitigation_applied: bool = False
    evidence_log: Optional[str] = None

class AttackStep(BaseModel):
    step_number: int
    from_node: str
    to_node: str
    protocol: str
    exploit_technique: str
    cwe: str
    stride: str
    severity: str

class AttackPath(BaseModel):
    id: str
    title: str
    entry_point: str
    target_node: str
    steps: List[AttackStep]
    risk_level: str
    overall_score: float
    description: str

class TestExecutionRequest(BaseModel):
    threat_id: str
    apply_mitigation: bool = False

class VirtualPacket(BaseModel):
    timestamp_offset_ms: int
    bus: str
    arbitration_id: str
    data_bytes: str
    direction: str  # "TX" or "RX"
    description: str
    flag: str  # "ATTACK", "NORMAL", "BLOCKED", "DEFENDED"

class TestExecutionResult(BaseModel):
    threat_id: str
    test_case_id: str
    test_title: str
    timestamp: str
    status: str  # "CONFIRMED_EXPLOIT" or "VERIFIED_MITIGATED"
    verdict: str
    mitigation_active: bool
    execution_trace: List[str]
    bus_traffic: List[VirtualPacket]
    mitigation_recommendation: str
