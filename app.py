import streamlit as st
import pandas as pd
import cv2
import numpy as np

from datetime import datetime
from fraud_detection import (
    analyse_transaction,
    scan_message,
    scan_website
)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

# SESSION STORAGE
if "history" not in st.session_state:
    st.session_state.history = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# DESIGN
st.markdown("""
<style>

.stApp {
    background-color: #080D0B;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #101A16;
}

h1, h2, h3 {
    color: #00FF88 !important;
}

.stButton button {
    background-color: #00FF88;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    background-color: #14231C;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.title("🛡️ FRAUDSHIELD AI")
st.subheader("Intelligent Cyber Fraud Detection & Prevention System")

st.caption("Your Digital Security. Our AI Protection.")

st.divider()


# SIDEBAR
st.sidebar.title("🛡️ FRAUDSHIELD")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Transaction Protection",
        "SMS Scanner",
        "Website Scanner",
        "QR Scanner",
        "Fraud Alerts",
        "Transaction History",
        "Security Assistant"
    ]
)


# SAVE RESULTS
def save_result(category, result, details):

    record = {
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "Category": category,
        "Details": details,
        "Risk": result["risk_level"],
        "Risk Score": result["risk_score"]
    }

    st.session_state.history.append(record)

    if result["risk_level"] == "HIGH RISK":
        st.session_state.alerts.append(record)


# DASHBOARD
if page == "Dashboard":

    st.header("Security Dashboard")

    total = len(st.session_state.history)

    high = sum(
        1 for x in st.session_state.history
        if x["Risk"] == "HIGH RISK"
    )

    medium = sum(
        1 for x in st.session_state.history
        if x["Risk"] == "MEDIUM RISK"
    )

    low = sum(
        1 for x in st.session_state.history
        if x["Risk"] == "LOW RISK"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Scans", total)
    c2.metric("High Risk", high)
    c3.metric("Medium Risk", medium)
    c4.metric("Low Risk", low)

    st.divider()

    st.subheader("Security Monitoring")

    if total == 0:
        st.info("No scans yet. Start analysing transactions or messages.")

    else:
        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df, use_container_width=True)

        chart_data = df["Risk"].value_counts()

        st.subheader("Fraud Risk Analysis")

        st.bar_chart(chart_data)

    st.success("FraudShield AI monitoring dashboard is active.")


# TRANSACTION PROTECTION
elif page == "Transaction Protection":

    st.header("💳 Transaction Protection")

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        step=100.0
    )

    new_receiver = st.checkbox(
        "This is a new or unverified receiver"
    )

    unusual = st.checkbox(
        "Unusual transaction activity detected"
    )

    if st.button("Analyse Transaction"):

        result = analyse_transaction(
            amount,
            new_receiver,
            unusual
        )

        st.metric("Risk Score", f"{result['risk_score']} / 100")

        if result["risk_level"] == "HIGH RISK":
            st.error("🚨 HIGH RISK TRANSACTION!")

        elif result["risk_level"] == "MEDIUM RISK":
            st.warning("⚠️ MEDIUM RISK TRANSACTION")

        else:
            st.success("✅ LOW RISK TRANSACTION")

        st.write("Risk Level:", result["risk_level"])

        st.write("Reasons:")

        if result["reasons"]:
            for reason in result["reasons"]:
                st.write("•", reason)
        else:
            st.write("No risk indicators detected by these rules.")

        save_result(
            "Transaction",
            result,
            f"₹{amount}"
        )

        if result["risk_level"] == "HIGH RISK":
            st.warning(
                "Please pause and independently verify the receiver "
                "before making any payment."
            )


# SMS SCANNER
elif page == "SMS Scanner":

    st.header("📩 SMS & Message Fraud Scanner")

    message = st.text_area(
        "Paste your suspicious SMS or message here"
    )

    st.info("Never paste your OTP, password or banking PIN.")

    if st.button("Scan Message"):

        if message.strip():

            result = scan_message(message)

            st.metric(
                "Risk Score",
                f"{result['risk_score']} / 100"
            )

            if result["risk_level"] == "HIGH RISK":
                st.error("🚨 Potential Fraud Message Detected")

            elif result["risk_level"] == "MEDIUM RISK":
                st.warning("⚠️ Suspicious Message")

            else:
                st.success("No strong warning signs detected.")

            st.write("Detected suspicious keywords:")

            st.write(result["keywords"] or "None")

            st.write("Links found:")

            st.write(result["links"] or "None")

            save_result(
                "SMS Scan",
                result,
                message[:80]
            )

        else:
            st.warning("Please enter a message first.")


# WEBSITE SCANNER
elif page == "Website Scanner":

    st.header("🌐 Website Fraud Scanner")

    url = st.text_input(
        "Enter website address"
    )

    if st.button("Check Website"):

        if url.strip():

            result = scan_website(url)

            st.metric(
                "Website Risk Score",
                f"{result['risk_score']} / 100"
            )

            if result["risk_level"] == "HIGH RISK":
                st.error("🚨 High Risk Website")

            elif result["risk_level"] == "MEDIUM RISK":
                st.warning("⚠️ Suspicious Website")

            else:
                st.success("No strong warning signs detected.")

            for reason in result["reasons"]:
                st.write("•", reason)

            save_result(
                "Website Scan",
                result,
                url
            )

            st.info(
                "This is a preliminary rule-based check, "
                "not a verified website reputation service."
            )

        else:
            st.warning("Enter a website address.")


# QR SCANNER
elif page == "QR Scanner":

    st.header("📷 QR Code Security Scanner")

    uploaded_file = st.file_uploader(
        "Upload a QR code image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        file_bytes = np.frombuffer(
            uploaded_file.read(),
            np.uint8
        )

        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        if image is not None:

            detector = cv2.QRCodeDetector()

            data, points, _ = detector.detectAndDecode(image)

            if data:

                st.success("QR Code detected!")

                st.write("QR Content:", data)

                if data.startswith(("http://", "https://")):

                    result = scan_website(data)

                    st.write(
                        "Website Risk:",
                        result["risk_level"]
                    )

                    st.write(
                        "Risk Score:",
                        result["risk_score"]
                    )

                    save_result(
                        "QR Scan",
                        result,
                        data
                    )

                else:
                    st.info(
                        "This QR code contains non-website data. "
                        "Check the destination before taking action."
                    )

            else:
                st.warning("No readable QR code found.")

        else:
            st.error("Unable to read this image.")


# FRAUD ALERTS
elif page == "Fraud Alerts":

    st.header("🚨 Security Alert Centre")

    if st.session_state.alerts:

        st.error("High-risk activities detected!")

        for alert in reversed(st.session_state.alerts):

            st.warning(
                f"{alert['Date']} | "
                f"{alert['Category']} | "
                f"{alert['Details']}"
            )

    else:

        st.success("No high-risk alerts recorded in this session.")


# TRANSACTION HISTORY
elif page == "Transaction History":

    st.header("📊 Security & Scan History")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Scan History",
            csv,
            "fraudshield_history.csv",
            "text/csv"
        )

    else:

        st.info("No transaction or scan history available.")


# SECURITY ASSISTANT
elif page == "Security Assistant":

    st.header("🤖 FraudShield Security Assistant")

    st.write(
        "Ask about common online fraud and digital security."
    )

    question = st.text_input(
        "Enter your security question"
    )

    if st.button("Get Security Advice"):

        q = question.lower()

        if "otp" in q:

            st.warning(
                "Never share your OTP with anyone, "
                "including people claiming to be bank employees."
            )

        elif "upi" in q or "payment" in q:

            st.info(
                "Never enter your UPI PIN to receive money. "
                "Verify the receiver before approving payments."
            )

        elif "link" in q or "website" in q:

            st.info(
                "Avoid unknown links. Verify website addresses "
                "before entering personal information."
            )

        elif "loan" in q:

            st.info(
                "Verify lenders through official regulatory "
                "and financial institution sources."
            )

        elif "scam" in q or "fraud" in q:

            st.warning(
                "Stop communication, do not transfer money, "
                "and contact your bank through its official channel "
                "if you suspect fraud."
            )

        else:

            st.info(
                "Stay alert. Never share passwords, OTPs or PINs. "
                "Verify suspicious requests independently."
            )


# FOOTER
st.divider()

st.caption(
    "FraudShield AI | Cyber Fraud Detection & Prevention System"
)

st.caption(
    "Prototype: Risk scores are rule-based indicators, "
    "not verified fraud determinations."
)
