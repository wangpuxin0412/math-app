import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Gradient & Steepest Ascent Demo", layout="wide")

# --- Title and Introduction ---
st.title("🏔️ Multivariable Functions: Gradient & Steepest Ascent")
st.markdown("""
**Assignment Context:** This interactive application visualizes the concept of gradients for a function of two variables $z=f(x,y)$.
The **Gradient Vector** $\\nabla f$ always points in the direction of the **steepest ascent** (fastest increase of the function).
""")

# --- Sidebar: User Controls ---
st.sidebar.header("1. Select Function Model")
function_option = st.sidebar.selectbox(
    "Choose a surface example:",
    ("Peak (Paraboloid)", "Saddle (Hyperbolic Paraboloid)", "Waves (Sin/Cos)")
)

st.sidebar.header("2. Adjust Position (x, y)")
x_val = st.sidebar.slider("X Coordinate", -2.0, 2.0, 0.5, 0.1)
y_val = st.sidebar.slider("Y Coordinate", -2.0, 2.0, 0.5, 0.1)

# --- Mathematical Logic ---
def calculate_function(name, x, y):
    if name == "Peak (Paraboloid)":
        # z = 4 - x^2 - y^2
        z = 4 - x**2 - y**2
        dz_dx = -2 * x
        dz_dy = -2 * y
        formula = r"f(x, y) = 4 - x^2 - y^2"
        
    elif name == "Saddle (Hyperbolic Paraboloid)":
        # z = x^2 - y^2
        z = x**2 - y**2
        dz_dx = 2 * x
        dz_dy = -2 * y
        formula = r"f(x, y) = x^2 - y^2"
        
    else: # Waves
        # z = sin(x) * cos(y)
        z = np.sin(x) * np.cos(y)
        dz_dx = np.cos(x) * np.cos(y)
        dz_dy = -np.sin(x) * np.sin(y)
        formula = r"f(x, y) = \sin(x) \cdot \cos(y)"
        
    return z, dz_dx, dz_dy, formula

# Calculations
z_val, grad_x, grad_y, formula_tex = calculate_function(function_option, x_val, y_val)
grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)

# --- Layout: Two Columns ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Calculations")
    st.info(f"Current Function:")
    st.latex(formula_tex)
    
    st.write("---")
    st.write(f"**Current Point:** P({x_val}, {y_val})")
    st.write(f"**Function Value (z):** {z_val:.4f}")
    
    st.write("---")
    st.write("**Partial Derivatives (Rate of Change):**")
    st.latex(rf"\frac{{\partial f}}{{\partial x}} = {grad_x:.4f}")
    st.latex(rf"\frac{{\partial f}}{{\partial y}} = {grad_y:.4f}")
    
    st.write("---")
    st.success("**Gradient Vector:**")
    st.latex(rf"\nabla f = \langle {grad_x:.4f}, {grad_y:.4f} \rangle")
    st.write(f"**Rate of Steepest Ascent (Magnitude):** {grad_magnitude:.4f}")
    
    st.caption("Note: If magnitude is 0, it indicates a critical point (e.g., peak, valley, or saddle point).")

with col2:
    st.subheader("🧊 3D Interactive Visualization")
    
    # 1. Generate Mesh Data
    x_range = np.linspace(-2.5, 2.5, 50)
    y_range = np.linspace(-2.5, 2.5, 50)
    X, Y = np.meshgrid(x_range, y_range)
    
    # Calculate Z based on selection
    if function_option == "Peak (Paraboloid)":
        Z = 4 - X**2 - Y**2
    elif function_option == "Saddle (Hyperbolic Paraboloid)":
        Z = X**2 - Y**2
    else:
        Z = np.sin(X) * np.cos(Y)
        
    # 2. Create 3D Figure
    fig = go.Figure()

    # Surface
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name='Surface'))

    # Current Point (Red Dot)
    fig.add_trace(go.Scatter3d(
        x=[x_val], y=[y_val], z=[z_val],
        mode='markers',
        marker=dict(size=8, color='red'),
        name='Current Point'
    ))

    # Gradient Arrow (Cone)
    fig.add_trace(go.Cone(
        x=[x_val], y=[y_val], z=[z_val], 
        u=[grad_x], v=[grad_y], w=[0],   
        sizemode="absolute",
        sizeref=0.5,
        anchor="tail",
        colorscale=[[0, 'red'], [1, 'red']],
        showscale=False,
        name='Gradient Direction'
    ))

    # Layout Updates
    fig.update_layout(
        title=f"3D View (Rotate/Zoom to Interact)",
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z (Height)',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Real-World Application (CO3) ---
st.write("---")
st.header("🌍 Real-World Significance")
st.markdown("""
Understanding gradients and steepest ascent is crucial in various fields:

1.  **Machine Learning & AI (Gradient Descent)**: 
    * In training AI models (like ChatGPT), the goal is to minimize an "error function". Algorithms use **Gradient Descent** to move in the opposite direction of the gradient (steepest descent) to find the lowest error, effectively "walking down the hill" to find the optimal solution.
    
2.  **Topography & Navigation**:
    * In physical geography, the gradient helps identify the steepest paths on a terrain. This is essential for planning hiking routes, water drainage systems, or understanding erosion patterns.
""")
