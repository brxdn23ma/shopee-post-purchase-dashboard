import pandas as pd
from pathlib import Path

TOTAL_ORDERS = 20000


def load_data():

    df = pd.read_csv(
        "data/disputes.csv",
        parse_dates=[
            "order_date",
            "case_open_date",
            "evidence_collection_date",
            "seller_response_date",
            "investigation_date",
            "decision_date",
            "refund_date",
            "close_date"
        ]
    )
    return df


# ==========================================
# EXECUTIVE KPIs
# ==========================================

def get_complaint_rate(df):

    return len(df) / TOTAL_ORDERS


def get_avg_resolution_time(df):

    return df["resolution_days"].mean()


def get_p95_resolution_time(df):

    return df["resolution_days"].quantile(0.95)


def get_refund_success_rate(df):

    return df["refund_approved"].mean()


def get_reopen_rate(df):

    return df["reopened"].mean()


def get_average_csat(df):

    return df["csat"].mean()


# ==========================================
# HEALTH INDEX
# ==========================================

def get_health_index(df):

    resolution_score = max(
        0,
        100 - (get_avg_resolution_time(df) * 5)
    )

    csat_score = (
        get_average_csat(df) / 5
    ) * 100

    refund_score = (
        get_refund_success_rate(df)
    ) * 100

    reopen_score = (
        1 - get_reopen_rate(df)
    ) * 100

    complaint_score = (
        1 - get_complaint_rate(df)
    ) * 100

    health_index = (
        resolution_score * 0.30
        + csat_score * 0.25
        + refund_score * 0.20
        + reopen_score * 0.15
        + complaint_score * 0.10
    )

    return round(health_index, 2)


# ==========================================
# PROCESS BOTTLENECKS
# ==========================================

def get_stage_analysis(df):

    stage_df = pd.DataFrame({
        "stage": [
            "Evidence Collection",
            "Seller Response",
            "Investigation",
            "Decision",
            "Refund Processing"
        ],

        "avg_days": [

            (
                df["evidence_collection_date"]
                - df["case_open_date"]
            ).dt.days.mean(),

            (
                df["seller_response_date"]
                - df["evidence_collection_date"]
            ).dt.days.mean(),

            (
                df["investigation_date"]
                - df["seller_response_date"]
            ).dt.days.mean(),

            (
                df["decision_date"]
                - df["investigation_date"]
            ).dt.days.mean(),

            (
                df["refund_date"]
                - df["decision_date"]
            ).dt.days.mean()

        ]
    })

    return stage_df


# ==========================================
# CATEGORY ANALYSIS
# ==========================================

def get_category_metrics(df):

    result = (
        df.groupby("category")
        .agg(
            avg_resolution_time=(
                "resolution_days",
                "mean"
            ),
            csat=(
                "csat",
                "mean"
            ),
            refund_success=(
                "refund_approved",
                "mean"
            ),
            reopen_rate=(
                "reopened",
                "mean"
            )
        )
        .reset_index()
    )

    return result


# ==========================================
# SELLER ANALYSIS
# ==========================================

def get_seller_metrics(df):

    result = (
        df.groupby("seller_type")
        .agg(
            avg_resolution_time=(
                "resolution_days",
                "mean"
            ),
            csat=(
                "csat",
                "mean"
            ),
            refund_success=(
                "refund_approved",
                "mean"
            ),
            reopen_rate=(
                "reopened",
                "mean"
            )
        )
        .reset_index()
    )

    return result


# ==========================================
# LOGISTICS ANALYSIS
# ==========================================

def get_logistics_metrics(df):

    result = (
        df.groupby("logistics_provider")
        .agg(
            avg_resolution_time=(
                "resolution_days",
                "mean"
            ),
            csat=(
                "csat",
                "mean"
            ),
            refund_success=(
                "refund_approved",
                "mean"
            ),
            reopen_rate=(
                "reopened",
                "mean"
            )
        )
        .reset_index()
    )

    return result


# ==========================================
# RETENTION ANALYSIS
# ==========================================

def get_retention_analysis(df):

    temp = df.copy()

    temp["resolution_bucket"] = pd.cut(
        temp["resolution_days"],
        bins=[0, 3, 7, 999],
        labels=[
            "<3 Days",
            "3-7 Days",
            ">7 Days"
        ]
    )

    result = (
        temp.groupby(
            "resolution_bucket",
            observed=False
        )
        .agg(
            retention_30d=(
                "retained_30d",
                "mean"
            ),
            retention_90d=(
                "retained_90d",
                "mean"
            ),
            cases=(
                "order_id",
                "count"
            )
        )
        .reset_index()
    )

    return result


# ==========================================
# MONTHLY TREND
# ==========================================

def get_monthly_trend(df):

    temp = df.copy()

    temp["month"] = (
        temp["case_open_date"]
        .dt.to_period("M")
        .astype(str)
    )

    trend = (
        temp.groupby("month")
        .agg(
            avg_resolution_time=(
                "resolution_days",
                "mean"
            ),
            csat=(
                "csat",
                "mean"
            ),
            cases=(
                "order_id",
                "count"
            )
        )
        .reset_index()
    )

    return trend