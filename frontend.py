import utils
import requests
import logging
import pandas as pd
import streamlit as st 
from dotenv import dotenv_values
import data.cfg as cfg
import data.source_code


class MentalDataFrontend:
    def __init__(self):
        self.setup_logging()
        self.run()


    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)


    @st.cache_data
    def load_data(_self):
        data = pd.read_csv(dotenv_values('.env')['PATH'])
        return data


    def dispaly_graphs(self, graph_generator):
        st.title("Mental Health Statistics")
        
        with st.container():
            st.markdown("### Firtly, lets draw some graphs to see general information. This pie chart shows the distribution of different diagnoses among men. The diagnosis is made in four categories: Generalized Anxiety, Panic Disorder, Major Depressive Disorder and Bipolar Disorder.")
        st.plotly_chart(graph_generator.generate_men_chart(), key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['first_table'], language='python')
        with st.container():
            st.markdown("## Generalized Anxiety is rather a common diagnosis among men. Panic Disorder and Major Depressive Disorder are also significant problems, but they are less common than Generalized Anxiety. Bipolar Disorder has the disease itself from all four categories, but is close in value to Panic Disorder and Major Depressive Disorder.")

        with st.container():
            st.markdown("### This pie chart shows the distribution of different diagnoses among women. Diagnoses are presented in four categories: Generalized Anxiety, Panic Disorder, Major Depressive Disorder and Bipolar Disorder.")
        st.plotly_chart(graph_generator.generate_women_chart(), key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['second_table'], language='python')
        with st.container():
            st.markdown("### Generalized Anxiety is the most common diagnosis among women. Bipolar Disorder and Major Depressive Disorder are also significant problems, but are slightly less common than Generalized Anxiety. Panic Disorder has a significantly lower prevalence compared to other diagnoses.")

        with st.container():
            st.markdown("### The graph shows the dependence of the average indicators for Symptom Severity (1-10) and Stress Level (1-10) depending on the age of the patient.")
        st.plotly_chart(graph_generator.sympthom_sev_stress_lev(), key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['third_table'], language='python')
        with st.container():
            st.markdown("### At a young age, stress levels and severity of symptoms are high, with peaks and troughs, and short-term significant changes are possible, possibly related to external factors (studies, career). In middle age, values show relative stabilization, this may be due to a more stable lifestyle, although stress levels remain noticeable. At a later age, the indicators become less variable, and the stress level is slightly lower than in earlier periods, which may be due to retirement or a decrease in the pressure of external factors.")

        with st.container():
            st.markdown("### The graph shows the dependence of the average Sleep Quality and Mood Score on Physical Activity in hours per week for people with mental illness.")
        st.plotly_chart(graph_generator.sleep_qual_mood_sc(), key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['fourth_table'], language='python')
        with st.container():
            st.markdown("### For people with mental illness, physical activity is associated with a positive effect on sleep quality and mood, although the effect on sleep is more pronounced than on mood. It takes more hours of physical activity to boost mood (the threshold is 6+ hours per week).")

        with st.container():
            st.markdown("### This graph shows the average values of three metrics: Treatment Duration (week), Treatment Progress (1-10) and Symptom Severity (1-10) for various Therapy Types.")
        st.plotly_chart(graph_generator.avg_treatment_ther_type(), key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['fifth_table'], language='python')
        with st.container():
            st.markdown("### Cognitive Behavioral Therapy and Dialectical Behavioral Therapy show the best results in terms of treatment progress and symptom severity reduction. Mindfulness-Based Therapy, although it has a long duration, shows less pronounced progress and a decrease in symptoms. Interpersonal Therapy is located between these two groups in terms of effectiveness.")

        with st.container():
            st.markdown("### This graph shows the distribution of therapy outcomes for different Therapy Types. Outcomes are presented on a scale from 1 to 4 and are divided into three categories: deterioration (blue columns), no change (red columns) and improvement (green columns).")
        st.plotly_chart(graph_generator.analysis_outcomes(), use_container_width=True, key=graph_generator.generate_key())
        with st.expander("Show/Close code"):
            st.code(data.source_code.source_code_data_list['sixth_table'], language='python')
        with st.container():
            st.markdown("### Cognitive Behavioral Therapy and Dialectical Behavioral Therapy show the greatest effectiveness with minimal risk of deterioration. Interpersonal Therapy and Mindfulness-Based Therapy demonstrate an increased risk of deterioration, which requires careful assessment before their use. Mindfulness-Based Therapy shows the lowest rate of improvement among all methods.")

        with st.container():
            st.markdown("### Summarize")
            st.markdown("### The data highlights key trends in mental health:")
            st.markdown("### Diagnoses: Generalized Anxiety is the most common among men and women, but there are gender differences in the prevalence of other diagnoses.")
            st.markdown("### Age: The younger age group is more prone to stress and severity of symptoms, but older people also require attention to their mental state.")
            st.markdown("### Physical activity: Physical activity is an important element of therapy, especially for improving sleep, with an additional effect on mood with increased activity.")
            st.markdown("### Types of Therapy: Cognitive Behavioral Therapy and Dialectical Behavioral Therapy are the most effective approaches for treatment, unlike Mindfulness-Based Therapy")
            st.markdown("### Outcomes: Cognitive Behavioral Therapy and Dialectical Behavioral Therapy demonstrate minimal risk of deterioration, which makes them the preferred methods for most patients.")

    def display_form(self):
        st.header("Add your data")
        with st.form("Mental_form"):
            age = st.number_input("Age (18-60)", min_value=18, max_value=60, step=1)
            gender = st.selectbox("Gender", ["Male", "Female"])
            diagnosis = st.selectbox("Diagnosis", ["Generalized Anxiety", "Panic Disorder", "Major Depressive Disorder", "Bipolar Disorder"])
            symptom_severity = st.slider("Symptom Severity (1-10)", min_value=1, max_value=10, step=1)
            mood_score = st.slider("Mood Score (1-10)", min_value=1, max_value=10, step=1)
            sleep_quality = st.slider("Sleep Quality (1-10)", min_value=1, max_value=10, step=1)
            physical_activity = st.slider("Physical Activity (hrs/week)", min_value=1, max_value=10, step=1)
            therapy_type = st.selectbox("Therapy Type", ["Cognitive Behavioral Therapy", "Dialectical Behavioral Therapy", "Interpersonal Therapy", "Mindfulness-Based Therapy"])
            treatment_duration = st.slider("Treatment Duration (weeks)", min_value=0, max_value=60, step=1)
            stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, step=1)
            outcome = st.selectbox("Outcome", ["Deteriorated", "No Change", "Improved"])
            treatment_progress = st.slider("Treatment Progress (1-10)", min_value=1, max_value=10, step=1)            

            submitted = st.form_submit_button("Submit")

        if submitted:
            n_data = {
                "age": age,
                "gender": gender,
                "diagnosis": diagnosis,
                "symptom_severity": symptom_severity,
                "mood_score": mood_score,
                "sleep_quality": sleep_quality,
                "physical_activity": physical_activity,
                "therapy_type": therapy_type,
                "treatment_duration": treatment_duration,
                "stress_level": stress_level,
                "outcome": outcome,
                "treatment_progress": treatment_progress,
            }
            self.handle_submission(n_data)


    def handle_submission(self, n_data):
        try:
            response = requests.post(cfg.SUBMIT_URL, json=n_data)

            if response.status_code == 200:
                st.success("Data sent successfully.")
                with st.expander("Show/Close sent data"):
                    st.json(response.json())
                st.cache_data.clear()
                data = self.load_data()
                graph_generator = utils.GenerateGraph(data)
                self.dispaly_graphs(graph_generator)
            else:
                st.error("An error occured while sending the data.")
                self.logger.info(n_data)
                self.logger.info(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error("Could not connect to the server.")
            self.logger.error(f"Connection error: {e}")


    def run(self):
        data = self.load_data()
        graph_generator = utils.GenerateGraph(data)
        self.dispaly_graphs(graph_generator)
        self.display_form()


if __name__ == "__main__":
    MentalDataFrontend()
