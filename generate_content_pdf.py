import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def generate_pdf():
    pdf_path = r"c:\Users\mdbaa\OneDrive\Desktop\L&T\ThreatPath_TECHgium_Presentation_Content_TG0915208.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_blue = colors.HexColor("#0f172a") # Dark Slate
    accent_blue = colors.HexColor("#0284c7")  # Tech Blue
    accent_teal = colors.HexColor("#0f766e")  # Teal
    text_dark = colors.HexColor("#1e293b")
    text_muted = colors.HexColor("#475569")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_blue,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_blue,
        spaceAfter=10
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_muted
    )

    slide_header_style = ParagraphStyle(
        'SlideHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.white
    )

    subhead_style = ParagraphStyle(
        'SubHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=accent_blue,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=text_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title & Metadata Header Banner
    header_data = [
        [
            Paragraph("<b>L&T TECHgium® 10th Edition — Presentation Round Content Dossier</b>", title_style),
        ],
        [
            Paragraph("<b>Concept: ThreatPath — AI-Assisted Threat Modeling & Security Validation for Embedded Systems</b>", subtitle_style),
        ],
        [
            Paragraph("<b>PID:</b> TG0915208 &nbsp;|&nbsp; <b>Authors:</b> Mohammed H, Mohammed J, RAJALAKSHMI M<br/><b>Institution:</b> PSNA College of Engineering and Technology, Dindigul, Tamil Nadu", meta_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, accent_blue),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    def make_slide_card(slide_num, title, content_flowables):
        header = Table([[Paragraph(f"<b>SLIDE {slide_num}: {title.upper()}</b>", slide_header_style)]], colWidths=[540])
        header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), primary_blue),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        
        body_table = Table([[content_flowables]], colWidths=[540])
        body_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_light),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return [header, body_table, Spacer(1, 10)]

    # -------------------------------------------------------------
    # SLIDE 1
    # -------------------------------------------------------------
    s1_content = [
        Paragraph("<b>Concept Title:</b> ThreatPath: AI-Assisted Threat Modeling and Security Validation for Embedded Systems", body_style),
        Paragraph("<b>PID Number:</b> TG0915208 &nbsp;(Rename PPT as: <i>15208_TG10_Presentation Round.pptx</i>)", body_style),
        Paragraph("<b>Team Members:</b> 1. Mohammed H &nbsp;|&nbsp; 2. Mohammed J &nbsp;|&nbsp; 3. RAJALAKSHMI M", body_style),
        Paragraph("<b>College Name, City, State:</b> PSNA College of Engineering and Technology, Dindigul, Tamil Nadu", body_style),
        Paragraph("<b>Challenge Statement / Domain:</b> Embedded Systems Cybersecurity / Software-Defined Vehicle Security", body_style),
        Paragraph("<i>Note: Paste passport-size photographs of the 3 team members into the author placeholders on Slide 1.</i>", meta_style)
    ]
    story.extend(make_slide_card(1, "Title Slide Details", s1_content))

    # -------------------------------------------------------------
    # SLIDE 2
    # -------------------------------------------------------------
    s2_content = [
        Paragraph("<b>Industry Context & Regulatory Mandate:</b>", subhead_style),
        Paragraph("• Modern connected vehicles integrate 80–120 ECUs across CAN, CAN-FD, LIN, Automotive Ethernet, and 4G/OTA.", bullet_style),
        Paragraph("• Stringent international regulations (<b>ISO/SAE 21434</b> & <b>UNECE WP.29 R155/R156</b>) legally mandate verifiable Threat Analysis and Risk Assessment (TARA) throughout the engineering lifecycle.", bullet_style),
        Paragraph("• Over 80% of OEMs and Tier-1 suppliers still execute TARA manually via spreadsheets (Excel) and Microsoft Threat Modeling Tool (TMT).", bullet_style),
        
        Paragraph("<b>The Core Challenge & Industry Gaps:</b>", subhead_style),
        Paragraph("• <b>Component-Isolation Flaw:</b> Existing tools evaluate components in isolation, missing multi-hop lateral attack paths (e.g. TCU cellular socket &rarr; Central Gateway &rarr; Braking Controller).", bullet_style),
        Paragraph("• <b>Zero Dynamic Verification:</b> Current threat models are purely theoretical 'shelf-ware'—they cannot empirically test or confirm whether a vulnerability is practically exploitable in code or bus protocols.", bullet_style),
        Paragraph("• <b>Prohibitive Cost & Time:</b> Physical Hardware-in-the-Loop (HIL) penetration testing costs $15k–$30k per ECU and requires 4–8 weeks per validation cycle.", bullet_style),
        Paragraph("• <b>Project Objective:</b> Build ThreatPath: an automated framework that ingests embedded architecture (AUTOSAR/C code), synthesizes attack trees, and executes closed-loop validation in an isolated virtual simulation environment without physical hardware.", bullet_style)
    ]
    story.extend(make_slide_card(2, "Challenge Statement", s2_content))

    # -------------------------------------------------------------
    # SLIDE 3
    # -------------------------------------------------------------
    s3_content = [
        Paragraph("<b>Concept Summary:</b> A closed-loop cybersecurity validation pipeline for automotive embedded systems.", subhead_style),
        Paragraph("• <b>1. Multi-Modal Ingestion:</b> Deserializes AUTOSAR Classic/Adaptive ARXML (Software Components, Ports, PDUs), CAN DBC signal matrices, and embedded C source code ASTs.", bullet_style),
        Paragraph("• <b>2. Deterministic Rule Matching:</b> Applies STRIDE-per-element rules mapped directly to automotive Common Weakness Enumeration standards (CWE-306, CWE-120, CWE-345) and ISO 21434 impact parameters.", bullet_style),
        Paragraph("• <b>3. Graph-Theoretic Attack Paths:</b> Uses <b>NetworkX</b> to construct a directed multigraph G(V, E) of the vehicle network, computing Dijkstra shortest exploit paths from untrusted ingress to safety actuators.", bullet_style),
        Paragraph("• <b>4. Isolated Virtual Hardware Sandbox:</b> Automatically generates and injects targeted CAN frames and UDS (ISO 14229) test payloads into a virtual CAN socket (vcan0) to confirm vulnerabilities without hardware risk.", bullet_style),
        Paragraph("• <b>5. Cryptographic Mitigation Verification:</b> Enforces AUTOSAR SecOC (AES-128 CMAC + Freshness Counter) and re-executes tests to verify threat mitigation in real time.", bullet_style)
    ]
    story.extend(make_slide_card(3, "Concept / Proposed Solution", s3_content))

    # -------------------------------------------------------------
    # SLIDE 4
    # -------------------------------------------------------------
    table_data = [
        [
            Paragraph("<b>Parameter</b>", meta_style),
            Paragraph("<b>Manual TARA (Excel)</b>", meta_style),
            Paragraph("<b>Microsoft TMT / SAST</b>", meta_style),
            Paragraph("<b>ThreatPath (Our Solution)</b>", meta_style)
        ],
        [
            Paragraph("<b>Architecture Ingestion</b>", body_style),
            Paragraph("Manual entry (slow, error-prone)", body_style),
            Paragraph("Generic DFD drawing blocks", body_style),
            Paragraph("<b>AUTOSAR ARXML, C AST, DBC</b>", body_style)
        ],
        [
            Paragraph("<b>Domain Scope</b>", body_style),
            Paragraph("Subjective checklists", body_style),
            Paragraph("Generic enterprise / web IT", body_style),
            Paragraph("<b>CAN, UDS, AUTOSAR SecOC, ISO 21434</b>", body_style)
        ],
        [
            Paragraph("<b>Multi-Hop Attack Paths</b>", body_style),
            Paragraph("Not supported (isolated audits)", body_style),
            Paragraph("Component-level only", body_style),
            Paragraph("<b>NetworkX graph traversal & pivots</b>", body_style)
        ],
        [
            Paragraph("<b>Dynamic Validation</b>", body_style),
            Paragraph("None (Static documentation)", body_style),
            Paragraph("None (Requires separate pen-test)", body_style),
            Paragraph("<b>Automated virtual CAN packet replay</b>", body_style)
        ],
        [
            Paragraph("<b>Turnaround Time</b>", body_style),
            Paragraph("4 to 8 weeks per ECU", body_style),
            Paragraph("1 to 2 weeks", body_style),
            Paragraph("<b>Under 2 minutes (Automated)</b>", body_style)
        ],
        [
            Paragraph("<b>Hardware Dependency</b>", body_style),
            Paragraph("Physical HIL test rig needed", body_style),
            Paragraph("None (static only)", body_style),
            Paragraph("<b>$0 (100% Virtualized Sockets)</b>", body_style)
        ]
    ]
    comp_table = Table(table_data, colWidths=[110, 130, 130, 150])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor("#f0fdf4")),
    ]))

    s4_content = [
        Paragraph("<b>Competitive Benchmarking:</b>", subhead_style),
        comp_table,
        Paragraph("<b>Engineering Pros:</b> 100x faster execution; empirical closed-loop proof; native ISO 21434 compliance; shift-left testing.", body_style),
        Paragraph("<b>Trade-off & Workaround:</b> Pure software simulation cannot detect physical analog bus degradation; ThreatPath focuses on protocol, memory, and routing logic as the automated gate prior to final physical sign-off.", body_style)
    ]
    story.extend(make_slide_card(4, "Pros and Cons of the Solution", s4_content))

    # Page break for clean reading
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 5
    # -------------------------------------------------------------
    s5_content = [
        Paragraph("<b>Pillar 1: Architecture Ingestion & AST Scanner</b>", subhead_style),
        Paragraph("• Parses AUTOSAR Classic & Adaptive ARXML: extracts Software Components (SWCs), Client-Server & Sender-Receiver ports, and PDU descriptors.", bullet_style),
        Paragraph("• Scans C/C++ embedded firmware AST (Tree-sitter/Clang) for buffer overflows (CWE-120), format strings, and unauthenticated diagnostic handlers.", bullet_style),
        
        Paragraph("<b>Pillar 2: Hybrid Deterministic Threat Engine</b>", subhead_style),
        Paragraph("• Evaluates every communication interface across the STRIDE matrix: Spoofing (CAN ID injection), Tampering (OTA updates), Elevation of Privilege (UDS 0x27).", bullet_style),
        Paragraph("• TARA Risk Formulation: Computes Risk R = Impact (Safety ASIL-A to D, Financial, Operational) &times; Attack Feasibility (Time, Expertise, Window).", bullet_style),

        Paragraph("<b>Pillar 3: NetworkX Attack Graph Synthesis</b>", subhead_style),
        Paragraph("• Models vehicle as directed multigraph G(V, E); V = {ECUs, Ports, Memories}, E = {CAN-FD, LIN, Ethernet, Internal SPI}.", bullet_style),
        Paragraph("• Edge Weight W = f(Encryption, Authentication, Gateway Filtering). Dijkstra algorithm discovers weakest path to ASIL-D nodes.", bullet_style),

        Paragraph("<b>Pillar 4: Virtual CAN & UDS Simulation Sandbox</b>", subhead_style),
        Paragraph("• Isolated virtual CAN socket (vcan0) emulator with zero physical hardware risk.", bullet_style),
        Paragraph("• Replays UDS (ISO 14229) diagnostic sessions (0x10, 0x27, 0x34) and evaluates ECU status responses in real time.", bullet_style)
    ]
    story.extend(make_slide_card(5, "Technical Description", s5_content))

    # -------------------------------------------------------------
    # SLIDE 6
    # -------------------------------------------------------------
    s6_algo = [
        Paragraph("<b>Algorithm 1: Automated Threat Modeling & Dynamic Validation Pipeline</b>", subhead_style),
        Paragraph("1. INGESTION: Parse ARXML, DBC, and C source code &rarr; Construct System Graph G(V, E).", code_style),
        Paragraph("2. STRIDE MAPPING: For each node v &isin; V, match deterministic CWE rules & assign ASIL Impact.", code_style),
        Paragraph("3. GRAPH TRAVERSAL: NetworkX Dijkstra computes shortest attack paths from external ingress to safety nodes.", code_style),
        Paragraph("4. TEST SYNTHESIS: Generate CAN Frame ID = 0x020, DLC = 8, Payload = [80 00 00 FF 00 00 00 00].", code_style),
        Paragraph("5. SANDBOX EXECUTION: Inject packet into virtual CAN bus &rarr; Target ECU actuates &rarr; CONFIRMED EXPLOIT.", code_style),
        Paragraph("6. DEFENSE VERIFICATION: Enforce AUTOSAR SecOC (AES-128 CMAC) &rarr; Re-inject &rarr; Target rejects frame &rarr; MITIGATED.", code_style),
        Paragraph("7. COMPLIANCE AUDIT: Emit ISO/SAE 21434 and UNECE WP.29 security assessment report.", code_style),
        Spacer(1, 4),
        Paragraph("<b>Full-Stack Architecture:</b>", subhead_style),
        Paragraph("• <b>Frontend:</b> Modern React 18, Tailwind CSS, React Flow visualizer, Lucide Icons, Vite.", bullet_style),
        Paragraph("• <b>Backend:</b> Python 3.11+, FastAPI (REST API), NetworkX graph traversal engine, SQLite.", bullet_style),
        Paragraph("• <b>Simulation Layer:</b> Pure virtual SocketCAN emulation with ISO 14229 UDS state machine.", bullet_style)
    ]
    story.extend(make_slide_card(6, "Implementation Plan — System Workflow & Algorithm", s6_algo))

    # -------------------------------------------------------------
    # SLIDE 7
    # -------------------------------------------------------------
    s7_content = [
        Paragraph("<b>Development Modules & Verification Roadmap:</b>", subhead_style),
        Paragraph("• <b>Module 1: Ingestion & Parser Core (100% Complete)</b> &mdash; ARXML SWC/PDU parser, CAN DBC signal extractor, and embedded C AST scanner.", bullet_style),
        Paragraph("• <b>Module 2: STRIDE & TARA Rule Matrix (100% Complete)</b> &mdash; Deterministic CWE classifications, ISO 21434 impact parameters, and risk scoring.", bullet_style),
        Paragraph("• <b>Module 3: Attack Graph Synthesis (100% Complete)</b> &mdash; NetworkX shortest-path calculation, lateral pivot detection, and topology mapping.", bullet_style),
        Paragraph("• <b>Module 4: Virtual Hardware Test Sandbox (100% Complete)</b> &mdash; Virtual CAN socket replayer, UDS diagnostic session state machine, and SecOC verifier.", bullet_style),
        Paragraph("• <b>Module 5: Interactive Web UI & Reporting (100% Complete)</b> &mdash; Live packet monitor, interactive graph canvas, and downloadable audit report.", bullet_style),
        Paragraph("• <b>Jury Demonstration (Ready):</b> Pre-loaded connected automotive ECU scenario (Telematics &rarr; Gateway &rarr; Braking ECU) executable in 60 seconds.", bullet_style)
    ]
    story.extend(make_slide_card(7, "Implementation Plan — Modules & Roadmap", s7_content))

    # -------------------------------------------------------------
    # SLIDE 8
    # -------------------------------------------------------------
    s8_content = [
        Paragraph("<b>Demonstrated Automotive Attack Scenario:</b>", subhead_style),
        Paragraph("• <b>Topology:</b> Telematics Unit (TCU, 4G LTE) &rarr; Central Gateway &rarr; Safety Braking ECU (ASIL-D).", bullet_style),
        Paragraph("• <b>Test Case 1 (Remote Ingress):</b> Injected UDS Service 0x34 (RequestDownload) on UDP 13400 without mTLS &rarr; TCU responded 0x74 (Positive ACK) &rarr; <b>CONFIRMED EXPLOIT (CWE-306).</b>", bullet_style),
        Paragraph("• <b>Test Case 2 (Gateway Lateral Pivot):</b> Unfiltered routing between Ethernet and Chassis CAN &rarr; Packet forwarded without SecOC token &rarr; <b>CONFIRMED EXPLOIT (CWE-284).</b>", bullet_style),
        Paragraph("• <b>Test Case 3 (Brake Command Injection):</b> Injected forged CAN frame ID 0x020 (Deceleration Override) &rarr; Braking controller actuated hydraulic solenoid (120 bar) &rarr; <b>CONFIRMED EXPLOIT (CWE-345, CVSS 9.9 Critical).</b>", bullet_style),
        Paragraph("• <b>Mitigation Re-Validation:</b> Applied AUTOSAR SecOC (AES-128 CMAC + Freshness Counter) &rarr; Replayed attack packet &rarr; Target ECU dropped packet with error 0x7F 27 35 &rarr; <b>VERIFIED MITIGATED in 42 seconds!</b>", bullet_style)
    ]
    story.extend(make_slide_card(8, "Validation / Testing / Analysis", s8_content))

    # Page break for final section
    story.append(PageBreak())

    # -------------------------------------------------------------
    # SLIDE 9
    # -------------------------------------------------------------
    s9_content = [
        Paragraph("<b>Commercial Industry Costs (Traditional Approach):</b>", subhead_style),
        Paragraph("• External Automotive Cybersecurity Firm: <b>$15,000 to $30,000</b> per individual ECU audit.", bullet_style),
        Paragraph("• Physical Hardware-in-the-Loop (HIL) Testbenches: <b>$100,000+</b> capital expenditure per setup.", bullet_style),
        Paragraph("• Annual Program Cost across 20 Vehicle ECUs: <b>$300,000 to $600,000</b> annually.", bullet_style),
        Paragraph("• Development Turnaround Latency: <b>4 to 8 weeks</b> delay per firmware release cycle.", bullet_style),
        Spacer(1, 4),
        Paragraph("<b>ThreatPath Solution Economics:</b>", subhead_style),
        Paragraph("• Software Licensing: <b>$0</b> (Built on open-source stack: React, FastAPI, NetworkX, Python).", bullet_style),
        Paragraph("• Hardware Infrastructure: <b>$0</b> (Runs in virtual memory sockets on standard developer workstations).", bullet_style),
        Paragraph("• Cloud Container Hosting (Optional): ~$30 to $50 / month for enterprise multi-user deployment.", bullet_style),
        Paragraph("• <b>ROI & Impact:</b> <b>&gt;90% cost reduction</b> in recurring security testing; shortens validation cycle from weeks to under 2 minutes.", bullet_style)
    ]
    story.extend(make_slide_card(9, "Cost Estimate & Financial Feasibility", s9_content))

    # -------------------------------------------------------------
    # SLIDE 10
    # -------------------------------------------------------------
    s10_content = [
        Paragraph("<b>Key Engineering Assumptions & Scope:</b>", subhead_style),
        Paragraph("1. <b>Communication Standards:</b> Target systems adhere to standard automotive protocols (CAN 2.0B, CAN-FD, UDS ISO 14229, DoIP ISO 13400).", bullet_style),
        Paragraph("2. <b>Architecture Models:</b> Input specifications are provided in standard AUTOSAR ARXML or structured network topology schemas.", bullet_style),
        Paragraph("3. <b>Strictly Isolated Testing:</b> All dynamic tests execute inside safe, isolated virtual CAN memory sockets (vcan0). <b>Zero packets are transmitted to live vehicles or external networks.</b>", bullet_style),
        Paragraph("4. <b>Regulatory Compliance:</b> Threat modeling taxonomies and risk scoring are strictly grounded in <b>ISO/SAE 21434:2021</b> and <b>UNECE WP.29 R155/R156</b>.", bullet_style),
        Paragraph("5. <b>Shift-Left Development:</b> ThreatPath acts as an automated software validation tool during early design; physical environmental audits remain complementary final steps.", bullet_style)
    ]
    story.extend(make_slide_card(10, "Assumptions & Operational Constraints", s10_content))

    # -------------------------------------------------------------
    # SLIDE 11
    # -------------------------------------------------------------
    s11_content = [
        Paragraph("<b>Formal Industry & Academic References:</b>", subhead_style),
        Paragraph("1. <b>ISO/SAE 21434:2021:</b> <i>Road vehicles &mdash; Cybersecurity engineering</i>, International Organization for Standardization / SAE International.", bullet_style),
        Paragraph("2. <b>UNECE WP.29 Regulation No. 155:</b> <i>Uniform provisions concerning the approval of vehicles with regards to cyber security and CSMS</i>, United Nations.", bullet_style),
        Paragraph("3. <b>AUTOSAR Specification of Secure Onboard Communication (SecOC):</b> <i>Classic Platform Release 4.4.0</i>, AUTOSAR Development Partnership.", bullet_style),
        Paragraph("4. <b>ISO 14229-1:2020:</b> <i>Road vehicles &mdash; Unified diagnostic services (UDS) &mdash; Part 1: Application layer specification</i>.", bullet_style),
        Paragraph("5. <b>MITRE CWE:</b> <i>Common Weakness Enumeration for Hardware & Embedded Design Weaknesses</i> (CWE-120, CWE-284, CWE-306, CWE-345).", bullet_style),
        Paragraph("6. <b>Shostack, Adam:</b> <i>Threat Modeling: Designing for Security</i>, John Wiley & Sons, 2014.", bullet_style)
    ]
    story.extend(make_slide_card(11, "References & Standards", s11_content))

    # -------------------------------------------------------------
    # SLIDE 12
    # -------------------------------------------------------------
    s12_content = [
        Paragraph("<b>ThreatPath: AI-Assisted Threat Modeling and Security Validation for Embedded Systems</b>", subhead_style),
        Paragraph("<b>PID Number:</b> TG0915208 &nbsp;|&nbsp; 10th Edition L&T TECHgium Presentation Round", body_style),
        Paragraph("<b>Team Members:</b> Mohammed H &nbsp;|&nbsp; Mohammed J &nbsp;|&nbsp; RAJALAKSHMI M", body_style),
        Paragraph("<b>Institution:</b> PSNA College of Engineering and Technology, Dindigul, Tamil Nadu", body_style),
        Paragraph("<b>Live Prototype:</b> Ready for live demonstration (Full-stack React + FastAPI + Virtual CAN Simulator).", body_style),
        Paragraph("<i>Thank you to the L&T TECHgium Jury. We are open for Technical Q&A and Prototype Walkthrough.</i>", subhead_style)
    ]
    story.extend(make_slide_card(12, "Thank You Slide Details", s12_content))

    # Build the document
    doc.build(story)
    print(f"[OK] Generated PDF: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
