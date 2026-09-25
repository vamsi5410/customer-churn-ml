import io
import os
import requests
import pandas as pd
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ChurnAI Enterprise",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. ENTERPRISE UI THEME
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background: #f5f6f7;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background: #eef1f4;
        border-right: 1px solid #d5dce2;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        border-radius: 4px;
        min-height: 38px;
        font-weight: 600;
    }


    /* =========================
       KPI CARDS
       ========================= */

    .kpi-card {
        background: #ffffff;
        border: 1px solid #d9dfe3;
        border-radius: 6px;
        padding: 16px 18px;
        min-height: 105px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }

    .kpi-label {
        color: #64727f;
        font-size: 13px;
    }

    .kpi-value {
        color: #1d2d3d;
        font-size: 29px;
        font-weight: 600;
        margin-top: 8px;
    }

    .kpi-foot {
        color: #64727f;
        font-size: 11px;
        margin-top: 4px;
    }


    /* =========================
       DATAFRAME
       ========================= */

    [data-testid="stDataFrame"] {
        border: 1px solid #d9dfe3;
        border-radius: 6px;
    }


    /* =========================
       DARK MODE
       ========================= */

    @media (prefers-color-scheme: dark) {

        .stApp {
            background: #111827;
        }

        [data-testid="stSidebar"] {
            background: #17202b;
            border-right: 1px solid #34404d;
        }

        .kpi-card {
            background: #1b2530;
            border-color: #3a4652;
        }

        .kpi-value {
            color: #f3f4f6;
        }

        .kpi-label,
        .kpi-foot {
            color: #b8c2cc;
        }

        [data-testid="stDataFrame"] {
            border-color: #3a4652;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. ENTERPRISE HEADER
# ============================================================
# Native Streamlit heading is used here.
# This prevents raw HTML from appearing on the screen.

st.title("◉ ChurnAI Enterprise")

st.caption(
    "Customer Retention & AI Risk Management  |  "
    "AI Operations  |  Workspace"
)


# ============================================================
# 4. API CONFIGURATION
# ============================================================

DEFAULT_API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

try:
    DEFAULT_API_URL = st.secrets.get(
        "API_URL",
        DEFAULT_API_URL
    )
except Exception:
    pass


API_URL = st.sidebar.text_input(
    "FastAPI URL",
    DEFAULT_API_URL
).rstrip("/")


# ============================================================
# 5. APPLICATION TITLE
# ============================================================

st.caption(
    "Enterprise Customer Retention Platform"
)


# ============================================================
# 6. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("### Navigation")

pages = [
    "Executive Dashboard",
    "Customer Prediction",
    "Customer Management",
    "Bulk Prediction",
    "Prediction History",
    "Model Information",
]

page = st.sidebar.radio(
    "Navigation",
    pages
)


# ============================================================
# 7. API HELPER FUNCTIONS
# ============================================================

def api_get(path, **kwargs):
    return requests.get(
        f"{API_URL}{path}",
        timeout=30,
        **kwargs
    )


def api_post(path, **kwargs):
    return requests.post(
        f"{API_URL}{path}",
        timeout=60,
        **kwargs
    )


# ============================================================
# 8. EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("📊 Executive Dashboard")

    st.caption(
        "Enterprise overview of customer churn and retention risk."
    )

    try:

        response = api_get(
            "/analytics/summary"
        )

        response.raise_for_status()

        summary = response.json()


        # ----------------------------------------------------
        # KPI SECTION
        # ----------------------------------------------------

        st.subheader("Business Overview")

        a, b, c, d = st.columns(4)

        a.metric(
            "Total Customers",
            summary["total_customers"]
        )

        b.metric(
            "High Risk",
            summary["high_risk"]
        )

        c.metric(
            "Medium Risk",
            summary["medium_risk"]
        )

        d.metric(
            "Avg Churn Probability",
            f"{summary['average_churn_probability']:.1%}"
        )


        # ----------------------------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------------------------

        st.subheader("Risk Distribution")

        chart = pd.DataFrame(
            {
                "Risk": [
                    "High",
                    "Medium",
                    "Low"
                ],

                "Customers": [
                    summary["high_risk"],
                    summary["medium_risk"],
                    summary["low_risk"],
                ],
            }
        ).set_index("Risk")


        st.bar_chart(chart)


        # ----------------------------------------------------
        # FINANCIAL RISK
        # ----------------------------------------------------

        st.subheader("Financial Risk")

        st.metric(
            "Monthly Revenue at Risk",
            f"₹{summary['monthly_revenue_at_risk']:,.2f}"
        )


    except Exception as exc:

        st.error(
            f"API connection failed: {exc}"
        )


# ============================================================
# 9. CUSTOMER PREDICTION
# ============================================================

elif page == "Customer Prediction":

    st.header(
        "🔮 Customer Churn Prediction"
    )

    st.caption(
        "Use the trained ML model to estimate the customer's churn risk."
    )


    # --------------------------------------------------------
    # CUSTOMER INFORMATION
    # --------------------------------------------------------

    st.subheader("Customer Information")

    customer_id = st.text_input(
        "Customer ID",
        "C-DEMO-001"
    )

    name = st.text_input(
        "Customer Name",
        "Demo Customer"
    )

    email = st.text_input(
        "Email",
        "customer@example.com"
    )

    phone = st.text_input(
        "Phone",
        "+91-9000000000"
    )


    # --------------------------------------------------------
    # CUSTOMER FEATURES
    # --------------------------------------------------------

    st.subheader("Customer Profile")

    c1, c2, c3 = st.columns(3)


    with c1:

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=120,
            value=4
        )

        monthly = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            max_value=10000.0,
            value=109.0
        )

        total = st.number_input(
            "Total Charges",
            min_value=0.0,
            max_value=1000000.0,
            value=436.0
        )


    with c2:

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        internet = st.selectbox(
            "Internet Service",
            [
                "DSL",
                "Fiber optic",
                "No"
            ]
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Bank transfer",
                "Credit card",
                "Mailed check"
            ]
        )


    with c3:

        tech = st.selectbox(
            "Tech Support",
            [
                "No",
                "Yes"
            ]
        )

        security = st.selectbox(
            "Online Security",
            [
                "No",
                "Yes"
            ]
        )


    # --------------------------------------------------------
    # API PAYLOAD
    # --------------------------------------------------------

    payload = {

        "customer_id": customer_id,

        "name": name,

        "email": email,

        "phone": phone,

        "tenure": tenure,

        "monthly_charges": monthly,

        "total_charges": total,

        "contract": contract,

        "internet_service": internet,

        "payment_method": payment,

        "tech_support": tech,

        "online_security": security,
    }


    # --------------------------------------------------------
    # PREDICTION BUTTON
    # --------------------------------------------------------

    if st.button(
        "🚀 Predict Churn",
        type="primary",
        use_container_width=True
    ):

        try:

            response = api_post(
                "/predict",
                json=payload
            )


            if response.ok:

                result = response.json()

                st.session_state[
                    "last_prediction"
                ] = result

                st.success(
                    "Prediction completed successfully."
                )

            else:

                st.error(
                    response.text
                )


        except Exception as exc:

            st.error(
                f"API connection failed: {exc}"
            )


    # --------------------------------------------------------
    # AI RISK ANALYSIS
    # --------------------------------------------------------

    result = st.session_state.get(
        "last_prediction"
    )


    if result:

        st.divider()

        st.subheader(
            "📊 AI Risk Analysis"
        )


        p1, p2, p3 = st.columns(3)


        p1.metric(
            "Churn Probability",
            f"{result['churn_probability']:.1%}"
        )


        p2.metric(
            "Risk Level",
            result["risk_level"]
        )


        p3.metric(
            "Prediction",
            (
                "Likely Churn"
                if result["prediction"]
                else "Likely Stay"
            )
        )


        st.subheader(
            "🤖 AI Retention Recommendation"
        )


        st.info(
            result["recommendation"]
        )


# ============================================================
# 10. CUSTOMER MANAGEMENT
# ============================================================

elif page == "Customer Management":

    st.header(
        "👥 Customer Management"
    )

    st.caption(
        "Create, search and filter customer records."
    )


    # --------------------------------------------------------
    # ADD CUSTOMER
    # --------------------------------------------------------

    with st.expander(
        "➕ Add Customer"
    ):

        with st.form(
            "add_customer"
        ):

            cid = st.text_input(
                "Customer ID"
            )

            name = st.text_input(
                "Name"
            )

            email = st.text_input(
                "Email"
            )

            phone = st.text_input(
                "Phone"
            )

            tenure = st.number_input(
                "Tenure",
                min_value=0,
                max_value=120,
                value=12
            )

            monthly = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                value=70.0
            )

            total = st.number_input(
                "Total Charges",
                min_value=0.0,
                value=840.0
            )

            contract = st.selectbox(
                "Contract",
                [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ]
            )

            internet = st.selectbox(
                "Internet",
                [
                    "DSL",
                    "Fiber optic",
                    "No"
                ]
            )

            payment = st.selectbox(
                "Payment",
                [
                    "Electronic check",
                    "Bank transfer",
                    "Credit card",
                    "Mailed check"
                ]
            )

            tech = st.selectbox(
                "Tech Support",
                [
                    "No",
                    "Yes"
                ]
            )

            security = st.selectbox(
                "Online Security",
                [
                    "No",
                    "Yes"
                ]
            )


            submitted = st.form_submit_button(
                "Create Customer"
            )


            if submitted:

                payload = {

                    "customer_id": cid,

                    "name": name,

                    "email": email,

                    "phone": phone,

                    "tenure": tenure,

                    "monthly_charges": monthly,

                    "total_charges": total,

                    "contract": contract,

                    "internet_service": internet,

                    "payment_method": payment,

                    "tech_support": tech,

                    "online_security": security,
                }


                try:

                    response = api_post(
                        "/customers",
                        json=payload
                    )


                    if response.ok:

                        st.success(
                            "Customer created."
                        )

                    else:

                        st.error(
                            response.text
                        )


                except Exception as exc:

                    st.error(
                        f"API connection failed: {exc}"
                    )


    # --------------------------------------------------------
    # CUSTOMER TABLE
    # --------------------------------------------------------

    try:

        response = api_get(
            "/customers?limit=1000"
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data)


        if not df.empty:

            # ------------------------------------------------
            # SEARCH
            # ------------------------------------------------

            search = st.text_input(
                "🔎 Search by customer ID, name or email"
            )


            if search:

                mask = (

                    df["customer_id"]
                    .astype(str)
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )

                    |

                    df["name"]
                    .astype(str)
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )

                    |

                    df["email"]
                    .astype(str)
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                )

                df = df[mask]


            # ------------------------------------------------
            # RISK FILTER
            # ------------------------------------------------

            risk = st.multiselect(
                "Filter Risk",
                [
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ],
                default=[
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                ]
            )


            if "risk_level" in df.columns:

                df = df[
                    df["risk_level"]
                    .fillna("UNSCORED")
                    .isin(
                        risk + ["UNSCORED"]
                    )
                ]


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "No customers yet. Add one or use Bulk Prediction."
            )


    except Exception as exc:

        st.error(
            f"API connection failed: {exc}"
        )


# ============================================================
# 11. BULK PREDICTION
# ============================================================

elif page == "Bulk Prediction":

    st.header(
        "📂 Bulk Customer Prediction"
    )

    st.caption(
        "Upload a CSV and score multiple customers using the ML model."
    )


    # --------------------------------------------------------
    # CSV TEMPLATE
    # --------------------------------------------------------

    template = pd.DataFrame(
        [
            {
                "customer_id": "C1001",
                "tenure": 4,
                "monthly_charges": 109,
                "total_charges": 436,
                "contract": "Month-to-month",
                "internet_service": "Fiber optic",
                "payment_method": "Electronic check",
                "tech_support": "No",
                "online_security": "No",
            }
        ]
    )


    st.download_button(
        "⬇️ Download CSV Template",

        template.to_csv(
            index=False
        ),

        "churnai_template.csv",

        "text/csv"
    )


    # --------------------------------------------------------
    # FILE UPLOAD
    # --------------------------------------------------------

    uploaded = st.file_uploader(
        "Upload customer CSV",
        type=["csv"]
    )


    if uploaded:

        try:

            preview = pd.read_csv(
                uploaded
            )


            st.subheader(
                "Preview"
            )


            st.dataframe(
                preview.head(20),
                use_container_width=True
            )


            # ------------------------------------------------
            # BULK PREDICTION
            # ------------------------------------------------

            if st.button(
                "🚀 Predict All Customers",
                type="primary"
            ):

                uploaded.seek(0)

                response = api_post(
                    "/predict/bulk",

                    files={
                        "file": (
                            uploaded.name,
                            uploaded.getvalue(),
                            "text/csv"
                        )
                    }
                )


                if response.ok:

                    result = response.json()


                    st.success(
                        f"Processed {result['processed']} customers."
                    )


                    x, y, z = st.columns(3)


                    x.metric(
                        "High Risk",
                        result["high_risk"]
                    )


                    y.metric(
                        "Medium Risk",
                        result["medium_risk"]
                    )


                    z.metric(
                        "Low Risk",
                        result["low_risk"]
                    )


                    result_df = pd.DataFrame(
                        result["results"]
                    )


                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )


                    st.download_button(
                        "⬇️ Download Prediction Results",

                        result_df.to_csv(
                            index=False
                        ),

                        "churn_predictions.csv",

                        "text/csv"
                    )


                else:

                    st.error(
                        response.text
                    )


        except Exception as exc:

            st.error(
                f"Bulk prediction failed: {exc}"
            )


# ============================================================
# 12. PREDICTION HISTORY
# ============================================================

elif page == "Prediction History":

    st.header(
        "🕘 Prediction History"
    )

    st.caption(
        "Previously generated churn predictions."
    )


    try:

        response = api_get(
            "/predictions?limit=500"
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data)


        if df.empty:

            st.info(
                "No prediction history yet."
            )


        else:

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            st.download_button(
                "⬇️ Download History",

                df.to_csv(
                    index=False
                ),

                "prediction_history.csv",

                "text/csv"
            )


    except Exception as exc:

        st.error(
            f"API connection failed: {exc}"
        )


# ============================================================
# 13. MODEL INFORMATION
# ============================================================

elif page == "Model Information":

    st.header(
        "🧠 Model Information"
    )

    st.caption(
        "Information returned by the deployed ML model."
    )


    try:

        response = api_get(
            "/model/info"
        )

        response.raise_for_status()

        info = response.json()


        st.json(
            info
        )


    except Exception as exc:

        st.error(
            f"API connection failed: {exc}"
        )


# ============================================================
# 14. SIDEBAR FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "ChurnAI • ML + FastAPI + Streamlit + SQL"
)