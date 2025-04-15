import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="np-Chart Generator", layout="centered", page_icon="📊")

# Title
st.title("📊 Responsive np-Chart Generator")
st.markdown("Track the number of defectives per sample using an **np-Chart** and view full solution steps.")

# Input Form
with st.form("np_chart_form"):
    st.subheader("🔧 Required Input Parameters")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Sample size (n)", min_value=1, value=None, format="%d", help="Same sample size for all samples")
    with col2:
        p = st.number_input("Defect rate (p)", min_value=0.0, max_value=1.0, value=None, format="%.2f", help="Historical defect rate (e.g., 0.08)")

    defectives_input = st.text_area(
        "Number of defectives per sample (comma-separated)",
        placeholder="e.g. 3, 5, 4, 7, 6, 2, 9, 5, 4, 8"
    )

    col_plot, col_steps = st.columns([1, 1])
    submit = col_plot.form_submit_button("📈 Plot np-Chart")
    show_steps = col_steps.form_submit_button("🧮 Show Steps")

# Validate inputs before proceeding
inputs_valid = n is not None and p is not None and defectives_input.strip() != ""

if submit or show_steps:
    if not inputs_valid:
        st.error("❗ Please fill in **all required fields** before continuing.")
    else:
        try:
            defectives = [int(x.strip()) for x in defectives_input.split(",") if x.strip() != ""]
            sample_numbers = list(range(1, len(defectives) + 1))

            # Control Chart Calculations
            np_bar = n * p
            sigma = np.sqrt(n * p * (1 - p))
            UCL = np_bar + 3 * sigma
            LCL = max(0, np_bar - 3 * sigma)

            out_x = [i + 1 for i, y in enumerate(defectives) if y > UCL or y < LCL]
            out_y = [y for y in defectives if y > UCL or y < LCL]

            # 📈 Plot chart if requested
            if submit:
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

            # 🧮 Show solution steps if requested
            if show_steps:
                with st.expander("📘 Step-by-Step Math Solution", expanded=True):
                    st.markdown("### Step 1: Calculate the Expected Number of Defectives")
                    st.latex(r"\bar{np} = n \times p = " + f"{n} \\times {p} = {np_bar:.2f}")

                    st.markdown("### Step 2: Calculate the Standard Deviation")
                    st.latex(r"\sigma = \sqrt{n \times p \times (1 - p)}")
                    st.latex(rf"\sigma = \sqrt{{{n} \times {p} \times (1 - {p})}} = {sigma:.3f}")

                    st.markdown("### Step 3: Calculate Control Limits")
                    st.latex(rf"UCL = \bar{{np}} + 3\sigma = {np_bar:.2f} + 3 \times {sigma:.3f} = {UCL:.2f}")
                    st.latex(rf"LCL = \bar{{np}} - 3\sigma = {np_bar:.2f} - 3 \times {sigma:.3f} = {LCL:.2f}")
                    if LCL < 0:
                        st.markdown("Since LCL is negative, we set:")
                        st.latex(rf"LCL = 0")

                    st.markdown("### Step 4: Sample Observations")
                    st.write(f"Samples: {defectives}")

                    st.markdown("### Step 5: Identify Out-of-Control Points")
                    if out_x:
                        st.warning(f"🔺 Out-of-control points found at sample(s): {out_x}")
                    else:
                        st.success("✅ All points are within control limits.")

        except ValueError:
            st.error("❌ Invalid input. Please enter comma-separated integers for defectives.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
    