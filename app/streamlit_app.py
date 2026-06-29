import streamlit as st
from typing import List
import pandas as pd
import altair as alt

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
        margin-bottom: 8px;
        color: #0b1220;
    }

    /* Make images a bit smaller and rounded */
    .stImage img {
        border-radius: 8px;
        max-width: 100%;
        height: auto;
    }

    /* Footer caption spacing + muted color */
    .stCaption {
        margin-top: 12px;
        color: #475569;
    }
    </style>
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

# LEFT column: Graphs + Examples + Benchmarking
with left:
    st.header("Results & Examples")

    # Placeholder for result-graph: will be populated after form submission
    st.subheader("Your risk breakdown")
    result_chart_placeholder = st.empty()

    st.divider()

    st.subheader("Example cases")
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
    st.subheader("Benchmark: average profiles")
    bench_placeholder = st.empty()

# MIDDLE column: interactive form (main app)
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

        # Prepare data for left-column result chart (presence of each risk factor)
        possible_factors = [
            "Older age",
            "Middle-age risk factor",
            "High cholesterol",
            "Borderline cholesterol",
            "High blood pressure",
            "Elevated blood pressure",
            "Lower maximum heart rate",
            "Exercise-induced angina",
            "Typical angina chest pain",
            "Asymptomatic chest pain category",
            "Secondhand smoke exposure",
            "Possible secondhand smoke exposure",
            "Difficulty accessing timely healthcare",
            "Occasional difficulty accessing timely healthcare",
        ]

        presence = [1 if f in risk_factors else 0 for f in possible_factors]
        df_presence = pd.DataFrame({"Risk Factor": possible_factors, "Present": presence})

        # Bar chart: risk factor presence
        chart = alt.Chart(df_presence[df_presence.Present == 1]).mark_bar(color="#ef4444").encode(
            x=alt.X('Present:Q', title='Present (1 = yes)'),
            y=alt.Y('Risk Factor:N', sort='-x', title='Risk factor')
        ).properties(height=300)

        left.success(f"Computed risk awareness score: {risk_score}")
        result_chart_placeholder.altair_chart(chart, use_container_width=True)

        # Benchmarking: compute average male/female example profiles
        male_profile = {"age": 55, "resting_bp": 135, "cholesterol": 230, "max_hr": 140,
                        "chest_pain": "Atypical Angina", "exercise_angina": "No",
                        "secondhand_smoke": "No", "healthcare_access": "No"}
        female_profile = {"age": 55, "resting_bp": 125, "cholesterol": 220, "max_hr": 150,
                          "chest_pain": "Non-Anginal Pain", "exercise_angina": "No",
                          "secondhand_smoke": "No", "healthcare_access": "No"}

        m_score, _ = compute_risk_score(**male_profile)
        f_score, _ = compute_risk_score(**female_profile)

        df_bench = pd.DataFrame({
            "Profile": ["You", "Avg Male (55)", "Avg Female (55)"],
            "Score": [risk_score, m_score, f_score]
        })

        bench_chart = alt.Chart(df_bench).mark_bar().encode(
            x=alt.X('Profile:N', sort=None),
            y=alt.Y('Score:Q', scale=alt.Scale(domain=[0, max(df_bench.Score.max(), 6)])),
            color=alt.condition(alt.datum.Profile == 'You', alt.value('#ef4444'), alt.value('#0ea5a4'))
        ).properties(height=240)

        bench_placeholder.altair_chart(bench_chart, use_container_width=True)

# RIGHT column: images and contact info
with right:
    st.header("Illustrations & Contact")

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

    st.markdown("---")
    st.subheader("About & Links")
    st.markdown(
        "- **Prototype purpose**: educational risk-awareness and care navigation suggestions.\n"
        "- **Source code**: [GitHub repository](https://github.com/archishakaspha29/cardiovascular-risk-alert-ai)\n"
        "- **Datasets used**: public heart disease datasets (included in /data)"
    )

    st.markdown("---")
    st.subheader("Contact / Learn more")
    st.write("Author: archishakaspha29 · Educational project")

# Footer
st.markdown("---")
st.caption(
    "Medical disclaimer: This app is an educational prototype and not a substitute for professional medical advice, diagnosis, or treatment."
)
