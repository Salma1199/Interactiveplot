
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

# if __name__ == "__main__":
#     df = pd.read_csv('optimal2_political_lines.csv')
#     interactive_plot(df)

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Define a consistent color map for your categories
CATEGORY_COLORS = {
    'integration': '#1f77b4',  # blue
    'public attitudes': '#ff7f0e',  # orange
    'flows': '#2ca02c',  # green
    'systems/policy': '#d62728',  # red
    'economics': '#9467bd',  # purple
    'crime/law': '#8c564b',  # brown
    'international issues/benchmarks': '#e377c2',  # pink
}

def interactive_plot(result_df):
    st.title('Interactive Plot of Cluster Results')

    plot_options = {
        'Guardian vs Telegraph': ('Effective_Guardian_prop', 'Effective_Telegraph_prop'),
        'Global North vs Global South': ('GS_prop', None),
        'EU vs Non-EU': ('nonEU_prop', None)
    }
    plot_type = st.selectbox('Plot Type', options=list(plot_options.keys()))

    color_options = {
        'Macro Topics': 'macro',
        'Perspective (WS)': 'Perspective(ws)',
        'Perspective (WO)': 'Perspective(wo)',
        'Value (S)': 'Value(s)',
        'Value (O)': 'Value(o)',
        'Dictionary Counts': 'total_dictionaries'
    }
    color = st.selectbox('Color', options=list(color_options.keys()))

    size_options = {
        'Number of Articles': 'n_articles',
        'Number of SVOs': 'num_svos'
    }
    size = st.selectbox('Size', options=list(size_options.keys()))

    num_clusters = st.slider('Number of Clusters', min_value=1, max_value=len(result_df), value=10)
    filtered_df = result_df.nlargest(num_clusters, 'n_articles')

    if not filtered_df.empty:
        fig = go.Figure()

        x_col, y_col = plot_options[plot_type]
        is_horizontal = y_col is None

        if is_horizontal:
            y_values = [0] * len(filtered_df)
        else:
            y_values = filtered_df[y_col]

        # Create hover text
        if plot_type == 'Guardian vs Telegraph':
            hover_text = filtered_df.apply(lambda row: (
                f"Title: {row['title']}<br>"
                f"Macro: {row['macro']}<br>"
                f"Guardian Proportion: {row[x_col]:.3f}<br>"
                f"Telegraph Proportion: {row[y_col]:.3f}<br>"
                f"{size}: {row[size_options[size]]}"
            ), axis=1)
        elif plot_type == 'Global North vs Global South':
            hover_text = filtered_df.apply(lambda row: (
                f"Title: {row['title']}<br>"
                f"Macro: {row['macro']}<br>"
                f"Global South Proportion: {row[x_col]:.3f}<br>"
                f"{size}: {row[size_options[size]]}"
            ), axis=1)
        else:  # EU vs Non-EU
            hover_text = filtered_df.apply(lambda row: (
                f"Title: {row['title']}<br>"
                f"Macro: {row['macro']}<br>"
                f"Non-EU Proportion: {row[x_col]:.3f}<br>"
                f"{size}: {row[size_options[size]]}"
            ), axis=1)

        if color_options[color] == 'macro':
            for category in filtered_df['macro'].unique():
                subset = filtered_df[filtered_df['macro'] == category]
                fig.add_trace(go.Scatter(
                    x=subset[x_col],
                    y=y_values[:len(subset)] if is_horizontal else subset[y_col],
                    mode='markers',
                    name=category,
                    marker=dict(
                        size=subset[size_options[size]],
                        color=CATEGORY_COLORS.get(category, '#7f7f7f'),  # default to gray if category not found
                        sizemode='area',
                        sizeref=2.*max(filtered_df[size_options[size]])/(40.**2),
                        sizemin=4
                    ),
                    text=hover_text[subset.index],
                    hoverinfo='text'
                ))
        else:
            fig.add_trace(go.Scatter(
                x=filtered_df[x_col],
                y=y_values if is_horizontal else filtered_df[y_col],
                mode='markers',
                marker=dict(
                    size=filtered_df[size_options[size]],
                    color=filtered_df[color_options[color]],
                    colorscale='Viridis',
                    showscale=True,
                    sizemode='area',
                    sizeref=2.*max(filtered_df[size_options[size]])/(40.**2),
                    sizemin=4
                ),
                text=hover_text,
                hoverinfo='text'
            ))

        # Set axis titles
        if plot_type == 'Guardian vs Telegraph':
            x_title = 'Guardian Proportion'
            y_title = 'Telegraph Proportion'
        elif plot_type == 'Global North vs Global South':
            x_title = 'Global South Proportion'
            y_title = None
        else:  # EU vs Non-EU
            x_title = 'Non-EU Proportion'
            y_title = None

        fig.update_layout(
            title=f'Distribution of Clusters: {plot_type}',
            xaxis_title=x_title,
            yaxis_title=y_title,
            showlegend=color_options[color] == 'macro',
            yaxis_visible=not is_horizontal,
            yaxis_showticklabels=not is_horizontal,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    df = pd.read_csv('original_political_lines.csv')
    interactive_plot(df)
