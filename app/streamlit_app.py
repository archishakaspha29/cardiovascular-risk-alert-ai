import streamlit as st
from typing import List

st.set_page_config(
    page_title="Cardiovascular Risk-Alert Tool",
    page_icon="❤️",
    layout="wide",
)

# --- Stronger custom styles: higher-contrast background, thicker borders --------
st.markdown(
    """
    <style>
    /* Page background gradient with stronger contrast */
    .stApp {
        background: linear-gradient(180deg, #e6f0ff 0%, #ffffff 60%);
        color: #0b1220;
        min-height: 100vh;
    }

    /* Top banner (stronger) */
    .top-banner-strong {
        background: linear-gradient(90deg, #ef4444 0%, #f97316 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 14px;
        box-shadow: 0 8px 30px rgba(249,115,22,0.12);
        font-weight: 700;
        text-align: center;
        font-size: 15px;
    }

    /* Make the column "cards" more visible with thicker borders and contrast */
    .stColumns > div:nth-child(1) {
        background: #eaf4ff;
        border: 2px solid #1d4ed8; /* blue */
        border-radius: 12px;
        padding: 20px 18px;
        box-shadow: 0 6px 20px rgba(29,78,216,0.06);
    }

    .stColumns > div:nth-child(2) {
        background: #ffffff;
        border: 2px solid #0ea5a4; /* teal */
        border-radius: 12px;
        padding: 22px 20px;
        box-shadow: 0 8px 28px rgba(14,165,164,0.04);
    }

    .stColumns > div:nth-child(3) {
        background: #fff7ed;
        border: 2px solid #f97316; /* orange */
        border-radius: 12px;
        padding: 20px 18px;
        box-shadow: 0 6px 20px rgba(249,115,22,0.06);
    }

    /* Ensure headings inside cards have good contrast */
    .stColumns h2, .stColumns h3, .stColumns h1 {
        margin-top: 6px;
        margin-bottom: 10px;
        color: #0b1220;
    }

    /* Stronger styled call-to-action button look */
    button.stButton>button {
        background: linear-gradient(90deg,#ef4444,#f97316) !important;
        color: white !important;
        border: none !important;
        padding: 10px 16px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 24px rgba(249,115,22,0.12) !important;
    }

    /* Make alerts stand out more */
    .stAlert {
        border-left: 6px solid rgba(14,165,164,0.9) !important;
        border-radius: 8px;
        padding: 12px 14px !important;
    }

    /* Images rounded and full width inside card */
    .stImage img {
        border-radius: 8px;
        max-width: 100%;
        height: auto;
        display:block;
        margin-left:auto;
        margin-right:auto;
    }

    /* Footer caption spacing + muted color */
    .stCaption {
        margin-top: 14px;
        color: #334155;
    }

    /* Responsive tweaks: stack columns on narrow screens */
    @media (max-width: 900px) {
        .stColumns > div { padding: 12px; }
        .top-banner-strong { font-size: 13px; padding: 8px 12px; }
    }
    </style>

    <div class="top-banner-strong">Cardiovascular Risk-Alert Tool — educational prototype (not a medical diagnosis)</div>
    """,
    unsafe_allow_html=True,
)

# --- Helper functions -------------------------------------------------

def compute_risk_score(age: int, resting_bp: int, cholesterol: int, max_hr: int,
                       chest_pain: str, exercise_angina: str,
                       secondhand_smoke: str, healthcare_access: str) -> (int, List[str]):
    score = 0
    factors = []

    # Age risk
    if age >= 65:
        score += 2
        factors.append("Older age")
    elif age >= 45:
        score += 1
        factors.append("Middle-age risk factor")

    # Cholesterol risk
    if cholesterol >= 240:
        score += 2
        factors.append("High cholesterol")
    elif cholesterol >= 200:
        score += 1
        factors.append("Borderline cholesterol")

    # Blood pressure risk
    if resting_bp >= 140:
        score += 2
        factors.append("High blood pressure")
    elif resting_bp >= 120:
        score += 1
        factors.append("Elevated blood pressure")

    # Maximum heart rate
    if max_hr < 100:
        score += 1
        factors.append("Lower maximum heart rate")

    # Exercise-induced angina
    if exercise_angina == "Yes":
        score += 2
        factors.append("Exercise-induced angina")

    # Chest pain category
    if chest_pain == "Typical Angina":
        score += 2
        factors.append("Typical angina chest pain")
    elif chest_pain == "Asymptomatic":
        score += 1
        factors.append("Asymptomatic chest pain category")

    # Secondhand smoke exposure
    if secondhand_smoke == "Yes":
        score += 1
        factors.append("Secondhand smoke exposure")
    elif secondhand_smoke == "Not Sure":
        factors.append("Possible secondhand smoke exposure")

    # Healthcare access barrier
    if healthcare_access == "Yes":
        score += 1
        factors.append("Difficulty accessing timely healthcare")
    elif healthcare_access == "Sometimes":
        factors.append("Occasional difficulty accessing timely healthcare")

    return score, factors


# --- Layout -----------------------------------------------------------

st.title("AI-Assisted Cardiovascular Risk-Alert Tool")
st.markdown(
    "This educational prototype supports cardiovascular risk awareness and encourages early care-seeking. "
    "It is NOT a medical diagnostic tool."
)

cols = st.columns([1, 2, 1])  # left, middle, right
left, middle, right = cols

# Left column: links, quick info, resources
with left:
    st.header("About & Links")
    st.markdown(
        "- **Prototype purpose**: educational risk-awareness and care navigation suggestions.\n"
        "- **Source code**: [GitHub repository](https://github.com/archishakaspha29/cardiovascular-risk-alert-ai)\n"
        "- **Datasets used**: public heart disease datasets (included in /data)"
    )

    st.markdown("---")
    st.subheader("Quick tips")
    st.write(
        "- If you have emergency symptoms (chest pain, fainting, severe breathlessness) seek urgent care.\n"
        "- This tool shows general risk indicators only."
    )

    st.markdown("---")
    st.subheader("Contact / Learn more")
    st.write("Author: archishakaspha29 · Educational project")

# Middle column: interactive form (main app)
with middle:
    st.header("Enter Health Information")

    with st.form(key="risk_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=40)

        resting_bp = st.number_input(
            "Resting Blood Pressure / Systolic BP (mm Hg)", min_value=50, max_value=250, value=120
        )

        cholesterol = st.number_input(
            "Cholesterol (mg/dL)", min_value=50, max_value=600, value=200
        )

        max_hr = st.number_input("Maximum Heart Rate", min_value=50, max_value=250, value=150)

        chest_pain = st.selectbox(
            "Chest Pain Type",
            [
                "Typical Angina",
                "Atypical Angina",
                "Non-Anginal Pain",
                "Asymptomatic",
            ],
        )

        exercise_angina = st.selectbox("Exercise-Induced Angina", ["No", "Yes"]) 

        secondhand_smoke = st.selectbox("Secondhand Smoke Exposure", ["No", "Yes", "Not Sure"]) 

        healthcare_access = st.selectbox(
            "Do you have difficulty accessing timely healthcare?",
            ["No", "Yes", "Sometimes"],
        )

        emergency_symptoms = st.checkbox(
            "I am experiencing chest pain, shortness of breath, fainting, severe weakness, or another serious symptom."
        )

        submitted = st.form_submit_button("Check Risk Awareness Result")

    if emergency_symptoms:
        st.error(
            "This may be urgent. Please seek emergency medical care immediately. "
            "This app cannot evaluate emergency symptoms."
        )

    elif submitted:
        risk_score, risk_factors = compute_risk_score(
            age, resting_bp, cholesterol, max_hr, chest_pain, exercise_angina, secondhand_smoke, healthcare_access
        )

        st.subheader("Risk Awareness Result")

        if risk_score >= 6:
            st.error("Higher risk indicators detected.")
            st.write("Consider contacting a healthcare provider for professional guidance.")

        elif risk_score >= 3:
            st.warning("Moderate risk indicators detected.")
            st.write("Consider monitoring your health and discussing concerns with a healthcare provider.")

        else:
            st.success("Lower risk indicators based on the entered values.")
            st.write("Continue healthy habits and routine medical checkups.")

        st.subheader("Risk Awareness Score")
        st.write(f"Your risk awareness score is: **{risk_score}**")

        st.subheader("Main Risk Factors")
        if risk_factors:
            for factor in risk_factors:
                st.write(f"- {factor}")
        else:
            st.write("No major risk indicators were detected from the entered values.")

        st.info(
            "This result is based on simple rule-based risk-awareness logic and is not a diagnosis. "
            "Future versions may connect to trained models after validation."
        )

# Right column: examples, images, and quick cases
with right:
    st.header("Examples & Visuals")

    st.subheader("Example cases")
    st.write("Try these example inputs to see how the score changes:")

    examples = [
        {
            "name": "Higher-risk older adult",
            "age": 70,
            "resting_bp": 150,
            "cholesterol": 260,
            "max_hr": 90,
            "chest_pain": "Typical Angina",
            "exercise_angina": "Yes",
            "secondhand_smoke": "No",
            "healthcare_access": "Yes",
        },
        {
            "name": "Middle-age moderate",
            "age": 50,
            "resting_bp": 130,
            "cholesterol": 210,
            "max_hr": 110,
            "chest_pain": "Atypical Angina",
            "exercise_angina": "No",
            "secondhand_smoke": "Not Sure",
            "healthcare_access": "Sometimes",
        },
        {
            "name": "Lower-risk younger adult",
            "age": 30,
            "resting_bp": 115,
            "cholesterol": 180,
            "max_hr": 170,
            "chest_pain": "Non-Anginal Pain",
            "exercise_angina": "No",
            "secondhand_smoke": "No",
            "healthcare_access": "No",
        },
    ]

    for ex in examples:
        with st.expander(ex["name"]):
            st.write(
                f"Age: {ex['age']}, Resting BP: {ex['resting_bp']}, Cholesterol: {ex['cholesterol']}, "
                f"Max HR: {ex['max_hr']}, Chest pain: {ex['chest_pain']}, Exercise angina: {ex['exercise_angina']}"
            )
            s, f = compute_risk_score(
                ex['age'], ex['resting_bp'], ex['cholesterol'], ex['max_hr'],
                ex['chest_pain'], ex['exercise_angina'], ex['secondhand_smoke'], ex['healthcare_access']
            )
            st.write(f"Computed score: **{s}**")
            if f:
                st.write("Main risk factors:")
                for item in f:
                    st.write(f"- {item}")

    st.markdown("---")
    st.subheader("Illustrations")
    # Public domain / Wikimedia images used as illustrations
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Heart_font_awesome.svg/512px-Heart_font_awesome.svg.png",
        caption="Heart (illustration)",
    )
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Heartbeat.svg/512px-Heartbeat.svg.png",
        caption="ECG / Heart rate illustration",
    )


# Footer
st.markdown("---")
st.caption(
    "Medical disclaimer: This app is an educational prototype and not a substitute for professional medical advice, diagnosis, or treatment."
)
