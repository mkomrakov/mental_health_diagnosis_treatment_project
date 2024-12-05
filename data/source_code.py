source_code_data_list = {
    'first_table': """
    men_df = df[df['Gender'] == 'Male']

    diagnosis_counts_men = men_df['Diagnosis'].value_counts()

    diagnosis_percentages_men = (diagnosis_counts_men / diagnosis_counts_men.sum()) * 100

    fig = go.Figure(
        data=[go.Pie(
            labels=diagnosis_percentages_men.index,
            values=diagnosis_percentages_men,
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            marker=dict(line=dict(color='#000000', width=1))
        )]
    )

    fig.update_layout(
        title='Distribution of Diagnoses among Men',
        template='plotly_white'
    )

    fig.show()
    """,
    'second_table': '''
    women_df = df[df['Gender'] == 'Female']

    diagnosis_counts = women_df['Diagnosis'].value_counts()

    diagnosis_percentages = (diagnosis_counts / diagnosis_counts.sum()) * 100

    fig = go.Figure(
        data=[go.Pie(
            labels=diagnosis_percentages.index,
            values=diagnosis_percentages,
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            marker=dict(line=dict(color='#000000', width=1))
        )]
    )

    fig.update_layout(
        title='Distribution of Diagnoses among Women',
        template='plotly_white'
    )

    fig.show()''',
    'third_table': """
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

    grouped = df.groupby('Age').agg({
        'Symptom Severity (1-10)': 'mean',
        'Stress Level (1-10)': 'mean'
    }).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grouped['Age'],
        y=grouped['Symptom Severity (1-10)'],
        mode='lines+markers',
        name='Symptom Severity',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=grouped['Age'],
        y=grouped['Stress Level (1-10)'],
        mode='lines+markers',
        name='Stress Level',
        line=dict(color='red')
    ))

    fig.update_layout(
        title='Average Symptom Severity and Stress Level by Age',
        xaxis_title='Age',
        yaxis_title='Average values',
        legend_title='Metrics',
        template='plotly_white'
    )

    fig.show()""", 
        'fourth_table': """
    grouped_activity = df.groupby('Physical Activity (hrs/week)').agg({
        'Sleep Quality (1-10)': 'mean',
        'Mood Score (1-10)': 'mean'
    }).reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grouped_activity['Physical Activity (hrs/week)'],
        y=grouped_activity['Sleep Quality (1-10)'],
        name='Sleep Quality',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=grouped_activity['Physical Activity (hrs/week)'],
        y=grouped_activity['Mood Score (1-10)'],
        name='Mood Score',
        marker_color='green'
    ))

    fig.update_layout(
        title='Average Sleep Quality and Mood Score by Physical Activity (hrs/week)',
        xaxis_title='Physical Activity (hrs/week)',
        yaxis_title='Average values',
        barmode='group',
        legend_title='Metrics',
        template='plotly_white'
    )

    fig.show()""",
        'fifth_table': """
        grouped_therapy = df.groupby('Therapy Type').agg({
            'Treatment Duration (weeks)': 'mean',
            'Treatment Progress (1-10)': 'mean',
            'Symptom Severity (1-10)': 'mean'
        }).reset_index()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Treatment Duration (weeks)'],
            name='Treatment Duration (weeks)',
            marker_color='purple'
        ))

        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Treatment Progress (1-10)'],
            name='Treatment Progress (1-10)',
            marker_color='orange'
        ))

        fig.add_trace(go.Bar(
            x=grouped_therapy['Therapy Type'],
            y=grouped_therapy['Symptom Severity (1-10)'],
            name='Symptom Severity (1-10)',
            marker_color='blue'
        ))

        fig.update_layout(
            title='Average Treatment Metrics by Therapy Type',
            xaxis_title='Therapy Type',
            yaxis_title='Average values',
            barmode='group',
            legend_title='Metrics',
            template='plotly_white'
        )

        fig.show()""",
    'sixth_table': """
    therapy_stats = (
        df.groupby('Therapy Type')['Outcome']
        .value_counts(normalize=True)
        .mul(10)  # Convert to 10-point scale
        .unstack(fill_value=0)
        [['Deteriorated', 'No Change', 'Improved']]
    )

    therapy_stats.reset_index(inplace=True)

    therapy_melted = therapy_stats.melt(
        id_vars='Therapy Type',
        value_vars=['Deteriorated', 'No Change', 'Improved'],
        var_name='Outcome',
        value_name='Average values'
    )

    import plotly.express as px

    fig = px.bar(
        therapy_melted,
        x='Therapy Type',
        y='Average values',
        color='Outcome',
        barmode='group',
        text='Average values',
        title="Analysis of Outcomes by Therapy Type",
        labels={
            'Therapy Type': 'Therapy Type',
            'Average values': 'Average Values (10-point scale)',
            'Outcome': 'Outcome'
        }
    )

    fig.update_layout(
        xaxis_title="Therapy Type",
        yaxis_title="Average Values (10-point scale)",
        legend_title="Outcome",
        template="plotly_white"
    )

    fig.show()"""
}
