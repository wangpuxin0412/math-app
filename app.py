import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 页面配置 ---
st.set_page_config(page_title="梯度与最陡上升方向演示", layout="wide")

# --- 标题与简介 ---
st.title("🏔️ 多元函数可视化：梯度与最陡上升方向")
st.markdown("""
**作业说明：** 本应用旨在帮助理解二元函数 $z=f(x,y)$ 的梯度概念。
梯度向量 $\\nabla f$ 总是指向函数值增长最快（最陡峭）的方向。
""")

# --- 侧边栏：用户交互区 ---
st.sidebar.header("1. 选择函数模型")
function_option = st.sidebar.selectbox(
    "请选择一个曲面示例：",
    ("山峰 (抛物面)", "马鞍面 (双曲抛物面)", "波浪 (正弦余弦)")
)

st.sidebar.header("2. 调整位置 (x, y)")
x_val = st.sidebar.slider("X 坐标", -2.0, 2.0, 0.5, 0.1)
y_val = st.sidebar.slider("Y 坐标", -2.0, 2.0, 0.5, 0.1)

# --- 数学逻辑定义 ---
# 我们定义三个不同的函数及其偏导数
def calculate_function(name, x, y):
    if name == "山峰 (抛物面)":
        # z = 4 - x^2 - y^2
        z = 4 - x**2 - y**2
        dz_dx = -2 * x
        dz_dy = -2 * y
        formula = r"f(x, y) = 4 - x^2 - y^2"
        
    elif name == "马鞍面 (双曲抛物面)":
        # z = x^2 - y^2
        z = x**2 - y**2
        dz_dx = 2 * x
        dz_dy = -2 * y
        formula = r"f(x, y) = x^2 - y^2"
        
    else: # 波浪
        # z = sin(x) * cos(y)
        z = np.sin(x) * np.cos(y)
        dz_dx = np.cos(x) * np.cos(y)
        dz_dy = -np.sin(x) * np.sin(y)
        formula = r"f(x, y) = \sin(x) \cdot \cos(y)"
        
    return z, dz_dx, dz_dy, formula

# 获取当前点的计算结果
z_val, grad_x, grad_y, formula_tex = calculate_function(function_option, x_val, y_val)
grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)

# --- 页面布局：分两列 ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 数学计算结果")
    st.info(f"当前选择的函数：")
    st.latex(formula_tex)
    
    st.write("---")
    st.write(f"**当前位置：** P({x_val}, {y_val})")
    st.write(f"**函数高度 (z)：** {z_val:.4f}")
    
    st.write("---")
    st.write("**偏导数 (变化率)：**")
    st.latex(rf"\frac{{\partial f}}{{\partial x}} = {grad_x:.4f}")
    st.latex(rf"\frac{{\partial f}}{{\partial y}} = {grad_y:.4f}")
    
    st.write("---")
    st.success("**梯度向量 (Gradient):**")
    st.latex(rf"\nabla f = \langle {grad_x:.4f}, {grad_y:.4f} \rangle")
    st.write(f"**最陡上升的速率 (模长)：** {grad_magnitude:.4f}")
    
    st.caption("注：如果模长为0，说明到达了临界点（如山顶或鞍点）。")

with col2:
    st.subheader("🧊 3D 交互可视化")
    
    # 1. 生成网格数据用于画曲面
    x_range = np.linspace(-2.5, 2.5, 50)
    y_range = np.linspace(-2.5, 2.5, 50)
    X, Y = np.meshgrid(x_range, y_range)
    
    # 根据选择计算整个网格的高度 Z
    if function_option == "山峰 (抛物面)":
        Z = 4 - X**2 - Y**2
    elif function_option == "马鞍面 (双曲抛物面)":
        Z = X**2 - Y**2
    else:
        Z = np.sin(X) * np.cos(Y)
        
    # 2. 创建 3D 图形
    fig = go.Figure()

    # 添加曲面
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name='地形曲面'))

    # 添加当前的点 (红球)
    fig.add_trace(go.Scatter3d(
        x=[x_val], y=[y_val], z=[z_val],
        mode='markers',
        marker=dict(size=8, color='red'),
        name='当前位置'
    ))

    # 添加梯度箭头 (使用 Cone)
    # 这是一个可视化的技巧：为了让箭头看得清，我们把它画在点的位置
    # 箭头的方向由 (grad_x, grad_y) 决定
    # 为了美观，我们让箭头稍微指向空中一点点，或者就平贴着
    fig.add_trace(go.Cone(
        x=[x_val], y=[y_val], z=[z_val], # 箭头的起点
        u=[grad_x], v=[grad_y], w=[0],   # 箭头的向量分量 (这里设w=0表示在水平面上看方向)
        sizemode="absolute",
        sizeref=0.5,
        anchor="tail",
        colorscale=[[0, 'red'], [1, 'red']],
        showscale=False,
        name='梯度方向'
    ))

    # 更新图表布局
    fig.update_layout(
        title=f"3D 视图 (请尝试用鼠标旋转/缩放)",
        scene=dict(
            xaxis_title='X 轴',
            yaxis_title='Y 轴',
            zaxis_title='Z (函数值)',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- 现实世界联系 (CO3) ---
st.write("---")
st.header("🌍 现实世界的应用 (Real-World Significance)")
st.markdown("""
这个应用演示的原理不仅仅是数学公式，它在现实世界有广泛应用：

1.  **机器学习 (Machine Learning)**: 
    * 在训练 AI 时，我们需要找到误差最小的参数。计算机会计算**梯度下降 (Gradient Descent)**，也就是沿着梯度的反方向（下山最快的方向）一步步调整参数，直到找到最优解。
2.  **地理与导航**:
    * 在复杂地形中，梯度帮助我们识别哪里是山脊（梯度为0但在某个方向弯曲）或最陡峭的攀登路径。
""")
