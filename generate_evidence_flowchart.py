import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_evidence_ai_flowchart(output_path="evidence_ai_flowchart.png"):
    # High resolution canvas: 11 x 18 inches
    fig, ax = plt.subplots(figsize=(11, 18.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 22.5)
    ax.axis('off')

    # Color Palette - Modern High-Tech Engineering
    c_blue = '#0284C7'         # Ocean Blue
    c_dark_navy = '#0F172A'    # Slate 900
    c_text_sub = '#475569'     # Slate 600
    c_green = '#059669'        # Emerald Green (Confirmed)
    c_amber = '#D97706'        # Amber (Decision / Insufficient)
    c_purple = '#7C3AED'       # Purple (Test Recommender / Feedback)
    c_indigo = '#4338CA'       # Indigo

    def draw_box(x, y, w, h, title, subtitle="", bg='#FFFFFF', border='#0284C7', title_color='#0F172A', sub_color='#475569', lw=2):
        # Shadow
        shadow = patches.FancyBboxPatch(
            (x - w/2 + 0.06, y - h/2 - 0.07), w, h,
            boxstyle="round,pad=0.12,rounding_size=0.25",
            facecolor='#CBD5E1', edgecolor='none', alpha=0.45, zorder=2
        )
        ax.add_patch(shadow)

        # Box
        rect = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.12,rounding_size=0.25",
            facecolor=bg, edgecolor=border, linewidth=lw, zorder=3
        )
        ax.add_patch(rect)

        # Content
        if subtitle:
            ax.text(x, y + 0.22, title, ha='center', va='center',
                    fontsize=12, fontweight='bold', color=title_color, zorder=4)
            ax.text(x, y - 0.28, subtitle, ha='center', va='center',
                    fontsize=9.5, fontweight='normal', color=sub_color, style='italic', zorder=4)
        else:
            ax.text(x, y, title, ha='center', va='center',
                    fontsize=12.5, fontweight='bold', color=title_color, zorder=4)

    def draw_diamond(x, y, w, h, title, subtitle="", border='#D97706'):
        shadow_pts = [(x, y + h/2 - 0.07), (x + w/2 + 0.06, y - 0.07), (x, y - h/2 - 0.07), (x - w/2 + 0.06, y - 0.07)]
        shadow = patches.Polygon(shadow_pts, closed=True, facecolor='#CBD5E1', edgecolor='none', alpha=0.45, zorder=2)
        ax.add_patch(shadow)

        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        diamond = patches.Polygon(pts, closed=True, facecolor='#FFFBEB', edgecolor=border, linewidth=2.5, zorder=3)
        ax.add_patch(diamond)

        ax.text(x, y + 0.14, title, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color='#92400E', zorder=4)
        if subtitle:
            ax.text(x, y - 0.26, subtitle, ha='center', va='center',
                    fontsize=8.5, fontweight='normal', color='#B45309', zorder=4)

    def draw_arrow(x1, y1, x2, y2, color='#475569', lw=2, style="-|>"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                    mutation_scale=17, shrinkA=0, shrinkB=0),
                    zorder=5)

    # Title header
    ax.text(5.5, 21.8, "Evidence-Based Multi-Hypothesis AI Diagnostic Engine", ha='center', va='center',
            fontsize=16.5, fontweight='bold', color='#0F172A')
    ax.text(5.5, 21.3, "Hypothesis Generation • Evidence Triangulation • Bayesian Updating • Test Recommendation", ha='center', va='center',
            fontsize=9.5, color='#64748B')
    ax.plot([1.8, 9.2], [20.9, 20.9], color='#94A3B8', lw=1, zorder=1)

    box_w = 7.4
    box_h = 1.05

    # 1. Problem Ingestion
    y1 = 19.8
    draw_box(5.5, y1, box_w, box_h, "1. Problem Ingestion & Symptom Intake",
             "Technical failure logs, sensor telemetry, error codes & operating conditions",
             bg='#FFFFFF', border='#0284C7')

    # 2. Hypothesis Generation Engine
    y2 = 17.8
    draw_arrow(5.5, y1 - box_h/2 - 0.12, 5.5, y2 + box_h/2 + 0.12)
    draw_box(5.5, y2, box_w, box_h, "2. Multi-Hypothesis Generation Engine",
             "Formulates distinct competing explanations (H₁ ... Hₙ) + Explicit 'Unknown Cause' (H₀)",
             bg='#FFFFFF', border='#0284C7')

    # 3. Evidence Analysis Module
    y3 = 15.8
    draw_arrow(5.5, y2 - box_h/2 - 0.12, 5.5, y3 + box_h/2 + 0.12)
    draw_box(5.5, y3, box_w, box_h, "3. Evidence Analysis & Triangulation Module",
             "Identifies Supporting Facts (+), Conflicting Information (-), and Missing Evidence (?)",
             bg='#FFFFFF', border='#0284C7')

    # 4. Scoring System
    y4 = 13.8
    draw_arrow(5.5, y3 - box_h/2 - 0.12, 5.5, y4 + box_h/2 + 0.12)
    draw_box(5.5, y4, box_w, box_h, "4. Dynamic Evidential & Confidence Scoring Engine",
             "Bayesian belief updating across all candidate explanations as evidence evolves",
             bg='#FFFFFF', border='#0284C7')

    # 5. Decision Diamond: Sufficient Evidence?
    y5 = 11.6
    draw_arrow(5.5, y4 - box_h/2 - 0.12, 5.5, y5 + 0.8)
    draw_diamond(5.5, y5, 4.2, 1.6, "Sufficient Evidence?", "Confidence >= Threshold & Clear Separation")

    # Branches
    y_branch = 9.3
    branch_w = 4.2
    branch_h = 1.05

    # YES Branch (Left)
    ax.plot([5.5 - 2.1, 2.7], [y5, y5], color=c_green, lw=2.2, zorder=5)
    ax.plot([2.7, 2.7], [y5, y_branch + branch_h/2 + 0.12], color=c_green, lw=2.2, zorder=5)
    draw_arrow(2.7, y_branch + branch_h/2 + 0.2, 2.7, y_branch + branch_h/2 + 0.12, color=c_green, lw=2.2)

    ax.text(3.7, y5 + 0.25, "YES", ha='center', va='center',
            fontsize=10, fontweight='bold', color=c_green,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DCFCE7', edgecolor=c_green, lw=1.2), zorder=6)

    draw_box(2.7, y_branch, branch_w, branch_h, "Decisive Conclusion Identified",
             "Validated root cause supported by solid proof",
             bg='#F0FDF4', border=c_green, title_color='#065F46', sub_color='#047857')

    # NO Branch (Right)
    ax.plot([5.5 + 2.1, 8.3], [y5, y5], color=c_amber, lw=2.2, zorder=5)
    ax.plot([8.3, 8.3], [y5, y_branch + branch_h/2 + 0.12], color=c_amber, lw=2.2, zorder=5)
    draw_arrow(8.3, y_branch + branch_h/2 + 0.2, 8.3, y_branch + branch_h/2 + 0.12, color=c_amber, lw=2.2)

    ax.text(7.3, y5 + 0.25, "NO", ha='center', va='center',
            fontsize=10, fontweight='bold', color=c_amber,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEF3C7', edgecolor=c_amber, lw=1.2), zorder=6)

    draw_box(8.3, y_branch, branch_w, branch_h, "Acknowledge Insufficient Info",
             "Refuses to guess; flags active ambiguity",
             bg='#FFFBEB', border=c_amber, title_color='#92400E', sub_color='#B45309')

    # 6. Test Recommendation Feature (Below the NO branch)
    y_test = 6.9
    ax.plot([8.3, 8.3], [y_branch - branch_h/2 - 0.12, y_test + branch_h/2 + 0.12], color=c_purple, lw=2.2, zorder=5)
    draw_arrow(8.3, y_test + branch_h/2 + 0.2, 8.3, y_test + branch_h/2 + 0.12, color=c_purple, lw=2.2)

    draw_box(8.3, y_test, branch_w, branch_h, "Test Recommendation Engine",
             "Prescribes targeted diagnostic tests to separate hypotheses",
             bg='#FAF5FF', border=c_purple, title_color='#5B21B6', sub_color='#6D28D9')

    # Feedback Loop: From Test Recommendation -> Back to Evidence Module (Step 3 or Step 4)
    # Loop lines going along right margin
    loop_x = 10.4
    ax.plot([8.3 + branch_w/2 + 0.12, loop_x], [y_test, y_test], color=c_purple, lw=2, linestyle='--', zorder=5)
    ax.plot([loop_x, loop_x], [y_test, y3], color=c_purple, lw=2, linestyle='--', zorder=5)
    draw_arrow(loop_x, y3, 5.5 + box_w/2 + 0.12, y3, color=c_purple, lw=2)

    # Label on feedback loop
    ax.text(loop_x - 0.15, (y_test + y3)/2, "Execute Recommended Test &\nFeed New Evidence Back",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_purple, rotation=270,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#F3E8FF', edgecolor=c_purple, lw=1), zorder=6)

    # 7. Convergence to Dashboard
    y_dash = 4.4
    # Connect Conclusive (Left) directly down to Dashboard
    ax.plot([2.7, 2.7], [y_branch - branch_h/2 - 0.12, y_dash + 0.8], color='#475569', lw=2, zorder=5)
    ax.plot([2.7, 5.5], [y_dash + 0.8, y_dash + 0.8], color='#475569', lw=2, zorder=5)

    # Connect Test Engine (Right) down to Dashboard
    ax.plot([8.3, 8.3], [y_test - branch_h/2 - 0.12, y_dash + 0.8], color='#475569', lw=2, zorder=5)
    ax.plot([8.3, 5.5], [y_dash + 0.8, y_dash + 0.8], color='#475569', lw=2, zorder=5)

    draw_arrow(5.5, y_dash + 0.8, 5.5, y_dash + box_h/2 + 0.12, color='#475569', lw=2)

    draw_box(5.5, y_dash, box_w, box_h, "5. Interactive Investigation Dashboard",
             "Displays ranked conclusions, live confidence levels, and missing evidence gaps",
             bg='#EFF6FF', border='#3B82F6', title_color='#1E40AF', sub_color='#2563EB')

    # 8. Evaluation & Decision Report
    y_report = 2.4
    draw_arrow(5.5, y_dash - box_h/2 - 0.12, 5.5, y_report + box_h/2 + 0.12, color='#475569', lw=2)
    draw_box(5.5, y_report, box_w, box_h, "6. V&V Evaluation & Diagnostic Audit Report",
             "",
             bg='#0F172A', border='#0284C7', title_color='#F8FAFC', lw=2.2)
    
    ax.text(5.5, y_report - 0.28, "Measures accuracy, evidence handling rigor & decision auditability",
            ha='center', va='center', fontsize=9.5, color='#94A3B8', style='italic', zorder=4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Flowchart successfully saved to {output_path}")

if __name__ == "__main__":
    create_evidence_ai_flowchart("c:/Users/mdbaa/OneDrive/Desktop/L&T/evidence_ai_flowchart.png")
