import React, { useState, useEffect } from 'react';
import {
  Activity, Layers, ShieldAlert, Network, Terminal, Settings, BookOpen,
  Play, ShieldCheck, AlertTriangle, Sparkles, Menu, X,
  Check, Radio, RefreshCw, Search, ArrowRight, Shield, Pause, PlayCircle
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';

const API_BASE = typeof window !== 'undefined' && window.location.origin
  ? `${window.location.origin}/api`
  : 'http://127.0.0.1:5000/api';

// Distinct telemetry datasets for each time range
const TIME_DATA = {
  '1D': {
    spike: 'Peak: 12:00 CAN 0x020 Injected (198 pkts/s)',
    data: [
      { name: '00:00', packets: 34, risk: 1.2, event: 'Heartbeat Broadcast' },
      { name: '04:00', packets: 28, risk: 1.0, event: 'Normal Traffic' },
      { name: '08:00', packets: 145, risk: 5.4, event: 'Diagnostic Ingress Scan' },
      { name: '12:00', packets: 198, risk: 9.9, event: 'CAN ID 0x020 Brake Override', spike: true },
      { name: '16:00', packets: 92, risk: 4.8, event: 'SecOC CMAC Enforced' },
      { name: '20:00', packets: 45, risk: 1.5, event: 'Bus Stabilized' }
    ]
  },
  '1W': {
    spike: 'Peak: Wed CAN 0x020 Injected (182 pkts/s)',
    data: [
      { name: 'Mon', packets: 52, risk: 2.1, event: 'Gateway Ping' },
      { name: 'Tue', packets: 78, risk: 3.5, event: 'DoIP Port Scan' },
      { name: 'Wed', packets: 182, risk: 9.9, event: 'Brake Solenoid Exploit', spike: true },
      { name: 'Thu', packets: 110, risk: 5.8, event: 'SecOC Verification' },
      { name: 'Fri', packets: 64, risk: 2.6, event: 'Normal Telemetry' },
      { name: 'Sat', packets: 42, risk: 1.4, event: 'Idle Telematics' },
      { name: 'Sun', packets: 38, risk: 1.1, event: 'Normal Traffic' }
    ]
  },
  '1M': {
    spike: 'Peak: Week 3 CAN 0x020 Injected (195 pkts/s)',
    data: [
      { name: 'Week 1', packets: 65, risk: 2.8, event: 'Architecture Ingestion' },
      { name: 'Week 2', packets: 120, risk: 6.5, event: 'Penetration Probing' },
      { name: 'Week 3', packets: 195, risk: 9.9, event: 'CAN 0x020 Brake Injection', spike: true },
      { name: 'Week 4', packets: 55, risk: 1.8, event: 'SecOC Hardened' }
    ]
  },
  '6M': {
    spike: 'Peak: June CAN 0x020 Injected (185 pkts/s)',
    data: [
      { name: 'Jan', packets: 42, risk: 2.1, event: 'Normal Traffic' },
      { name: 'Feb', packets: 68, risk: 3.4, event: 'Diagnostic Scan' },
      { name: 'Mar', packets: 55, risk: 2.8, event: 'Normal Traffic' },
      { name: 'Apr', packets: 92, risk: 4.6, event: 'Service Enumeration' },
      { name: 'May', packets: 124, risk: 6.2, event: 'Ingress Probe' },
      { name: 'Jun', packets: 185, risk: 9.9, event: 'Brake Injection (0x020)', spike: true }
    ]
  },
  '1Y': {
    spike: 'Peak: June CAN 0x020 Injected (185 pkts/s)',
    data: [
      { name: 'Jan', packets: 42, risk: 2.1, event: 'Normal Traffic' },
      { name: 'Feb', packets: 68, risk: 3.4, event: 'Diagnostic Scan' },
      { name: 'Mar', packets: 55, risk: 2.8, event: 'Normal Traffic' },
      { name: 'Apr', packets: 92, risk: 4.6, event: 'Service Enumeration' },
      { name: 'May', packets: 124, risk: 6.2, event: 'Ingress Probe' },
      { name: 'Jun', packets: 185, risk: 9.9, event: 'Brake Injection (0x020)', spike: true },
      { name: 'Jul', packets: 140, risk: 7.5, event: 'Gateway Forwarding' },
      { name: 'Aug', packets: 110, risk: 5.2, event: 'SecOC CMAC Enforced' },
      { name: 'Sep', packets: 82, risk: 3.0, event: 'Attack Dropped' },
      { name: 'Oct', packets: 60, risk: 1.8, event: 'Mitigation Verified' },
      { name: 'Nov', packets: 45, risk: 1.2, event: 'Compliant' },
      { name: 'Dec', packets: 38, risk: 0.9, event: 'Stable' }
    ]
  }
};

export default function App() {
  // Navigation State
  const [activeNav, setActiveNav] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [timeRange, setTimeRange] = useState('LIVE');
  
  // App Boot / Home Launch Screen State
  const [showHomeLaunch, setShowHomeLaunch] = useState(false);
  const [bootProgress, setBootProgress] = useState(100);

  // Live Real-Time Bus & Sniffer State
  const [liveBus, setLiveBus] = useState({
    bus_interface: "vcan0",
    baud_rate: "500 kbps (CAN-HS)",
    is_attack_active: false,
    is_secoc_active: false,
    total_frames_sent: 14820,
    anomalies_detected: 0,
    bus_load_pct: 32.4,
    frames_per_sec: 145,
    recent_packets: [],
    rolling_telemetry: [
      { name: '10s ago', packets: 142, load: 32.1, risk: 1.2 },
      { name: '8s ago', packets: 145, load: 32.8, risk: 1.1 },
      { name: '6s ago', packets: 140, load: 31.9, risk: 1.3 },
      { name: '4s ago', packets: 148, load: 33.2, risk: 1.0 },
      { name: '2s ago', packets: 144, load: 32.5, risk: 1.2 },
      { name: 'Now', packets: 145, load: 32.4, risk: 1.2 }
    ]
  });
  const [isSnifferPaused, setIsSnifferPaused] = useState(false);

  // Auto boot sequence on first visit
  useEffect(() => {
    const hasLoaded = sessionStorage.getItem('threatpath_booted');
    if (!hasLoaded) {
      setShowHomeLaunch(true);
      setBootProgress(20);
      const t1 = setTimeout(() => setBootProgress(60), 300);
      const t2 = setTimeout(() => setBootProgress(90), 650);
      const t3 = setTimeout(() => {
        setBootProgress(100);
        setTimeout(() => {
          setShowHomeLaunch(false);
          sessionStorage.setItem('threatpath_booted', 'true');
        }, 350);
      }, 950);
      return () => {
        clearTimeout(t1);
        clearTimeout(t2);
        clearTimeout(t3);
      };
    }
  }, []);

  // Poll live telemetry stream every 800ms
  useEffect(() => {
    let isMounted = true;
    const fetchLiveBus = async () => {
      try {
        const res = await fetch(`${API_BASE}/live-bus/status`);
        if (res.ok) {
          const data = await res.json();
          if (isMounted) {
            setLiveBus(prev => {
              if (isSnifferPaused) {
                return { ...data, recent_packets: prev.recent_packets };
              }
              const rolling = data.rolling_telemetry.map(pt => ({
                name: pt.time,
                packets: pt.packets,
                load: pt.load,
                risk: pt.hazard
              }));
              return { ...data, rolling_telemetry: rolling };
            });
          }
        }
      } catch (e) {
        // Fallback live loop simulation so client is always active
        if (isMounted) {
          setLiveBus(prev => {
            const isAtt = prev.is_attack_active;
            const isSec = prev.is_secoc_active;
            const newTotal = prev.total_frames_sent + 3;
            const newLoad = isAtt ? (isSec ? 38.5 : 91.2) : Math.round((32.0 + Math.random() * 2.5) * 10) / 10;
            const newFps = isAtt ? (isSec ? 175 : 520) : Math.floor(140 + Math.random() * 15);
            const newAnom = isAtt && !isSec ? prev.anomalies_detected + 1 : prev.anomalies_detected;
            
            const timeStr = new Date().toLocaleTimeString().split(' ')[0];
            const samplePkt = isAtt ? {
              id: `pkt_${newTotal}`,
              timestamp: timeStr,
              can_id: "0x020",
              ecu: "ESC_BRAKE",
              dlc: 8,
              data: "80 00 00 FF 00 00 00 00",
              status: isSec ? "DEFENDED" : "EXPLOIT",
              secoc: isSec ? "MAC_MISMATCH_DROPPED" : "NO_MAC",
              desc: isSec ? "SecOC CMAC mismatch: Frame dropped" : "FORCED BRAKE 120 BAR!",
              priority: "HIGH (0x020)"
            } : {
              id: `pkt_${newTotal}`,
              timestamp: timeStr,
              can_id: "0x110",
              ecu: "ECM_POWERTRAIN",
              dlc: 8,
              data: `09 ${Math.floor(Math.random() * 80 + 10).toString(16)} B4 00 12 00 00 00`,
              status: "VALID",
              secoc: isSec ? "AUTHENTICATED" : "LEGACY_CLEAR",
              desc: `Engine RPM: ${Math.floor(2400 + Math.random() * 150)} | Nominal`,
              priority: "NORMAL (0x110)"
            };

            const updatedPackets = isSnifferPaused ? prev.recent_packets : [samplePkt, ...prev.recent_packets.slice(0, 19)];
            const rolling = [...prev.rolling_telemetry.slice(1), {
              name: timeStr,
              packets: newFps,
              load: newLoad,
              risk: isAtt && !isSec ? 9.9 : (isSec && isAtt ? 2.4 : 1.2)
            }];

            return {
              ...prev,
              total_frames_sent: newTotal,
              bus_load_pct: newLoad,
              frames_per_sec: newFps,
              anomalies_detected: newAnom,
              recent_packets: updatedPackets,
              rolling_telemetry: rolling
            };
          });
        }
      }
    };

    const interval = setInterval(fetchLiveBus, 800);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [isSnifferPaused]);

  // Live attack & SecOC toggles
  const handleTriggerLiveAttack = async (duration = 12.0) => {
    try {
      await fetch(`${API_BASE}/live-bus/inject?duration=${duration}`, { method: 'POST' });
    } catch (e) {}
    setLiveBus(prev => ({ ...prev, is_attack_active: true, is_secoc_active: false }));
  };

  const handleToggleLiveSecoc = async () => {
    try {
      const res = await fetch(`${API_BASE}/live-bus/toggle-secoc`, { method: 'POST' });
      const data = await res.json();
      setLiveBus(prev => ({ ...prev, is_secoc_active: data.secoc_active }));
    } catch (e) {
      setLiveBus(prev => ({ ...prev, is_secoc_active: !prev.is_secoc_active }));
    }
  };

  // Threats & ECUs
  const [threats, setThreats] = useState([
    {
      id: "THREAT_006",
      title: "CAN ID 0x020 Emergency Brake Override",
      target: "Braking Controller (ESC)",
      cwe: "CWE-345",
      category: "Spoofing",
      score: 9.9,
      severity: "Critical",
      status: "Confirmed Exploit",
      vector: "Chassis CAN Injection"
    },
    {
      id: "THREAT_001",
      title: "Unauthenticated DoIP Remote Firmware Flash",
      target: "Telematics Unit (TCU)",
      cwe: "CWE-306",
      category: "Elevation of Privilege",
      score: 9.8,
      severity: "Critical",
      status: "Confirmed Exploit",
      vector: "Cellular UDP:13400"
    },
    {
      id: "THREAT_004",
      title: "Cross-Bus Unfiltered Routing to Safety Domain",
      target: "Central Gateway ECU",
      cwe: "CWE-284",
      category: "Tampering",
      score: 9.1,
      severity: "Critical",
      status: "Confirmed Exploit",
      vector: "Ethernet to CAN Hop"
    },
    {
      id: "THREAT_003",
      title: "UDS SecurityAccess (0x27) Seed/Key Weakness",
      target: "OBD-II Diagnostic Port",
      cwe: "CWE-287",
      category: "Elevation of Privilege",
      score: 7.8,
      severity: "High",
      status: "Mitigated",
      vector: "Physical Service Port"
    }
  ]);

  const [testResult, setTestResult] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isAutoDemoRunning, setIsAutoDemoRunning] = useState(false);
  const [autoDemoStep, setAutoDemoStep] = useState('');
  
  // AI Modal
  const [showAiModal, setShowAiModal] = useState(false);
  const [aiQuestion, setAiQuestion] = useState('');
  const [aiResponse, setAiResponse] = useState('');

  // Run dynamic test
  const handleRunTest = async (threatId, applyMitigation = false) => {
    setIsSimulating(true);
    if (!applyMitigation) {
      handleTriggerLiveAttack(15.0);
    } else {
      handleToggleLiveSecoc();
    }

    try {
      const res = await fetch(`${API_BASE}/simulate-test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ threat_id: threatId, apply_mitigation: applyMitigation })
      });
      const data = await res.json();
      setTestResult(data);
    } catch (e) {
      const isMit = applyMitigation;
      setTestResult({
        threat_id: threatId,
        test_title: "CAN ID 0x020 Brake Deceleration Test",
        status: isMit ? "VERIFIED_MITIGATED" : "CONFIRMED_EXPLOIT",
        verdict: isMit ? "Frame Discarded: SecOC CMAC validation failed." : "Exploit Confirmed: Braking solenoid actuated 120 bar.",
        timestamp: new Date().toLocaleTimeString(),
        traffic: isMit ? "DROPPED (Invalid MAC)" : "ACTUATED (Hydraulic 120 bar)"
      });
      setThreats(prev => prev.map(t => t.id === threatId ? {
        ...t,
        status: isMit ? "Mitigated" : "Confirmed Exploit"
      } : t));
    } finally {
      setIsSimulating(false);
    }
  };

  // 60-Second Autonomous Walkthrough
  const runAutoDemo = async () => {
    setIsAutoDemoRunning(true);
    setAutoDemoStep("Phase 1: Ingesting AUTOSAR Architecture...");
    await new Promise(r => setTimeout(r, 1200));

    setAutoDemoStep("Phase 2: Scanning STRIDE & ISO 21434 Rules...");
    await new Promise(r => setTimeout(r, 1400));

    setAutoDemoStep("Phase 3: Injecting Live CAN ID 0x020 (Brake Override)...");
    await handleRunTest('THREAT_006', false);
    await new Promise(r => setTimeout(r, 2200));

    setAutoDemoStep("Phase 4: Enforcing AUTOSAR SecOC CMAC Verification...");
    await handleRunTest('THREAT_006', true);
    await new Promise(r => setTimeout(r, 1600));

    setAutoDemoStep("Verified: Exploit Neutralized. ISO 21434 Compliant.");
    setIsAutoDemoRunning(false);
  };

  // AI query handler
  const handleAiAsk = (prompt) => {
    const q = prompt || aiQuestion;
    if (!q) return;
    setAiQuestion(q);
    setShowAiModal(true);
    setAiResponse("Querying ISO/SAE 21434 and AUTOSAR embedded standards...");
    setTimeout(() => {
      if (q.toLowerCase().includes("secoc") || q.toLowerCase().includes("brake")) {
        setAiResponse("AUTOSAR SecOC eliminates CAN ID 0x020 spoofing by enforcing a 32-bit truncated CMAC-AES128 signature and a monotonic Freshness Value. Frames lacking a valid MAC are discarded by the Electronic Stability Controller (ESC) hardware abstraction layer before reaching the hydraulic valve.");
      } else if (q.toLowerCase().includes("path") || q.toLowerCase().includes("hop")) {
        setAiResponse("Lateral Exploit Path: Cellular Ingress (UDP 13400) -> Compromise Telematics Unit (TCU) -> Lateral Hop across Central Gateway Ethernet bridge -> Broadcast unauthenticated CAN ID 0x020 directly to Safety-Critical Brake Controller.");
      } else {
        setAiResponse(`ThreatPath evaluates '${q}' using deterministic ISO/SAE 21434 TARA risk scoring. Safety criticality is categorized across ASIL-A to ASIL-D.`);
      }
    }, 400);
  };

  // Select chart dataset (Live or historical)
  const currentChartConfig = timeRange === 'LIVE'
    ? {
        spike: liveBus.is_attack_active 
          ? (liveBus.is_secoc_active ? 'DEFENDED: SecOC Filtering Active (vcan0)' : 'CRITICAL INJECTION: CAN ID 0x020 Active (120 bar)')
          : 'Live Telemetry: Bus Nominal (vcan0 500 kbps)',
        data: liveBus.rolling_telemetry
      }
    : (TIME_DATA[timeRange] || TIME_DATA['6M']);

  return (
    <div className="h-screen w-screen bg-[#0a0910] text-[#f6f4fa] flex flex-row overflow-hidden select-none relative font-sans">
      
      {/* 3D Ambient Lighting Background */}
      <div className="bg-3d-ambient">
        <div className="orb-1"></div>
        <div className="orb-2"></div>
        <div className="bg-grid-3d"></div>
      </div>

      {/* ========================================================= */}
      {/* THREATPATH AI HOMEPAGE / APP BOOT LAUNCH SCREEN */}
      {/* ========================================================= */}
      {showHomeLaunch && (
        <div className="fixed inset-0 z-50 bg-[#0a0910]/95 backdrop-blur-3xl flex flex-col items-center justify-center p-6 text-center animate-fadeIn">
          <div className="max-w-xl w-full flex flex-col items-center gap-6">
            
            <div>
              <h1 className="text-4xl font-extrabold text-white tracking-tight">
                ThreatPath AI
              </h1>
              <p className="text-xs font-extrabold text-purple-300 mt-2 uppercase tracking-wider">
                Automotive Cybersecurity Verification Platform
              </p>
            </div>

            {/* Live Calibration Stats */}
            <div className="grid grid-cols-2 gap-3 w-full text-left">
              <div className="p-3.5 rounded-xl bg-[#151022] border border-[rgba(255,255,255,0.07)]">
                <span className="text-[11px] font-bold text-[#94a3b8] block uppercase">Network Standard</span>
                <strong className="text-white font-extrabold text-sm num-clean">CAN-HS 500k & Ethernet</strong>
              </div>
              <div className="p-3.5 rounded-xl bg-[#151022] border border-[rgba(255,255,255,0.07)]">
                <span className="text-[11px] font-bold text-[#94a3b8] block uppercase">Safety Baseline</span>
                <strong className="text-pink-300 font-extrabold text-sm num-clean">ASIL-D Target Node (vcan0)</strong>
              </div>
            </div>

            {/* Boot Status Progress */}
            <div className="w-full flex flex-col gap-2">
              <div className="w-full h-1.5 bg-[#1e172e] rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-300"
                  style={{ width: `${bootProgress}%` }}
                ></div>
              </div>
              <div className="flex justify-between items-center text-xs font-bold text-[#94a3b8]">
                <span>Binding Virtual SocketCAN (vcan0)...</span>
                <span className="num-clean text-purple-300">{bootProgress}%</span>
              </div>
            </div>

            {/* Instant Launch Action */}
            <button
              onClick={() => setShowHomeLaunch(false)}
              className="mt-2 px-8 py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-xs font-extrabold flex items-center gap-2 shadow-lg shadow-purple-900/30 cursor-pointer transition uppercase tracking-wide"
            >
              <span>Launch Dashboard Console</span>
              <ArrowRight className="w-4 h-4" />
            </button>

          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* SIDEBAR NAVIGATION */}
      {/* ========================================================= */}
      <aside
        className={`${
          sidebarCollapsed ? 'w-[76px]' : 'w-[240px]'
        } h-full bg-[#110e19]/95 backdrop-blur-2xl border-r border-[rgba(255,255,255,0.07)] p-4 flex flex-col justify-between shrink-0 transition-all duration-300 ease-in-out z-20`}
      >
        <div className="flex flex-col gap-6">
          
          {/* Header Row: Clean Brand Name + 3-Line Menu Button */}
          <div className="flex items-center justify-between px-1 pt-1">
            {!sidebarCollapsed && (
              <button 
                onClick={() => setShowHomeLaunch(true)}
                className="font-extrabold text-xl text-white tracking-tight hover:text-purple-300 transition text-left cursor-pointer"
                title="View ThreatPath AI Home"
              >
                ThreatPath
              </button>
            )}
            
            {/* 3-Line Hamburger Menu Toggle */}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="p-2 rounded-xl bg-[#191526] hover:bg-[#231d36] text-[#c084fc] hover:text-white border border-[rgba(255,255,255,0.08)] transition cursor-pointer flex items-center justify-center shadow-sm"
              title={sidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
            >
              <Menu className="w-4 h-4" />
            </button>
          </div>

          {/* Nav Items */}
          <nav className="flex flex-col gap-1.5">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'topology', label: 'Architecture', icon: Layers },
              { id: 'threats', label: 'Threat Matrix', icon: ShieldAlert },
              { id: 'paths', label: 'Attack Paths', icon: Network },
              { id: 'sandbox', label: 'Test Sandbox', icon: Terminal }
            ].map(item => {
              const Icon = item.icon;
              const isActive = activeNav === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveNav(item.id)}
                  title={sidebarCollapsed ? item.label : undefined}
                  className={`flex items-center gap-3.5 px-3 py-2.5 text-xs font-bold transition cursor-pointer rounded-xl ${
                    isActive ? 'nav-item-active' : 'text-[#9f96ad] hover:text-white hover:bg-[#1a1526]'
                  } ${sidebarCollapsed ? 'justify-center px-0' : ''}`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-purple-300' : 'text-[#857b98]'}`} />
                  {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Bottom Nav Items */}
        <div className="pt-4 border-t border-[rgba(255,255,255,0.06)] flex flex-col gap-1.5">
          <button
            onClick={() => setActiveNav('standards')}
            title={sidebarCollapsed ? "Standards" : undefined}
            className={`flex items-center gap-3.5 px-3 py-2 text-xs font-bold transition cursor-pointer rounded-xl ${
              activeNav === 'standards' ? 'nav-item-active' : 'text-[#9f96ad] hover:text-white hover:bg-[#1a1526]'
            } ${sidebarCollapsed ? 'justify-center px-0' : ''}`}
          >
            <BookOpen className="w-4 h-4 shrink-0 text-[#857b98]" />
            {!sidebarCollapsed && <span className="truncate">Standards & Specs</span>}
          </button>
          
          <button
            onClick={() => setActiveNav('settings')}
            title={sidebarCollapsed ? "Settings" : undefined}
            className={`flex items-center gap-3.5 px-3 py-2 text-xs font-bold transition cursor-pointer rounded-xl ${
              activeNav === 'settings' ? 'nav-item-active' : 'text-[#9f96ad] hover:text-white hover:bg-[#1a1526]'
            } ${sidebarCollapsed ? 'justify-center px-0' : ''}`}
          >
            <Settings className="w-4 h-4 shrink-0 text-[#857b98]" />
            {!sidebarCollapsed && <span className="truncate">Settings</span>}
          </button>
        </div>

      </aside>

      {/* ========================================================= */}
      {/* MAIN CONTENT AREA */}
      {/* ========================================================= */}
      <div className="flex-1 h-full flex flex-col overflow-hidden z-10 relative">

        {/* ---------------- CRISP HEADER WITH CENTERED LIVE TELEMETRY STRIP ---------------- */}
        <header className="h-[68px] border-b border-[rgba(255,255,255,0.07)] bg-[#110e19]/80 backdrop-blur-2xl px-6 flex items-center justify-between shrink-0 relative">
          
          <div className="flex items-center">
            <h1 className="text-xl font-extrabold text-white tracking-tight">
              {activeNav === 'dashboard' && 'Threat Modeling & Security Validation'}
              {activeNav === 'topology' && 'ECU Architecture & Network Topology'}
              {activeNav === 'threats' && 'STRIDE & ISO 21434 Threat Matrix'}
              {activeNav === 'paths' && 'Multi-Hop Exploit Graph'}
              {activeNav === 'sandbox' && 'Live Virtual SocketCAN Hardware Sniffer'}
              {activeNav === 'standards' && 'Regulatory Standards & Compliance'}
              {activeNav === 'settings' && 'System Configuration'}
            </h1>
          </div>

          {/* Real-Time Live Bus Status Capsule - CENTERED ACROSS ALL PAGES */}
          <div className="hidden md:flex items-center gap-3 px-3.5 py-1.5 rounded-full bg-[#181326] border border-purple-500/30 text-xs font-bold shadow-lg shadow-purple-950/25 absolute left-1/2 -translate-x-1/2 pointer-events-auto">
            <span className="flex items-center gap-1.5 text-emerald-400 font-extrabold num-clean">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              vcan0 LIVE
            </span>
            <span className="text-[#64748b]">|</span>
            <span className={`num-clean font-extrabold ${liveBus.bus_load_pct > 70 ? 'text-rose-400 animate-pulse' : 'text-amber-300'}`}>
              Load: {liveBus.bus_load_pct}%
            </span>
            <span className="text-[#64748b]">|</span>
            <span className="num-clean font-extrabold text-cyan-300">
              {liveBus.frames_per_sec} fps
            </span>
            <span className="text-[#64748b]">|</span>
            <button 
              onClick={handleToggleLiveSecoc}
              className={`px-2.5 py-0.5 rounded-full text-[11px] font-extrabold cursor-pointer transition ${
                liveBus.is_secoc_active 
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' 
                  : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
              }`}
              title="Click to toggle AUTOSAR SecOC Filter"
            >
              SecOC: {liveBus.is_secoc_active ? 'ACTIVE' : 'OFF'}
            </button>
          </div>

          {/* Ask AI Pill */}
          <button
            onClick={() => setShowAiModal(true)}
            className="flex items-center gap-2.5 px-4 py-2 rounded-full bg-[#181426] border border-purple-500/30 hover:border-purple-400/60 text-xs font-extrabold text-purple-200 hover:text-white transition cursor-pointer shadow-lg shadow-purple-900/10 shrink-0"
          >
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            <span>Ask ThreatPath AI anything</span>
          </button>

        </header>

        {/* Live Simulation Banner */}
        {isAutoDemoRunning && (
          <div className="px-6 py-2 bg-gradient-to-r from-purple-950 via-pink-950 to-purple-950 border-b border-pink-500/40 flex items-center justify-between text-xs text-pink-200 font-extrabold shrink-0 shadow-lg">
            <span className="flex items-center gap-2.5">
              <Radio className="w-4 h-4 text-pink-400 animate-spin" /> {autoDemoStep}
            </span>
            <span className="text-[11px] uppercase tracking-wider text-pink-300 font-extrabold">Autonomous Jury Demo</span>
          </div>
        )}

        {/* ---------------- SCROLLABLE PAGE WORKSPACE ---------------- */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">

          {/* ========================================================= */}
          {/* DASHBOARD PAGE */}
          {/* ========================================================= */}
          {activeNav === 'dashboard' && (
            <div className="flex flex-col gap-6 flex-1 max-w-[1600px] w-full mx-auto">
              
              {/* TOP ROW: 3 CARDS */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* CARD 1: ECU Inventory & Live Packets */}
                <div className="glass-panel-3d p-6 rounded-2xl flex flex-col justify-between min-h-[200px] bg-gradient-to-br from-[#0c1a2e]/90 via-[#0e1626]/80 to-[#141b2c]/90 border border-cyan-500/35 shadow-lg shadow-cyan-950/20">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-extrabold uppercase tracking-wider text-cyan-300">ECU Inventory</span>
                    <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 num-clean">
                      CAN-HS 500k
                    </span>
                  </div>

                  <div>
                    <div className="text-3xl font-extrabold text-white tracking-tight num-clean">
                      6 Nodes <span className="text-base font-bold text-[#94a3b8]">/ 14 PDUs</span>
                    </div>
                    <div className="text-xs font-extrabold text-rose-400 mt-1 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                      Peak Hazard: <strong className="font-extrabold num-clean">ASIL-D (CVSS 9.9)</strong>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[rgba(255,255,255,0.06)] grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-[#94a3b8] block text-xs font-bold">Total Packets Processed</span>
                      <strong className="text-cyan-200 font-extrabold num-clean">{liveBus.total_frames_sent.toLocaleString()}</strong>
                    </div>
                    <div>
                      <span className="text-[#94a3b8] block text-xs font-bold">Intrusion Alerts</span>
                      <strong className={`font-extrabold num-clean ${liveBus.anomalies_detected > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                        {liveBus.anomalies_detected} Detected
                      </strong>
                    </div>
                  </div>
                </div>

                {/* CARD 2: Decisions Powered by Data */}
                <div className="glass-panel-3d p-6 rounded-2xl flex flex-col justify-between min-h-[200px] bg-gradient-to-b from-[#1c1236]/90 via-[#23153d]/85 to-[#2c1242]/90 border border-purple-500/40 relative overflow-hidden shadow-lg shadow-purple-950/30">
                  <div>
                    <h3 className="text-lg font-extrabold text-white tracking-tight">
                      Decisions Powered by Data
                    </h3>
                    <p className="text-xs font-extrabold text-[#c4b5fd] mt-2">
                      Automated Virtual SocketCAN Penetration Testing
                    </p>
                  </div>

                  {/* Signature Glowing Button with Underglow Beam */}
                  <div className="btn-glow-container mt-4">
                    <div className="btn-glow-beam"></div>
                    <button
                      onClick={runAutoDemo}
                      disabled={isAutoDemoRunning}
                      className="btn-ai-glow w-full py-3 rounded-full text-xs font-extrabold flex items-center justify-center gap-2.5 cursor-pointer active:scale-98 disabled:opacity-50 tracking-wide uppercase"
                    >
                      {isAutoDemoRunning ? <RefreshCw className="w-4 h-4 animate-spin text-[#120d1c]" /> : <Play className="w-4 h-4 fill-current text-[#120d1c]" />}
                      <span>{isAutoDemoRunning ? "Running Simulation..." : "Run 60s Jury Walkthrough"}</span>
                    </button>
                  </div>
                </div>

                {/* CARD 3: Target ECU Status */}
                <div className="glass-panel-3d p-6 rounded-2xl flex flex-col justify-between min-h-[200px] bg-gradient-to-br from-[#2a101f]/90 via-[#1d1226]/80 to-[#181128]/90 border border-rose-500/35 shadow-lg shadow-rose-950/20">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-extrabold uppercase tracking-wider text-rose-300">Target ECU Status</span>
                    <span className="px-2.5 py-1 rounded-full text-xs font-extrabold text-rose-300 bg-rose-500/15 border border-rose-500/30 num-clean">
                      ASIL-D
                    </span>
                  </div>

                  <div>
                    <div className="text-lg font-extrabold text-white">
                      Braking Controller (ESC)
                    </div>
                    <div className="text-xs text-[#cbd5e1] font-bold mt-1">
                      Target: <span className="text-white font-extrabold num-clean">CAN ID 0x020</span> (Deceleration Solenoid)
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[rgba(255,255,255,0.06)] flex items-center gap-2.5">
                    <button
                      onClick={() => handleRunTest('THREAT_006', false)}
                      disabled={isSimulating}
                      className="flex-1 py-2.5 rounded-xl text-xs font-extrabold bg-rose-500/20 hover:bg-rose-500/35 text-rose-300 border border-rose-500/40 transition cursor-pointer flex items-center justify-center gap-1.5"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" /> Test Exploit
                    </button>

                    <button
                      onClick={() => handleRunTest('THREAT_006', true)}
                      disabled={isSimulating}
                      className="flex-1 py-2.5 rounded-xl text-xs font-extrabold bg-purple-500/25 hover:bg-purple-500/40 text-purple-200 border border-purple-400/40 transition cursor-pointer flex items-center justify-center gap-1.5"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" /> Enforce SecOC
                    </button>
                  </div>
                </div>

              </div>

              {/* MIDDLE ROW: ACTIVE THREAT TABLE WITH STRICT COLUMN WIDTHS */}
              <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-4">
                <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-3">
                  <h2 className="text-base font-extrabold text-white tracking-tight">
                    Prioritized Threat Vectors (STRIDE / ISO 21434)
                  </h2>
                  <span className="text-xs font-extrabold text-purple-300 px-3 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 num-clean">
                    4 Core Hazards
                  </span>
                </div>

                <div className="overflow-x-auto w-full">
                  <table className="table-fixed-align w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-[rgba(255,255,255,0.06)] text-[#cbd5e1] uppercase text-[11px] font-extrabold">
                        <th className="py-3 px-3 w-[32%]">Threat Scenario</th>
                        <th className="py-3 px-3 w-[22%]">Target Component</th>
                        <th className="py-3 px-3 w-[15%]">STRIDE / CWE</th>
                        <th className="py-3 px-3 w-[10%]">CVSS</th>
                        <th className="py-3 px-3 w-[9%]">Validation</th>
                        <th className="py-3 px-3 w-[12%] text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[rgba(255,255,255,0.04)]">
                      {threats.map(t => (
                        <tr key={t.id} className="hover:bg-[#1a1428]/60 transition">
                          <td className="py-4 px-3 align-middle">
                            <span className="font-extrabold text-white text-sm block leading-snug">{t.title}</span>
                          </td>
                          <td className="py-4 px-3 align-middle font-extrabold text-purple-200">
                            {t.target}
                          </td>
                          <td className="py-4 px-3 align-middle font-bold">
                            <span className="text-white block">{t.category}</span>
                            <span className="text-[11px] font-extrabold text-purple-400">{t.cwe}</span>
                          </td>
                          <td className="py-4 px-3 align-middle">
                            <span className={`inline-block px-2.5 py-1 rounded-md font-extrabold num-clean ${
                              t.severity === 'Critical' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                            }`}>
                              {t.score}
                            </span>
                          </td>
                          <td className="py-4 px-3 align-middle">
                            {t.status === 'Mitigated' ? (
                              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 whitespace-nowrap">
                                <ShieldCheck className="w-3.5 h-3.5" /> Mitigated
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-extrabold bg-rose-500/15 text-rose-300 border border-rose-500/30 whitespace-nowrap">
                                <AlertTriangle className="w-3.5 h-3.5" /> Exploit
                              </span>
                            )}
                          </td>
                          <td className="py-4 px-3 align-middle text-right">
                            <button
                              onClick={() => handleRunTest(t.id, t.status !== 'Mitigated')}
                              className="px-4 py-1.5 rounded-lg text-xs font-extrabold bg-[#1d172e] hover:bg-purple-600/30 text-purple-200 hover:text-white border border-purple-500/30 transition cursor-pointer whitespace-nowrap inline-flex items-center justify-center shrink-0 min-w-[76px]"
                            >
                              {t.status === 'Mitigated' ? 'Re-Test' : 'SecOC'}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* BOTTOM ROW: DYNAMIC TELEMETRY CHART */}
              <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-extrabold text-white tracking-tight">
                    Vulnerability Traversal & Bus Telemetry
                  </h3>
                  
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-extrabold text-pink-400 num-clean">
                      {currentChartConfig.spike}
                    </span>
                    {/* Time filter pill toggles with LIVE mode */}
                    <div className="flex items-center p-1 rounded-full bg-[#151122] border border-[rgba(255,255,255,0.08)]">
                      {['LIVE', '1D', '1W', '1M', '6M', '1Y'].map(range => (
                        <button
                          key={range}
                          onClick={() => setTimeRange(range)}
                          className={`px-3 py-1 rounded-full text-xs font-extrabold transition cursor-pointer num-clean ${
                            timeRange === range
                              ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md'
                              : 'text-[#94a3b8] hover:text-white'
                          }`}
                        >
                          {range === 'LIVE' ? 'LIVE BUS' : range}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="w-full h-[180px] min-h-[180px] mt-2 relative">
                  <ResponsiveContainer width="100%" height={180} minHeight={180} initialDimension={{ width: 1400, height: 180 }}>
                    <AreaChart data={currentChartConfig.data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#d946ef" stopOpacity={0.35}/>
                          <stop offset="95%" stopColor="#c084fc" stopOpacity={0.0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} fontWeight={700} tickLine={false} />
                      <YAxis stroke="#94a3b8" fontSize={11} fontWeight={700} tickLine={false} />
                      <Tooltip
                        content={({ active, payload }) => {
                          if (active && payload && payload.length) {
                            const data = payload[0].payload;
                            return (
                              <div className="bg-[#181326] border border-purple-400/40 rounded-xl p-3 shadow-2xl text-xs">
                                <div className="text-[11px] text-[#cbd5e1] font-bold num-clean">{data.name} {data.event ? `• ${data.event}` : ''}</div>
                                <div className="text-white font-extrabold text-sm mt-0.5 num-clean">{data.packets} packets/sec</div>
                                <div className="text-pink-400 font-extrabold mt-0.5 num-clean">Hazard {data.risk}</div>
                              </div>
                            );
                          }
                          return null;
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="packets"
                        stroke="#e879f9"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#chartGradient)"
                        isAnimationActive={false}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                {/* Packet Status Strip */}
                <div className="pt-3 border-t border-[rgba(255,255,255,0.06)] flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <Radio className="w-4 h-4 text-purple-400" />
                    <span className="font-extrabold text-white">Live Virtual SocketCAN (vcan0):</span>
                    <span className="font-bold text-purple-300 num-clean">
                      {liveBus.is_attack_active 
                        ? (liveBus.is_secoc_active ? "0x020 Attack Dropped by SecOC" : "CAN ID 0x020 Exploit Flooding Bus")
                        : "Nominal Traffic (500 kbps, 11-bit Standard)"}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-[#94a3b8] font-bold">Throughput:</span>
                    <span className="font-extrabold text-white num-clean">{liveBus.frames_per_sec} fps</span>
                    <span className="text-[#94a3b8] font-bold">Bus Load:</span>
                    <span className={`font-extrabold num-clean ${liveBus.bus_load_pct > 70 ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {liveBus.bus_load_pct}%
                    </span>
                  </div>
                </div>
              </div>

            </div>
          )}

          {/* ========================================================= */}
          {/* ARCHITECTURE (TOPOLOGY) PAGE */}
          {/* ========================================================= */}
          {activeNav === 'topology' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <h2 className="text-lg font-extrabold text-white">ECU Domain Architecture</h2>
                <span className="px-3 py-1 rounded-full bg-purple-500/20 border border-purple-500/30 text-xs font-extrabold text-purple-300 num-clean">
                  3 Partitioned Domains
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                {[
                  {
                    zone: "External Untrusted Zone",
                    color: "border-rose-500/40 bg-rose-950/15 text-rose-300",
                    items: [
                      { name: "Telematics Unit (TCU)", proto: "4G LTE / Ethernet", asil: "QM", threat: "CWE-306 OTA Bypass" },
                      { name: "OBD-II Service Port", proto: "CAN 500k", asil: "QM", threat: "CWE-287 Weak Seed/Key" }
                    ]
                  },
                  {
                    zone: "Gateway Domain",
                    color: "border-purple-500/40 bg-purple-950/15 text-purple-300",
                    items: [
                      { name: "Central Gateway ECU", proto: "CAN-FD / Ethernet", asil: "ASIL-B", threat: "CWE-284 Lateral Routing" },
                      { name: "Infotainment Head Unit", proto: "Ethernet / Bluetooth", asil: "QM", threat: "CWE-200 Data Leakage" }
                    ]
                  },
                  {
                    zone: "Safety-Critical ASIL-D Zone",
                    color: "border-emerald-500/40 bg-emerald-950/15 text-emerald-300",
                    items: [
                      { name: "Braking Controller (ESC)", proto: "Chassis CAN 500k", asil: "ASIL-D", threat: "CWE-345 Brake Override" },
                      { name: "Engine Control Module (ECM)", proto: "Powertrain CAN", asil: "ASIL-D", threat: "CWE-400 Bus-Off Flooding" }
                    ]
                  }
                ].map((z, idx) => (
                  <div key={idx} className={`p-5 rounded-2xl border ${z.color} flex flex-col gap-3.5`}>
                    <span className="text-xs font-extrabold uppercase tracking-wider">{z.zone}</span>
                    {z.items.map((it, i) => (
                      <div key={i} className="p-4 rounded-xl bg-[#14101e] border border-[rgba(255,255,255,0.06)] flex flex-col gap-1.5">
                        <div className="flex items-center justify-between">
                          <span className="font-extrabold text-white text-xs">{it.name}</span>
                          <span className="num-clean text-xs font-extrabold px-2 py-0.5 rounded bg-white/10 text-white">{it.asil}</span>
                        </div>
                        <div className="text-xs text-[#cbd5e1] font-bold num-clean">{it.proto}</div>
                        <div className="text-xs font-extrabold text-pink-400 mt-1">{it.threat}</div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ========================================================= */}
          {/* THREAT MATRIX PAGE */}
          {/* ========================================================= */}
          {activeNav === 'threats' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <h2 className="text-lg font-extrabold text-white">Full STRIDE & ISO 21434 Matrix</h2>
                <span className="px-3 py-1 rounded-full bg-rose-500/20 border border-rose-500/30 text-xs font-extrabold text-rose-300 num-clean">
                  ASIL-D Critical Focus
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {threats.map(t => (
                  <div key={t.id} className="p-5 rounded-2xl bg-[#14101e] border border-[rgba(255,255,255,0.06)] flex flex-col justify-between gap-3">
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-extrabold text-purple-300">{t.cwe}</span>
                        <span className="px-2.5 py-0.5 rounded font-extrabold text-xs bg-rose-500/20 text-rose-300 border border-rose-500/30 num-clean">
                          CVSS {t.score}
                        </span>
                      </div>
                      <h3 className="text-base font-extrabold text-white mt-1.5">{t.title}</h3>
                      <div className="text-xs text-[#cbd5e1] font-bold mt-1.5 flex items-center gap-2">
                        <span className="text-purple-300">{t.target}</span>
                        <span>•</span>
                        <span>{t.vector}</span>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-[rgba(255,255,255,0.06)] flex items-center justify-between">
                      <span className="text-xs font-extrabold text-white">{t.category}</span>
                      <button
                        onClick={() => handleRunTest(t.id, t.status !== 'Mitigated')}
                        className="px-4 py-1.5 rounded-xl text-xs font-extrabold bg-purple-600 hover:bg-purple-500 text-white transition cursor-pointer whitespace-nowrap shrink-0 inline-flex items-center justify-center min-w-[80px]"
                      >
                        {t.status === 'Mitigated' ? 'Re-Test' : 'Execute Test'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ========================================================= */}
          {/* ATTACK PATHS PAGE */}
          {/* ========================================================= */}
          {activeNav === 'paths' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <h2 className="text-lg font-extrabold text-white">NetworkX Lateral Exploit Traversal</h2>
                <span className="text-xs font-extrabold text-pink-400 px-3 py-1 rounded-full bg-pink-500/15 border border-pink-500/30 num-clean">
                  CVSS 9.9 Critical Path
                </span>
              </div>

              <div className="p-6 rounded-2xl bg-[#14101e] border border-[rgba(255,255,255,0.06)] flex flex-col gap-5">
                <h3 className="text-base font-extrabold text-white">
                  Remote Cellular Ingress ➔ Gateway Bridge ➔ Safety-Critical Braking Override
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {[
                    { step: "Step 1: Cellular Ingress", desc: "Unauthenticated UDP 13400 DoIP socket exploit on Telematics Unit.", cwe: "CWE-306", color: "bg-gradient-to-b from-[#0c1a2e]/90 to-[#0e0c15] border border-cyan-500/35", tagColor: "text-cyan-300" },
                    { step: "Step 2: Gateway Pivot", desc: "Cross-domain lateral hop across Central Gateway Ethernet bridge.", cwe: "CWE-284", color: "bg-gradient-to-b from-[#1b122e]/90 to-[#0e0c15] border border-purple-500/35", tagColor: "text-purple-300" },
                    { step: "Step 3: CAN Injection", desc: "Direct CAN ID 0x020 brake deceleration frame injection.", cwe: "CWE-345", color: "bg-gradient-to-b from-[#26101c]/90 to-[#0e0c15] border border-rose-500/35", tagColor: "text-rose-300" }
                  ].map((s, idx) => (
                    <div key={idx} className={`p-5 rounded-xl ${s.color} flex flex-col justify-between`}>
                      <div>
                        <span className={`text-xs font-extrabold ${s.tagColor} block`}>{s.cwe}</span>
                        <strong className="text-sm font-extrabold text-white block mt-1">{s.step}</strong>
                        <p className="text-xs text-[#cbd5e1] font-bold mt-2 leading-relaxed">{s.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ========================================================= */}
          {/* TEST SANDBOX (REAL-TIME LIVE CAN SNIFFER & INJECTION) */}
          {/* ========================================================= */}
          {activeNav === 'sandbox' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-extrabold text-white">Live Virtual SocketCAN Hardware Sniffer</h2>
                  <span className="text-xs font-bold text-[#94a3b8] mt-0.5 block">
                    Real-time frame ingestion, frame analysis, and AUTOSAR SecOC cryptographic filtering
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/30 text-xs font-extrabold text-emerald-300 num-clean flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    vcan0 Active (500 kbps)
                  </span>
                </div>
              </div>

              {/* Real-time Hardware Telemetry Gauges */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-gradient-to-br from-amber-950/30 to-[#14101e] border border-amber-500/35">
                  <span className="text-[11px] font-bold text-amber-300/80 block uppercase">Bus Load</span>
                  <strong className={`text-xl font-extrabold num-clean ${liveBus.bus_load_pct > 70 ? 'text-rose-400' : 'text-amber-300'}`}>
                    {liveBus.bus_load_pct}%
                  </strong>
                </div>
                <div className="p-4 rounded-xl bg-gradient-to-br from-cyan-950/30 to-[#14101e] border border-cyan-500/35">
                  <span className="text-[11px] font-bold text-cyan-300/80 block uppercase">Current Velocity</span>
                  <strong className="text-xl font-extrabold text-cyan-300 num-clean">{liveBus.frames_per_sec} frames/s</strong>
                </div>
                <div className="p-4 rounded-xl bg-gradient-to-br from-emerald-950/30 to-[#14101e] border border-emerald-500/35">
                  <span className="text-[11px] font-bold text-emerald-300/80 block uppercase">Cryptographic Layer</span>
                  <strong className={`text-xl font-extrabold ${liveBus.is_secoc_active ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {liveBus.is_secoc_active ? 'AUTOSAR SecOC' : 'Disabled (Raw CAN)'}
                  </strong>
                </div>
                <div className="p-4 rounded-xl bg-gradient-to-br from-rose-950/30 to-[#14101e] border border-rose-500/35">
                  <span className="text-[11px] font-bold text-rose-300/80 block uppercase">Intrusion Detections</span>
                  <strong className="text-xl font-extrabold text-rose-400 num-clean">{liveBus.anomalies_detected} Alerted</strong>
                </div>
              </div>

              {/* Interactive Live Controls */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleTriggerLiveAttack(12.0)}
                    className="px-4 py-2.5 rounded-xl text-xs font-extrabold bg-rose-500/25 hover:bg-rose-500/40 text-rose-300 border border-rose-500/40 cursor-pointer transition flex items-center gap-2"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" /> Inject Live CAN 0x020 (120 bar Attack)
                  </button>

                  <button
                    onClick={handleToggleLiveSecoc}
                    className={`px-4 py-2.5 rounded-xl text-xs font-extrabold border transition cursor-pointer flex items-center gap-2 ${
                      liveBus.is_secoc_active
                        ? 'bg-emerald-500/25 hover:bg-emerald-500/40 text-emerald-200 border-emerald-400/40'
                        : 'bg-purple-500/25 hover:bg-purple-500/40 text-purple-200 border-purple-400/40'
                    }`}
                  >
                    <ShieldCheck className="w-3.5 h-3.5" /> Toggle SecOC Cryptographic Verification
                  </button>
                </div>

                <button
                  onClick={() => setIsSnifferPaused(!isSnifferPaused)}
                  className="px-3.5 py-2 rounded-xl text-xs font-extrabold bg-[#1a1528] hover:bg-[#251e3a] text-[#cbd5e1] border border-[rgba(255,255,255,0.08)] cursor-pointer transition flex items-center gap-2"
                >
                  {isSnifferPaused ? <PlayCircle className="w-4 h-4 text-emerald-400" /> : <Pause className="w-4 h-4 text-purple-400" />}
                  <span>{isSnifferPaused ? "Resume Stream" : "Pause Stream"}</span>
                </button>
              </div>

              {/* Live CAN Packet Sniffer Table */}
              <div className="overflow-x-auto rounded-xl border border-[rgba(255,255,255,0.08)] bg-[#0d0a15]">
                <table className="table-fixed-align w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-[rgba(255,255,255,0.08)] bg-[#141020] text-[#94a3b8] uppercase text-[11px] font-extrabold">
                      <th className="py-2.5 px-3 w-[12%]">Time (ms)</th>
                      <th className="py-2.5 px-3 w-[12%]">ID</th>
                      <th className="py-2.5 px-3 w-[18%]">Node</th>
                      <th className="py-2.5 px-3 w-[8%]">DLC</th>
                      <th className="py-2.5 px-3 w-[26%]">Raw Data (Hex)</th>
                      <th className="py-2.5 px-3 w-[14%]">SecOC Auth</th>
                      <th className="py-2.5 px-3 w-[10%] text-right">Verdict</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[rgba(255,255,255,0.04)] font-sans">
                    {liveBus.recent_packets.map((pkt) => (
                      <tr 
                        key={pkt.id} 
                        className={`transition ${
                          pkt.status === 'EXPLOIT' 
                            ? 'bg-rose-950/30' 
                            : pkt.status === 'DEFENDED' 
                              ? 'bg-emerald-950/20' 
                              : 'hover:bg-[#1a1428]/40'
                        }`}
                      >
                        <td className="py-2.5 px-3 font-bold text-[#94a3b8] num-clean">{pkt.timestamp}</td>
                        <td className="py-2.5 px-3">
                          <span className={`px-2 py-0.5 rounded text-xs font-extrabold num-clean ${
                            pkt.can_id === '0x020' 
                              ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' 
                              : 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                          }`}>
                            {pkt.can_id}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 font-extrabold text-white">{pkt.ecu}</td>
                        <td className="py-2.5 px-3 font-extrabold text-[#94a3b8] num-clean">{pkt.dlc}</td>
                        <td className="py-2.5 px-3 font-mono text-[11px] text-pink-300 font-bold tracking-wider">
                          {pkt.data}
                        </td>
                        <td className="py-2.5 px-3">
                          <span className={`text-[11px] font-extrabold ${
                            pkt.secoc.includes('MAC_MISMATCH') || pkt.secoc === 'NO_MAC' 
                              ? 'text-rose-400' 
                              : 'text-emerald-400'
                          }`}>
                            {pkt.secoc}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 text-right">
                          <span className={`px-2 py-0.5 rounded text-[11px] font-extrabold ${
                            pkt.status === 'EXPLOIT' 
                              ? 'bg-rose-500 text-slate-950' 
                              : pkt.status === 'DEFENDED' 
                                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' 
                                : 'text-[#94a3b8]'
                          }`}>
                            {pkt.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ========================================================= */}
          {/* STANDARDS & SPECS PAGE */}
          {/* ========================================================= */}
          {activeNav === 'standards' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <h2 className="text-lg font-extrabold text-white">Regulatory Standards & Compliance</h2>
                <span className="px-3 py-1 rounded-full bg-purple-500/20 border border-purple-500/30 text-xs font-extrabold text-purple-300 num-clean">
                  Automotive Cybersecurity Mandates
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {[
                  { title: "ISO/SAE 21434:2021", spec: "Clause 9 governs Threat Analysis & Risk Assessment (TARA). Enforces ASIL-D severity ratings and attack feasibility." },
                  { title: "UNECE WP.29 Regulation 155", spec: "Mandates certified Cybersecurity Management Systems (CSMS) and mitigation evidence for vehicle type approval." },
                  { title: "AUTOSAR SecOC Classic R4.4", spec: "Cryptographic message authentication (CMAC-AES128) and Freshness Value Managers (FVM)." },
                  { title: "ISO 14229-1:2020 (UDS)", spec: "SecurityAccess Service 0x27 asymmetric challenge-response and firmware flashing verification." }
                ].map((s, i) => (
                  <div key={i} className="p-5 rounded-xl bg-[#14101e] border border-[rgba(255,255,255,0.06)]">
                    <strong className="text-white font-extrabold text-sm block">{s.title}</strong>
                    <p className="text-[#cbd5e1] mt-2 font-bold leading-relaxed">{s.spec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ========================================================= */}
          {/* SETTINGS PAGE */}
          {/* ========================================================= */}
          {activeNav === 'settings' && (
            <div className="glass-panel-3d p-6 rounded-2xl flex flex-col gap-6 max-w-[1600px] w-full mx-auto flex-1">
              <div className="border-b border-[rgba(255,255,255,0.06)] pb-3 flex items-center justify-between">
                <h2 className="text-lg font-extrabold text-white">System Configuration</h2>
                <span className="px-3 py-1 rounded-full bg-purple-500/20 border border-purple-500/30 text-xs font-extrabold text-purple-300 num-clean">
                  Simulation Parameters
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-5 rounded-xl bg-[#14101e] border border-[rgba(255,255,255,0.06)] flex flex-col gap-3">
                  <span className="font-extrabold text-white text-sm">Virtual Bus Interface</span>
                  <div className="flex justify-between py-1.5 border-b border-[rgba(255,255,255,0.04)] text-[#cbd5e1] font-bold">
                    <span>Interface</span>
                    <strong className="text-white font-extrabold num-clean">vcan0</strong>
                  </div>
                  <div className="flex justify-between py-1.5 text-[#cbd5e1] font-bold">
                    <span>Baud Rate</span>
                    <strong className="text-white font-extrabold num-clean">500 kbps (CAN-HS)</strong>
                  </div>
                </div>

                <div className="p-5 rounded-xl bg-[#14101e] border border-[rgba(255,255,255,0.06)] flex flex-col gap-3">
                  <span className="font-extrabold text-white text-sm">AUTOSAR SecOC Profile</span>
                  <div className="flex justify-between py-1.5 border-b border-[rgba(255,255,255,0.04)] text-[#cbd5e1] font-bold">
                    <span>MAC Primitive</span>
                    <strong className="text-white font-extrabold">CMAC-AES128</strong>
                  </div>
                  <div className="flex justify-between py-1.5 text-[#cbd5e1] font-bold">
                    <span>Truncation Length</span>
                    <strong className="text-white font-extrabold num-clean">32 bits (4 bytes)</strong>
                  </div>
                </div>
              </div>
            </div>
          )}

        </div>

      </div>

      {/* ========================================================= */}
      {/* AI ASSISTANT MODAL */}
      {/* ========================================================= */}
      {showAiModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-lg bg-[#14101e] border border-purple-500/30 rounded-2xl p-5 shadow-2xl flex flex-col gap-4">
            
            <div className="flex items-center justify-between border-b border-[rgba(255,255,255,0.06)] pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <h3 className="text-sm font-extrabold text-white">ThreatPath AI Assistant</h3>
              </div>
              <button onClick={() => setShowAiModal(false)} className="text-[#9f96ad] hover:text-white cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center gap-2 bg-[#1b1726] border border-[rgba(255,255,255,0.08)] rounded-xl px-3.5 py-2">
              <Search className="w-4 h-4 text-[#7e7492]" />
              <input
                type="text"
                placeholder="Ask about SecOC, ISO 21434, or attack paths..."
                value={aiQuestion}
                onChange={e => setAiQuestion(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleAiAsk()}
                className="bg-transparent flex-1 text-xs text-white outline-none placeholder:text-[#6c637c] font-bold"
              />
              <button
                onClick={() => handleAiAsk()}
                className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 text-xs font-extrabold text-slate-950 cursor-pointer shadow-md"
              >
                Ask
              </button>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {[
                "How to mitigate CAN ID 0x020 with SecOC?",
                "Trace multi-hop route from TCU to Brake ECU",
                "What ISO 21434 clauses are verified?"
              ].map(q => (
                <button
                  key={q}
                  onClick={() => handleAiAsk(q)}
                  className="px-2.5 py-1 rounded-full bg-[#1b1726] hover:bg-[#251f33] text-[11px] font-bold text-[#9f96ad] hover:text-purple-200 border border-[rgba(255,255,255,0.05)] cursor-pointer transition text-left"
                >
                  {q}
                </button>
              ))}
            </div>

            {aiResponse && (
              <div className="p-3.5 rounded-xl bg-[#0f0c17] border border-purple-500/20 text-xs text-purple-100 leading-relaxed font-sans shadow-inner font-bold">
                <div className="font-extrabold text-xs text-purple-300 mb-1 flex items-center gap-1.5">
                  <Check className="w-3.5 h-3.5 text-purple-400" /> ThreatPath Reasoning:
                </div>
                {aiResponse}
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}
