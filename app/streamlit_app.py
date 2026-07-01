import streamlit as st
from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    if exercise_angina.startswith("Yes"):
        score += 2
        factors.append("Exercise-induced angina")

    # Chest pain category
    if chest_pain.startswith("Typical Angina"):
        score += 2
        factors.append("Typical angina chest pain")
    elif chest_pain.startswith("Asymptomatic"):
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


def create_sample_dataset() -> pd.DataFrame:
    """
    Create a mock sample dataset with age, gender, cholesterol, blood pressure, 
    and calculated risk score values for educational visualization.
    """
    np.random.seed(42)
    
    # Generate sample data
    ages = []
    genders = []
    cholesterols = []
    bps = []
    max_hrs = []
    chest_pains = []
    exercise_anginas = []
    smoke_exposures = []
    healthcare_accesses = []
    
    chest_pain_options = ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"]
    
    # Generate ~200 sample profiles (100 female, 100 male, spread across ages 25-75)
    for _ in range(100):
        ages.append(np.random.randint(25, 76))
        genders.append("Female")
        cholesterols.append(np.random.randint(120, 280))
        bps.append(np.random.randint(100, 160))
        max_hrs.append(np.random.randint(80, 200))
        chest_pains.append(np.random.choice(chest_pain_options))
        exercise_anginas.append(np.random.choice(["No", "Yes"]))
        smoke_exposures.append(np.random.choice(["No", "Yes", "Not Sure"]))
        healthcare_accesses.append(np.random.choice(["No", "Yes", "Sometimes"]))
    
    for _ in range(100):
        ages.append(np.random.randint(25, 76))
        genders.append("Male")
        cholesterols.append(np.random.randint(120, 280))
        bps.append(np.random.randint(100, 160))
        max_hrs.append(np.random.randint(80, 200))
        chest_pains.append(np.random.choice(chest_pain_options))
        exercise_anginas.append(np.random.choice(["No", "Yes"]))
        smoke_exposures.append(np.random.choice(["No", "Yes", "Not Sure"]))
        healthcare_accesses.append(np.random.choice(["No", "Yes", "Sometimes"]))
    
    df = pd.DataFrame({
        "age": ages,
        "gender": genders,
        "cholesterol": cholesterols,
        "resting_bp": bps,
        "max_hr": max_hrs,
        "chest_pain": chest_pains,
        "exercise_angina": exercise_anginas,
        "secondhand_smoke": smoke_exposures,
        "healthcare_access": healthcare_accesses,
    })
    
    # Calculate risk score for each sample profile
    risk_scores = []
    for _, row in df.iterrows():
        score, _ = compute_risk_score(
            row["age"],
            row["resting_bp"],
            row["cholesterol"],
            row["max_hr"],
            row["chest_pain"],
            row["exercise_angina"],
            row["secondhand_smoke"],
            row["healthcare_access"]
        )
        risk_scores.append(score)
    
    df["risk_score"] = risk_scores
    return df


def calculate_percentile(user_score: int, user_gender: str, user_age: int, sample_df: pd.DataFrame, age_range: int = 5) -> float:
    """
    Calculate the user's percentile compared to similar profiles 
    (same gender, age within ±age_range years).
    """
    # Filter for same gender and similar age range
    mask = (sample_df["gender"] == user_gender) & \
           (sample_df["age"] >= user_age - age_range) & \
           (sample_df["age"] <= user_age + age_range)
    similar_profiles = sample_df[mask]
    
    if len(similar_profiles) == 0:
        return None
    
    # Calculate percentile
    scores_below = len(similar_profiles[similar_profiles["risk_score"] < user_score])
    percentile = (scores_below / len(similar_profiles)) * 100
    
    return percentile


def plot_percentile_comparison(user_age: int, user_score: int, user_gender: str, sample_df: pd.DataFrame):
    """
    Create side-by-side plots showing average risk score trend by age for female and male groups,
    with the user's profile highlighted on the appropriate graph.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Age and Gender Risk Percentile Comparison\n(Dataset-Based Educational Visualization)", 
                 fontsize=14, fontweight="bold")
    
    genders = ["Female", "Male"]
    colors = ["#e91e63", "#2196f3"]  # Pink for Female, Blue for Male
    
    for idx, (ax, gender, color) in enumerate(zip(axes, genders, colors)):
        # Filter data for this gender
        gender_data = sample_df[sample_df["gender"] == gender]
        
        # Group by age and calculate mean risk score
        age_groups = gender_data.groupby("age")["risk_score"].mean().sort_index()
        
        # Plot trend line
        ax.plot(age_groups.index, age_groups.values, marker="o", color=color, 
                linewidth=2.5, markersize=6, label=f"Average {gender} Risk Score", alpha=0.7)
        
        # Highlight user's profile if it matches this gender
        if user_gender == gender:
            ax.scatter(user_age, user_score, color="red", s=300, marker="*", 
                      zorder=5, label="Your Profile", edgecolors="darkred", linewidth=2)
        
        ax.set_xlabel("Age (years)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Risk-Awareness Score", fontsize=11, fontweight="bold")
        ax.set_title(f"{gender}", fontsize=12, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(loc="upper left", fontsize=10)
        ax.set_xlim(20, 80)
        
    plt.tight_layout()
    return fig


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

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"],
        )

        st.write("**Resting Blood Pressure** (the top number in a blood pressure reading, such as 120 in 120/80)")
        resting_bp = st.number_input(
            "Resting Blood Pressure / Systolic BP (mm Hg)", min_value=50, max_value=250, value=120
        )
        st.caption(
            "📋 **How to measure at home**: Use a home blood pressure cuff. Sit quietly for at least 5 minutes, keep feet flat on the floor, "
            "keep your back supported, place the cuff on bare skin, keep your arm supported at heart level, avoid talking during the reading, "
            "and avoid caffeine, exercise, or smoking for about 30 minutes before measuring. **Important**: Do not guess if you do not have a blood pressure monitor—ask your healthcare provider."
        )

        st.write("**Cholesterol** (from a blood test/lipid panel)")
        cholesterol = st.number_input(
            "Cholesterol (mg/dL)", min_value=50, max_value=600, value=200
        )
        st.caption(
            "📋 **How to provide this value**: Enter your total cholesterol in mg/dL from a recent lab result if you know it "
            "(usually from your doctor's office, clinic, or lab). **Important**: Do not guess. If you do not know your cholesterol, "
            "ask your healthcare provider for a recent lipid panel result."
        )

        st.write("**Maximum Heart Rate** (the highest heart rate reached during exercise)")
        max_hr_option = st.radio(
            "Do you know your maximum heart rate?",
            ["Yes, I know my exact maximum heart rate", "No, I do not know—use an estimate"],
            index=1
        )
        
        if max_hr_option == "Yes, I know my exact maximum heart rate":
            max_hr = st.number_input("Maximum Heart Rate", min_value=50, max_value=250, value=150)
        else:
            age_value = age
            estimated_max_hr = 220 - age_value
            st.info(
                f"**Estimated Maximum Heart Rate**: {estimated_max_hr} bpm (using formula: 220 − your age). "
                f"This is **only an estimate**, not a medical measurement. Most people do not know their true maximum heart rate "
                f"unless they used a fitness tracker during intense exercise or had a medical stress test."
            )
            max_hr = estimated_max_hr

        st.write("**Chest Pain Type**")
        chest_pain = st.selectbox(
            "Chest Pain Type",
            [
                "Typical Angina (chest pressure, tightness, squeezing, or discomfort that may happen with exercise or stress and may improve with rest)",
                "Atypical Angina (chest discomfort that does not follow the classic pattern and may feel different or have unclear triggers)",
                "Non-Anginal Pain (chest pain less likely to be heart-related and may come from muscle strain, digestion, anxiety, or breathing-related causes)",
                "Asymptomatic (no noticeable chest pain symptoms)",
            ],
        )
        st.caption(
            "⚠️ **Safety note**: If chest pain is severe, new, worsening, or occurs with shortness of breath, fainting, sweating, or weakness, "
            "seek emergency medical help immediately."
        )

        st.write("**Exercise-Induced Angina**")
        exercise_angina = st.selectbox(
            "Exercise-Induced Angina",
            [
                "No (no chest pain, pressure, tightness, or discomfort during physical activity)",
                "Yes (chest pain, pressure, tightness, or discomfort during exercise or physical activity)"
            ]
        ) 

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

        # --- New: Age and Gender Risk Percentile Comparison Section ---
        st.markdown("---")
        st.subheader("Age and Gender Risk Percentile Comparison")
        
        st.markdown(
            "**Educational Dataset Visualization**: This section compares your entered risk-awareness score "
            "with sample profiles of the same gender and similar age range (±5 years). "
            "This is an educational comparison only and is NOT a clinical percentile or medical diagnosis."
        )
        
        # Create or load sample dataset
        sample_df = create_sample_dataset()
        
        # Calculate user's percentile
        percentile = calculate_percentile(risk_score, gender, age, sample_df, age_range=5)
        
        if percentile is not None:
            # Display percentile explanation
            st.write(
                f"**Your percentile**: {percentile:.1f}th percentile"
            )
            st.write(
                f"Your risk-awareness score of **{risk_score}** is higher than approximately "
                f"**{percentile:.1f}%** of sample profiles in this educational dataset "
                f"with the same gender ({gender}) and similar age ({age}±5 years)."
            )
            st.write(
                "**What this means**: A higher percentile indicates your entered risk indicators are "
                "higher compared with similar sample profiles. A lower percentile means your entered indicators "
                "are lower compared with similar sample profiles. This is educational context only and should "
                "not be interpreted as a clinical diagnosis or medical risk assessment."
            )
            
            # Plot comparison graphs
            fig = plot_percentile_comparison(age, risk_score, gender, sample_df)
            st.pyplot(fig)
            
            st.markdown("**Graph Explanation:**")
            st.write(
                "- The line shows the average risk-awareness score trend by age for each gender group.\n"
                "- The red star marks **your profile** on the appropriate gender graph.\n"
                "- This visualization helps you see where your entered risk indicators fall relative to the age and gender trend in the sample dataset."
            )
        else:
            st.warning("Not enough similar profiles in the sample dataset to calculate percentile.")
        
        # Disclaimer
        st.info(
            "⚠️ **Important Disclaimer**: This dataset-based percentile comparison is NOT a clinical percentile, "
            "NOT a medical diagnosis, and NOT a substitute for professional medical advice. It is an educational "
            "visualization based on a mock sample dataset. Your actual cardiovascular risk should be assessed by a "
            "qualified healthcare provider using clinically validated tools and your complete medical history."
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
            "gender": "Female",
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
            "gender": "Male",
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
            "gender": "Female",
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
                f"Age: {ex['age']}, Gender: {ex['gender']}, Resting BP: {ex['resting_bp']}, Cholesterol: {ex['cholesterol']}, "
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
