import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_clean_flowchart(output_path="evidence_ai_flowchart.png"):
    # Standard presentation / report landscape aspect ratio: 15 x 9.5 inches
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Coordinate space
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Color definitions
    c_blue = '#1D4ED8'        # Royal Blue
    c_sky = '#0284C7'         # Sky Blue
    c_slate_dark = '#0F172A'  # Dark Slate
    c_slate_mid = '#334155'
    c_slate_light = '#64748B'
    c_green = '#059669'       # Success / Confirmed
    c_amber = '#D97706'       # Warning / Unknown
    c_purple = '#7C3AED'      # Action / Tests
    c_line = '#475569'

    # Helper: Draw Card
    def draw_card(x, y, w, h, step_num, title, bullets=[], bg='#FFFFFF', border='#2563EB', title_color='#0F172A', badge=None):
        # Drop shadow
        shadow = patches.FancyBboxPatch(
            (x - w/2 + 0.06, y - h/2 - 0.06), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.18",
            facecolor='#E2E8F0', edgecolor='none', alpha=0.6, zorder=2
        )
        ax.add_patch(shadow)

        # Card body
        card = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.1,rounding_size=0.18",
            facecolor=bg, edgecolor=border, linewidth=2, zorder=3
        )
        ax.add_patch(card)

        # Step badge / header
        header_y = y + h/2 - 0.35
        if step_num:
            ax.text(x - w/2 + 0.3, header_y, step_num, fontsize=9.5, fontweight='bold', color=border, zorder=4)
            ax.text(x - w/2 + 0.9, header_y, title, fontsize=11, fontweight='bold', color=title_color, zorder=4)
        else:
            ax.text(x, header_y, title, ha='center', fontsize=11.5, fontweight='bold', color=title_color, zorder=4)

        # Divider line inside card
        ax.plot([x - w/2 + 0.25, x + w/2 - 0.25], [header_y - 0.18, header_y - 0.18], color='#E2E8F0', lw=1.2, zorder=4)

        # Bullets / details
        text_y = header_y - 0.45
        for b in bullets:
            ax.text(x - w/2 + 0.3, text_y, f"• {b}", fontsize=9, color=c_slate_mid, zorder=4)
            text_y -= 0.32

    # Helper: Draw Diamond
    def draw_diamond(x, y, w, h, title, subtitle="", bg='#FFFBEB', border='#D97706'):
        shadow_pts = [(x, y + h/2 - 0.06), (x + w/2 + 0.06, y - 0.06), (x, y - h/2 - 0.06), (x - w/2 + 0.06, y - 0.06)]
        shadow = patches.Polygon(shadow_pts, closed=True, facecolor='#E2E8F0', edgecolor='none', alpha=0.6, zorder=2)
        ax.add_patch(shadow)

        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        diamond = patches.Polygon(pts, closed=True, facecolor=bg, edgecolor=border, linewidth=2.2, zorder=3)
        ax.add_patch(diamond)

        ax.text(x, y + 0.12, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#92400E', zorder=4)
        if subtitle:
            ax.text(x, y - 0.22, subtitle, ha='center', va='center', fontsize=8.5, color='#B45309', zorder=4)

    # Helper: Clean Arrow
    def draw_arrow(x1, y1, x2, y2, color=c_line, lw=2, dashed=False):
        ls = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                    mutation_scale=16, shrinkA=2, shrinkB=2),
                    zorder=5)

    # Main Header
    ax.text(7.5, 9.0, "Evidence-Based Multi-Hypothesis AI Architecture", ha='center', va='center',
            fontsize=17, fontweight='bold', color=c_slate_dark)
    ax.text(7.5, 8.6, "System Workflow: Hypothesis Generation → Evidence Triangulation → Confidence Scoring → Test Recommendation",
            ha='center', va='center', fontsize=10, color=c_slate_light)
    ax.plot([1.5, 13.5], [8.35, 8.35], color='#CBD5E1', lw=1.2, zorder=1)

    # Layout: 4 Columns
    col_w = 3.1
    card_h = 1.9

    # COLUMN 1: Ingestion & Hypotheses (x = 2.0)
    col1_x = 2.1
    # 1. Problem Ingestion
    draw_card(col1_x, 7.0, col_w, card_h, "STEP 1", "Problem Ingestion",
              ["Technical failure symptoms", "System error codes & telemetry", "Operational environment logs"],
              border=c_sky)

    # Arrow Down
    draw_arrow(col1_x, 7.0 - card_h/2, col1_x, 4.3 + card_h/2)

    # 2. Hypothesis Generation
    draw_card(col1_x, 4.3, col_w, card_h, "STEP 2", "Hypothesis Generation",
              ["Generates candidate causes (H₁, H₂...)", "Explicit 'Unknown Cause' baseline", "Reduces tunnel-vision bias"],
              border=c_sky)

    # Arrow from Col 1 to Col 2
    draw_arrow(col1_x + col_w/2, 4.3, 5.7 - col_w/2, 7.0)

    # COLUMN 2: Evidence & Scoring (x = 5.7)
    col2_x = 5.7
    # 3. Evidence Analysis
    draw_card(col2_x, 7.0, col_w, card_h, "STEP 3", "Evidence Analysis",
              ["Extracts Supporting Facts (+)", "Identifies Conflicting Data (-)", "Flags Missing Evidence (?)"],
              border=c_blue)

    # Arrow Down
    draw_arrow(col2_x, 7.0 - card_h/2, col2_x, 4.3 + card_h/2)

    # 4. Scoring Engine
    draw_card(col2_x, 4.3, col_w, card_h, "STEP 4", "Dynamic Scoring",
              ["Bayesian belief updating", "Weight evidence by reliability", "Adapts as new facts arrive"],
              border=c_blue)

    # Arrow from Col 2 to Decision Diamond in Col 3
    draw_arrow(col2_x + col_w/2, 4.3, 9.3 - 1.4, 4.3)

    # COLUMN 3: Decision & Resolution (x = 9.3)
    col3_x = 9.3
    # Diamond at (9.3, 4.3)
    draw_diamond(col3_x, 4.3, 2.6, 1.6, "Sufficient\nEvidence?", "Confidence Check")

    # Branch UP: YES (Decisive Conclusion)
    ax.plot([col3_x, col3_x], [4.3 + 0.8, 6.0], color=c_green, lw=2.2, zorder=5)
    draw_arrow(col3_x, 6.0, col3_x, 7.0 - card_h/2 + 0.1, color=c_green, lw=2.2)

    # Green YES label
    ax.text(col3_x + 0.45, 5.2, "YES", fontsize=9.5, fontweight='bold', color=c_green,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DCFCE7', edgecolor=c_green, lw=1), zorder=6)

    draw_card(col3_x, 7.0, col_w, card_h, "RESULT", "Decisive Conclusion",
              ["Top verified root cause", "High confidence separation", "Complete proof audit trail"],
              bg='#F0FDF4', border=c_green, title_color='#065F46')

    # Branch DOWN: NO (Insufficient Info)
    ax.plot([col3_x, col3_x], [4.3 - 0.8, 2.6], color=c_amber, lw=2.2, zorder=5)
    draw_arrow(col3_x, 2.6, col3_x, 1.8 + card_h/2 - 0.1, color=c_amber, lw=2.2)

    # Red/Amber NO label
    ax.text(col3_x + 0.4, 3.4, "NO", fontsize=9.5, fontweight='bold', color=c_amber,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEF3C7', edgecolor=c_amber, lw=1), zorder=6)

    draw_card(col3_x, 1.8, col_w, card_h, "NOTICE", "Acknowledge Ambiguity",
              ["Refuses to guess without data", "Highlights critical missing facts", "Prevents false conclusions"],
              bg='#FFFBEB', border=c_amber, title_color='#92400E')

    # COLUMN 4: Test Recommendation & Feedback Loop (x = 13.0)
    col4_x = 13.0

    # Test Recommendation Card (at y = 1.8)
    draw_card(col4_x, 1.8, col_w, card_h, "ACTION", "Test Recommender",
              ["Prescribes distinguishing tests", "Resolves competing causes", "Ranks tests by diagnostic value"],
              bg='#FAF5FF', border=c_purple, title_color='#5B21B6')

    # Arrow from Acknowledge Ambiguity to Test Recommender
    draw_arrow(col3_x + col_w/2, 1.8, col4_x - col_w/2, 1.8, color=c_purple, lw=2.2)

    # Interactive Dashboard & Final Report Card (at y = 7.0)
    draw_card(col4_x, 7.0, col_w, card_h, "OUTPUT", "Dashboard & Audit",
              ["Ranked conclusions display", "Live confidence distributions", "Missing evidence gap matrix"],
              bg='#F8FAFC', border=c_slate_dark, title_color=c_slate_dark)

    # Arrow from Decisive Conclusion to Dashboard
    draw_arrow(col3_x + col_w/2, 7.0, col4_x - col_w/2, 7.0, color=c_slate_dark, lw=2.2)

    # Clean Horizontal FEEDBACK LOOP from Test Recommender back to Evidence Analysis!
    # Path: From top of Test Recommender (y=2.75) -> Up along right -> Across top (y=8.15) -> Down into Evidence Analysis (col2_x)
    fb_y = 8.1
    ax.plot([col4_x, col4_x], [1.8 + card_h/2, fb_y], color=c_purple, lw=2, linestyle='--', zorder=5)
    ax.plot([col4_x, col2_x], [fb_y, fb_y], color=c_purple, lw=2, linestyle='--', zorder=5)
    draw_arrow(col2_x, fb_y, col2_x, 7.0 + card_h/2, color=c_purple, lw=2, dashed=True)

    # Feedback badge on the loop line
    ax.text(9.3, fb_y + 0.18, "Feedback Loop: Conduct Test → Ingest New Evidence → Update Scores",
            ha='center', va='center', fontsize=9, fontweight='bold', color=c_purple,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#F3E8FF', edgecolor=c_purple, lw=1.2), zorder=6)

    # Bottom Footer
    ax.text(7.5, 0.45, "Designed for AI-Assisted Root Cause Analysis • Compliant with L&T Hackathon Evaluation Criteria",
            ha='center', va='center', fontsize=9, color=c_slate_light, style='italic')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Clean landscape flowchart successfully saved to {output_path}")

if __name__ == "__main__":
    create_clean_flowchart("c:/Users/mdbaa/OneDrive/Desktop/L&T/evidence_ai_flowchart.png")
