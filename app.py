import streamlit as st

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #080D0B;
    color: #00FF88;
}
h1, h2, h3 {
    color: #00FF88 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ FraudShield AI")

st.subheader("Intelligent Cyber Fraud Detection & Prevention System")

st.success("Welcome to FraudShield AI!")

st.write("AI-Powered Cyber Fraud Detection Dashboard")

st.divider()

st.header("Transaction Analysis")

amount = st.number_input(
    "Enter Transaction Amount (₹)",
    min_value=0.0,
    step=100.0
)

if st.button("Analyse Transaction"):
    if amount >= 50000:
        st.error("HIGH RISK - Please verify this transaction!")
    elif amount >= 10000:
        st.warning("MEDIUM RISK - Additional verification recommended.")
    else:
        st.success("LOW RISK - No amount-based alert.")

st.caption("FraudShield AI | Cyber Security Project")
