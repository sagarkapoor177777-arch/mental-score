
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ==================================================
# 1. PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Social Media Impact on Daily Life",
    page_icon="🧠",
    layout="wide"
)

MODEL_PATH = Path(__file__).parent / "Mental_Health_Model.pkl"

# ==================================================
# 2. LOAD MODEL
# ==================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.stApp {
    background: #F5F7FC;
    color: #25294A;
}

[data-testid="stSidebar"] {
    background: #ECEEFF;
}

.hero {
    background: linear-gradient(120deg, #E5E7FF, #DDF3FF);
    padding: 28px;
    border-radius: 20px;
    margin-bottom: 22px;
}

.hero h1 {
    color: #292D63;
    font-size: 32px;
}

.hero p {
    color: #555B7D;
    font-size: 16px;
}

.metric {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E5E8F2;
    min-height: 110px;
}

.metric-label {
    color: #777D98;
    font-size: 14px;
}

.metric-value {
    color: #4549B7;
    font-size: 23px;
    font-weight: bold;
    margin-top: 10px;
}

.result {
    background: white;
    border: 1px solid #E5E8F2;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
}

.result-score {
    color: #5558C9;
    font-size: 44px;
    font-weight: bold;
}

div.stButton > button {
    background: #5558C9;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. SCORE INTERPRETATION
# ==================================================

def interpret_score(score):
    """
    Assumption: higher score means better wellbeing.
    Confirm this against the target used during training.
    Thresholds below are provisional, not clinical cutoffs.
    """

    if score >= 7:
        return (
            "Strong Mental Wellbeing",
            "🟢",
            "The predicted score is in the higher range."
        )

    elif score >= 5:
        return (
            "Medium Mental Wellbeing",
            "🟡",
            "The predicted score is in the middle range."
        )

    else:
        return (
            "Very Low Mental Wellbeing",
            "🔵",
            "The predicted score is in the lower range."
        )


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:
    st.title("🧠 MindTrack")
    st.caption("Social Media & Daily Life")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Mental Health Assessment",
            "About Project"
        ]
    )

    st.divider()
    st.markdown("### Project Creator")
    st.markdown("**Sagar Kapoor**")


# ==================================================
# 6. HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🧠 Social Media Impact on Daily Life</h1>
    <p>
        Explore how social media habits, sleep, study,
        stress and physical activity relate to wellbeing.
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# 7. DASHBOARD
# ==================================================

if page == "Dashboard":

    st.subheader("Project Dashboard")

    st.write(
        "This application uses a trained machine learning model "
        "to generate a prediction from lifestyle and social media inputs."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">Project Domain</div>
            <div class="metric-value">Wellbeing</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">ML Algorithm</div>
            <div class="metric-value">Random Forest</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric">
            <div class="metric-label">Frontend</div>
            <div class="metric-value">Streamlit</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Features Considered")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        - Study hours
        - Age
        - Average daily social media usage
        - Daily phone unlocks
        - Physical activity
        - Sleep hours
        """)

    with right:
        st.markdown("""
        - Stress level
        - Gender
        - Academic level
        - Most-used platform
        - Purpose of use
        - Grouped country
        """)

    st.info(
        "Assessment page par jaakar inputs enter karein "
        "aur model prediction generate karein."
    )


# ==================================================
# 8. MENTAL HEALTH ASSESSMENT
# ==================================================

elif page == "Mental Health Assessment":

    st.subheader("📝 Mental Health Assessment")

    if not MODEL_PATH.exists():
        st.error(
            "Model file nahi mili. app.py aur "
            "Mental_Health_Model.pkl ko same folder mein rakhein."
        )
        st.stop()

    try:
        model = load_model()
    except Exception as e:
        st.error(
            "Model load nahi hua. Neeche diye gaye "
            "scikit-learn version steps follow karein."
        )
        st.code(str(e))
        st.stop()

    with st.form("assessment_form"):

        st.markdown("### Personal Information")

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input(
                "Age",
                min_value=13,
                max_value=100,
                value=21
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )

            academic_level = st.selectbox(
                "Academic Level",
                [
                    "High School",
                    "Undergraduate",
                    "Postgraduate",
                    "Other"
                ]
            )

            country = st.text_input(
                "Grouped Country",
                value="India"
            )

        with c2:
            study_hours = st.number_input(
                "Study Hours",
                min_value=0.0,
                max_value=24.0,
                value=4.0,
                step=0.5
            )

            sleep_hours = st.number_input(
                "Sleep Hours Per Night",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5
            )

            physical_activity = st.number_input(
                "Physical Activity Hours",
                min_value=0.0,
                max_value=24.0,
                value=1.0,
                step=0.5
            )

        st.divider()
        st.markdown("### Social Media Usage")

        c1, c2 = st.columns(2)

        with c1:
            usage_hours = st.number_input(
                "Average Daily Usage Hours",
                min_value=0.0,
                max_value=24.0,
                value=3.0,
                step=0.5
            )

            daily_unlocks = st.number_input(
                "Daily Unlocks",
                min_value=0,
                max_value=1000,
                value=50
            )

            most_used_platform = st.selectbox(
                "Most-Used Platform",
                [
                    "Instagram",
                    "Facebook",
                    "TikTok",
                    "YouTube",
                    "Snapchat",
                    "Twitter",
                    "WhatsApp",
                    "Other"
                ]
            )

        with c2:
            stress_level = st.selectbox(
                "Stress Level",
                ["Low", "Medium", "High", "Very High"]
            )

            purpose_of_use = st.selectbox(
                "Purpose of Use",
                [
                    "Entertainment",
                    "Communication",
                    "Education",
                    "Work",
                    "News",
                    "Other"
                ]
            )

        submitted = st.form_submit_button(
            "Generate Prediction",
            use_container_width=True
        )

    # ==================================================
    # 9. PREDICTION
    # ==================================================

    if submitted:

        if not country.strip():
            st.warning("Grouped Country enter karein.")
            st.stop()

        # Exact feature names from the saved model
        input_data = pd.DataFrame([{
            "Study_Hours": study_hours,
            "Age": age,
            "Avg_Daily_Usage_Hours": usage_hours,
            "Daily_Unlocks": daily_unlocks,
            "Physical_Activity_Hours": physical_activity,
            "Sleep_Hours_Per_Night": sleep_hours,
            "Stress_Level": stress_level,
            "Gender": gender,
            "Academic_Level": academic_level,
            "Most_Used_Platform": most_used_platform,
            "Purpose_Of_Use": purpose_of_use,
            "Grouped_country": country.strip()
        }])

        try:
            prediction = model.predict(input_data)
            score = float(prediction[0])

            category, emoji, explanation = interpret_score(score)

            st.divider()
            st.subheader("📊 Prediction Result")

            st.markdown(f"""
            <div class="result">
                <div class="result-score">{score:.2f}</div>
                <p>Predicted Model Score</p>
                <h2>{emoji} {category}</h2>
                <p>{explanation}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### Assessment Summary")
            st.dataframe(
                input_data.T.rename(columns={0: "Your Input"}),
                use_container_width=True
            )

            csv_data = input_data.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Assessment CSV",
                data=csv_data,
                file_name="mental_health_assessment.csv",
                mime="text/csv"
            )

            st.caption(
                "Educational prediction only, not a medical diagnosis. "
                "Score categories and thresholds must be verified "
                "against the original training target."
            )

        except Exception as e:
            st.error(
                "Prediction error. Check the feature categories "
                "against the original training dataset."
            )
            st.code(str(e))


# ==================================================
# 10. ABOUT PROJECT
# ==================================================

elif page == "About Project":

    st.subheader("About This Project")

    st.write("""
    Social Media Impact on Daily Life is a machine learning project
    that explores how social media use and everyday habits relate
    to a predicted wellbeing score.

    The application uses a saved Random Forest model with a
    preprocessing pipeline. Inputs are transformed by the saved
    pipeline before the model generates its prediction.
    """)

    st.markdown("### Technologies Used")

    st.markdown("""
    - Python
    - Pandas
    - Scikit-learn
    - Random Forest Regressor
    - Streamlit
    """)

    st.markdown("### Project Creator")
    st.markdown("**Sagar Kapoor**")

    st.warning(
        "The model output is not a clinical diagnosis. "
        "The score's meaning must be checked against the training data."
    )


# ==================================================
# 11. FOOTER
# ==================================================

st.divider()

st.caption(
    "Social Media Impact on Daily Life | Created by Sagar Kapoor"
)
