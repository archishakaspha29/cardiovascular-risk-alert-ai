import streamlit as st

st.set_page_config(
    page_title="Cardiovascular Risk-Alert Tool",
    page_icon="❤️",
    layout="centered"
)

st.title("AI-Assisted Cardiovascular Risk-Alert Tool")

st.write(
    "This educational prototype is designed to support cardiovascular risk awareness "
    "and encourage early care-seeking, especially for people who may face barriers "
    "to timely healthcare access."
)

st.warning(
    "Medical Disclaimer: This app is not a medical diagnosis tool and does not replace "
    "professional medical care, diagnosis, or treatment. If you have chest pain, "
    "shortness of breath, fainting, severe weakness, or emergency symptoms, "
    "seek medical help immediately."
)

st.header("Enter Health Information")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=40
)

resting_bp = st.number_input(
    "Resting Blood Pressure / Systolic BP",
    min_value=50,
    max_value=250,
    value=120
)

cholesterol = st.number_input(
    "Cholesterol",
    min_value=50,
    max_value=600,
    value=200
)

max_hr = st.number_input(
    "Maximum Heart Rate",
    min_value=50,
    max_value=250,
    value=150
)

chest_pain = st.selectbox(
    "Chest Pain Type",
    [
        "Typical Angina",
        "Atypical Angina",
        "Non-Anginal Pain",
        "Asymptomatic"
    ]
)

exercise_angina = st.selectbox(
    "Exercise-Induced Angina",
    ["No", "Yes"]
)

secondhand_smoke = st.selectbox(
    "Secondhand Smoke Exposure",
    ["No", "Yes", "Not Sure"]
)

healthcare_access = st.selectbox(
    "Do you have difficulty accessing timely healthcare?",
    ["No", "Yes", "Sometimes"]
)

emergency_symptoms = st.checkbox(
    "I am experiencing chest pain, shortness of breath, fainting, severe weakness, "
    "or another serious symptom."
)

if emergency_symptoms:
    st.error(
        "This may be urgent. Please seek emergency medical care immediately. "
        "This app cannot evaluate emergency symptoms."
    )

else:
    if st.button("Check Risk Awareness Result"):

        risk_score = 0
        risk_factors = []

        # Age risk
        if age >= 65:
            risk_score += 2
            risk_factors.append("Older age")
        elif age >= 45:
            risk_score += 1
            risk_factors.append("Middle-age risk factor")

        # Cholesterol risk
        if cholesterol >= 240:
            risk_score += 2
            risk_factors.append("High cholesterol")
        elif cholesterol >= 200:
            risk_score += 1
            risk_factors.append("Borderline cholesterol")

        # Blood pressure risk
        if resting_bp >= 140:
            risk_score += 2
            risk_factors.append("High blood pressure")
        elif resting_bp >= 120:
            risk_score += 1
            risk_factors.append("Elevated blood pressure")

        # Maximum heart rate
        if max_hr < 100:
            risk_score += 1
            risk_factors.append("Lower maximum heart rate")

        # Exercise-induced angina
        if exercise_angina == "Yes":
            risk_score += 2
            risk_factors.append("Exercise-induced angina")

        # Chest pain category
        if chest_pain == "Typical Angina":
            risk_score += 2
            risk_factors.append("Typical angina chest pain")
        elif chest_pain == "Asymptomatic":
            risk_score += 1
            risk_factors.append("Asymptomatic chest pain category")

        # Secondhand smoke exposure
        if secondhand_smoke == "Yes":
            risk_score += 1
            risk_factors.append("Secondhand smoke exposure")
        elif secondhand_smoke == "Not Sure":
            risk_factors.append("Possible secondhand smoke exposure")

        # Healthcare access barrier
        if healthcare_access == "Yes":
            risk_score += 1
            risk_factors.append("Difficulty accessing timely healthcare")
        elif healthcare_access == "Sometimes":
            risk_factors.append("Occasional difficulty accessing timely healthcare")

        st.subheader("Risk Awareness Result")

        if risk_score >= 6:
            st.error("Higher risk indicators detected.")
            st.write(
                "Consider contacting a healthcare provider for professional guidance."
            )

        elif risk_score >= 3:
            st.warning("Moderate risk indicators detected.")
            st.write(
                "Consider monitoring your health and discussing concerns with a healthcare provider."
            )

        else:
            st.success("Lower risk indicators based on the entered values.")
            st.write(
                "Continue healthy habits and routine medical checkups."
            )

        st.subheader("Risk Awareness Score")
        st.write(f"Your risk awareness score is: **{risk_score}**")

        st.subheader("Main Risk Factors")

        if risk_factors:
            for factor in risk_factors:
                st.write(f"- {factor}")
        else:
            st.write(
                "No major risk indicators were detected from the entered values."
            )

        st.info(
            "This result is based on general risk-awareness rules and is not a diagnosis. "
            "Future versions may connect to the trained Random Forest model after additional validation."
        )
