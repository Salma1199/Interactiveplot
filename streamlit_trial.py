
# import pandas as pd
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# def interactive_plot(result_df):
#     st.title('Interactive Plot of Cluster Results')

#     x_axis = st.selectbox('X-Axis', options=['Effective_Guardian_prop', 'GN_prop', 'EU_prop'], index=0)
#     y_axis = st.selectbox('Y-Axis', options=['Effective_Telegraph_prop', 'GS_prop', 'nonEU_prop'], index=1)
#     color = st.selectbox('Color', options=['macro', 'Perspective(ws)', 'Perspective(wo)', 'Value(s)', 'Value(o)', 'total_dictionaries'], index=0)
#     size = st.selectbox('Size', options=['n_articles', 'num_svos'], index=0)
#     num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)

#     filtered_df = result_df.nlargest(num_clusters, 'n_articles')
    
#     if not filtered_df.empty:
#         fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=color, size=size,
#                          size_max=15, hover_name='title', template='simple_white')
#         fig.update_layout(transition_duration=500)
#         st.plotly_chart(fig, use_container_width=True)

import pandas as pd
import streamlit as st
import plotly.express as px

def interactive_plot(result_df):
    st.title('Interactive Plot of Cluster Results')

    # User-friendly mappings for x-axis and y-axis
    x_axis_options = {
        'Guardian Proportion': 'Effective_Guardian_prop',
        'GN Proportion': 'GN_prop',
        'EU Proportion': 'EU_prop'
    }
    y_axis_options = {
        'Telegraph Proportion': 'Effective_Telegraph_prop',
        'GS Proportion': 'GS_prop',
        'Non-EU Proportion': 'nonEU_prop'
    }

    # User-friendly options for color
    color_options = {
        'Macro Topics': 'macro',
        'Perspective (WS)': 'Perspective(ws)',
        'Perspective (WO)': 'Perspective(wo)',
        'Value (S)': 'Value(s)',
        'Value (O)': 'Value(o)',
        'Dictionary Counts': 'total_dictionaries'
    }

    # User-friendly options for size
    size_options = {
        'Number of Articles': 'n_articles',
        'Number of SVOs': 'num_svos'
    }

    # Streamlit widgets for user interaction
    x_axis = st.selectbox('X-Axis', options=list(x_axis_options.keys()), index=0)
    y_axis = st.selectbox('Y-Axis', options=list(y_axis_options.keys()), index=1)
    color = st.selectbox('Color', options=list(color_options.keys()), index=0)
    size = st.selectbox('Size', options=list(size_options.keys()), index=0)
    num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)

    # Filter the data based on the number of clusters
    filtered_df = result_df.nlargest(num_clusters, size_options[size])

    # Create and display the plot
    if not filtered_df.empty:
        fig = px.scatter(
            filtered_df,
            x=x_axis_options[x_axis],
            y=y_axis_options[y_axis],
            color=color_options[color],
            size=size_options[size],
            size_max=15,
            hover_name='title',
            template='simple_white'
        )
        fig.update_layout(transition_duration=500)
        st.plotly_chart(fig, use_container_width=True)
        
if __name__ == "__main__":
    df = pd.read_csv('original_political_lines.csv')
    interactive_plot(df)
