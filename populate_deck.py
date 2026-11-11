import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    src_pptx = r'C:\Users\mdbaa\Downloads\00000_TG10_Presentation Round.pptx'
    dst_pptx = r'c:\Users\mdbaa\OneDrive\Desktop\L&T\15208_TG10_Presentation Round.pptx'
    
    prs = pptx.Presentation(src_pptx)
    print(f"Loaded presentation with {len(prs.slides)} slides.")

    # Colors
    c_navy = RGBColor(15, 23, 42)
    c_blue = RGBColor(2, 132, 199)
    c_darkblue = RGBColor(14, 116, 144)
    c_slate = RGBColor(51, 65, 85)
    c_light_slate = RGBColor(100, 116, 139)
    c_white = RGBColor(255, 255, 255)
    c_emerald = RGBColor(16, 185, 129)
    c_rose = RGBColor(225, 29, 72)
    c_amber = RGBColor(217, 119, 6)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    
    # Update title texts
    for sh in s1.shapes:
        if sh.has_text_frame:
            txt = sh.text_frame.text.strip()
            if '00000' in txt:
                sh.text_frame.text = 'TG0915208'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(16)
                sh.text_frame.paragraphs[0].font.color.rgb = c_blue
            elif 'Concept Title' in txt:
                sh.text_frame.text = 'ThreatPath: AI-Assisted Threat Modeling and Security Validation for Embedded Systems'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(20)
                sh.text_frame.paragraphs[0].font.color.rgb = c_navy
            elif 'College name, City, State' in txt:
                sh.text_frame.text = 'PSNA College of Engineering and Technology, Dindigul, Tamil Nadu'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(14)
                sh.text_frame.paragraphs[0].font.color.rgb = c_darkblue
            elif txt == 'Name 1':
                sh.text_frame.text = 'Mohammed H'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(12)
            elif txt == 'Name 2':
                sh.text_frame.text = 'Mohammed J'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(12)
            elif txt == 'Name 3':
                sh.text_frame.text = 'RAJALAKSHMI M'
                sh.text_frame.paragraphs[0].font.bold = True
                sh.text_frame.paragraphs[0].font.size = Pt(12)
            elif txt == 'Name 4':
                sh.text_frame.text = '' # Blank out 4th name
            elif 'Author 4' in txt:
                # hide author 4 box
                sh.text_frame.text = ''
                sh.line.color.rgb = c_white
                sh.fill.background()

    # Re-center the 3 author boxes cleanly
    # Width of slide = 13.33 inches = 12192000 emu
    # 3 boxes: lefts = 3.6", 5.8", 8.0" (in inches)
    author_rects = [s for s in s1.shapes if s.name in ['Rectangle 7', 'Rectangle 9', 'Rectangle 10']]
    author_labels = [s for s in s1.shapes if s.name in ['TextBox 12', 'TextBox 14', 'TextBox 15']]
    
    x_positions = [Inches(3.4), Inches(5.8), Inches(8.2)]
    for idx, r in enumerate(author_rects):
        r.left = x_positions[idx]
        r.width = Inches(1.8)
        r.height = Inches(1.6)
    for idx, l in enumerate(author_labels):
        l.left = x_positions[idx]
        l.width = Inches(1.8)

    # -------------------------------------------------------------------------
    # Helper to clean content placeholder
    # -------------------------------------------------------------------------
    def get_content_placeholder(slide):
        for s in slide.shapes:
            if s.has_text_frame and s.name.startswith("Text Placeholder"):
                return s
        return None

    # -------------------------------------------------------------------------
    # SLIDE 2: Challenge Statement
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    cp2 = get_content_placeholder(s2)
    if cp2:
        cp2.text_frame.text = "" # clear default empty bullet
    
    # Left Card: Industry Context & Critical Problem
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3))
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    c1.line.color.rgb = RGBColor(203, 213, 225)
    c1.line.width = Pt(1.5)
    
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.3)
    tf1.margin_right = Inches(0.3)
    tf1.margin_top = Inches(0.3)
    
    p = tf1.paragraphs[0]
    p.text = "INDUSTRY CONTEXT & REGULATORY MANDATE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    
    points1 = [
        ("Hyper-Connected Architectures: ", "Modern Software-Defined Vehicles (SDVs) integrate 100+ Electronic Control Units (ECUs) over CAN, CAN-FD, Automotive Ethernet, and cellular OTA."),
        ("Strict International Regulations: ", "ISO/SAE 21434 and UNECE WP.29 R155/R156 legally mandate verifiable Threat Analysis and Risk Assessment (TARA) throughout the engineering lifecycle."),
        ("Manual Spreadsheet Bottleneck: ", "Over 85% of OEM & Tier-1 threat modeling remains entirely manual (Excel tables & Microsoft TMT), requiring weeks of error-prone engineering time.")
    ]
    for b_title, b_desc in points1:
        p = tf1.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_blue
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = c_slate

    # Right Card: The Core Challenge
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(241, 245, 249)
    c2.line.color.rgb = RGBColor(2, 132, 199)
    c2.line.width = Pt(2)
    
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_right = Inches(0.3)
    tf2.margin_top = Inches(0.3)
    
    p = tf2.paragraphs[0]
    p.text = "THE CORE CHALLENGE & INDUSTRY GAPS"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_blue
    
    points2 = [
        ("Siloed Component Analysis: ", "Conventional tools evaluate components in isolation. They fail to trace multi-hop lateral attack paths (e.g. TCU cellular bug -> Gateway pivoting -> Brake controller spoofing)."),
        ("Lack of Dynamic Verification: ", "Current threat models are purely theoretical 'shelf-ware'—they cannot empirically test or confirm whether a vulnerability is practically exploitable in code/protocol."),
        ("Prohibitive Hardware & Testing Cost: ", "Physical Hardware-In-The-Loop (HIL) penetration testing costs $15k–$30k per ECU and requires 4–8 weeks per validation cycle."),
        ("The Challenge Objective: ", "Develop ThreatPath: an automated platform that ingests embedded architecture (AUTOSAR/C code), synthesizes attack trees, and executes closed-loop validation in an isolated virtual simulation environment.")
    ]
    for b_title, b_desc in points2:
        p = tf2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_rose if "Objective" not in b_title else c_emerald
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = c_navy if "Objective" in b_title else c_slate

    # -------------------------------------------------------------------------
    # SLIDE 3: Concept / Proposed Solution
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    cp3 = get_content_placeholder(s3)
    if cp3:
        cp3.text_frame.text = ""
        
    # Add Architecture Image
    arch_img_path = r'c:\Users\mdbaa\OneDrive\Desktop\L&T\architecture_diagram.png'
    if os.path.exists(arch_img_path):
        s3.shapes.add_picture(arch_img_path, Inches(0.8), Inches(1.35), width=Inches(11.7))

    # -------------------------------------------------------------------------
    # SLIDE 4: Pros and Cons of the solution
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    cp4 = get_content_placeholder(s4)
    if cp4:
        cp4.text_frame.text = ""

    comp_img_path = r'c:\Users\mdbaa\OneDrive\Desktop\L&T\comparison_matrix.png'
    if os.path.exists(comp_img_path):
        s4.shapes.add_picture(comp_img_path, Inches(0.8), Inches(1.35), width=Inches(11.7))

    # -------------------------------------------------------------------------
    # SLIDE 5: Technical Description
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    cp5 = get_content_placeholder(s5)
    if cp5:
        cp5.text_frame.text = ""

    # 4 Pillar Boxes
    pillars = [
        {"title": "1. Multi-Modal Ingestion", "color": c_blue, "bg": RGBColor(240, 249, 255),
         "bullets": ["Parses AUTOSAR Classic & Adaptive ARXML (SWCs, Port Interfaces, PDU descriptors).", "Extracts CAN/CAN-FD DBC communication matrices and bus topologies.", "AST Static Analysis (Tree-sitter/Clang) scans embedded C/C++ firmware for memory flaws (CWE-120, CWE-121)."]},
        {"title": "2. Hybrid Reasoning Engine", "color": RGBColor(124, 58, 237), "bg": RGBColor(245, 243, 255),
         "bullets": ["Deterministic STRIDE-per-Element Matrix guarantees zero hallucination of security rules.", "Automotive Standard Alignment: Directly maps to ISO/SAE 21434 TARA & UNECE WP.29 R155.", "Contextual AI synthesis generates tailored mitigation guidance and threat summaries."]},
        {"title": "3. Attack Path Graph Engine", "color": c_amber, "bg": RGBColor(254, 252, 232),
         "bullets": ["NetworkX Directed Multigraph G=(V, E) models all ECUs, gateways, and buses.", "Dijkstra & Exploitability Algorithms discover weakest multi-hop attack routes.", "Detects Lateral Pivots: Traces remote cellular entry through gateway to safety brake controller."]},
        {"title": "4. Virtual ECU Test Sandbox", "color": c_emerald, "bg": RGBColor(240, 253, 244),
         "bullets": ["Isolated virtual CAN socket (vcan) simulator with zero physical hardware risk.", "Crafts dynamic test vectors: UDS Diagnostic (ISO 14229) & CAN ID spoofing.", "Closed-loop verdict: Validates confirmed exploits vs. verified SecOC mitigations."]}
    ]

    for idx, p_info in enumerate(pillars):
        x = Inches(0.8 + idx * 2.95)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.4), Inches(2.8), Inches(5.4))
        box.fill.solid()
        box.fill.fore_color.rgb = p_info['bg']
        box.line.color.rgb = p_info['color']
        box.line.width = Pt(2)
        
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = p_info['title']
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = p_info['color']
        
        for b in p_info['bullets']:
            p = tf.add_paragraph()
            p.space_before = Pt(12)
            p.text = "• " + b
            p.font.size = Pt(9.5)
            p.font.color.rgb = c_navy

    # -------------------------------------------------------------------------
    # SLIDE 6: Implementation Plan (Architecture & System Workflow)
    # -------------------------------------------------------------------------
    s6 = prs.slides[5]
    cp6 = get_content_placeholder(s6)
    if cp6:
        cp6.text_frame.text = ""

    # Left: Algorithm Box
    b_algo = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4))
    b_algo.fill.solid()
    b_algo.fill.fore_color.rgb = RGBColor(15, 23, 42) # dark slate
    b_algo.line.color.rgb = RGBColor(56, 189, 248)
    b_algo.line.width = Pt(1.5)
    
    tf_algo = b_algo.text_frame
    tf_algo.word_wrap = True
    tf_algo.margin_left = Inches(0.25)
    tf_algo.margin_right = Inches(0.25)
    tf_algo.margin_top = Inches(0.25)
    
    p = tf_algo.paragraphs[0]
    p.text = "ALGORITHM: END-TO-END THREAT MODELING & VALIDATION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(56, 189, 248)
    
    code_text = (
        "Input : ARXML System Spec, CAN DBC, C Code AST\n"
        "Output: TARA Risk Report, Verified Attack Paths, SecOC Defenses\n"
        "--------------------------------------------------\n"
        "1. Construct System Graph G(V, E):\n"
        "   - V = {ECUs, Sensors, Memory, Diagnostics}\n"
        "   - E = {CAN, Ethernet, SPI, Trust Boundaries}\n"
        "2. For each Component v in V:\n"
        "   - Query STRIDE-per-Element Deterministic Rules\n"
        "   - Scan AST for CWE Weaknesses (CWE-120, CWE-306)\n"
        "   - Assign Base Exploitability & ASIL Impact Scores\n"
        "3. NetworkX Graph Synthesis:\n"
        "   - Compute multi-hop attack paths from External Ingress\n"
        "   - Identify critical Pivot Nodes (e.g. Central Gateway)\n"
        "4. Automated Test Vector Synthesis:\n"
        "   - Generate targeted CAN frames & UDS payloads (ISO 14229)\n"
        "5. Execute Test in Virtual ECU Sandbox:\n"
        "   - If target ECU accepts frame -> CONFIRMED EXPLOIT\n"
        "   - If rejected / timed-out -> UNVERIFIED THREAT\n"
        "6. Verification of Mitigation:\n"
        "   - Apply AUTOSAR SecOC CMAC & Freshness counter -> Re-test\n"
        "   - Confirm frame rejection (0x7F 27 35 Access Denied)"
    )
    p2 = tf_algo.add_paragraph()
    p2.text = code_text
    p2.font.size = Pt(8.5)
    p2.font.name = "Consolas"
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(8)

    # Right: Full-Stack Tech Stack Architecture
    b_stack = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.4))
    b_stack.fill.solid()
    b_stack.fill.fore_color.rgb = RGBColor(248, 250, 252)
    b_stack.line.color.rgb = RGBColor(203, 213, 225)
    b_stack.line.width = Pt(1.5)
    
    tf_stack = b_stack.text_frame
    tf_stack.word_wrap = True
    tf_stack.margin_left = Inches(0.25)
    tf_stack.margin_right = Inches(0.25)
    tf_stack.margin_top = Inches(0.25)
    
    p = tf_stack.paragraphs[0]
    p.text = "FULL-STACK PRODUCTION IMPLEMENTATION"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = c_navy
    
    stack_layers = [
        ("Presentation Layer (Frontend)", "React 18 + Vite + TailwindCSS. Uses React Flow for interactive architecture & attack graph rendering, Lucide icons, and dynamic test console."),
        ("Backend Application Engine", "Python 3.11+ with FastAPI. High-performance async REST APIs, NetworkX graph modeling engine, and SQLite audit repository."),
        ("Security Analysis Core", "Tree-sitter & Clang AST parsers for C/C++ static inspection, combined with deterministic STRIDE/CWE rule tables."),
        ("Hardware Simulation Sandbox", "Pure virtual CAN emulation (python-can / socketcan) with UDS ISO 14229 diagnostic protocol test runner. Zero hardware dependencies."),
        ("Executive Reporting Engine", "Generates downloadable ISO/SAE 21434 & UNECE WP.29 security audit reports with cryptographic verification evidence.")
    ]
    for st_title, st_desc in stack_layers:
        p = tf_stack.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "• " + st_title + ": "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = c_blue
        r2 = p.add_run()
        r2.text = st_desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = c_slate

    # -------------------------------------------------------------------------
    # SLIDE 7: Implementation Plan (Roadmap & Technical Milestones)
    # -------------------------------------------------------------------------
    s7 = prs.slides[6]
    cp7 = get_content_placeholder(s7)
    if cp7:
        cp7.text_frame.text = ""

    # Implementation Roadmap Table / Cards
    stages = [
        ("Phase 1: Ingestion & Parser Core", "Status: 100% COMPLETE", c_emerald,
         ["AUTOSAR ARXML parser for SWC, Port, and PDU extraction.", "CAN DBC signal and message identifier parser.", "Tree-sitter embedded C/C++ AST analyzer for CWE detection."]),
        ("Phase 2: Hybrid STRIDE & TARA Engine", "Status: 100% COMPLETE", c_emerald,
         ["Deterministic STRIDE-per-element rule classification.", "ISO/SAE 21434 risk scoring matrix (Safety ASIL, Financial, Operational).", "NetworkX directed attack graph and lateral pivot traversal."]),
        ("Phase 3: Virtual CAN & UDS Test Sandbox", "Status: 100% COMPLETE", c_emerald,
         ["Isolated virtual CAN socket emulator without hardware requirements.", "Automated test generator for UDS Diagnostic (ISO 14229) & frame spoofing.", "Dynamic exploit verification & SecOC mitigation re-testing."]),
        ("Phase 4: Dashboard & Interactive Visualizer", "Status: 100% COMPLETE", c_emerald,
         ["React Flow architecture canvas with real-time node drilldowns.", "Live attack tree exploration with exploitability paths.", "Executive PDF / JSON compliance report generation for ISO 21434."]),
        ("Phase 5: Automotive Scenario & Jury Demo", "Status: READY FOR JURY", c_blue,
         ["Pre-loaded connected vehicle ECU scenario (TCU -> Gateway -> Braking).", "One-click end-to-end execution demonstrating threat-to-validation in 60s.", "Fully runnable local prototype for seamless presentation round demo."])
    ]

    for idx, (st_name, st_status, st_col, st_bullets) in enumerate(stages):
        y = Inches(1.35 + idx * 1.15)
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.05))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(248, 250, 252)
        box.line.color.rgb = st_col
        box.line.width = Pt(1.5)
        
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.1)
        
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = st_name
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_navy
        
        r2 = p.add_run()
        r2.text = f"   [{st_status}]"
        r2.font.bold = True
        r2.font.size = Pt(10)
        r2.font.color.rgb = st_col
        
        p2 = tf.add_paragraph()
        p2.space_before = Pt(3)
        p2.text = "   • " + "   • ".join(st_bullets)
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = c_slate

    # -------------------------------------------------------------------------
    # SLIDE 8: Validation / Testing / Analysis
    # -------------------------------------------------------------------------
    s8 = prs.slides[7]
    cp8 = get_content_placeholder(s8)
    if cp8:
        cp8.text_frame.text = ""

    # Embed attack_path_diagram & validation_workflow side-by-side or stacked
    val_img_path = r'c:\Users\mdbaa\OneDrive\Desktop\L&T\attack_path_diagram.png'
    if os.path.exists(val_img_path):
        s8.shapes.add_picture(val_img_path, Inches(0.8), Inches(1.35), width=Inches(11.7))

    # -------------------------------------------------------------------------
    # SLIDE 9: Cost Estimate
    # -------------------------------------------------------------------------
    s9 = prs.slides[8]
    cp9 = get_content_placeholder(s9)
    if cp9:
        cp9.text_frame.text = ""

    # Left: Traditional Manual Pen-Testing
    b_trad = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4))
    b_trad.fill.solid()
    b_trad.fill.fore_color.rgb = RGBColor(254, 242, 242)
    b_trad.line.color.rgb = RGBColor(239, 68, 68)
    b_trad.line.width = Pt(2)
    
    tf_trad = b_trad.text_frame
    tf_trad.word_wrap = True
    tf_trad.margin_left = Inches(0.3)
    tf_trad.margin_right = Inches(0.3)
    tf_trad.margin_top = Inches(0.3)
    
    p = tf_trad.paragraphs[0]
    p.text = "TRADITIONAL INDUSTRY SECURITY AUDITING"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = c_rose
    
    trad_points = [
        ("External TARA & Pentesting Firms: ", "$15,000 to $30,000 per individual ECU audit cycle."),
        ("Physical HIL Testbench Hardware: ", "$100,000+ capital investment per hardware test bench (dSPACE, Vector VT System)."),
        ("Development Turnaround Delay: ", "4 to 8 weeks latency per iteration; cannot run in continuous CI/CD pipelines."),
        ("Human Expertise Scarcity: ", "High dependency on rare automotive embedded cybersecurity specialists."),
        ("Annual Cost for 1 Vehicle Program: ", "> $450,000 annually across 15–30 safety-critical ECUs.")
    ]
    for tp_title, tp_desc in trad_points:
        p = tf_trad.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + tp_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = c_rose
        r2 = p.add_run()
        r2.text = tp_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_slate

    # Right: ThreatPath Solution
    b_threat = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4))
    b_threat.fill.solid()
    b_threat.fill.fore_color.rgb = RGBColor(240, 253, 244)
    b_threat.line.color.rgb = RGBColor(16, 185, 129)
    b_threat.line.width = Pt(2)
    
    tf_threat = b_threat.text_frame
    tf_threat.word_wrap = True
    tf_threat.margin_left = Inches(0.3)
    tf_threat.margin_right = Inches(0.3)
    tf_threat.margin_top = Inches(0.3)
    
    p = tf_threat.paragraphs[0]
    p.text = "THREATPATH SOLUTION COST & ROI"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = c_emerald
    
    threat_points = [
        ("Software Infrastructure: ", "Built on open-source foundation (React, FastAPI, NetworkX, Clang/Tree-sitter). Zero per-seat licensing fees."),
        ("Hardware Cost: ", "$0 Physical Hardware. Uses fully isolated virtual CAN (vcan) software emulation."),
        ("Compute Infrastructure: ", "Lightweight containerized deployment ($50/month cloud host or $0 on local workstations)."),
        ("Execution Turnaround Time: ", "Under 2 minutes per comprehensive architecture threat model and validation run."),
        ("Total Savings & ROI: ", "> 92% cost reduction in recurring cybersecurity engineering budgets, enabling daily Shift-Left verification.")
    ]
    for tp_title, tp_desc in threat_points:
        p = tf_threat.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + tp_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = c_emerald
        r2 = p.add_run()
        r2.text = tp_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_navy

    # -------------------------------------------------------------------------
    # SLIDE 10: Assumptions
    # -------------------------------------------------------------------------
    s10 = prs.slides[9]
    cp10 = get_content_placeholder(s10)
    if cp10:
        cp10.text_frame.text = ""

    b_assump = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    b_assump.fill.solid()
    b_assump.fill.fore_color.rgb = RGBColor(248, 250, 252)
    b_assump.line.color.rgb = RGBColor(203, 213, 225)
    b_assump.line.width = Pt(1.5)
    
    tf_as = b_assump.text_frame
    tf_as.word_wrap = True
    tf_as.margin_left = Inches(0.4)
    tf_as.margin_right = Inches(0.4)
    tf_as.margin_top = Inches(0.3)
    
    p = tf_as.paragraphs[0]
    p.text = "ENGINEERING ASSUMPTIONS & OPERATIONAL SCOPE"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    
    assumptions = [
        ("Automotive Communication Standards: ", "Target ECUs utilize standard automotive protocols including CAN 2.0B, CAN-FD, UDS (ISO 14229-1), and Automotive Ethernet (DoIP ISO 13400)."),
        ("Architecture Specification Format: ", "Input architectures are modeled following standardized AUTOSAR Classic/Adaptive specifications (ARXML) or structured topology descriptions."),
        ("Strictly Isolated & Ethical Simulation: ", "All automated dynamic tests execute strictly inside isolated virtual socket containers (vcan/socketcan). No live vehicle networks or unauthorized external systems are scanned."),
        ("Regulatory & Compliance Grounding: ", "Risk ratings and threat taxonomies are strictly grounded in ISO/SAE 21434 (Road Vehicles — Cybersecurity Engineering) and UNECE WP.29 R155/R156 standards."),
        ("Complementary Physical Verification: ", "ThreatPath is designed as a Shift-Left security validation tool that dramatically shortens development cycles; final physical environmental and side-channel audits remain complementary.")
    ]
    for a_title, a_desc in assumptions:
        p = tf_as.add_paragraph()
        p.space_before = Pt(14)
        r1 = p.add_run()
        r1.text = "1. " + a_title if assumptions.index((a_title, a_desc)) == 0 else f"{assumptions.index((a_title, a_desc))+1}. " + a_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_blue
        r2 = p.add_run()
        r2.text = a_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = c_slate

    # -------------------------------------------------------------------------
    # SLIDE 11: References
    # -------------------------------------------------------------------------
    s11 = prs.slides[10]
    cp11 = get_content_placeholder(s11)
    if cp11:
        cp11.text_frame.text = ""

    b_ref = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.4))
    b_ref.fill.solid()
    b_ref.fill.fore_color.rgb = RGBColor(248, 250, 252)
    b_ref.line.color.rgb = RGBColor(203, 213, 225)
    b_ref.line.width = Pt(1.5)
    
    tf_ref = b_ref.text_frame
    tf_ref.word_wrap = True
    tf_ref.margin_left = Inches(0.4)
    tf_ref.margin_right = Inches(0.4)
    tf_ref.margin_top = Inches(0.3)
    
    p = tf_ref.paragraphs[0]
    p.text = "KEY STANDARDS, REGULATIONS & ACADEMIC REFERENCES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    
    refs = [
        ("ISO/SAE 21434:2021: ", "Road vehicles — Cybersecurity engineering, International Organization for Standardization / SAE International."),
        ("UNECE WP.29 Regulation No. 155 & 156: ", "Cyber Security and Cyber Security Management Systems; Software Update and Software Update Management Systems, United Nations."),
        ("AUTOSAR Specification of Secure Onboard Communication (SecOC): ", "Classic Platform Release 4.4.0, AUTOSAR Development Partnership."),
        ("ISO 14229-1:2020: ", "Road vehicles — Unified diagnostic services (UDS) — Part 1: Application layer specification."),
        ("MITRE ATT&CK for Industrial Control Systems (ICS) & CWE-Hardware: ", "Common Weakness Enumeration for Embedded Design (CWE-120, CWE-306, CWE-345)."),
        ("Shostack, Adam: ", "Threat Modeling: Designing for Security. John Wiley & Sons, Indianapolis, IN, 2014."),
        ("Checkoway, S., et al.: ", "Comprehensive Experimental Analyses of Automotive Attack Surfaces. In USENIX Security Symposium, 2011.")
    ]
    for r_title, r_desc in refs:
        p = tf_ref.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"[{refs.index((r_title, r_desc))+1}] " + r_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = c_blue
        r2 = p.add_run()
        r2.text = r_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_slate

    # -------------------------------------------------------------------------
    # SLIDE 12: Thank You
    # -------------------------------------------------------------------------
    s12 = prs.slides[11]
    
    # Add a custom summary card on the left of Thank You
    b_ty = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))
    b_ty.fill.solid()
    b_ty.fill.fore_color.rgb = RGBColor(248, 250, 252)
    b_ty.line.color.rgb = RGBColor(2, 132, 199)
    b_ty.line.width = Pt(2)
    
    tf_ty = b_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = Inches(0.4)
    tf_ty.margin_right = Inches(0.4)
    tf_ty.margin_top = Inches(0.4)
    
    p = tf_ty.paragraphs[0]
    p.text = "ThreatPath: AI-Assisted Threat Modeling & Security Validation"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    
    p_sub = tf_ty.add_paragraph()
    p_sub.text = "PID No: TG0915208 | L&T TECHgium 10th Edition"
    p_sub.font.bold = True
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = c_blue
    p_sub.space_before = Pt(4)
    
    ty_items = [
        ("Team Members: ", "Mohammed H, Mohammed J, RAJALAKSHMI M"),
        ("Institution: ", "PSNA College of Engineering and Technology, Dindigul, Tamil Nadu"),
        ("Prototype Demonstration: ", "Full-Stack React + FastAPI application running live locally with virtual CAN ECU exploit simulation."),
        ("Ready for Jury Discussion: ", "Open for Q&A, technical architecture deep-dive, and live test demonstration.")
    ]
    for tit, val in ty_items:
        p = tf_ty.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = tit
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = c_darkblue
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_slate

    # Save presentation
    prs.save(dst_pptx)
    print(f"Successfully generated: {dst_pptx}")
    
    # Also save a copy in Downloads just in case
    downloads_dst = r'C:\Users\mdbaa\Downloads\15208_TG10_Presentation Round.pptx'
    prs.save(downloads_dst)
    print(f"Also saved copy to: {downloads_dst}")

if __name__ == '__main__':
    build_deck()
