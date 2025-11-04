# Horizontal risk bar for blood test indicators (configurable for 4 different metrics).
# Style mimics the sample: rounded gradient bar with soft shadow and a black value bubble with a small pointer.
# Supports both normal direction (higher = more dangerous) and reverse direction (lower = more dangerous).

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server-side rendering

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib as mpl
import io
import base64

# -------------------- Indicator Configurations --------------------
INDICATORS = {
    'bilirubin': {
        'title': 'Total Bilirubin',
        'unit': 'mg/dL',
        'vmin': 0.1,
        'vmax': 3.5,
        'ranges': [(0.1, 1.2), (1.2, 2.5), (2.5, 3.5)],
        'labels': ['0.1-1.2', '1.2-2.5', '2.5+'],
        'reverse': False  # Higher = more dangerous (red on RIGHT)
    },
    'albumin': {
        'title': 'Albumin',
        'unit': 'g/dL',
        'vmin': 1.5,
        'vmax': 5.5,
        'ranges': [(1.5, 2.0), (2.0, 3.5), (3.5, 5.5)],
        'labels': ['<2.0', '2.0-3.5', '3.5-5.5'],
        'reverse': True   # Lower = more dangerous (red on LEFT)
    },
    'inr': {
        'title': 'INR',
        'unit': '',
        'vmin': 0.8,
        'vmax': 2.5,
        'ranges': [(0.8, 1.1), (1.1, 2.0), (2.0, 2.5)],
        'labels': ['0.8-1.1', '1.1-2.0', '2.0+'],
        'reverse': False  # Higher = more dangerous (red on RIGHT)
    },
    'platelet': {
        'title': 'Platelet',
        'unit': '×10⁴ /µL',
        'vmin': 50,
        'vmax': 450,
        'ranges': [(50, 75), (75, 150), (150, 450)],
        'labels': ['<75K', '75K-150K', '150K-450K'],
        'reverse': True,  # Lower = more dangerous (red on LEFT)
        'display_multiplier': 1000,  # DB stores divided by 1000, display as full value
        'display_divisor': 10000  # Divide by 10000 for display
    }
}

# -------------------- Helpers --------------------
def lerp(a, b, t):
    return a + (b - a) * t

def gradient_colors(n=600, reverse=False):
    """Return an (n,1,3) RGB gradient: green → yellow → red (left→right).
    If reverse=True, flip the gradient (red → yellow → green)."""
    left  = np.array(mpl.colors.to_rgb("#2ecc71"))  # green
    mid   = np.array(mpl.colors.to_rgb("#f1c40f"))  # yellow
    right = np.array(mpl.colors.to_rgb("#e74c3c"))  # red
    
    if reverse:
        left, right = right, left  # Swap colors for reverse gradient
    
    arr = np.zeros((n, 1, 3), dtype=float)
    half = n // 2
    for i in range(half):
        t = i / max(1, half - 1)
        arr[i, 0, :] = lerp(left, mid, t)
    for i in range(half, n):
        t = (i - half) / max(1, n - half - 1)
        arr[i, 0, :] = lerp(mid, right, t)
    return arr

def draw_value_bubble(ax, x, y, text, fontsize=14):
    """Centered black rounded bubble with a small bottom pointer."""
    w, h = 70, 34
    # rounded capsule
    bubble = FancyBboxPatch((x - w/2, y), w, h, boxstyle="round,pad=0.02,rounding_size=8",
                            ec="none", fc="black", zorder=5)
    ax.add_patch(bubble)
    # small pointer
    tri = mpl.patches.Polygon([[x-6, y], [x+6, y], [x, y-8]], closed=True, fc="black", ec="none", zorder=5)
    ax.add_patch(tri)
    ax.text(x, y + h*0.55, text, color="white", fontsize=fontsize, fontweight="bold",
            ha="center", va="center", zorder=6)

def generate_risk_bar(indicator, value):
    """
    Generate a risk bar graph for a given indicator and value.
    Returns base64 encoded PNG image.
    
    Args:
        indicator (str): One of 'bilirubin', 'albumin', 'inr', 'platelet'
        value (float): The value to display on the graph
    
    Returns:
        str: Base64 encoded PNG image
    """
    if indicator not in INDICATORS:
        raise ValueError(f"Invalid indicator: {indicator}")
    
    # Get configuration
    config = INDICATORS[indicator]
    title = config['title']
    unit = config['unit']
    vmin = config['vmin']
    vmax = config['vmax']
    ranges = config['ranges']
    labels = config['labels']
    reverse = config['reverse']
    
    # Handle platelet display multiplier
    display_value = value
    if indicator == 'platelet' and 'display_multiplier' in config:
        display_value = value * config['display_multiplier']
    
    # -------------------- Figure --------------------
    fig = plt.figure(figsize=(8, 2.2))
    ax = plt.axes([0,0,1,1])
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 220)
    ax.axis('off')
    
    # Title
    ax.text(20, 200, title, fontsize=16, fontweight="bold", va="top")
    
    # Bar geometry
    bar_x, bar_y = 40, 80
    bar_w, bar_h = 720, 36
    radius = bar_h / 2
    
    # Soft shadow (light gray rounded rectangle, slightly offset)
    shadow = FancyBboxPatch((bar_x, bar_y-5), bar_w, bar_h, boxstyle=f"round,pad=0,rounding_size={radius}",
                            ec="none", fc="#e6e6e6", zorder=0)
    ax.add_patch(shadow)
    
    # White housing
    housing = FancyBboxPatch((bar_x, bar_y), bar_w, bar_h, boxstyle=f"round,pad=0,rounding_size={radius}",
                             ec="none", fc="white", zorder=1)
    ax.add_patch(housing)
    
    # Gradient fill (imshow clipped to rounded rect)
    grad = gradient_colors(1000, reverse=reverse)
    im = ax.imshow(grad.transpose(1,0,2), extent=(bar_x, bar_x+bar_w, bar_y, bar_y+bar_h),
                   origin="lower", zorder=2, interpolation="bicubic")
    im.set_clip_path(housing)
    
    # Outline
    outline = FancyBboxPatch((bar_x, bar_y), bar_w, bar_h, boxstyle=f"round,pad=0,rounding_size={radius}",
                             ec="#cccccc", fc="none", lw=2, zorder=3)
    ax.add_patch(outline)
    
    # Value mapping
    v = max(vmin, min(vmax, value))
    t = (v - vmin) / (vmax - vmin + 1e-9)
    px = bar_x + t * bar_w
    
    # Value bubble (display formatted value WITHOUT unit)
    if indicator == 'platelet':
        # Divide by 10000 and show 2 decimal places
        bubble_text = f"{display_value / 10000:.2f}"
    else:
        bubble_text = f"{display_value:.1f}"
    draw_value_bubble(ax, px, bar_y + bar_h + 20, bubble_text, fontsize=14)

    # Unit label in bottom right corner
    ax.text(bar_x + bar_w, bar_y - 25, f"{unit}", fontsize=9, ha="right", va="top", color="#666666")

    # Optional ticks for ranges
    for (a, b), lab in zip(ranges, labels):
        ta = (a - vmin) / (vmax - vmin); tb = (b - vmin) / (vmax - vmin)
        mx = bar_x + (ta + tb)/2 * bar_w
        ax.text(mx, bar_y - 12, lab, fontsize=8, ha="center", va="top", color="#555555")
    
    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, transparent=True)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return img_base64
