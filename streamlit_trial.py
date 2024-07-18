
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

# import pandas as pd
# import streamlit as st
# import plotly.express as px

# def interactive_plot(result_df):
#     st.title('Interactive Plot of Cluster Results')

#     # Mapping user-friendly names to DataFrame column names for axes
#     x_axis_options = {
#         'Guardian Proportion': 'Effective_Guardian_prop',
#         'GN Proportion': 'GN_prop',
#         'EU Proportion': 'EU_prop'
#     }
#     y_axis_options = {
#         'Telegraph Proportion': 'Effective_Telegraph_prop',
#         'GS Proportion': 'GS_prop',
#         'Non-EU Proportion': 'nonEU_prop'
#     }

#     # Select boxes for X and Y axes using friendly names
#     x_axis = st.selectbox('X-Axis', options=list(x_axis_options.keys()), index=0)
#     y_axis = st.selectbox('Y-Axis', options=list(y_axis_options.keys()), index=0)

#     # Mapping for color options with friendly names
#     color_options = {
#         'Macro Topics': 'macro',
#         'Perspective (WS)': 'Perspective(ws)',
#         'Perspective (WO)': 'Perspective(wo)',
#         'Value (S)': 'Value(s)',
#         'Value (O)': 'Value(o)',
#         'Dictionary Counts': 'total_dictionaries'
#     }
#     color = st.selectbox('Color', options=list(color_options.keys()), index=0)

#     # Size options with friendly names
#     size_options = {
#         'Number of Articles': 'n_articles',
#         'Number of SVOs': 'num_svos'
#     }
#     size = st.selectbox('Size', options=list(size_options.keys()), index=0)

#     num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)

#     # Filtering DataFrame based on the number of clusters
#     filtered_df = result_df.nlargest(num_clusters, 'n_articles')
    
#     if not filtered_df.empty:
#         fig = px.scatter(
#             filtered_df,
#             x=x_axis_options[x_axis],  # Map user-friendly names to DataFrame columns for X axis
#             y=y_axis_options[y_axis],  # Map user-friendly names to DataFrame columns for Y axis
#             color=color_options[color],  # Use the mapping for color
#             size=size_options[size],  # Map user-friendly names to DataFrame columns for size
#             size_max=15,
#             hover_name='title',
#             template='simple_white'
#         )
#         # Update axis titles to be user-friendly
#         fig.update_layout(
#             xaxis_title=x_axis,
#             yaxis_title=y_axis,
#             transition_duration=500
#          )
#          st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     df = pd.read_csv('original_political_lines.csv')
#     interactive_plot(df)

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def interactive_plot(result_df):
    st.title('Interactive Plot of Cluster Results')

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

    x_axis = st.selectbox('X-Axis', options=list(x_axis_options.keys()), index=0)
    y_axis = st.selectbox('Y-Axis', options=list(y_axis_options.keys()), index=1)

    color_options = {
        'Macro Topics': 'macro',
        'Perspective (WS)': 'Perspective(ws)',
        'Perspective (WO)': 'Perspective(wo)',
        'Value (S)': 'Value(s)',
        'Value (O)': 'Value(o)',
        'Dictionary Counts': 'total_dictionaries'
    }
    color = st.selectbox('Color', options=list(color_options.keys()), index=0)

    size_options = {
        'Number of Articles': 'n_articles',
        'Number of SVOs': 'num_svos'
    }
    size = st.selectbox('Size', options=list(size_options.keys()), index=0)

    num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)
    filtered_df = result_df.nlargest(num_clusters, 'n_articles')

    if not filtered_df.empty:
        is_color_categorical = color_options[color] == 'macro'
        
        if x_axis == 'Guardian Proportion' and y_axis == 'Telegraph Proportion':
            # Regular scatter plot for Guardian vs Telegraph
            fig = px.scatter(
                filtered_df,
                x=x_axis_options[x_axis],
                y=y_axis_options[y_axis],
                color=color_options[color],
                size=size_options[size],
                size_max=50,
                hover_name='title',
                color_discrete_sequence=px.colors.qualitative.Set1 if is_color_categorical else None,
                color_continuous_scale='Viridis' if not is_color_categorical else None,
                template='simple_white'
            )
        else:
            # Horizontal line plot for GN/GS and EU/Non-EU
            if 'GS Proportion' in [x_axis, y_axis]:
                x_values = filtered_df['GS_prop']
                x_title = 'Global South Proportion'
            elif 'Non-EU Proportion' in [x_axis, y_axis]:
                x_values = filtered_df['nonEU_prop']
                x_title = 'Non-EU Proportion'
            else:
                st.error("Invalid axis combination")
                return

            fig = px.scatter(
                filtered_df,
                x=x_values,
                y=[0] * len(filtered_df),
                color=color_options[color],
                size=size_options[size],
                size_max=50,
                hover_name='title',
                color_discrete_sequence=px.colors.qualitative.Set1 if is_color_categorical else None,
                color_continuous_scale='Viridis' if not is_color_categorical else None,
                template='simple_white'
            )

            fig.update_layout(
                xaxis_title=x_title,
                yaxis_visible=False,
                yaxis_showticklabels=False
            )

        fig.update_layout(
            title=f'Distribution of Clusters Based on {x_axis} and {y_axis}',
            transition_duration=500
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    df = pd.read_csv('original_political_lines.csv')
    interactive_plot(df)
