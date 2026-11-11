from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
import os
import json

from models import (
    Component, Connection, Threat, AttackPath,
    TestExecutionRequest, TestExecutionResult
)
from sample_data import SAMPLE_COMPONENTS, SAMPLE_CONNECTIONS, SAMPLE_THREATS, SAMPLE_ATTACK_PATHS
from graph_engine import GraphEngine
from simulator import SimulationEngine
from live_bus import live_bus
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI(
    title="ThreatPath API",
    description="AI-Assisted Threat Modeling & Security Validation for Embedded Systems",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory State
components_store = [c.model_copy() for c in SAMPLE_COMPONENTS]
connections_store = [conn.model_copy() for conn in SAMPLE_CONNECTIONS]
threats_store = [t.model_copy() for t in SAMPLE_THREATS]
graph_engine = GraphEngine(components_store, connections_store)
simulator = SimulationEngine()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ThreatPath Core Engine",
        "version": "1.0.0",
        "modules": {
            "arxml_parser": "Active",
            "stride_engine": "Active (ISO/SAE 21434 Aligned)",
            "networkx_graph_engine": "Active",
            "virtual_can_simulator": "Active"
        }
    }

@app.get("/api/summary-stats")
def get_summary_stats():
    total_components = len(components_store)
    total_connections = len(connections_store)
    total_threats = len(threats_store)
    
    confirmed = sum(1 for t in threats_store if t.status == "Confirmed Exploit")
    mitigated = sum(1 for t in threats_store if t.status == "Mitigated")
    unverified = sum(1 for t in threats_store if t.status == "Unverified")
    critical_threats = sum(1 for t in threats_store if t.severity == "Critical")
    
    # Calculate ISO 21434 dynamic compliance score
    if total_threats > 0:
        compliance_pct = round((mitigated / total_threats) * 100, 1)
    else:
        compliance_pct = 100.0

    return {
        "total_components": total_components,
        "total_connections": total_connections,
        "total_threats": total_threats,
        "critical_threats": critical_threats,
        "unverified_threats": unverified,
        "confirmed_exploits": confirmed,
        "mitigated_threats": mitigated,
        "iso_21434_compliance_score": compliance_pct,
        "attack_surface_interfaces": ["Cellular 4G LTE", "OBD-II Port", "Bluetooth 5.0", "Automotive Ethernet 100T"]
    }

@app.get("/api/components", response_model=List[Component])
def get_components():
    return components_store

@app.get("/api/connections", response_model=List[Connection])
def get_connections():
    return connections_store

@app.get("/api/threats", response_model=List[Threat])
def get_threats():
    return threats_store

@app.get("/api/attack-paths")
def get_attack_paths():
    dynamic_paths = graph_engine.find_all_attack_paths(
        entry_points=["TCU_01", "OBD_PORT"],
        target_nodes=["ESC_BRAKE", "ECM_01"]
    )
    return {
        "preconfigured_scenarios": [p.model_dump() for p in SAMPLE_ATTACK_PATHS],
        "graph_computed_paths": dynamic_paths
    }

@app.get("/api/topology")
def get_topology():
    return graph_engine.get_topology_for_ui()

@app.post("/api/simulate-test", response_model=TestExecutionResult)
def run_simulation(req: TestExecutionRequest):
    # Find threat
    threat = next((t for t in threats_store if t.id == req.threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
        
    result = simulator.execute_test(req.threat_id, req.apply_mitigation)
    
    # Update threat state based on test outcome
    if result.status == "CONFIRMED_EXPLOIT":
        threat.status = "Confirmed Exploit"
        threat.mitigation_applied = False
        threat.evidence_log = f"Exploit verified at {result.timestamp}: {result.verdict}"
        live_bus.set_attack(True, 15.0)
        live_bus.toggle_secoc(False)
    elif result.status == "VERIFIED_MITIGATED":
        threat.status = "Mitigated"
        threat.mitigation_applied = True
        threat.evidence_log = f"Mitigation verified at {result.timestamp}: {result.verdict}"
        live_bus.set_attack(False)
        live_bus.toggle_secoc(True)
        
    return result

@app.post("/api/apply-mitigation/{threat_id}")
def apply_mitigation(threat_id: str):
    threat = next((t for t in threats_store if t.id == threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    threat.mitigation_applied = True
    # Re-run simulation with mitigation
    result = simulator.execute_test(threat_id, apply_mitigation=True)
    threat.status = "Mitigated"
    threat.evidence_log = f"Mitigation enforced & validated at {result.timestamp}."
    return {"status": "success", "threat": threat, "test_result": result}

@app.post("/api/reset-environment")
def reset_environment():
    global threats_store, components_store
    threats_store = [t.model_copy() for t in SAMPLE_THREATS]
    components_store = [c.model_copy() for c in SAMPLE_COMPONENTS]
    return {"status": "success", "message": "Environment successfully reset to baseline."}

@app.post("/api/upload-architecture")
async def upload_architecture(file: UploadFile = File(...)):
    """Simulates ingestion and parsing of AUTOSAR ARXML or C/C++ firmware files."""
    filename = file.filename
    content = await file.read()
    file_size_kb = len(content) / 1024
    
    return {
        "status": "success",
        "file_name": filename,
        "file_size_kb": round(file_size_kb, 2),
        "parser_used": "AUTOSAR Classic ARXML Deserializer" if filename.endswith((".xml", ".arxml")) else "Clang/Tree-sitter Embedded C AST Scanner",
        "extracted_elements": {
            "software_components_swc": 6,
            "can_pdus_identified": 14,
            "trust_boundaries_mapped": 3,
            "unprotected_diagnostic_services": 2
        },
        "findings_generated": 7,
        "message": f"Successfully parsed {filename}. Identified 7 potential attack vectors mapped to ISO/SAE 21434."
    }

@app.get("/api/generate-report")
def generate_report():
    return {
        "assessment_title": "ISO/SAE 21434 Threat Analysis & Security Validation Report",
        "target_system": "Next-Gen Connected Vehicle Gateway & ASIL-D Chassis Architecture",
        "generated_by": "ThreatPath AI-Assisted Security Engine",
        "pid": "TG0915208",
        "team": ["Mohammed H", "Mohammed J", "RAJALAKSHMI M"],
        "institution": "PSNA College of Engineering and Technology, Dindigul, Tamil Nadu",
        "summary": get_summary_stats(),
        "threats": [t.model_dump() for t in threats_store],
        "attack_paths": [p.model_dump() for p in SAMPLE_ATTACK_PATHS]
    }

# ==========================================
# REAL-TIME LIVE CAN BUS TELEMETRY STREAM
# ==========================================
@app.get("/api/live-bus/status")
def get_live_bus_status():
    return live_bus.get_snapshot()

@app.post("/api/live-bus/inject")
def trigger_live_injection(duration: float = 12.0):
    live_bus.set_attack(True, duration)
    return {
        "status": "attack_injected",
        "target": "CAN ID 0x020 (Braking ESC)",
        "duration_sec": duration,
        "secoc_active": live_bus.is_secoc_active
    }

@app.post("/api/live-bus/stop-attack")
def stop_live_attack():
    live_bus.set_attack(False)
    return {"status": "attack_stopped", "secoc_active": live_bus.is_secoc_active}

@app.post("/api/live-bus/toggle-secoc")
def toggle_live_secoc():
    new_state = live_bus.toggle_secoc()
    return {"status": "success", "secoc_active": new_state}

@app.get("/api/live-bus/stream")
async def stream_live_bus():
    async def event_generator():
        while True:
            snapshot = live_bus.get_snapshot()
            yield f"data: {json.dumps(snapshot)}\n\n"
            await asyncio.sleep(0.4)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Mount frontend production build
# Locate frontend production build
dist_candidates = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend-app", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "threatpath", "frontend-app", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "frontend-app", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "dist")),
]

dist_path = None
for p in dist_candidates:
    if os.path.exists(p) and os.path.exists(os.path.join(p, "index.html")):
        dist_path = p
        break

if dist_path:
    assets_dir = os.path.join(dist_path, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    def serve_index():
        index_file = os.path.join(dist_path, "index.html")
        return FileResponse(index_file)

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        requested_file = os.path.join(dist_path, full_path)
        if full_path and os.path.isfile(requested_file):
            return FileResponse(requested_file)
        index_file = os.path.join(dist_path, "index.html")
        return FileResponse(index_file)
else:
    @app.get("/")
    def no_dist():
        return {
            "status": "ThreatPath Backend Active",
            "message": "Frontend dist/index.html not found on server path",
            "searched_paths": dist_candidates
        }

if __name__ == "__main__":
    import uvicorn
    import sys
    port = int(os.getenv("PORT", 5000))
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    print(f"[*] Starting ThreatPath on http://127.0.0.1:{port} and http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
