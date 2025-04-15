import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="np-Chart Generator", layout="centered", page_icon="📊")

# Title and Description
st.title("📊 Responsive np-Chart Generator")
st.markdown(
    "Monitor your process by tracking the **number of defective items** per sample. "
    "This np-Chart automatically calculates **control limits** and highlights any out-of-control points."
)

# Input Form
with st.form("np_chart_form"):
    st.subheader("🔧 Input Parameters")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Sample size (n)", min_value=1, value=50)
    with col2:
        p = st.number_input("Defect rate (p)", min_value=0.0, max_value=1.0, value=0.08, step=0.01)

    defectives_input = st.text_area(
        "Enter number of defectives per sample (comma-separated)",
        placeholder="e.g. 3, 5, 4, 7, 6, 2, 9, 5, 4, 8"
    )

    submit = st.form_submit_button("Plot np-Chart")

if submit:
    try:
        defectives = [int(x.strip()) for x in defectives_input.split(",") if x.strip() != ""]
        sample_numbers = list(range(1, len(defectives) + 1))

        np_bar = n * p
        sigma = np.sqrt(n * p * (1 - p))
        UCL = np_bar + 3 * sigma
        LCL = max(0, np_bar - 3 * sigma)

        # Highlight out-of-control points
        out_x = [i + 1 for i, y in enumerate(defectives) if y > UCL or y < LCL]
        out_y = [y for y in defectives if y > UCL or y < LCL]

        # Plotting
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=sample_numbers, y=defectives,
            mode='markers+lines',
            name='Observed Defectives',
            marker=dict(color='blue', size=10),
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=sample_numbers, y=[np_bar] * len(defectives),
            mode='lines', name='Center Line (CL)',
            line=dict(color='green', dash='dash')
        ))

        fig.add_trace(go.Scatter(
            x=sample_numbers, y=[UCL] * len(defectives),
            mode='lines', name='Upper Control Limit (UCL)',
            line=dict(color='red', dash='dot')
        ))

        fig.add_trace(go.Scatter(
            x=sample_numbers, y=[LCL] * len(defectives),
            mode='lines', name='Lower Control Limit (LCL)',
            line=dict(color='red', dash='dot')
        ))

        if out_x:
            fig.add_trace(go.Scatter(
                x=out_x, y=out_y,
                mode='markers',
                name='Out of Control',
                marker=dict(color='orange', size=12, symbol='diamond'),
            ))

        fig.update_layout(
            title="📈 np-Chart",
            xaxis_title="Sample Number",
            yaxis_title="Number of Defectives",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=50, b=30),
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Control Limits & Summary", expanded=True):
            st.success(f"🔹 Center Line (CL): {np_bar:.2f}")
            st.info(f"🔺 Upper Control Limit (UCL): {UCL:.2f}")
            st.info(f"🔻 Lower Control Limit (LCL): {LCL:.2f}")
            st.markdown(f"**Out of Control Points:** {out_x if out_x else 'None'}")

    except Exception as e:
        st.error(f"❌ Error processing input: {e}")
