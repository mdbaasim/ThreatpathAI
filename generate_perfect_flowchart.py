import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_perfect_flowchart(output_path="evidence_ai_flowchart.png"):
    # Standard 16:9 presentation slide ratio (16 x 9 inches)
    fig, ax = plt.subplots(figsize=(16, 9.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC') # Clean background
    ax.set_facecolor('#F8FAFC')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.2)
    ax.axis('off')

    # Color Palette
    c_blue = '#2563EB'
    c_sky = '#0284C7'
    c_dark = '#0F172A'
    c_sub = '#475569'
    c_green = '#059669'
    c_amber = '#D97706'
    c_purple = '#7C3AED'
    c_border_gray = '#CBD5E1'

    def draw_card(x, y, w, h, tag, title, bullets=[], bg='#FFFFFF', border='#2563EB', tag_color='#2563EB', title_color='#0F172A'):
        # Soft shadow
        shadow = patches.FancyBboxPatch(
            (x - w/2 + 0.05, y - h/2 - 0.06), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.18",
            facecolor='#E2E8F0', edgecolor='none', alpha=0.5, zorder=2
        )
        ax.add_patch(shadow)

        # Card rectangle
        card = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.18",
            facecolor=bg, edgecolor=border, linewidth=2, zorder=3
        )
        ax.add_patch(card)

        # Header tag & title
        header_y = y + h/2 - 0.38
        if tag:
            ax.text(x, header_y + 0.12, tag.upper(), ha='center', va='center',
                    fontsize=8.5, fontweight='bold', color=tag_color, zorder=4)
            ax.text(x, header_y - 0.22, title, ha='center', va='center',
                    fontsize=11.5, fontweight='bold', color=title_color, zorder=4)
        else:
            ax.text(x, header_y - 0.05, title, ha='center', va='center',
                    fontsize=12, fontweight='bold', color=title_color, zorder=4)

        # Divider
        ax.plot([x - w/2 + 0.25, x + w/2 - 0.25], [header_y - 0.44, header_y - 0.44], color='#E2E8F0', lw=1.2, zorder=4)

        # Bullets
        text_y = header_y - 0.72
        for b in bullets:
            ax.text(x - w/2 + 0.3, text_y, f"• {b}", ha='left', va='center',
                    fontsize=9.2, color=c_sub, zorder=4)
            text_y -= 0.36

    def draw_diamond(x, y, w, h, title, subtitle="", bg='#FFFBEB', border='#D97706'):
        shadow_pts = [(x, y + h/2 - 0.06), (x + w/2 + 0.05, y - 0.06), (x, y - h/2 - 0.06), (x - w/2 + 0.05, y - 0.06)]
        shadow = patches.Polygon(shadow_pts, closed=True, facecolor='#E2E8F0', edgecolor='none', alpha=0.5, zorder=2)
        ax.add_patch(shadow)

        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        diamond = patches.Polygon(pts, closed=True, facecolor=bg, edgecolor=border, linewidth=2.2, zorder=3)
        ax.add_patch(diamond)

        ax.text(x, y + 0.14, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color='#92400E', zorder=4)
        if subtitle:
            ax.text(x, y - 0.24, subtitle, ha='center', va='center',
                    fontsize=8.5, color='#B45309', zorder=4)

    def draw_arrow(x1, y1, x2, y2, color='#475569', lw=2, dashed=False):
        ls = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                    mutation_scale=16, shrinkA=0, shrinkB=0),
                    zorder=5)

    # Title Banner
    ax.text(8.0, 8.7, "Evidence-Based Multi-Hypothesis AI Architecture", ha='center', va='center',
            fontsize=17, fontweight='bold', color=c_dark)
    ax.text(8.0, 8.3, "End-to-End Workflow: Ingestion → Hypotheses → Evidence Triangulation → Scoring → Adaptive Action",
            ha='center', va='center', fontsize=10, color='#64748B')
    ax.plot([1.5, 14.5], [8.0, 8.0], color='#CBD5E1', lw=1.2, zorder=1)

    # -------------------------------------------------------------
    # TOP ROW: 4 Pipeline Cards (y = 6.2)
    # -------------------------------------------------------------
    card_w = 3.1
    card_h = 2.4
    y_top = 6.4

    # 1. Problem Ingestion
    x1 = 2.0
    draw_card(x1, y_top, card_w, card_h, "Stage 1", "Problem Ingestion",
              ["Technical symptom logs", "Sensor & error telemetry", "Operating environment context"],
              border=c_sky, tag_color=c_sky)

    # 2. Hypothesis Generation
    x2 = 5.6
    draw_arrow(x1 + card_w/2, y_top, x2 - card_w/2, y_top)
    draw_card(x2, y_top, card_w, card_h, "Stage 2", "Hypothesis Generator",
              ["Generates candidate causes (H₁...Hₙ)", "Explicit 'Unknown Cause' (H₀)", "Prevents early tunnel-vision"],
              border=c_sky, tag_color=c_sky)

    # 3. Evidence Analysis
    x3 = 9.2
    draw_arrow(x2 + card_w/2, y_top, x3 - card_w/2, y_top)
    draw_card(x3, y_top, card_w, card_h, "Stage 3", "Evidence Analysis",
              ["Extracts Supporting Facts (+)", "Identifies Conflicting Data (-)", "Catalogs Missing Evidence (?)"],
              border=c_blue, tag_color=c_blue)

    # 4. Dynamic Scoring
    x4 = 12.8
    draw_arrow(x3 + card_w/2, y_top, x4 - card_w/2, y_top)
    draw_card(x4, y_top, card_w, card_h, "Stage 4", "Dynamic Scoring",
              ["Bayesian probability updates", "Reliability-weighted facts", "Adapts continuously to new data"],
              border=c_blue, tag_color=c_blue)

    # -------------------------------------------------------------
    # MIDDLE DECISION: From Stage 4 down to Diamond
    # -------------------------------------------------------------
    y_diamond = 3.6
    x_diamond = 12.8

    draw_arrow(x4, y_top - card_h/2, x_diamond, y_diamond + 0.9, color='#475569')
    draw_diamond(x_diamond, y_diamond, 2.8, 1.7, "Sufficient\nEvidence?", "Confidence Check")

    # -------------------------------------------------------------
    # BRANCH 1: YES -> Decisive Conclusion (Right side, y = 1.9)
    # -------------------------------------------------------------
    # From right of diamond -> Down to Decisive Conclusion
    x_yes = 14.5
    y_bottom = 1.8
    bottom_h = 2.3
    bottom_w = 2.6

    # Green YES Branch: Right of diamond to Right card
    ax.plot([x_diamond + 1.4, x_yes], [y_diamond, y_diamond], color=c_green, lw=2.2, zorder=5)
    draw_arrow(x_yes, y_diamond, x_yes, y_bottom + bottom_h/2, color=c_green, lw=2.2)

    ax.text(x_yes - 0.4, y_diamond + 0.25, "YES", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=c_green,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DCFCE7', edgecolor=c_green, lw=1.2), zorder=6)

    draw_card(x_yes, y_bottom, bottom_w, bottom_h, "Resolution", "Decisive Conclusion",
              ["Top verified cause", "High confidence delta", "Audit-ready evidence"],
              bg='#F0FDF4', border=c_green, tag_color=c_green, title_color='#065F46')

    # -------------------------------------------------------------
    # BRANCH 2: NO -> Acknowledge Ambiguity & Test Recommender (Leftwards!)
    # -------------------------------------------------------------
    # Amber NO Branch: Left of diamond -> Down to Acknowledge Ambiguity
    x_no = 9.8
    ax.plot([x_diamond - 1.4, x_no], [y_diamond, y_diamond], color=c_amber, lw=2.2, zorder=5)
    draw_arrow(x_no, y_diamond, x_no, y_bottom + bottom_h/2, color=c_amber, lw=2.2)

    ax.text(x_no + 0.4, y_diamond + 0.25, "NO", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=c_amber,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEF3C7', edgecolor=c_amber, lw=1.2), zorder=6)

    draw_card(x_no, y_bottom, bottom_w, bottom_h, "Notice", "Acknowledge Ambiguity",
              ["Refuses to guess blindly", "Flags critical data gaps", "Prevents false alarms"],
              bg='#FFFBEB', border=c_amber, tag_color=c_amber, title_color='#92400E')

    # From Acknowledge Ambiguity -> Test Recommendation Engine (To the left!)
    x_test = 6.2
    draw_arrow(x_no - bottom_w/2, y_bottom, x_test + bottom_w/2, y_bottom, color=c_purple, lw=2.2)
    draw_card(x_test, y_bottom, bottom_w, bottom_h, "Action", "Test Recommender",
              ["Prescribes target tests", "Differentiates causes", "Ranks by info gain"],
              bg='#FAF5FF', border=c_purple, tag_color=c_purple, title_color='#5B21B6')

    # -------------------------------------------------------------
    # FEEDBACK LOOP: From Test Recommender UP to Stage 3 (Evidence Analysis)
    # Clean, unobstructed vertical line directly upwards!
    # -------------------------------------------------------------
    # Test Recommender is at x_test = 6.2. Stage 3 is at x3 = 9.2.
    # Let's take the feedback arrow: From top of Test Recommender -> Up to y=4.5 -> Right to x3 -> Up into Stage 3 bottom!
    ax.plot([x_test, x_test], [y_bottom + bottom_h/2, 4.2], color=c_purple, lw=2, linestyle='--', zorder=5)
    ax.plot([x_test, x3 - 0.4], [4.2, 4.2], color=c_purple, lw=2, linestyle='--', zorder=5)
    draw_arrow(x3 - 0.4, 4.2, x3 - 0.4, y_top - card_h/2, color=c_purple, lw=2, dashed=True)

    # Feedback badge in the clear space
    ax.text((x_test + x3 - 0.4)/2, 4.5, "New Evidence Loop: Run Recommended Test → Update Evidence",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_purple,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#F3E8FF', edgecolor=c_purple, lw=1), zorder=6)

    # -------------------------------------------------------------
    # FINAL OUTPUT: Investigation Dashboard & Report (Bottom Left, x = 2.0)
    # -------------------------------------------------------------
    x_dash = 2.0
    draw_card(x_dash, y_bottom, bottom_w, bottom_h, "Output", "Dashboard & Audit",
              ["Ranked conclusions display", "Live confidence meters", "Missing evidence matrix"],
              bg='#F8FAFC', border=c_dark, tag_color=c_dark, title_color=c_dark)

    # Connect Decisive Conclusion to Dashboard (via a clean bottom path)
    ax.plot([x_yes, x_yes], [y_bottom - bottom_h/2, 0.4], color='#475569', lw=1.8, zorder=5)
    ax.plot([x_yes, x_dash], [0.4, 0.4], color='#475569', lw=1.8, zorder=5)
    draw_arrow(x_dash, 0.4, x_dash, y_bottom - bottom_h/2, color='#475569', lw=1.8)

    # Label on report path
    ax.text(8.0, 0.4, "Generates Final Evaluation & Verification Report",
            ha='center', va='center', fontsize=8.5, color='#475569', style='italic',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1), zorder=6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Perfect flowchart saved to {output_path}")

if __name__ == "__main__":
    create_perfect_flowchart("c:/Users/mdbaa/OneDrive/Desktop/L&T/evidence_ai_flowchart.png")
