import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI CLM Paralegal", layout="wide")

st.title("⚖️ AI CLM Paralegal Assistant")
st.write("Upload a contract (PDF or text) and get a full legal risk analysis.")

# Initialize session state for contract Q&A
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False
if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = []


def display_results(result):
    """Render the full-analysis response (risks, legal, bias, stress, fraud, recommendation)."""
    st.success("Analysis Completed ✅")

    st.subheader("📊 Risk Analysis")
    st.write(result.get("risks"))

    st.subheader("⚖ Legal Intelligence")
    st.write(result.get("legal_intelligence"))

    st.subheader("📈 Bias Analysis")
    st.write(result.get("bias_analysis"))

    st.subheader("🧪 Stress Test")
    st.write(result.get("stress_test"))

    st.subheader("🚨 Fraud Indicators")
    st.write(result.get("fraud_indicators"))

    st.subheader("🏁 Final Recommendation")
    rec = result.get("recommendation")
    if isinstance(rec, dict):
        st.write(rec.get("final_recommendation") or rec.get("error") or rec)
    else:
        st.write(rec)


# ---------------------------
# INPUT SECTION
# ---------------------------

input_option = st.radio(
    "Choose Input Type:",
    ["Upload PDF", "Paste Contract Text"]
)

contract_text = None
uploaded_file = None

if input_option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload Contract PDF", type=["pdf"])

elif input_option == "Paste Contract Text":
    contract_text = st.text_area("Paste Contract Here", height=250)

# ---------------------------
# ANALYSIS BUTTON
# ---------------------------

if st.button("Run Full Analysis"):

    if input_option == "Upload PDF" and uploaded_file:
        with st.spinner("Analyzing PDF..."):
            response = requests.post(
                f"{BACKEND_URL}/full-analysis-pdf",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
            )
            if response.status_code == 200:
                data = response.json()
                display_results(data)
                st.session_state["analysis_done"] = True
            else:
                st.error(response.text)

    elif input_option == "Paste Contract Text" and contract_text:
        with st.spinner("Analyzing Text..."):
            response = requests.post(
                f"{BACKEND_URL}/full-analysis",
                json={"contract_text": contract_text},
            )
            if response.status_code == 200:
                data = response.json()
                display_results(data)
                st.session_state["analysis_done"] = True
            else:
                st.error(response.text)

    else:
        st.warning("Please provide input before running analysis.")


# ---------------------------
# CONTRACT Q&A SECTION
# ---------------------------

st.markdown("---")
st.subheader("💬 Ask questions about this contract")

if not st.session_state.get("analysis_done"):
    st.info("Run a full analysis first to enable contract Q&A.")
else:
    question = st.text_input("Ask a question about this contract:")

    if question:
        with st.spinner("Thinking..."):
            resp = requests.post(
                f"{BACKEND_URL}/rag/ask-with-memory",
                json={
                    "session_id": st.session_state["session_id"],
                    "question": question,
                },
            )

        if resp.status_code == 200:
            answer = resp.json().get("answer")
            st.session_state["qa_history"].append({"q": question, "a": answer})
        else:
            st.error(resp.text)

    # Display conversation history
    for pair in st.session_state["qa_history"]:
        st.markdown(f"**You:** {pair['q']}")
        st.markdown(f"**Assistant:** {pair['a']}")

