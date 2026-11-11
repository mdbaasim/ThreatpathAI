import networkx as nx
from typing import List, Dict, Any
from models import Component, Connection, AttackPath, AttackStep

class GraphEngine:
    def __init__(self, components: List[Component], connections: List[Connection]):
        self.components = {c.id: c for c in components}
        self.connections = connections
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        for cid, comp in self.components.items():
            self.graph.add_node(
                cid,
                name=comp.name,
                type=comp.type,
                trust_zone=comp.trust_zone,
                safety=comp.safety_criticality,
                vulnerabilities=comp.vulnerabilities
            )
        
        for conn in self.connections:
            weight = 1.0
            if not conn.authenticated:
                weight *= 0.5  # Easier to traverse
            if not conn.encrypted:
                weight *= 0.7
            
            self.graph.add_edge(
                conn.source,
                conn.target,
                id=conn.id,
                protocol=conn.protocol,
                bus_id=conn.bus_id,
                authenticated=conn.authenticated,
                encrypted=conn.encrypted,
                weight=weight
            )

    def find_all_attack_paths(self, entry_points: List[str], target_nodes: List[str]) -> List[Dict[str, Any]]:
        results = []
        path_idx = 1
        
        for entry in entry_points:
            for target in target_nodes:
                if entry not in self.graph or target not in self.graph:
                    continue
                if nx.has_path(self.graph, entry, target):
                    for path in nx.all_simple_paths(self.graph, source=entry, target=target, cutoff=5):
                        steps = []
                        total_score = 0.0
                        
                        for i in range(len(path) - 1):
                            u = path[i]
                            v = path[i+1]
                            edge_data = self.graph.get_edge_data(u, v)
                            u_comp = self.components.get(u)
                            v_comp = self.components.get(v)
                            
                            step_vuln = v_comp.vulnerabilities[0] if v_comp and v_comp.vulnerabilities else "CWE-General"
                            
                            steps.append({
                                "step_number": i + 1,
                                "from_node": u_comp.name if u_comp else u,
                                "to_node": v_comp.name if v_comp else v,
                                "protocol": edge_data.get("protocol", "BUS"),
                                "authenticated": edge_data.get("authenticated", False),
                                "cwe": step_vuln,
                                "technique": f"Traverse {edge_data.get('protocol')} without authentication -> Target {v}"
                            })
                            total_score += 3.0 if not edge_data.get("authenticated") else 1.0

                        risk_lvl = "CRITICAL (ASIL-D)" if total_score >= 6 else "HIGH"
                        results.append({
                            "id": f"GEN_PATH_{path_idx}",
                            "title": f"Exploit Route: {self.components[entry].name} -> {self.components[target].name}",
                            "entry_point": entry,
                            "target_node": target,
                            "nodes_traversed": path,
                            "steps": steps,
                            "risk_level": risk_lvl,
                            "overall_score": min(9.9, 7.0 + total_score * 0.5)
                        })
                        path_idx += 1
                        
        return results

    def get_topology_for_ui(self) -> Dict[str, Any]:
        """Formats graph nodes and edges with coordinates for React Flow."""
        coords = {
            "TCU_01": {"x": 100, "y": 80},
            "OBD_PORT": {"x": 100, "y": 320},
            "IVI_01": {"x": 420, "y": 60},
            "GW_01": {"x": 420, "y": 200},
            "ECM_01": {"x": 750, "y": 100},
            "ESC_BRAKE": {"x": 750, "y": 280}
        }
        
        nodes = []
        for cid, data in self.graph.nodes(data=True):
            pos = coords.get(cid, {"x": 200, "y": 200})
            nodes.append({
                "id": cid,
                "name": data.get("name", cid),
                "type": data.get("type", "ECU"),
                "trust_zone": data.get("trust_zone"),
                "safety": data.get("safety"),
                "vulnerabilities": data.get("vulnerabilities", []),
                "position": pos
            })
            
        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "id": data.get("id", f"{u}_{v}"),
                "source": u,
                "target": v,
                "protocol": data.get("protocol"),
                "bus_id": data.get("bus_id"),
                "authenticated": data.get("authenticated", False),
                "encrypted": data.get("encrypted", False)
            })
            
        return {"nodes": nodes, "edges": edges}
