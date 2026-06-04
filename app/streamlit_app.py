import streamlit as st

st.set_page_config(
    page_title="Cardiovascular Risk-Alert Tool",
    page_icon="❤️"
)

st.title("AI-Assisted Cardiovascular Risk-Alert Tool")
st.write(
    "This prototype is designed to support cardiovascular risk awareness "
    "and encourage early care-seeking."
)

st.warning(
    "Medical Disclaimer: This app is not a medical diagnosis tool and does not replace "
    "professional medical care. If you have chest pain, shortness of breath, fainting, "
    "severe weakness, or emergency symptoms, seek medical help immediately."
)

st.header("Enter Health Information")

age = st.number_input("Age", min_value=1, max_value=120, value=40)
resting_bp = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120)
cholesterol = st.number_input("Cholesterol", min_value=50, max_value=600, value=200)
max_hr = st.number_input("Maximum Heart Rate", min_value=50, max_value=250, value=150)

chest_pain = st.selectbox(
    "Chest Pain Type",
    ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"]
)

exercise_angina = st.selectbox(
    "Exercise-Induced Angina",
    ["No", "Yes"]
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

        if cholesterol >= 240:
            risk_score += 2
            risk_factors.append("High cholesterol")
        elif cholesterol >= 200:
            risk_score += 1
            risk_factors.append("Borderline cholesterol")

        if resting_bp >= 140:
            risk_score += 2
            risk_factors.append("High blood pressure")
        elif resting_bp >= 120:
            risk_score += 1
            risk_factors.append("Elevated blood pressure")

        if max_hr < 100:
            risk_score += 1
            risk_factors.append("Lower maximum heart rate")

        if exercise_angina == "Yes":
            risk_score += 2
            risk_factors.append("Exercise-induced angina")

        if chest_pain == "Asymptomatic":
            risk_score += 1
            risk_factors.append("Asymptomatic chest pain category")

        st.subheader("Risk Awareness Result")

        if risk_score >= 5:
            st.error("Higher risk indicators detected.")
            st.write("Consider contacting a healthcare provider for professional guidance.")
        elif risk_score >= 3:
            st.warning("Moderate risk indicators detected.")
            st.write("Consider monitoring your health and discussing concerns with a healthcare provider.")
        else:
            st.success("Lower risk indicators based on the entered values.")
            st.write("Continue healthy habits and routine medical checkups.")

        st.subheader("Main Risk Factors")
        if risk_factors:
            for factor in risk_factors:
                st.write(f"- {factor}")
        else:
            st.write("No major risk indicators were detected from the entered values.")

        st.info(
            "This result is based on general risk-awareness rules and is not a diagnosis. "
            "Future versions may connect to the trained Random Forest model after additional validation."
)
