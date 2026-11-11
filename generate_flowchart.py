import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_flowchart(output_path="flowchart.png"):
    # Set high DPI for sharp, professional rendering
    fig, ax = plt.subplots(figsize=(10, 16), dpi=300)
    fig.patch.set_facecolor('#F8FAFC') # Clean slate/off-white background
    ax.set_facecolor('#F8FAFC')

    # Coordinate system: 0 to 10 x, 0 to 20 y
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 20.5)
    ax.axis('off')

    # Color Palette - Professional Modern Engineering
    c_primary = '#1E3A8A'      # Deep Navy
    c_blue = '#2563EB'         # Royal Blue
    c_box_bg = '#FFFFFF'       # Clean white box
    c_border = '#0284C7'       # Ocean blue border
    c_text_main = '#0F172A'    # Slate 900
    c_text_sub = '#475569'     # Slate 600
    c_yes = '#059669'          # Emerald Green
    c_no = '#DC2626'           # Crimson Red
    c_decision = '#F59E0B'     # Amber / Gold

    def draw_box(x, y, w, h, title, subtitle="", bg='#FFFFFF', border='#2563EB', title_color='#0F172A', badge=""):
        # Shadow effect
        shadow = patches.FancyBboxPatch(
            (x - w/2 + 0.05, y - h/2 - 0.06), w, h,
            boxstyle="round,pad=0.12,rounding_size=0.25",
            facecolor='#CBD5E1', edgecolor='none', alpha=0.45, zorder=2
        )
        ax.add_patch(shadow)

        # Main box
        rect = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.12,rounding_size=0.25",
            facecolor=bg, edgecolor=border, linewidth=2, zorder=3
        )
        ax.add_patch(rect)

        # Text
        if subtitle:
            ax.text(x, y + 0.22, title, ha='center', va='center',
                    fontsize=12, fontweight='bold', color=title_color, zorder=4)
            ax.text(x, y - 0.28, subtitle, ha='center', va='center',
                    fontsize=9.5, fontweight='normal', color=c_text_sub, style='italic', zorder=4)
        else:
            ax.text(x, y, title, ha='center', va='center',
                    fontsize=12.5, fontweight='bold', color=title_color, zorder=4)

    def draw_diamond(x, y, w, h, title, subtitle="", border='#D97706'):
        # Shadow
        shadow_pts = [(x, y + h/2 - 0.06), (x + w/2 + 0.05, y - 0.06), (x, y - h/2 - 0.06), (x - w/2 + 0.05, y - 0.06)]
        shadow = patches.Polygon(shadow_pts, closed=True, facecolor='#CBD5E1', edgecolor='none', alpha=0.45, zorder=2)
        ax.add_patch(shadow)

        # Diamond polygon
        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        diamond = patches.Polygon(pts, closed=True, facecolor='#FFFBEB', edgecolor=border, linewidth=2.5, zorder=3)
        ax.add_patch(diamond)

        ax.text(x, y + 0.12, title, ha='center', va='center',
                fontsize=12, fontweight='bold', color='#92400E', zorder=4)
        if subtitle:
            ax.text(x, y - 0.26, subtitle, ha='center', va='center',
                    fontsize=9, fontweight='normal', color='#B45309', zorder=4)

    def draw_arrow(x1, y1, x2, y2, color='#475569', lw=2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    mutation_scale=18, shrinkA=0, shrinkB=0),
                    zorder=5)

    # Title header at top
    ax.text(5, 19.8, "Hybrid Digital Twin for Industrial Pumps", ha='center', va='center',
            fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(5, 19.3, "AI-Driven Predictive Modelling & Physics-Validated Architecture", ha='center', va='center',
            fontsize=10.5, color='#64748B')
    ax.plot([2.5, 7.5], [18.9, 18.9], color='#94A3B8', lw=1, zorder=1)

    # Node coordinates (x, y)
    box_w = 6.2
    box_h = 1.05

    # 1. Collect Pump Data
    y1 = 17.8
    draw_box(5, y1, box_w, box_h, "1. Collect Real-Time Pump Data",
             "Telemetry: Vibration, Pressure, Flow Rate, Current & Temperature",
             bg='#FFFFFF', border='#0284C7')

    # 2. Build AI Model
    y2 = 15.8
    draw_arrow(5, y1 - box_h/2 - 0.12, 5, y2 + box_h/2 + 0.12)
    draw_box(5, y2, box_w, box_h, "2. Train Machine Learning Surrogate Model",
             "Learns baseline operating curves & system dynamics",
             bg='#FFFFFF', border='#0284C7')

    # 3. Predict Machine Behaviour
    y3 = 13.8
    draw_arrow(5, y2 - box_h/2 - 0.12, 5, y3 + box_h/2 + 0.12)
    draw_box(5, y3, box_w, box_h, "3. Predict Machine Behaviour & Health",
             "Forecasts power draw, head degradation & cavitation risk",
             bg='#FFFFFF', border='#0284C7')

    # 4. Test Different Actions
    y4 = 11.8
    draw_arrow(5, y3 - box_h/2 - 0.12, 5, y4 + box_h/2 + 0.12)
    draw_box(5, y4, box_w, box_h, "4. Simulate Operational Actions",
             "Evaluates what-if adjustments: speed control, valve throttling",
             bg='#FFFFFF', border='#0284C7')

    # 5. Check Prediction Reliability
    y5 = 9.8
    draw_arrow(5, y4 - box_h/2 - 0.12, 5, y5 + box_h/2 + 0.12)
    draw_box(5, y5, box_w, box_h, "5. Evaluate Prediction Reliability",
             "Dynamic uncertainty estimation & residual error bounds check",
             bg='#FFFFFF', border='#0284C7')

    # 6. Decision Diamond: Reliable?
    y6 = 7.8
    draw_arrow(5, y5 - box_h/2 - 0.12, 5, y6 + 0.8)
    draw_diamond(5, y6, 3.8, 1.6, "Is Prediction", "Reliable?")

    # Branches: Left (Yes) / Right (No)
    y_branch = 5.5
    branch_w = 3.6
    branch_h = 1.05

    # Path for YES (Left)
    # Arrow out left of diamond
    ax.plot([5 - 1.9, 2.5], [y6, y6], color=c_yes, lw=2.2, zorder=5)
    ax.plot([2.5, 2.5], [y6, y_branch + branch_h/2 + 0.12], color=c_yes, lw=2.2, zorder=5)
    draw_arrow(2.5, y_branch + branch_h/2 + 0.2, 2.5, y_branch + branch_h/2 + 0.12, color=c_yes, lw=2.2)
    
    # YES label pill
    ax.text(3.4, y6 + 0.25, "YES", ha='center', va='center',
            fontsize=10, fontweight='bold', color=c_yes,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#DCFCE7', edgecolor=c_yes, lw=1.2), zorder=6)

    draw_box(2.5, y_branch, branch_w, branch_h, "Show Validated Results",
             "Deploy recommended setpoints to dashboard",
             bg='#F0FDF4', border=c_yes, title_color='#065F46')

    # Path for NO (Right)
    # Arrow out right of diamond
    ax.plot([5 + 1.9, 7.5], [y6, y6], color=c_no, lw=2.2, zorder=5)
    ax.plot([7.5, 7.5], [y6, y_branch + branch_h/2 + 0.12], color=c_no, lw=2.2, zorder=5)
    draw_arrow(7.5, y_branch + branch_h/2 + 0.2, 7.5, y_branch + branch_h/2 + 0.12, color=c_no, lw=2.2)

    # NO label pill
    ax.text(6.6, y6 + 0.25, "NO", ha='center', va='center',
            fontsize=10, fontweight='bold', color=c_no,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEE2E2', edgecolor=c_no, lw=1.2), zorder=6)

    draw_box(7.5, y_branch, branch_w, branch_h, "Trigger Safety Warning",
             "Flag low confidence & notify operator",
             bg='#FEF2F2', border=c_no, title_color='#991B1B')

    # 7. Compare with Simulator
    y7 = 3.3
    # Connect both branches down to Simulator
    ax.plot([2.5, 2.5], [y_branch - branch_h/2 - 0.12, y7 + 0.9], color='#475569', lw=2, zorder=5)
    ax.plot([2.5, 5], [y7 + 0.9, y7 + 0.9], color='#475569', lw=2, zorder=5)
    
    ax.plot([7.5, 7.5], [y_branch - branch_h/2 - 0.12, y7 + 0.9], color='#475569', lw=2, zorder=5)
    ax.plot([7.5, 5], [y7 + 0.9, y7 + 0.9], color='#475569', lw=2, zorder=5)

    draw_arrow(5, y7 + 0.9, 5, y7 + box_h/2 + 0.12, color='#475569', lw=2)

    draw_box(5, y7, box_w, box_h, "7. Cross-Verify with Physics Simulator",
             "High-fidelity hydraulic simulation validates boundary behavior",
             bg='#EFF6FF', border='#3B82F6', title_color='#1E40AF')

    # 8. Final Report
    y8 = 1.3
    draw_arrow(5, y7 - box_h/2 - 0.12, 5, y8 + box_h/2 + 0.12, color='#475569', lw=2)
    draw_box(5, y8, box_w, box_h, "8. Final Decision & Diagnostic Report",
             "",
             bg='#1E293B', border='#0F172A', title_color='#F8FAFC')
    
    # Subtitle with crisp light text
    ax.text(5, y8 - 0.28, "Actionable maintenance insights, safe operating limits & RUL",
            ha='center', va='center', fontsize=9.5, color='#94A3B8', style='italic', zorder=4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Flowchart successfully saved to {output_path}")

if __name__ == "__main__":
    create_flowchart("c:/Users/mdbaa/OneDrive/Desktop/L&T/flowchart.png")
