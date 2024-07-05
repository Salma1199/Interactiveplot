
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px

def interactive_plot(result_df):
    st.title('Interactive Plot of Cluster Results')

    x_axis = st.selectbox('X-Axis', options=['Effective_Guardian_prop', 'GN_prop', 'EU_prop'], index=0)
    y_axis = st.selectbox('Y-Axis', options=['Effective_Telegraph_prop', 'GS_prop', 'nonEU_prop'], index=1)
    color = st.selectbox('Color', options=['macro', 'Perspective(ws)', 'Value(s)', 'total_dictionaries', 'dehuman_score'], index=0)
    size = st.selectbox('Size', options=['n_articles', 'num_svos'], index=0)
    num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)

    filtered_df = result_df.nlargest(num_clusters, 'n_articles')
    
    if not filtered_df.empty:
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color, size=size,
                         size_max=15, hover_name='title', template='simple_white')
        fig.update_layout(transition_duration=500)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    df = pd.read_csv('optimal2_political_lines.csv')
    interactive_plot(df)