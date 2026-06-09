import streamlit as st
import plotly.express as px

from src.analysis import *

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Shopee Post-Purchase Dashboard",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📦 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Executive Overview",
        "Process Bottlenecks",
        "Root Cause Analysis",
        "Retention Impact"
    ]
)

# ==========================================
# EXECUTIVE OVERVIEW
# ==========================================

st.info(
    """
    Executive Summary

    Post-purchase experience is a key driver of customer retention.
    This dashboard identifies operational bottlenecks,
    measures dispute resolution performance,
    and quantifies the retention impact of poor customer experiences.
    """
)

if page == "Executive Overview":

    st.title("📊 Post-Purchase Experience Dashboard")

    st.markdown(
        """
        Monitor customer dispute performance,
        identify operational risks,
        and quantify business impact.
        """
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Complaint Rate",
        f"{get_complaint_rate(df):.1%}"
    )

    col2.metric(
        "Avg Resolution Time",
        f"{get_avg_resolution_time(df):.1f} Days"
    )

    col3.metric(
        "P95 Resolution Time",
        f"{get_p95_resolution_time(df):.1f} Days"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Refund Success Rate",
        f"{get_refund_success_rate(df):.1%}"
    )

    col5.metric(
        "Reopen Rate",
        f"{get_reopen_rate(df):.1%}"
    )

    col6.metric(
        "Average CSAT",
        f"{get_average_csat(df):.2f}"
    )

    st.divider()

    health_index = get_health_index(df)

    st.subheader("Key Insights")

    st.markdown(
        """
        • Cross-border sellers exhibit the longest resolution times.

        • Seller response stage is the primary process bottleneck.

        • Faster dispute resolution is strongly associated with higher customer retention.

        • Reopened cases show significantly lower customer loyalty.
        """
    )

    st.metric(
        "Post-Purchase Health Index",
        f"{health_index}/100"
    )

    if health_index >= 90:  # Health Status Thresholds
        status = "🟢 Excellent"

    elif health_index >= 75:
        status = "🟡 Healthy"

    elif health_index >= 60:
        status = "🟠 At Risk"

    else:
        status = "🔴 Critical"

    st.success(f"Current Status: {status}")

    st.divider()

    trend_df = get_monthly_trend(df)

    fig = px.line(
        trend_df,
        x="month",
        y="avg_resolution_time",
        title="Monthly Resolution Time Trend",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# PROCESS BOTTLENECKS
# ==========================================

elif page == "Process Bottlenecks":

    st.title("⏳ Process Bottleneck Analysis")

    stage_df = get_stage_analysis(df)

    fig = px.bar(
        stage_df,
        x="stage",
        y="avg_days",
        title="Average Days by Process Stage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        stage_df,
        use_container_width=True
    )

    worst_stage = (
        stage_df.sort_values(
            "avg_days",
            ascending=False
        )
        .iloc[0]
    )

    st.warning(
        f"""
        Primary Bottleneck:

        {worst_stage['stage']}

        Average Delay:
        {worst_stage['avg_days']:.1f} days
        """
    )

# ==========================================
# ROOT CAUSE ANALYSIS
# ==========================================

elif page == "Root Cause Analysis":

    st.title("🔍 Root Cause Segmentation")

    segment = st.selectbox(
        "Segment By",
        [
            "Category",
            "Seller Type",
            "Logistics Provider"
        ]
    )

    if segment == "Category":

        segment_df = get_category_metrics(df)
        label = "category"

    elif segment == "Seller Type":

        segment_df = get_seller_metrics(df)
        label = "seller_type"

    else:

        segment_df = get_logistics_metrics(df)
        label = "logistics_provider"

    worst_segment = (
        segment_df.sort_values(
            "avg_resolution_time",
            ascending=False
        )
        .iloc[0]
    )

    st.warning(
        f"""
        Highest Risk Segment:

        {worst_segment[label]}

        Avg Resolution Time:
        {worst_segment['avg_resolution_time']:.1f} days
        """
    )

    fig = px.bar(
        segment_df,
        x=label,
        y="avg_resolution_time",
        title="Average Resolution Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig2 = px.bar(
        segment_df,
        x=label,
        y="csat",
        title="Average CSAT"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(
        segment_df,
        use_container_width=True
    )

# ==========================================
# RETENTION IMPACT
# ==========================================

elif page == "Retention Impact":

    st.title("📈 Business Impact of Resolution Speed")

    retention_df = get_retention_analysis(df)

    fig = px.bar(
        retention_df,
        x="resolution_bucket",
        y="retention_90d",
        title="90-Day Retention by Resolution Speed",
        text_auto=".1%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig2 = px.bar(
        retention_df,
        x="resolution_bucket",
        y="retention_30d",
        title="30-Day Retention by Resolution Speed",
        text_auto=".1%"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(
        retention_df,
        use_container_width=True
    )