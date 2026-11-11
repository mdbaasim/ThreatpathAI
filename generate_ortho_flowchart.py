import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_ortho_flowchart(output_path="ortho_dialectic_flowchart.png"):
    # 16:9 widescreen presentation canvas (16 x 9.5 inches)
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Color Palette
    c_blue = '#1E40AF'
    c_sky = '#0284C7'
    c_dark = '#0F172A'
    c_slate = '#334155'
    c_sub = '#64748B'
    c_green = '#059669'
    c_amber = '#D97706'
    c_purple = '#7C3AED'
    c_rose = '#BE123C'
    c_indigo = '#4338CA'

    def draw_card(x, y, w, h, tag, title, bullets=[], bg='#FFFFFF', border='#2563EB', tag_color='#2563EB', title_color='#0F172A'):
        # Drop shadow
        shadow = patches.FancyBboxPatch(
            (x - w/2 + 0.05, y - h/2 - 0.06), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.18",
            facecolor='#E2E8F0', edgecolor='none', alpha=0.55, zorder=2
        )
        ax.add_patch(shadow)

        # Card container
        card = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.18",
            facecolor=bg, edgecolor=border, linewidth=2, zorder=3
        )
        ax.add_patch(card)

        # Header tag & title
        header_y = y + h/2 - 0.36
        if tag:
            ax.text(x, header_y + 0.12, tag.upper(), ha='center', va='center',
                    fontsize=8.5, fontweight='bold', color=tag_color, zorder=4)
            ax.text(x, header_y - 0.22, title, ha='center', va='center',
                    fontsize=11.5, fontweight='bold', color=title_color, zorder=4)
        else:
            ax.text(x, header_y - 0.05, title, ha='center', va='center',
                    fontsize=12, fontweight='bold', color=title_color, zorder=4)

        # Subtle divider
        ax.plot([x - w/2 + 0.25, x + w/2 - 0.25], [header_y - 0.44, header_y - 0.44], color='#E2E8F0', lw=1.2, zorder=4)

        # Bullet list
        text_y = header_y - 0.72
        for b in bullets:
            ax.text(x - w/2 + 0.3, text_y, f"• {b}", ha='left', va='center',
                    fontsize=9.2, color=c_slate, zorder=4)
            text_y -= 0.36

    def draw_arrow(x1, y1, x2, y2, color='#475569', lw=2, dashed=False):
        ls = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls,
                                    mutation_scale=16, shrinkA=2, shrinkB=2),
                    zorder=5)

    # Top Header Banner
    ax.text(8.0, 9.0, "OrthoDialectic: Two-Stage Competing Hypotheses & Convergence Engine", ha='center', va='center',
            fontsize=16.5, fontweight='bold', color=c_dark)
    ax.text(8.0, 8.6, "Stage 1: Multi-Axis Orthogonal Divergence  ⟶  Stage 2: Provenance-Aware Evidential Convergence",
            ha='center', va='center', fontsize=10, color=c_sub)
    ax.plot([1.2, 14.8], [8.3, 8.3], color='#CBD5E1', lw=1.2, zorder=1)

    # -------------------------------------------------------------------------
    # STAGE 1: DIVERGENCE PIPELINE (Top Row, y = 6.8)
    # -------------------------------------------------------------------------
    y_s1 = 6.8
    h_s1 = 2.4
    w_card = 4.3

    # Card 1: Problem & Ingestion
    x_c1 = 2.5
    draw_card(x_c1, y_s1, w_card, h_s1, "Input Ingestion", "Problem & Symptom Intake",
              ["Multi-modal anomaly logs & failure events", "Contextual environment telemetry", "Initial observation baseline"],
              border=c_sky, tag_color=c_sky)

    # Card 2: Orthogonal Divergence Engine
    x_c2 = 8.0
    draw_arrow(x_c1 + w_card/2, y_s1, x_c2 - w_card/2, y_s1)
    draw_card(x_c2, y_s1, w_card, h_s1, "Stage 1: Divergence", "Orthogonal Hypothesis Generator",
              ["4-Axis Distinctness: Cause, Assumption, Evidence, Effect",
               "Generates mutually competitive candidates (H₁ ... Hₖ)",
               "Anchors persistent Null/Unknown Candidate (H₀)"],
              border=c_indigo, tag_color=c_indigo)

    # Card 3: Provenance-Aware Evidence Matrix
    x_c3 = 13.5
    draw_arrow(x_c2 + w_card/2, y_s1, x_c3 - w_card/2, y_s1)
    draw_card(x_c3, y_s1, w_card, h_s1, "Stage 2: Convergence", "Evidence Triangulation Engine",
              ["Maps Supporting (+) & Contradicting (-) Facts",
               "Catalogs Missing Evidence (?) per candidate",
               "Provenance De-Biasing: Eliminates shared sources"],
              border=c_blue, tag_color=c_blue)

    # -------------------------------------------------------------------------
    # STAGE 2: SCORING & THE 4 TERMINAL OUTCOMES (Bottom Row, y = 2.15)
    # -------------------------------------------------------------------------
    y_s2 = 2.15
    h_s2 = 3.1
    w_hub = 3.6
    x_hub = 2.1

    # Draw Central Scoring & Stopping Rule Hub
    draw_card(x_hub, y_s2, w_hub, h_s2, "Convergence Core", "Bayesian Evidential Scoring\n& Budget Stopping Rule",
              ["Fixed exploration branch budget",
               "Likelihood ratio posterior updating",
               "Entropy-based stopping criterion",
               "Calculates calibrated confidence",
               "Selects deterministic terminal outcome"],
              bg='#FFFFFF', border=c_dark, tag_color=c_dark)

    # Connect Stage 1 Card 3 (Evidence) down and across to Scoring Hub
    ax.plot([x_c3, x_c3], [y_s1 - h_s1/2, 4.75], color=c_blue, lw=2, zorder=5)
    ax.plot([x_c3, x_hub], [4.75, 4.75], color=c_blue, lw=2, zorder=5)
    draw_arrow(x_hub, 4.75, x_hub, y_s2 + h_s2/2, color=c_blue, lw=2)

    # Badge on connector line
    ax.text(8.0, 4.75, "Evaluates Hypotheses Against Evidence Graph with Provenance Filtering",
            ha='center', va='center', fontsize=9, fontweight='bold', color=c_blue,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor=c_blue, lw=1.2), zorder=6)

    # Now Draw the 4 Deterministic Terminal Outcomes (Clean top distributor bus at y = 4.15)
    w_out = 2.7
    h_out = 3.1
    y_out = y_s2
    xs_out = [5.5, 8.5, 11.5, 14.5]

    # Clean distributor line: routes out of Hub at top-right (x=3.5, y=3.65) -> Up to y_bus (4.15) -> Across to 14.5
    y_bus = 4.15
    ax.plot([3.5, 3.5], [y_s2 + h_s2/2, y_bus], color=c_dark, lw=2, zorder=5)
    ax.plot([3.5, xs_out[3]], [y_bus, y_bus], color=c_dark, lw=2, zorder=5)

    # Clean vertical drop arrows into each of the 4 cards!
    for xo in xs_out:
        draw_arrow(xo, y_bus, xo, y_out + h_out/2, color=c_dark, lw=2)

    # Outcome label tag above distributor
    ax.text(9.9, y_bus + 0.22, "DETERMINISTIC TERMINAL OUTCOMES (ONE OF FOUR SELECTED)",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_dark,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1), zorder=6)

    # OUTCOME 1: SELECT
    draw_card(xs_out[0], y_out, w_out, h_out, "Outcome 1", "SELECT",
              ["Decisive cause chosen",
               "Posterior > threshold",
               "High separation margin",
               "Explainable audit trail"],
              bg='#F0FDF4', border=c_green, tag_color=c_green, title_color='#065F46')

    # OUTCOME 2: SYNTHESIZE
    draw_card(xs_out[1], y_out, w_out, h_out, "Outcome 2", "SYNTHESIZE",
              ["Composite cause",
               "Compatible co-factors",
               "Merges non-exclusive hypotheses",
               "Unifies disjoint clues"],
              bg='#EFF6FF', border=c_blue, tag_color=c_blue, title_color='#1E40AF')

    # OUTCOME 3: RECOMMEND TEST
    draw_card(xs_out[2], y_out, w_out, h_out, "Outcome 3", "TEST",
              ["Tie-breaking diagnostic",
               "Prescribes single test",
               "Max Information Gain",
               "Resolves top ambiguity"],
              bg='#FAF5FF', border=c_purple, tag_color=c_purple, title_color='#5B21B6')

    # OUTCOME 4: ABSTAIN
    draw_card(xs_out[3], y_out, w_out, h_out, "Outcome 4", "ABSTAIN",
              ["Explicit refusal to guess",
               "Insufficient evidence",
               "Null / Unknown (H₀) leads",
               "Honest confidence alert"],
              bg='#FFFBEB', border=c_amber, tag_color=c_amber, title_color='#92400E')

    # Bottom Footer
    ax.text(8.0, 0.25, "Designed for L&T Hackathon • AI Track: Evidence-Grounded Divergence & Convergence Reasoning Engine",
            ha='center', va='center', fontsize=9, color=c_sub, style='italic')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"OrthoDialectic Flowchart saved successfully to {output_path}")

if __name__ == "__main__":
    create_ortho_flowchart("c:/Users/mdbaa/OneDrive/Desktop/L&T/ortho_dialectic_flowchart.png")
