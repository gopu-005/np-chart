import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Title
st.title("📊 np-Chart Generator (Control Chart for Number of Defectives)")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

# Sample size (constant)
n = st.sidebar.number_input("Sample size (n)", min_value=1, value=100)

# Proportion defective (p)
p = st.sidebar.number_input("Historical defect rate (p)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

# Input defectives per sample (comma-separated values)
sample_data_str = st.sidebar.text_area("Enter defectives per sample (comma-separated)", "5,7,3,6,4,10,5,4,6")

# Process input data
try:
    defectives = [int(x.strip()) for x in sample_data_str.split(",") if x.strip() != '']
    sample_numbers = list(range(1, len(defectives) + 1))

    # Control limits
    np_bar = n * p
    sigma = np.sqrt(n * p * (1 - p))
    UCL = np_bar + 3 * sigma
    LCL = max(0, np_bar - 3 * sigma)

    # Streamlit chart
    st.subheader("📈 np-Chart")

    fig = go.Figure()

    # Plot np values
    fig.add_trace(go.Scatter(
        x=sample_numbers,
        y=defectives,
        mode='markers+lines',
        name='Observed Defectives',
        marker=dict(color='blue', size=10, symbol='circle'),
        line=dict(dash='solid', width=2)
    ))

    # Center Line
    fig.add_trace(go.Scatter(
        x=sample_numbers,
        y=[np_bar]*len(defectives),
        mode='lines',
        name='Center Line (CL)',
        line=dict(color='green', dash='dash')
    ))

    # UCL
    fig.add_trace(go.Scatter(
        x=sample_numbers,
        y=[UCL]*len(defectives),
        mode='lines',
        name='Upper Control Limit (UCL)',
        line=dict(color='red', dash='dot')
    ))

    # LCL
    fig.add_trace(go.Scatter(
        x=sample_numbers,
        y=[LCL]*len(defectives),
        mode='lines',
        name='Lower Control Limit (LCL)',
        line=dict(color='red', dash='dot')
    ))

    # Highlight out-of-control points
    out_of_control_x = [i+1 for i, y in enumerate(defectives) if y > UCL or y < LCL]
    out_of_control_y = [y for y in defectives if y > UCL or y < LCL]
    if out_of_control_x:
        fig.add_trace(go.Scatter(
            x=out_of_control_x,
            y=out_of_control_y,
            mode='markers',
            name='Out of Control',
            marker=dict(color='orange', size=12, symbol='diamond'),
        ))

    # Layout
    fig.update_layout(
        title="np-Chart: Number of Defective Items per Sample",
        xaxis_title="Sample Number",
        yaxis_title="Number of Defectives",
        template="plotly_white",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show calculated limits
    st.info(f"Center Line (CL): {np_bar:.2f}")
    st.info(f"Upper Control Limit (UCL): {UCL:.2f}")
    st.info(f"Lower Control Limit (LCL): {LCL:.2f}")

except Exception as e:
    st.error(f"Error processing input: {e}")
