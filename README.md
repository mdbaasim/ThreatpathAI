# ThreatPath: AI-Assisted Threat Modeling and Security Validation for Embedded Systems

**10th Edition L&T TECHgium® Competition — Presentation Round**  
- **PID:** `TG0915208`  
- **Team Members:** Mohammed H, Mohammed J, RAJALAKSHMI M  
- **Institution:** PSNA College of Engineering and Technology, Dindigul, Tamil Nadu  
- **Submission PPT Deck:** `15208_TG10_Presentation Round.pptx`

---

## 🚀 Quick Start: Launch the Prototype (1-Click)

To launch the full working application locally for your presentation or demo:

1. Double-click **`run_threatpath.bat`** (or pass a custom port like `run_threatpath.bat 3000`).
2. Your browser will automatically open: **`http://127.0.0.1:5000`**
3. On the top right of the dashboard, click the glowing cyan button: **`Run 60s Jury Walkthrough`**.
   - Watch the platform automatically demonstrate Architecture Ingestion $\rightarrow$ Threat Discovery $\rightarrow$ NetworkX Multi-Hop Attack Path $\rightarrow$ Dynamic CAN Frame Injection (Exploit Confirmed) $\rightarrow$ AUTOSAR SecOC Cryptographic Mitigation (Threat Mitigated)!

---

## 📋 PPT Slide-by-Slide Outline (`15208_TG10_Presentation Round.pptx`)

| Slide | Title | Key Talking Points (7-Min Pitch) |
|---|---|---|
| **1** | Title Slide | Introduce team, PID `TG0915208`, PSNA College of Engineering and Technology. State the mission: replacing manual spreadsheet threat modeling with automated, empirically validated embedded cybersecurity. |
| **2** | Challenge Statement | Modern SDVs have 100+ ECUs. ISO/SAE 21434 & UNECE WP.29 R155 mandate TARA. Current methods are manual, static (Excel/Microsoft TMT), lack multi-hop attack paths, and cost $15k–$30k per ECU with 4–8 weeks delay. |
| **3** | Concept / Proposed Solution | ThreatPath: Multi-modal ingestion (AUTOSAR ARXML, C code AST) $\rightarrow$ Hybrid Deterministic/LLM Reasoning $\rightarrow$ NetworkX Graph Engine $\rightarrow$ Isolated Virtual CAN Hardware Sandbox. |
| **4** | Pros and Cons Benchmark | 100x speedup (<2 min vs 6 weeks). Closed-loop empirical validation via virtual CAN socket replay instead of subjective guesses. Shift-left verification in CI/CD. |
| **5** | Technical Description | Deep-dive into the 4 architectural pillars: ARXML/Clang Ingestion, STRIDE-per-Element Rule Matrix, NetworkX Dijkstra Attack Trees, and SocketCAN / UDS (ISO 14229) Test Sandbox. |
| **6** | Implementation Plan (Algorithm & Stack) | Mathematical formulation: Graph $G(V, E)$, minimum-cost path traversal, test vector synthesis. Full-stack implementation: React 18, FastAPI, NetworkX, python-can. |
| **7** | Implementation Plan (Roadmap) | Phases 1 through 4 are 100% complete and integrated. Phase 5 pre-loaded scenario ready for live jury demo. |
| **8** | Validation / Testing / Analysis | Concrete automotive scenario: TCU (Cellular) $\rightarrow$ Gateway $\rightarrow$ Safety Braking ECU. CAN ID `0x020` injection confirmed $\rightarrow$ AUTOSAR SecOC CMAC enforced $\rightarrow$ Verified Mitigated in 42 seconds! |
| **9** | Cost Estimate & Feasibility | Traditional HIL testbenches and pen-testing firms cost >$450,000 annually per vehicle program. ThreatPath requires $0 hardware via virtualization, delivering a >92% cost reduction. |
| **10** | Assumptions | Protocol adherence (CAN 2.0B, CAN-FD, UDS ISO 14229), AUTOSAR Classic/Adaptive specs, and strict sandboxed execution with zero transmission to real vehicles. |
| **11** | References | ISO/SAE 21434:2021, UNECE WP.29 R155/R156, AUTOSAR SecOC R4.4, ISO 14229-1:2020, MITRE ATT&CK for ICS. |
| **12** | Thank You & Live Demo | Transition cleanly to live demo and invite jury questions. |

---

## 🎯 5-Minute Jury Q&A Defense Strategy

### Q1: "How is ThreatPath different from Microsoft Threat Modeling Tool (TMT)?"
> **Answer:** Microsoft TMT is a generic, static Data Flow Diagram (DFD) drawing tool designed for web and IT software. It has zero knowledge of automotive protocols (CAN, UDS, AUTOSAR SecOC) and **cannot dynamically test or validate threats**. ThreatPath is built specifically for embedded systems: it ingests native AUTOSAR ARXML and C firmware, computes multi-hop attack paths using graph algorithms, and executes live exploit frames in an isolated virtual CAN bus to empirically prove whether the threat is real.

### Q2: "Can this cause damage to physical vehicle hardware or safety systems?"
> **Answer:** No. ThreatPath is architected with a strict isolation barrier. All dynamic test executions occur inside software-virtualized sockets (`vcan` / socket containers). No frames are ever transmitted to physical CAN buses or live vehicles. It serves as a Shift-Left validation engine used during firmware and architecture design stages before physical hardware is fabricated.

### Q3: "How does the AI reasoning avoid hallucinations when scoring risks?"
> **Answer:** We employ a **Hybrid Deterministic Architecture**. Threat classification, STRIDE rules, CWE mappings, and ISO/SAE 21434 scoring matrices are enforced deterministically using strict mathematical rules and standards. The LLM is strictly used for contextual synthesis, architecture explanation, and generating tailored remediation advice—it is never permitted to invent or modify deterministic risk ratings.

### Q4: "What automotive standards does ThreatPath align with?"
> **Answer:** ThreatPath aligns natively with:
> 1. **ISO/SAE 21434:2021** (Clause 9: Threat Analysis and Risk Assessment - TARA).
> 2. **UNECE WP.29 Regulation 155** (Cybersecurity Management System verification).
> 3. **AUTOSAR Specification of Secure Onboard Communication (SecOC)** for MAC/Freshness counter defenses.
> 4. **ISO 14229-1 (UDS)** for diagnostic security validation.
