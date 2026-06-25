import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Property Sales Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .stApp {
        background-image: linear-gradient(to bottom, #ffffff, #f0f2f6);
    }
    .header {
        color: #2c3e50;
        text-align: center;
        padding: 1rem;
    }
    .plot-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .section-title {
        color: #3498db;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="header">🏠 Property Sales Analytics Dashboard</h1>', unsafe_allow_html=True)

# File upload
uploaded_file = st.sidebar.file_uploader("📤 Upload your sales data (CSV)", type="csv")

if uploaded_file is not None:
    df_sales = pd.read_csv(uploaded_file)
    
    # Check required columns
    required_columns = {'price', 'price_per_square', 'property_type'}
    if not required_columns.issubset(df_sales.columns):
        st.error(f"❌ Missing required columns in dataset. Needed: {', '.join(required_columns)}")
        st.stop()
    
    # Create filtered datasets
    p1 = df_sales['price'].quantile(0.01)
    p99 = df_sales['price'].quantile(0.99)
    p1_ = df_sales['price_per_square'].quantile(0.01)
    p99_ = df_sales['price_per_square'].quantile(0.99)
    df_filtered = df_sales[(df_sales['price'] >= p1) & (df_sales['price'] <= p99)]
    df_filtered_sqaure = df_sales[(df_sales['price_per_square'] >= p1_) & (df_sales['price_per_square'] <= p99_)]

    # ==== 1ST TO 99TH PERCENTILE FOR ALL SALES ====
    st.markdown('<h2 class="section-title">Price Distribution Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig1 = px.histogram(
            df_filtered,
            x="price",
            nbins=500,
            title="<b>Property Prices Distribution</b><br>(1st to 99th Percentile)",
            labels={"price": "Price", "count": "Number of Properties"},
            log_x=True,
            color_discrete_sequence=['#3498db']
        )
        fig1.update_traces(marker_line_color='black', marker_line_width=1)
        fig1.update_layout(bargap=0.05, template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig2 = px.histogram(
            df_filtered_sqaure,
            x="price_per_square",
            nbins=500,
            title="<b>Price per Square Distribution</b><br>(1st to 99th Percentile)",
            labels={"price_per_square": "Price per Square", "count": "Number of Properties"},
            log_x=True,
            color_discrete_sequence=['#2ecc71']
        )
        fig2.update_traces(marker_line_color='black', marker_line_width=1)
        fig2.update_layout(bargap=0.05, template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ==== LOG HISTOGRAM FOR ALL SALES SELL ====
    st.markdown('<h2 class="section-title">Logarithmic Price Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig3 = px.histogram(
            df_sales,
            x="price",
            nbins=120,
            title="<b>Property Prices</b> (Log Scale)",
            labels={"price": "Price (log scale)", "count": "Number of Properties"},
            log_x=True,
            color_discrete_sequence=['#9b59b6']
        )
        fig3.update_traces(marker_line_color='black', marker_line_width=1)
        fig3.update_layout(bargap=0.05, template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig4 = px.histogram(
            df_sales,
            x="price_per_square",
            nbins=100,
            title="<b>Price per Square</b> (Log Scale)",
            labels={"price_per_square": "Price per Square (log scale)", "count": "Number of Properties"},
            log_x=True,
            color_discrete_sequence=['#e74c3c']
        )
        fig4.update_traces(marker_line_color='black', marker_line_width=1)
        fig4.update_layout(bargap=0.05, template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ==== PLOT FOR ALL PROPERTY TYPES SELL ====
    st.markdown('<h2 class="section-title">Property Type Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig5 = px.histogram(
            df_filtered,
            x="price",
            nbins=500,
            color="property_type",
            barmode="overlay",
            title="<b>Price Distribution by Property Type</b>",
            labels={"price": "Price", "count": "Number of Properties"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig5.update_traces(marker_line_color='black', marker_line_width=0.5, opacity=0.7)
        fig5.update_layout(bargap=0.05, template="plotly_white", legend_title="Property Type")
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        fig6 = px.histogram(
            df_filtered,
            x="price_per_square",
            nbins=500,
            color="property_type",
            barmode="overlay",
            title="<b>Price per Square by Property Type</b>",
            labels={"price_per_square": "Price per Square", "count": "Number of Properties"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig6.update_traces(marker_line_color='black', marker_line_width=0.5, opacity=0.7)
        fig6.update_layout(bargap=0.05, template="plotly_white", legend_title="Property Type")
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ==== MAIN SELL ====
    st.markdown('<h2 class="section-title">Detailed Property Type Breakdown</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Sort property types from highest count to lowest for price count
    type_counts = df_filtered["property_type"].value_counts()
    property_types = type_counts.index.tolist()
    max_count = 0
    hist_data = {}
    for ptype in property_types:
        counts, bin_edges = np.histogram(
            df_filtered[df_filtered["property_type"] == ptype]["price"], 
            bins=500
        )
        counts = counts + 1  # Avoid zero counts for log scale
        hist_data[ptype] = (counts, bin_edges)
        max_count = max(max_count, counts.max())

    # Create subplots with sorted order
    fig7 = make_subplots(
        rows=len(property_types),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=[f"<b>{ptype}</b>" for ptype in property_types]
    )

    colors = px.colors.qualitative.Pastel
    for i, ptype in enumerate(property_types, start=1):
        counts, bin_edges = hist_data[ptype]
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        
        fig7.add_trace(
            go.Bar(
                x=bin_centers,
                y=counts,
                marker_line_color='black',
                marker_line_width=0.5,
                opacity=0.8,
                name=ptype,
                marker_color=colors[i % len(colors)]
            ),
            row=i,
            col=1
        )
        
        fig7.update_yaxes(
            type="log",
            range=[0, np.log10(max_count)],
            showticklabels=(i == 1),
            row=i,
            col=1
        )

    fig7.update_layout(
        height=250 * len(property_types),
        title="<b>Property Price Distribution by Property Type</b><br>(Sorted by Count, Log Scale)",
        bargap=0.05,
        legend_title="Property Type",
        margin=dict(l=0, r=0, t=80, b=0),
        template="plotly_white",
        showlegend=False
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    # Sort property types from highest count to lowest for price_per_square count
    type_counts_square = df_filtered_sqaure["property_type"].value_counts()
    property_types_square = type_counts_square.index.tolist()
    max_count_square = 0
    hist_data_square = {}

    for ptype in property_types_square:
        counts, bin_edges = np.histogram(
            df_filtered_sqaure[df_filtered_sqaure["property_type"] == ptype]["price_per_square"], 
            bins=500
        )
        counts = counts + 1  # Avoid zero counts for log scale
        hist_data_square[ptype] = (counts, bin_edges)
        max_count_square = max(max_count_square, counts.max())

    # Create subplots with sorted order
    fig8 = make_subplots(
        rows=len(property_types_square),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=[f"<b>{ptype}</b>" for ptype in property_types_square]
    )

    for i, ptype in enumerate(property_types_square, start=1):
        counts, bin_edges = hist_data_square[ptype]
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        
        fig8.add_trace(
            go.Bar(
                x=bin_centers,
                y=counts,
                marker_line_color='black',
                marker_line_width=0.5,
                opacity=0.8,
                name=ptype,
                marker_color=colors[i % len(colors)]
            ),
            row=i,
            col=1
        )
        
        fig8.update_yaxes(
            type="log",
            range=[0, np.log10(max_count_square)],
            showticklabels=(i == 1),
            row=i,
            col=1
        )

    fig8.update_layout(
        height=250 * len(property_types_square),
        title="<b>Price per Square Distribution by Property Type</b><br>(Sorted by Count, Log Scale)",
        bargap=0.05,
        legend_title="Property Type",
        margin=dict(l=0, r=0, t=80, b=0),
        template="plotly_white",
        showlegend=False
    )
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("ℹ️ Please upload a CSV file to begin analysis")
    st.image("https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", 
             caption="Property Sales Analytics Dashboard")