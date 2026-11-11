import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set font styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a') # Dark slate background

    # Title Banner
    ax.text(50, 95, "THREATPATH: AI-ASSISTED EMBEDDED THREAT MODELING & VALIDATION PIPELINE", 
            ha='center', va='center', color='#38bdf8', fontsize=14, fontweight='bold')
    ax.text(50, 90.5, "Unified Ingestion -> Hybrid Deterministic/LLM Reasoning -> Graph Synthesis -> Virtual Hardware Validation", 
            ha='center', va='center', color='#94a3b8', fontsize=9)

    # 4 Primary Stages
    stages = [
        {"x": 3, "w": 21, "title": "1. ARCHITECTURE INGESTION", "color": "#1e293b", "border": "#3b82f6",
         "items": ["• AUTOSAR ARXML Parser", "• Embedded C/C++ AST (Clang/Tree-sitter)", "• CAN/CAN-FD DBC & Network Topology", "• Hardware Peripherals & Trust Boundaries"]},
        {"x": 27, "w": 22, "title": "2. HYBRID REASONING ENGINE", "color": "#1e293b", "border": "#8b5cf6",
         "items": ["• Deterministic Rule Engine (ISO 21434)", "• STRIDE-per-Element Threat Mapping", "• CWE Hardware & Embedded Taxonomies", "• Contextual LLM Reasoning & TARA Scoring"]},
        {"x": 52, "w": 22, "title": "3. ATTACK PATH GRAPH", "color": "#1e293b", "border": "#f59e0b",
         "items": ["• NetworkX Multi-Hop Graph Traversal", "• Exploitability-Weighted Shortest Path", "• Lateral Pivot Detection (TCU → CAN)", "• Attack Trees & Entry-to-Target Flows"]},
        {"x": 77, "w": 20, "title": "4. TEST & VALIDATION SANDBOX", "color": "#1e293b", "border": "#10b981",
         "items": ["• Automated Security Test Generation", "• Virtual CAN/UDS (ISO 14229) Simulator", "• Confirmed vs Unverified Exploit Matrix", "• UNECE WP.29 Mitigations & SecOC"]}
    ]

    for s in stages:
        rect = patches.FancyBboxPatch((s['x'], 18), s['w'], 68, boxstyle="round,pad=1.2,rounding_size=2",
                                      facecolor=s['color'], edgecolor=s['border'], linewidth=2)
        ax.add_patch(rect)
        
        # Header Box
        header_rect = patches.FancyBboxPatch((s['x']+0.5, 78), s['w']-1, 7, boxstyle="round,pad=0.5,rounding_size=1",
                                             facecolor=s['border'], edgecolor='none', alpha=0.25)
        ax.add_patch(header_rect)
        ax.text(s['x'] + s['w']/2, 81.5, s['title'], ha='center', va='center', color='#f8fafc', fontsize=9.5, fontweight='bold')
        
        # Items
        y_pos = 71
        for item in s['items']:
            ax.text(s['x'] + 2, y_pos, item, ha='left', va='center', color='#cbd5e1', fontsize=8.5)
            y_pos -= 13

    # Connecting Flow Arrows
    for x_conn in [24.5, 49.5, 74.5]:
        ax.annotate('', xy=(x_conn + 2.2, 52), xytext=(x_conn - 0.2, 52),
                    arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2, headwidth=7, headlength=7))

    # Bottom Closed-Loop Feedback Arrow
    ax.annotate('', xy=(13.5, 14), xytext=(87, 14),
                arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=1.5, headwidth=6, headlength=6, linestyle='--'))
    ax.text(50, 10, "Continuous Feedback Loop: Empirical Sandbox Test Results Dynamically Refine Vulnerability & Risk Confidence",
            ha='center', va='center', color='#10b981', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    plt.savefig('architecture_diagram.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("architecture_diagram.png generated")

def create_attack_tree_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Title
    ax.text(50, 95, "AUTOMOTIVE MULTI-HOP ATTACK PATH & VALIDATION SCENARIO", 
            ha='center', va='center', color='#f43f5e', fontsize=14, fontweight='bold')
    ax.text(50, 90.5, "Scenario: Remote Cellular Ingress (TCU) → Gateway Pivoting → CAN Spoofing → Safety Braking ECU", 
            ha='center', va='center', color='#94a3b8', fontsize=9)

    # 4 Nodes representing the Attack Chain
    nodes = [
        {"x": 4, "y": 45, "w": 20, "h": 36, "title": "EXTERNAL ATTACKER\n(Cellular / Cloud)", "border": "#ef4444", "bg": "#1e293b",
         "badge": "Entry Point", "cwe": "CWE-306 (Missing Auth)", "action": "Exploits unauthenticated\nOTA firmware socket\non Telematics Unit (TCU)"},
        {"x": 28, "y": 45, "w": 20, "h": 36, "title": "TELEMATICS (TCU)\n(Linux / QNX)", "border": "#f97316", "bg": "#1e293b",
         "badge": "Compromised Node", "cwe": "CWE-120 (Buffer Overflow)", "action": "In-memory code execution\ngains root shell on TCU;\nsends payload to Gateway"},
        {"x": 52, "y": 45, "w": 20, "h": 36, "title": "CENTRAL GATEWAY\n(AUTOSAR Classic)", "border": "#f59e0b", "bg": "#1e293b",
         "badge": "Lateral Pivot", "cwe": "CWE-284 (Improper Routing)", "action": "Gateway lacks packet filtering\nand SecOC validation;\nroutes frame to Safety CAN"},
        {"x": 76, "y": 45, "w": 20, "h": 36, "title": "BRAKING / ESC ECU\n(Safety-Critical ASIL-D)", "border": "#dc2626", "bg": "#450a0a",
         "badge": "CRITICAL TARGET", "cwe": "CWE-345 (Missing Verif.)", "action": "Accepts spoofed CAN ID 0x020;\noverrides brake pressure.\nImmediate Physical Impact!"}
    ]

    for n in nodes:
        rect = patches.FancyBboxPatch((n['x'], n['y']), n['w'], n['h'], boxstyle="round,pad=0.8,rounding_size=2",
                                      facecolor=n['bg'], edgecolor=n['border'], linewidth=2)
        ax.add_patch(rect)
        
        # Badge
        ax.text(n['x'] + n['w']/2, n['y'] + n['h'] - 3.5, n['badge'], ha='center', va='center',
                color=n['border'], fontsize=8, fontweight='bold')
        
        # Title
        ax.text(n['x'] + n['w']/2, n['y'] + n['h'] - 10, n['title'], ha='center', va='center',
                color='#f8fafc', fontsize=8.5, fontweight='bold')
        
        # CWE Tag
        ax.text(n['x'] + n['w']/2, n['y'] + n['h'] - 17, n['cwe'], ha='center', va='center',
                color='#38bdf8', fontsize=7.5, fontweight='bold')
        
        # Description
        ax.text(n['x'] + n['w']/2, n['y'] + 8, n['action'], ha='center', va='center',
                color='#cbd5e1', fontsize=7.5)

    # Attack Arrows connecting nodes
    for x_arr in [24.5, 48.5, 72.5]:
        ax.annotate('', xy=(x_arr + 3, 63), xytext=(x_arr - 0.2, 63),
                    arrowprops=dict(facecolor='#ef4444', edgecolor='#ef4444', width=2.5, headwidth=8, headlength=8))

    # Bottom Box: ThreatPath Simulation & Mitigation
    mit_rect = patches.FancyBboxPatch((4, 6), 92, 30, boxstyle="round,pad=0.8,rounding_size=2",
                                      facecolor='#064e3b', edgecolor='#10b981', linewidth=1.5, alpha=0.9)
    ax.add_patch(mit_rect)
    
    ax.text(7, 30, "THREATPATH AUTOMATED VALIDATION & MITIGATION VERIFICATION", 
            color='#34d399', fontsize=10, fontweight='bold')
    
    val_points = [
        "1. Dynamic CAN Test Execution: ThreatPath Virtual CAN Bus replayed payload with ID 0x020 -> Safety ECU registered command (EXPLOIT CONFIRMED).",
        "2. Severity & Risk Scoring: ASIL-D Hazard | CVSS 9.8 (Critical) | Financial & Safety Loss: Catastrophic under ISO/SAE 21434 TARA.",
        "3. Deterministic Defense Verification: Injected AUTOSAR SecOC (Freshness Value + CMAC tag) -> Gateway dropped unauthenticated frame -> Threat MITIGATED."
    ]
    y_pt = 23
    for pt in val_points:
        ax.text(7, y_pt, pt, color='#ecfdf5', fontsize=8)
        y_pt -= 6.5

    plt.tight_layout()
    plt.savefig('attack_path_diagram.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("attack_path_diagram.png generated")

def create_comparison_matrix():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Title
    ax.text(50, 95, "THREATPATH BENCHMARK: REVOLUTIONIZING EMBEDDED THREAT MODELING", 
            ha='center', va='center', color='#38bdf8', fontsize=14, fontweight='bold')
    ax.text(50, 90.5, "Comparative Analysis against Conventional & Commercial Industry Approaches", 
            ha='center', va='center', color='#94a3b8', fontsize=9)

    # Table Headers
    cols = [
        {"name": "Capability / Feature", "x": 4, "w": 28},
        {"name": "Traditional Manual TARA\n(Excel / Spreadsheets)", "x": 33, "w": 20},
        {"name": "Microsoft Threat Tool\n& Generic SAST", "x": 54, "w": 20},
        {"name": "ThreatPath (Our Solution)\nAutomated & Dynamic", "x": 75, "w": 21}
    ]

    for c in cols:
        rect = patches.FancyBboxPatch((c['x'], 78), c['w'], 9, boxstyle="round,pad=0.3,rounding_size=1",
                                      facecolor='#1e293b', edgecolor='#475569', linewidth=1)
        ax.add_patch(rect)
        ax.text(c['x'] + c['w']/2, 82.5, c['name'], ha='center', va='center',
                color='#f8fafc', fontsize=8, fontweight='bold')

    # Rows
    rows = [
        ("Architecture Ingestion", "Manual entry only\n(Slow, error-prone)", "Generic DFD blocks\n(No embedded context)", "Native AUTOSAR ARXML,\nC/C++ AST, & CAN topologies"),
        ("Embedded Domain Rules", "Ad-hoc checklists\n(Inconsistent coverage)", "Generic IT/Web rules\n(Lacks CAN/UDS/AUTOSAR)", "ISO 21434, UNECE WP.29,\nAUTOSAR SecOC & Hardware CWE"),
        ("Attack Path Synthesis", "Static tree drawings\n(No multi-hop computation)", "Isolated component flaws\n(Cannot trace lateral pivots)", "NetworkX graph algorithms\n(Identifies weakest attack chains)"),
        ("Security Test Generation", "None (Manual pentest\nteams write custom tests)", "Generic unit test templates\n(No hardware simulation)", "Automates real virtual CAN\nand UDS ISO 14229 test vectors"),
        ("Closed-Loop Validation", "None (Static report only;\nno empirical validation)", "None (Relies entirely on\nseparate manual penetration)", "Isolated virtual CAN sandbox\nconfirms/refutes exploits"),
        ("Speed & Turnaround", "4 to 8 Weeks per ECU\n($15,000 - $30,000 cost)", "1 to 2 Weeks\n(Requires heavy triage)", "Under 2 Minutes\n(Continuous DevSecOps)")
    ]

    y_pos = 68
    for row_idx, r in enumerate(rows):
        bg_col = '#1e293b' if row_idx % 2 == 0 else '#0f172a'
        # Feature Col
        r1 = patches.Rectangle((4, y_pos), 28, 8.5, facecolor=bg_col, edgecolor='#334155', linewidth=0.5)
        ax.add_patch(r1)
        ax.text(5.5, y_pos + 4.25, r[0], ha='left', va='center', color='#e2e8f0', fontsize=8, fontweight='bold')
        
        # Manual Col
        r2 = patches.Rectangle((33, y_pos), 20, 8.5, facecolor=bg_col, edgecolor='#334155', linewidth=0.5)
        ax.add_patch(r2)
        ax.text(43, y_pos + 4.25, r[1], ha='center', va='center', color='#f87171', fontsize=7.5)
        
        # Generic Tool Col
        r3 = patches.Rectangle((54, y_pos), 20, 8.5, facecolor=bg_col, edgecolor='#334155', linewidth=0.5)
        ax.add_patch(r3)
        ax.text(64, y_pos + 4.25, r[2], ha='center', va='center', color='#fbbf24', fontsize=7.5)
        
        # ThreatPath Col (Highlight)
        r4 = patches.Rectangle((75, y_pos), 21, 8.5, facecolor='#064e3b' if row_idx % 2 == 0 else '#022c22',
                               edgecolor='#10b981', linewidth=1)
        ax.add_patch(r4)
        ax.text(85.5, y_pos + 4.25, r[3], ha='center', va='center', color='#34d399', fontsize=7.5, fontweight='bold')
        
        y_pos -= 9.5

    plt.tight_layout()
    plt.savefig('comparison_matrix.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("comparison_matrix.png generated")

if __name__ == '__main__':
    create_system_architecture()
    create_attack_tree_diagram()
    create_comparison_matrix()


def create_validation_workflow():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Title
    ax.text(50, 95, "CLOSED-LOOP AUTOMATED EMBEDDED SECURITY VALIDATION ENGINE", 
            ha='center', va='center', color='#38bdf8', fontsize=14, fontweight='bold')
    ax.text(50, 90.5, "From Theoretical Vulnerability to Automated Dynamic Exploit Verification & Cryptographic Mitigation", 
            ha='center', va='center', color='#94a3b8', fontsize=9)

    # 3 Large Flow Boxes
    # Box 1: Threat Detection & Rule Matching
    b1 = patches.FancyBboxPatch((3, 20), 28, 65, boxstyle="round,pad=1,rounding_size=2",
                               facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2)
    ax.add_patch(b1)
    ax.text(17, 80, "STAGE 1: HYPOTHESIS & RULES", ha='center', va='center', color='#38bdf8', fontsize=9.5, fontweight='bold')
    items1 = [
        "• Static AST & ARXML Scanned",
        "• Unprotected Service Discovered:\n  UDS Service 0x27 / 0x34\n  (Security Access & Request Download)",
        "• Missing Authentication CWE-306\n  matched via Deterministic Engine",
        "• STRIDE Mapping: Elevation of\n  Privilege & Tampering",
        "• Output: Formal Test Specification\n  targeting Virtual Gateway"
    ]
    y1 = 70
    for it in items1:
        ax.text(5, y1, it, color='#e2e8f0', fontsize=8)
        y1 -= 11.5

    # Box 2: Isolated Virtual ECU Simulation
    b2 = patches.FancyBboxPatch((36, 20), 28, 65, boxstyle="round,pad=1,rounding_size=2",
                               facecolor='#1e293b', edgecolor='#f59e0b', linewidth=2)
    ax.add_patch(b2)
    ax.text(50, 80, "STAGE 2: ISOLATED SIMULATION", ha='center', va='center', color='#f59e0b', fontsize=9.5, fontweight='bold')
    items2 = [
        "• Virtual CAN Socket initialized\n  in safe sandboxed container",
        "• Automated Test Harness injects\n  crafted CAN frame:\n  ID: 0x7DF, Data: [02 27 01 00...]",
        "• Replays diagnostic unlock vector\n  without cryptographic challenge",
        "• Observes Target Response:\n  Service responds 0x67 (Positive Reply)",
        "• Status: EXPLOIT CONFIRMED\n  (Zero physical hardware needed)"
    ]
    y2 = 70
    for it in items2:
        ax.text(38, y2, it, color='#e2e8f0', fontsize=8)
        y2 -= 11.5

    # Box 3: Verification & Cryptographic Mitigation
    b3 = patches.FancyBboxPatch((69, 20), 28, 65, boxstyle="round,pad=1,rounding_size=2",
                               facecolor='#1e293b', edgecolor='#10b981', linewidth=2)
    ax.add_patch(b3)
    ax.text(83, 80, "STAGE 3: MITIGATION VERIFIED", ha='center', va='center', color='#10b981', fontsize=9.5, fontweight='bold')
    items3 = [
        "• System enforces Countermeasure:\n  AUTOSAR SecOC CMAC Verification\n  & Challenge-Response Seed/Key",
        "• Automated Re-test Triggered:\n  Injected attack packet re-sent\n  across virtual CAN interface",
        "• Controller drops forged frame:\n  ECU responds with 0x7F 27 35\n  (Invalid Key / Access Denied)",
        "• Risk Level lowered: High -> Negligible",
        "• Generates ISO 21434 Audit Report"
    ]
    y3 = 70
    for it in items3:
        ax.text(71, y3, it, color='#e2e8f0', fontsize=8)
        y3 -= 11.5

    # Flow arrows
    ax.annotate('', xy=(35, 52), xytext=(32, 52),
                arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2, headwidth=7, headlength=7))
    ax.annotate('', xy=(68, 52), xytext=(65, 52),
                arrowprops=dict(facecolor='#f59e0b', edgecolor='#f59e0b', width=2, headwidth=7, headlength=7))

    # Bottom summary badge
    sum_rect = patches.FancyBboxPatch((15, 6), 70, 9, boxstyle="round,pad=0.5,rounding_size=1",
                                      facecolor='#0f766e', edgecolor='#14b8a6', linewidth=1.5)
    ax.add_patch(sum_rect)
    ax.text(50, 10.5, "RESULT: Full Loop Closed within 90 Seconds -- Eliminates Weeks of Manual Pen-Testing",
            ha='center', va='center', color='#ffffff', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig('validation_workflow.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("validation_workflow.png generated")

create_validation_workflow()
