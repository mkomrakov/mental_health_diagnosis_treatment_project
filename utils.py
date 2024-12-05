import uuid
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class GenerateGraph:
    def __init__(self, data): 
        self.df = data

    def generate_men_chart(self):
        # Фильтрация данных по мужчинам
        men_df = self.df[self.df['Gender'] == 'Male']

        # Подсчет количества мужчин для каждого диагноза
        diagnosis_counts_men = men_df['Diagnosis'].value_counts()

        # Вычисление процентов
        diagnosis_percentages_men = (diagnosis_counts_men / diagnosis_counts_men.sum()) * 100

        # Построение круговой диаграммы с использованием Plotly
        fig = go.Figure(
            data=[go.Pie(
                labels=diagnosis_percentages_men.index,
                values=diagnosis_percentages_men,
                textinfo='label+percent',  # Показывать подписи и проценты
                hoverinfo='label+value+percent',  # Дополнительная информация при наведении
                marker=dict(line=dict(color='#000000', width=1))  # Отделение сегментов черной линией
            )]
        )

        # Настройка графика
        fig.update_layout(
            title='Distribution of Diagnoses among Men',
            template='plotly_white'
        )

        # Отображение графика
        return fig.show()
 
    def generate_women_chart(self):
        # Фильтрация данных по женщинам
        women_df = self.df[self.df['Gender'] == 'Female']

        # Подсчет количества женщин для каждого диагноза
        diagnosis_counts = women_df['Diagnosis'].value_counts()

        # Вычисление процентов
        diagnosis_percentages = (diagnosis_counts / diagnosis_counts.sum()) * 100

        # Построение круговой диаграммы с использованием Plotly
        fig = go.Figure(
            data=[go.Pie(
                labels=diagnosis_percentages.index,
                values=diagnosis_percentages,
                textinfo='label+percent',  # Показывать подписи и проценты
                hoverinfo='label+value+percent',  # Дополнительная информация при наведении
                marker=dict(line=dict(color='#000000', width=1))  # Отделение сегментов черной линией
            )]
        )

        # Настройка графика
        fig.update_layout(
            title='Distribution of Diagnoses among Women',
            template='plotly_white'
        )

        # Отображение графика
        return fig.show()
    
    def sympthom_sev_stress_lev(self):
        # Преобразование данных, если требуется
        self.df['Age'] = pd.to_numeric(self.df['Age'], errors='coerce')

        # Группировка данных по возрасту и вычисление среднего
        grouped = self.df.groupby('Age').agg({
            'Symptom Severity (1-10)': 'mean',
            'Stress Level (1-10)': 'mean'
        }).reset_index()

        # Построение графика с использованием Plotly
        fig = go.Figure()

        # Линия для Symptom Severity
        fig.add_trace(go.Scatter(
            x=grouped['Age'],
            y=grouped['Symptom Severity (1-10)'],
            mode='lines+markers',
            name='Symptom Severity',
            line=dict(color='blue')
        ))

        # Линия для Stress Level
        fig.add_trace(go.Scatter(
            x=grouped['Age'],
            y=grouped['Stress Level (1-10)'],
            mode='lines+markers',
            name='Stress Level',
            line=dict(color='red')
        ))

        # Настройки графика
        fig.update_layout(
            title='Average Symptom Severity and Stress Level by Age',
            xaxis_title='Age',
            yaxis_title='Average values',
            legend_title='Metrics',
            template='plotly_white'
        )

        # Отображение графика
        return fig.show()
    
    def sleep_qual_mood_sc(self):
        # Группировка данных по Physical Activity (hrs/week) и вычисление среднего
        grouped_activity = self.df.groupby('Physical Activity (hrs/week)').agg({
            'Sleep Quality (1-10)': 'mean',
            'Mood Score (1-10)': 'mean'
        }).reset_index()

        # Построение графика с использованием Plotly
        fig = go.Figure()

        # Столбцы для Sleep Quality
        fig.add_trace(go.Bar(
            x=grouped_activity['Physical Activity (hrs/week)'],
            y=grouped_activity['Sleep Quality (1-10)'],
            name='Sleep Quality',
            marker_color='blue'
        ))

        # Столбцы для Mood Score
        fig.add_trace(go.Bar(
            x=grouped_activity['Physical Activity (hrs/week)'],
            y=grouped_activity['Mood Score (1-10)'],
            name='Mood Score',
            marker_color='green'
        ))

        # Настройки графика
        fig.update_layout(
            title='Average Sleep Quality and Mood Score by Physical Activity (hrs/week)',
            xaxis_title='Physical Activity (hrs/week)',
            yaxis_title='Average values',
            barmode='group',  # Группировка столбцов
            legend_title='Metrics',
            template='plotly_white'
        )

        # Отображение графика
        return fig.show()
    
    def avg_treatment_ther_type(self):
        # Группировка данных по Therapy Type и вычисление среднего
        grouped_therapy = self.df.groupby('Therapy Type').agg({
            'Treatment Duration (weeks)': 'mean',
            'Treatment Progress (1-10)': 'mean',
            'Symptom Severity (1-10)': 'mean'  # Добавляем Symptom Severity
        }).reset_index()

        # Построение графика с использованием Plotly
        fig = go.Figure()

        # Столбцы для Treatment Duration
        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Treatment Duration (weeks)'],
            name='Treatment Duration (weeks)',
            marker_color='purple'
        ))

        # Столбцы для Treatment Progress
        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Treatment Progress (1-10)'],
            name='Treatment Progress (1-10)',
            marker_color='orange'
        ))

        # Столбцы для Symptom Severity
        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Symptom Severity (1-10)'],
            name='Symptom Severity (1-10)',
            marker_color='blue'
        ))

        # Настройки графика
        fig.update_layout(
            title='Average Treatment Metrics by Therapy Type',
            xaxis_title='Therapy Type',
            yaxis_title='Average values',
            barmode='group',  # Группировка столбцов
            legend_title='Metrics',
            template='plotly_white'
        )

        # Отображение графика
        return fig.show()
    
    def analysis_outcomes(self):
        # Calculate the distribution of outcomes for each therapy type
        therapy_stats = (
            self.df.groupby('Therapy Type')['Outcome']
            .value_counts(normalize=True)  # Calculate proportions
            .mul(10)  # Convert to 10-point scale
            .unstack(fill_value=0)  # Convert to DataFrame for easier manipulation
            [['Deteriorated', 'No Change', 'Improved']]  # Select relevant outcomes
        )

        # Reset index for plotting
        therapy_stats.reset_index(inplace=True)

        # Melt the DataFrame for use with plotly express
        therapy_melted = therapy_stats.melt(
            id_vars='Therapy Type',
            value_vars=['Deteriorated', 'No Change', 'Improved'],
            var_name='Outcome',
            value_name='Average values'
        )

        # Plot the bar chart
        import plotly.express as px

        fig = px.bar(
            therapy_melted,
            x='Therapy Type',
            y='Average values',
            color='Outcome',
            barmode='group',  # Group bars for each therapy type
            text='Average values',  # Add labels to the bars
            title="Analysis of Outcomes by Therapy Type",
            labels={
                'Therapy Type': 'Therapy Type',
                'Average values': 'Average Values (10-point scale)',
                'Outcome': 'Outcome'
            }
        )

        # Customize layout
        fig.update_layout(
            xaxis_title="Therapy Type",
            yaxis_title="Average Values (10-point scale)",
            legend_title="Outcome",
            template="plotly_white"
        )

        # Show the plot
        return fig.show()

    def generate_key(self, prefix="chart"):
        return f"{prefix}_{uuid.uuid4().hex}"
