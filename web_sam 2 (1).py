import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="Web Gap Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border-radius: 12px;
        padding: 18px 20px;
        border-left: 4px solid;
        margin-bottom: 10px;
        min-height: 108px;
    }
    .kpi-value { font-size: 28px; font-weight: 700; margin: 4px 0; }
    .kpi-label { font-size: 11px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .kpi-delta { font-size: 12px; margin-top: 4px; }

    /* Section headers */
    .section-header {
        font-size: 18px; font-weight: 600; color: #e2e8f0;
        padding: 8px 0; margin: 16px 0 8px 0;
        border-bottom: 1px solid #2d3748;
    }

    /* Tab style override */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stSelectbox > div { background-color: #1e2130; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #13151f; }
    [data-testid="stSidebar"] .stMarkdown h1 { color: #e2e8f0; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# ─── DATA ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    # ── Banking Data ──────────────────────────────────────
    banking = pd.DataFrame({
        "Customer ID": [f"CUST{1000+i}" for i in range(30)],
        "Full Name": ["Arjun Sharma","Priya Nair","Kiran Patel","Sneha Reddy","Rahul Verma",
                      "Anjali Singh","Deepak Mehta","Pooja Iyer","Vivek Kumar","Nisha Gupta",
                      "Suresh Babu","Lakshmi Rao","Manish Joshi","Divya Thomas","Aakash Malik",
                      "Rekha Pillai","Sameer Khan","Tanvi Desai","Rohit Kapoor","Meena Nair",
                      "Sanjay Tiwari","Kavitha Rajan","Aman Bhatt","Sunita Yadav","Farhan Ahmed",
                      "Geeta Menon","Ravi Shankar","Pallavi Choudhary","Nikhil Roy","Asha Krishnan"],
        "Age": [39,27,32,60,34,62,37,42,31,54,46,29,62,60,27,35,29,62,30,48,34,25,25,35,25,58,37,54,61,39],
        "Account Type": ["Savings","Savings","Premium Savings","Savings","Premium Savings",
                         "Current","Premium Savings","Savings","Current","Fixed Deposit",
                         "Premium Savings","Premium Savings","Premium Savings","Premium Savings","Premium Savings",
                         "Fixed Deposit","Current","Savings","Current","Current",
                         "Savings","Current","Current","Checking","Premium Savings",
                         "Current","Fixed Deposit","Savings","Current","Savings"],
        "Balance": [338700,352828,513674,1211656,73507,248167,696079,405272,213747,140909,
                    895853,654974,1263295,735465,1224954,1134121,340922,347267,866436,1296435,
                    675677,1498927,571564,870874,124766,870483,596699,203022,795766,909220],
        "Credit Score": [602,563,629,785,666,731,688,658,837,574,789,782,809,607,822,652,723,566,674,577,
                         766,557,749,827,645,570,703,728,833,725],
        "Monthly Income": [143422,123217,62679,118839,160286,61663,198166,184798,119321,175693,
                           117595,25567,131569,187592,159021,149766,28681,175436,162308,142838,
                           57110,194574,71410,35667,36991,133391,105014,179151,77391,60629],
        "Loan Amount": [0,0,154515,2985309,4943180,3903481,4580690,369276,3949128,1260410,
                        0,2953598,0,104797,0,3649538,3887340,0,4623422,3653235,
                        1707174,921317,3464169,2588965,1420641,0,2735565,1888067,2637697,1403991],
        "Loan Status": ["None","None","Paid Off","Paid Off","Paid Off","Paid Off","Active","Active",
                        "Defaulted","Active","None","Paid Off","None","Pending","None","Pending",
                        "Pending","None","Active","Paid Off","Active","Pending","Active","Active",
                        "Pending","None","Active","Pending","Pending","Pending"],
        "Join Date": ["2023-02-19","2023-07-08","2020-02-03","2021-02-18","2016-04-28",
                      "2019-12-22","2023-04-22","2024-12-11","2024-07-19","2017-11-06",
                      "2023-01-22","2019-09-25","2017-06-25","2019-04-02","2017-11-16",
                      "2021-11-21","2023-04-19","2016-09-08","2021-04-04","2016-01-13",
                      "2022-04-28","2018-03-14","2022-05-14","2020-01-02","2016-11-28",
                      "2021-11-19","2016-01-15","2018-06-10","2016-03-09","2019-09-16"],
        "Branch": ["Kolkata","Ahmedabad","Kolkata","Hyderabad","Delhi","Delhi","Pune","Bangalore",
                   "Kolkata","Kolkata","Delhi","Chennai","Chennai","Bangalore","Chennai","Pune",
                   "Bangalore","Hyderabad","Delhi","Pune","Delhi","Ahmedabad","Ahmedabad",
                   "Ahmedabad","Bangalore","Pune","Delhi","Chennai","Delhi","Hyderabad"]
    })
    banking["Join Date"] = pd.to_datetime(banking["Join Date"])
    banking["Join Year"] = banking["Join Date"].dt.year

    # ── Course Data ───────────────────────────────────────
    courses = pd.DataFrame({
        "Enrollment ID": [f"ENR{2000+i}" for i in range(30)],
        "Student Name": ["Aditya Verma","Bhavna Rao","Chetan Iyer","Divya Reddy","Esha Patel",
                         "Farooq Sheikh","Gita Menon","Hari Prasad","Isha Kapoor","Jayant Tiwari",
                         "Kavya Nair","Lokesh Kumar","Mithun Das","Nalini Gupta","Om Prakash",
                         "Preethi Raj","Qadir Hussain","Ritu Sharma","Sagar Bhatt","Tanya Singh",
                         "Umesh Yadav","Vandana Pillai","Wasim Khan","Xena D'Souza","Yash Malhotra",
                         "Zara Fernandez","Anand Raman","Bala Murugan","Chitra Bansal","Dinesh Soni"],
        "Course": ["Financial Modelling","Business Communication","Data Analytics with Excel",
                   "Machine Learning A-Z","Digital Marketing Pro","Digital Marketing Pro",
                   "Photography Masterclass","Photography Masterclass","UI/UX Fundamentals",
                   "React & Node.js","Machine Learning A-Z","UI/UX Fundamentals",
                   "Data Analytics with Excel","Machine Learning A-Z","Business Communication",
                   "Business Communication","Data Analytics with Excel","Photography Masterclass",
                   "Data Analytics with Excel","Machine Learning A-Z","Data Analytics with Excel",
                   "Photography Masterclass","Python for Beginners","Python for Beginners",
                   "React & Node.js","Financial Modelling","Web Design Bootcamp",
                   "Web Design Bootcamp","Web Design Bootcamp","UI/UX Fundamentals"],
        "Category": ["Finance","Soft Skills","Data Science","Data Science","Marketing","Marketing",
                     "Creative","Creative","Design","Programming","Data Science","Design",
                     "Data Science","Data Science","Soft Skills","Soft Skills","Data Science",
                     "Creative","Data Science","Data Science","Data Science","Creative",
                     "Programming","Programming","Programming","Finance","Design","Design","Design","Design"],
        "Instructor": ["Rahul Mehta","Deepak Joshi","Suresh Kumar","Prof. Sneha Rao","Anjali Singh",
                       "Anjali Singh","Meena Nair","Meena Nair","Priya Thomas","Vivek Sharma",
                       "Prof. Sneha Rao","Priya Thomas","Suresh Kumar","Prof. Sneha Rao","Deepak Joshi",
                       "Deepak Joshi","Suresh Kumar","Meena Nair","Suresh Kumar","Prof. Sneha Rao",
                       "Suresh Kumar","Meena Nair","Dr. Arjun Dev","Dr. Arjun Dev","Vivek Sharma",
                       "Rahul Mehta","Kiran Patel","Kiran Patel","Kiran Patel","Priya Thomas"],
        "Enrollment Date": ["2022-04-27","2024-11-22","2022-09-27","2023-09-16","2023-10-23",
                            "2022-02-19","2023-11-25","2023-10-20","2023-01-02","2023-09-19",
                            "2024-02-01","2022-08-05","2023-02-28","2022-01-02","2023-09-09",
                            "2024-05-10","2022-12-05","2022-07-06","2024-07-07","2023-04-25",
                            "2023-09-18","2023-02-09","2024-10-18","2024-12-27","2024-12-20",
                            "2023-11-20","2024-02-14","2024-05-27","2024-02-03","2022-03-24"],
        "Completion": [51,40,32,80,99,52,23,17,27,65,28,83,24,30,86,63,19,36,72,77,93,100,37,85,17,20,73,14,79,75],
        "Score": [52,49,90,89,75,94,17,49,49,47,19,40,24,10,66,58,2,83,74,60,73,82,98,47,43,23,65,50,97,85],
        "Certificate": ["No"]*21 + ["Yes"] + ["No"]*8,
        "Duration": [10,50,40,20,50,40,50,50,10,60,40,10,20,20,50,40,10,10,60,30,40,60,50,20,50,60,10,50,10,40],
        "Price": [3630,1021,2645,3029,1686,8445,9776,3229,5461,5399,9236,7308,3153,7033,8552,
                  8864,1808,9561,4852,9730,9722,1927,7093,3437,9595,8639,1985,9429,5955,2835],
        "Rating": [4.9,3.6,3.6,3.1,4.7,4.8,3.7,4.1,3.1,4.3,4.8,3.5,3.4,4.5,3.2,3.0,4.8,3.8,3.5,4.5,3.5,3.3,3.1,3.3,3.2,3.1,3.8,4.3,5.0,4.1],
        "Status": ["In Progress"]*21 + ["Completed"] + ["In Progress"]*8
    })
    courses["Enrollment Date"] = pd.to_datetime(courses["Enrollment Date"])

    # ── EV Data ───────────────────────────────────────────
    ev = pd.DataFrame({
        "Vehicle ID": [f"EV{3000+i}" for i in range(30)],
        "Model": ["Model S Plaid","Model 3 LR","Ioniq 6","EV6 GT","Tata Nexon EV","Ather 450X",
                  "ID.4 Pro","Polestar 2","BYD Atto 3","Chevy Bolt EV","Rivian R1T","MG ZS EV",
                  "Ola S1 Pro","Audi e-tron GT","BMW iX","Nissan Ariya","Ford F-150 Lightning",
                  "Hyundai Kona EV","Lucid Air Pure","Mercedes EQS","Skoda Enyaq","Volvo EX40",
                  "Xiaomi SU7","Mahindra XEV 9e","Honda Prologue","Toyota bZ4X","GMC Hummer EV",
                  "Fisker Ocean","Tata Tiago EV","Bajaj Chetak"],
        "Brand": ["Tesla","Tesla","Hyundai","Kia","Tata","Ather","Volkswagen","Polestar","BYD",
                  "Chevrolet","Rivian","MG","Ola Electric","Audi","BMW","Nissan","Ford","Hyundai",
                  "Lucid","Mercedes","Skoda","Volvo","Xiaomi","Mahindra","Honda","Toyota","GMC",
                  "Fisker","Tata","Bajaj"],
        "Type": ["Sedan","Sedan","Sedan","SUV","SUV","Scooter","SUV","Sedan","SUV","Hatchback",
                 "Pickup","SUV","Scooter","Sedan","SUV","SUV","Pickup","SUV","Sedan","Sedan",
                 "SUV","SUV","Sedan","SUV","SUV","SUV","Pickup","SUV","Hatchback","Scooter"],
        "Battery": [100,82,77.4,77.4,40.5,3.7,77,78,60.5,65,135,51,4,93.4,111.5,87,131,65.4,88,107.8,77,69,99.6,79,85,72.8,212,113,24,3],
        "Range": [652,602,614,586,465,146,521,542,480,547,560,461,181,488,630,610,515,490,671,784,528,525,668,656,466,500,563,707,315,126],
        "Top Speed": [250,225,185,260,150,90,160,205,160,145,200,140,116,245,250,160,180,167,270,210,160,180,265,201,161,160,170,200,120,73],
        "Charge Time": [0.5,1,0.8,0.8,1.5,5,0.8,1,1.2,1,0.8,1.5,6.5,0.6,0.7,0.8,0.8,0.8,0.6,0.7,0.8,0.8,0.6,0.7,0.8,0.8,0.8,0.7,3.5,5],
        "Price": [109990,54990,45450,61450,19990,1499,47995,52995,37990,26500,73000,22000,1499,
                  104900,119300,49245,55974,33550,69900,104400,44900,56695,42900,30600,47400,
                  42000,89995,68999,12990,1099],
        "Units Sold": [145,320,198,112,520,870,143,95,240,175,65,310,960,48,32,120,98,185,55,40,130,88,200,160,110,145,35,25,680,720],
        "Stock Left": [12,45,30,8,72,150,22,15,38,28,6,55,200,5,4,18,10,27,9,6,20,12,35,22,16,24,3,2,105,130],
        "Availability": ["Limited","In Stock","In Stock","Limited","In Stock","In Stock","In Stock",
                         "Limited","In Stock","In Stock","Limited","In Stock","In Stock","Out of Stock",
                         "Out of Stock","Limited","Limited","In Stock","Limited","Limited","Limited",
                         "Limited","In Stock","In Stock","Limited","In Stock","Out of Stock",
                         "Out of Stock","In Stock","In Stock"]
    })
    ev["Revenue"] = ev["Price"] * ev["Units Sold"]

    return banking, courses, ev

banking, courses, ev = load_data()

# ─── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Web Gap Analysis")
    st.markdown("---")
    domain = st.radio(
        "Select Domain",
        ["🏠 Overview", "🏦 Banking Services", "🎓 Online Courses", "⚡ Electric Vehicles"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Data Source**")
    st.markdown("""
    - [Stackly Banking](https://santhosh-alt-debug.github.io/stackly-banking-2/#home)
    - [Online Course](https://mohammed-refai03.github.io/online-course/)
    - [Electric EV](https://mohammed-refai03.github.io/electric-vehicle/)
    """)
    st.markdown("---")
    st.caption("Dashboard v1.0 · Web Gap Analysis")

# ═══════════════════════════════════════════════════════════
# OVERVIEW TAB
# ═══════════════════════════════════════════════════════════
if domain == "🏠 Overview":
    st.title("📊 Web Gap Analysis — Multi-Domain Dashboard")
    st.markdown("Cross-domain performance overview across Banking, E-Learning, and Electric Vehicles.")
    st.markdown("---")

    # KPI Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"""<div class="kpi-card" style="border-color:#3b82f6">
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value" style="color:#3b82f6">{len(banking)}</div>
            <div class="kpi-delta">🏦 Banking</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-card" style="border-color:#10b981">
            <div class="kpi-label">Total AUM</div>
            <div class="kpi-value" style="color:#10b981">${banking['Balance'].sum()/1e6:.1f}M</div>
            <div class="kpi-delta">Assets Under Mgmt</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-card" style="border-color:#8b5cf6">
            <div class="kpi-label">Enrolled Students</div>
            <div class="kpi-value" style="color:#8b5cf6">{len(courses)}</div>
            <div class="kpi-delta">🎓 E-Learning</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-card" style="border-color:#f59e0b">
            <div class="kpi-label">Avg Completion</div>
            <div class="kpi-value" style="color:#f59e0b">{courses['Completion'].mean():.0f}%</div>
            <div class="kpi-delta">Course Progress</div></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="kpi-card" style="border-color:#ef4444">
            <div class="kpi-label">EV Units Sold</div>
            <div class="kpi-value" style="color:#ef4444">{ev['Units Sold'].sum():,}</div>
            <div class="kpi-delta">⚡ EV Platform</div></div>""", unsafe_allow_html=True)
    with col6:
        st.markdown(f"""<div class="kpi-card" style="border-color:#06b6d4">
            <div class="kpi-label">EV Revenue</div>
            <div class="kpi-value" style="color:#06b6d4">${ev['Revenue'].sum()/1e6:.0f}M</div>
            <div class="kpi-delta">Total Sales Value</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: 3 charts side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-header">🏦 Loan Portfolio Mix</div>', unsafe_allow_html=True)
        loan_counts = banking["Loan Status"].value_counts().reset_index()
        loan_counts.columns = ["Status","Count"]
        colors = {"None":"#3b82f6","Active":"#10b981","Paid Off":"#f59e0b","Defaulted":"#ef4444","Pending":"#8b5cf6"}
        fig = px.pie(loan_counts, values="Count", names="Status",
                     color="Status", color_discrete_map=colors,
                     hole=0.5)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0", showlegend=True, height=280,
                          margin=dict(t=10,b=10,l=10,r=10),
                          legend=dict(font_size=10))
        fig.update_traces(textfont_color="#fff")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">🎓 Course Category Distribution</div>', unsafe_allow_html=True)
        cat_counts = courses["Category"].value_counts().reset_index()
        cat_counts.columns = ["Category","Count"]
        fig2 = px.bar(cat_counts, x="Count", y="Category", orientation="h",
                      color="Count", color_continuous_scale="Purples")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=280, margin=dict(t=10,b=10,l=10,r=10),
                           yaxis=dict(tickfont=dict(size=10)), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown('<div class="section-header">⚡ EV Sales by Type</div>', unsafe_allow_html=True)
        ev_type = ev.groupby("Type")["Units Sold"].sum().reset_index()
        fig3 = px.pie(ev_type, values="Units Sold", names="Type",
                      color_discrete_sequence=px.colors.sequential.Teal, hole=0.5)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=280, margin=dict(t=10,b=10,l=10,r=10),
                           legend=dict(font_size=10))
        fig3.update_traces(textfont_color="#fff")
        st.plotly_chart(fig3, use_container_width=True)

    # Row 3: Gap Analysis
    st.markdown("---")
    st.markdown("### 🎯 Web Gap Analysis Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        gaps_bank = {
            "Metric": ["Loan Default Rate", "Active Loans", "Credit Score <650", "Low Balance Accounts"],
            "Website": ["Not shown", "Not shown", "Not shown", "Not shown"],
            "Data": [f"{(banking['Loan Status']=='Defaulted').mean()*100:.0f}%",
                     f"{(banking['Loan Status']=='Active').sum()} customers",
                     f"{(banking['Credit Score']<650).sum()} customers",
                     f"{(banking['Balance']<200000).sum()} accounts"]
        }
        st.markdown("**🏦 Banking Gaps**")
        st.dataframe(pd.DataFrame(gaps_bank), use_container_width=True, hide_index=True, height=160)

    with col2:
        gaps_course = {
            "Metric": ["Completion Rate", "Certificate Earners", "Avg Score", "Dropout Risk"],
            "Website": ["Not tracked", "Not shown", "Not shown", "Not shown"],
            "Data": [f"{(courses['Status']=='Completed').mean()*100:.0f}%",
                     f"{(courses['Certificate']=='Yes').sum()} students",
                     f"{courses['Score'].mean():.0f}%",
                     f"{(courses['Completion']<30).sum()} at risk"]
        }
        st.markdown("**🎓 Course Gaps**")
        st.dataframe(pd.DataFrame(gaps_course), use_container_width=True, hide_index=True, height=160)

    with col3:
        gaps_ev = {
            "Metric": ["Out of Stock Models", "Sell-through Rate", "Top Performer", "Low Stock Alert"],
            "Website": ["Not flagged", "Not shown", "Not highlighted", "Not shown"],
            "Data": [f"{(ev['Availability']=='Out of Stock').sum()} models",
                     f"{ev['Units Sold'].sum()/(ev['Units Sold'].sum()+ev['Stock Left'].sum())*100:.0f}%",
                     ev.loc[ev['Units Sold'].idxmax(), 'Model'],
                     f"{(ev['Stock Left']<10).sum()} models"]
        }
        st.markdown("**⚡ EV Gaps**")
        st.dataframe(pd.DataFrame(gaps_ev), use_container_width=True, hide_index=True, height=160)


# ═══════════════════════════════════════════════════════════
# BANKING TAB
# ═══════════════════════════════════════════════════════════
elif domain == "🏦 Banking Services":
    st.title("🏦 Stackly Banking — Customer Analytics")
    st.caption("Source: https://santhosh-alt-debug.github.io/stackly-banking-2/#home")
    st.markdown("---")

    # Filters
    col1, col2, col3 = st.columns(3)
    branch_filter = col1.multiselect("Branch", banking["Branch"].unique(), default=list(banking["Branch"].unique()))
    acc_filter    = col2.multiselect("Account Type", banking["Account Type"].unique(), default=list(banking["Account Type"].unique()))
    loan_filter   = col3.multiselect("Loan Status", banking["Loan Status"].unique(), default=list(banking["Loan Status"].unique()))

    df = banking[banking["Branch"].isin(branch_filter) & banking["Account Type"].isin(acc_filter) & banking["Loan Status"].isin(loan_filter)]

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Total Customers", len(df))
    k2.metric("Total Balance", f"${df['Balance'].sum()/1e6:.2f}M")
    k3.metric("Avg Credit Score", f"{df['Credit Score'].mean():.0f}")
    k4.metric("Total Loans", f"${df['Loan Amount'].sum()/1e6:.1f}M")
    k5.metric("Default Rate", f"{(df['Loan Status']=='Defaulted').mean()*100:.1f}%")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Balance Distribution by Account Type</div>', unsafe_allow_html=True)
        fig = px.box(df, x="Account Type", y="Balance", color="Account Type",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0", height=300, showlegend=False,
                          margin=dict(t=10,b=10), xaxis_title="", yaxis_title="Balance ($)")
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Loan Status Breakdown</div>', unsafe_allow_html=True)
        loan_data = df["Loan Status"].value_counts().reset_index()
        loan_data.columns = ["Status","Count"]
        colors = {"None":"#3b82f6","Active":"#10b981","Paid Off":"#f59e0b","Defaulted":"#ef4444","Pending":"#8b5cf6"}
        fig2 = px.bar(loan_data, x="Status", y="Count", color="Status",
                      color_discrete_map=colors, text="Count")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, showlegend=False,
                           margin=dict(t=10,b=10))
        fig2.update_traces(textposition="outside")
        fig2.update_yaxes(gridcolor="#2d3748")
        fig2.update_xaxes(showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Credit Score vs Balance (Bubble = Loan Amount)</div>', unsafe_allow_html=True)
        fig3 = px.scatter(df, x="Credit Score", y="Balance", size=df["Loan Amount"].clip(lower=100000),
                          color="Loan Status", color_discrete_map=colors,
                          hover_name="Full Name", size_max=30)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, margin=dict(t=10,b=10))
        fig3.update_xaxes(gridcolor="#2d3748")
        fig3.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Customers per Branch</div>', unsafe_allow_html=True)
        branch_data = df.groupby("Branch").agg(
            Customers=("Customer ID","count"),
            Avg_Balance=("Balance","mean"),
            Total_Loans=("Loan Amount","sum")
        ).reset_index()
        fig4 = px.bar(branch_data.sort_values("Customers", ascending=True),
                      x="Customers", y="Branch", orientation="h",
                      color="Avg_Balance", color_continuous_scale="Blues",
                      text="Customers")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, margin=dict(t=10,b=10),
                           coloraxis_colorbar=dict(title="Avg Balance"))
        fig4.update_traces(textposition="outside")
        fig4.update_xaxes(gridcolor="#2d3748")
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: conversion funnel
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Customer Acquisition by Year</div>', unsafe_allow_html=True)
        yr_data = df.groupby("Join Year").size().reset_index(name="New Customers")
        fig5 = px.line(yr_data, x="Join Year", y="New Customers", markers=True,
                       color_discrete_sequence=["#3b82f6"])
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=260, margin=dict(t=10,b=10))
        fig5.update_xaxes(gridcolor="#2d3748")
        fig5.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Age vs Monthly Income</div>', unsafe_allow_html=True)
        fig6 = px.scatter(df, x="Age", y="Monthly Income", color="Account Type",
                          hover_name="Full Name", size_max=8,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=260, margin=dict(t=10,b=10))
        fig6.update_xaxes(gridcolor="#2d3748")
        fig6.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig6, use_container_width=True)

    # Data table
    st.markdown('<div class="section-header">📋 Customer Records</div>', unsafe_allow_html=True)
    st.dataframe(df[["Customer ID","Full Name","Age","Account Type","Balance","Credit Score",
                      "Monthly Income","Loan Amount","Loan Status","Branch"]].reset_index(drop=True),
                 use_container_width=True, height=320)


# ═══════════════════════════════════════════════════════════
# ONLINE COURSES TAB
# ═══════════════════════════════════════════════════════════
elif domain == "🎓 Online Courses":
    st.title("🎓 Online Course Platform — Enrollment Analytics")
    st.caption("Source: https://santhosh-alt-debug.github.io/online-course/")
    st.markdown("---")

    # Filters
    col1, col2 = st.columns(2)
    cat_filter  = col1.multiselect("Category", courses["Category"].unique(), default=list(courses["Category"].unique()))
    stat_filter = col2.multiselect("Status", courses["Status"].unique(), default=list(courses["Status"].unique()))
    df = courses[courses["Category"].isin(cat_filter) & courses["Status"].isin(stat_filter)]

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Enrollments", len(df))
    k2.metric("Avg Completion", f"{df['Completion'].mean():.1f}%")
    k3.metric("Avg Score", f"{df['Score'].mean():.1f}%")
    k4.metric("Certificates", f"{(df['Certificate']=='Yes').sum()}")
    k5.metric("Revenue", f"${df['Price'].sum():,.0f}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Completion % by Course</div>', unsafe_allow_html=True)
        course_perf = df.groupby("Course").agg(Avg_Completion=("Completion","mean"), Count=("Enrollment ID","count")).reset_index()
        fig = px.bar(course_perf.sort_values("Avg_Completion"), x="Avg_Completion", y="Course",
                     orientation="h", color="Avg_Completion",
                     color_continuous_scale="Purples", text=course_perf.sort_values("Avg_Completion")["Avg_Completion"].round(0))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0", height=320, margin=dict(t=10,b=10),
                          coloraxis_showscale=False, xaxis_title="Avg Completion (%)", yaxis_title="")
        fig.update_xaxes(gridcolor="#2d3748")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
        fig2 = px.histogram(df, x="Score", nbins=10, color_discrete_sequence=["#8b5cf6"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=320, margin=dict(t=10,b=10))
        fig2.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
        rev_cat = df.groupby("Category")["Price"].sum().reset_index()
        fig3 = px.pie(rev_cat, values="Price", names="Category",
                      color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.45)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, margin=dict(t=10,b=10))
        fig3.update_traces(textfont_color="#fff")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Ratings by Instructor</div>', unsafe_allow_html=True)
        instr = df.groupby("Instructor").agg(Avg_Rating=("Rating","mean"), Students=("Enrollment ID","count")).reset_index()
        fig4 = px.bar(instr.sort_values("Avg_Rating"), x="Avg_Rating", y="Instructor",
                      orientation="h", color="Avg_Rating",
                      color_continuous_scale="Greens", text=instr.sort_values("Avg_Rating")["Avg_Rating"].round(1))
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, coloraxis_showscale=False,
                           margin=dict(t=10,b=10), xaxis_range=[0,5.5])
        fig4.update_xaxes(gridcolor="#2d3748")
        st.plotly_chart(fig4, use_container_width=True)

    # Completion funnel
    st.markdown('<div class="section-header">📐 Learner Conversion Funnel</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    with col1:
        total   = len(df)
        started = (df["Completion"] > 0).sum()
        halfway = (df["Completion"] >= 50).sum()
        done    = (df["Completion"] == 100).sum()
        certified = (df["Certificate"] == "Yes").sum()
        funnel_df = pd.DataFrame({"Stage":["Enrolled","Started","50% Complete","Completed","Certified"],
                                  "Count":[total, started, halfway, done, certified]})
        fig5 = go.Figure(go.Funnel(
            y=funnel_df["Stage"], x=funnel_df["Count"],
            textinfo="value+percent initial",
            marker=dict(color=["#8b5cf6","#7c3aed","#6d28d9","#5b21b6","#4c1d95"])
        ))
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.markdown('<div class="section-header">Completion vs Score Scatter</div>', unsafe_allow_html=True)
        fig6 = px.scatter(df, x="Completion", y="Score", color="Category",
                          size="Price", hover_name="Student Name", size_max=20,
                          color_discrete_sequence=px.colors.qualitative.Vivid)
        fig6.add_vline(x=50, line_dash="dash", line_color="#ef4444", annotation_text="50% milestone")
        fig6.add_hline(y=60, line_dash="dash", line_color="#10b981", annotation_text="Pass mark")
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=300, margin=dict(t=10,b=10))
        fig6.update_xaxes(gridcolor="#2d3748")
        fig6.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<div class="section-header">📋 Enrollment Records</div>', unsafe_allow_html=True)
    st.dataframe(df[["Enrollment ID","Student Name","Course","Category","Completion","Score","Certificate","Rating","Status"]].reset_index(drop=True),
                 use_container_width=True, height=280)


# ═══════════════════════════════════════════════════════════
# ELECTRIC VEHICLES TAB
# ═══════════════════════════════════════════════════════════
elif domain == "⚡ Electric Vehicles":
    st.title("⚡ Electric Vehicle Platform — Sales & Inventory")
    st.caption("Source: https://mohammed-refai03.github.io/electric-vehicle/")
    st.markdown("---")

    # Filters
    col1, col2 = st.columns(2)
    type_filter  = col1.multiselect("Vehicle Type", ev["Type"].unique(), default=list(ev["Type"].unique()))
    avail_filter = col2.multiselect("Availability", ev["Availability"].unique(), default=list(ev["Availability"].unique()))
    df = ev[ev["Type"].isin(type_filter) & ev["Availability"].isin(avail_filter)]

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Models", len(df))
    k2.metric("Total Units Sold", f"{df['Units Sold'].sum():,}")
    k3.metric("Total Revenue", f"${df['Revenue'].sum()/1e6:.1f}M")
    k4.metric("Avg Range", f"{df['Range'].mean():.0f} km")
    k5.metric("Out of Stock", f"{(df['Availability']=='Out of Stock').sum()} models")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Units Sold by Brand (Top 15)</div>', unsafe_allow_html=True)
        brand_sales = df.groupby("Brand")["Units Sold"].sum().sort_values(ascending=True).tail(15).reset_index()
        fig = px.bar(brand_sales, x="Units Sold", y="Brand", orientation="h",
                     color="Units Sold", color_continuous_scale="Teal", text="Units Sold")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="#e2e8f0", height=380, margin=dict(t=10,b=10),
                          coloraxis_showscale=False)
        fig.update_traces(textposition="outside")
        fig.update_xaxes(gridcolor="#2d3748")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Price vs Range (by Type)</div>', unsafe_allow_html=True)
        fig2 = px.scatter(df, x="Range", y="Price", color="Type",
                          size="Units Sold", hover_name="Model", size_max=25,
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=380, margin=dict(t=10,b=10))
        fig2.update_xaxes(gridcolor="#2d3748", title="Range (km)")
        fig2.update_yaxes(gridcolor="#2d3748", title="Price ($)")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Stock vs Units Sold (Inventory Health)</div>', unsafe_allow_html=True)
        fig3 = px.scatter(df, x="Units Sold", y="Stock Left", color="Availability",
                          size="Price", hover_name="Model", size_max=20,
                          color_discrete_map={"In Stock":"#10b981","Limited":"#f59e0b","Out of Stock":"#ef4444"})
        fig3.add_hline(y=10, line_dash="dash", line_color="#ef4444", annotation_text="Low stock threshold")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=320, margin=dict(t=10,b=10))
        fig3.update_xaxes(gridcolor="#2d3748")
        fig3.update_yaxes(gridcolor="#2d3748")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Revenue by Vehicle Type</div>', unsafe_allow_html=True)
        rev_type = df.groupby("Type")["Revenue"].sum().reset_index()
        fig4 = px.pie(rev_type, values="Revenue", names="Type",
                      color_discrete_sequence=px.colors.qualitative.Safe, hole=0.5)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="#e2e8f0", height=320, margin=dict(t=10,b=10))
        fig4.update_traces(textfont_color="#fff")
        st.plotly_chart(fig4, use_container_width=True)

    # Top models
    st.markdown('<div class="section-header">🏆 Top 10 Models by Revenue</div>', unsafe_allow_html=True)
    top10 = df.nlargest(10, "Revenue")[["Model","Brand","Type","Units Sold","Price","Revenue","Availability","Stock Left"]]
    top10["Revenue"] = top10["Revenue"].apply(lambda x: f"${x:,.0f}")
    top10["Price"]   = top10["Price"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(top10.reset_index(drop=True), use_container_width=True, height=360)

    # Battery vs Range
    st.markdown('<div class="section-header">Battery Capacity vs Range (Efficiency View)</div>', unsafe_allow_html=True)
    df2 = df.copy()
    df2["Efficiency"] = df2["Range"] / df2["Battery"].replace(0, np.nan)
    fig5 = px.scatter(df2, x="Battery", y="Range", color="Type",
                      size="Units Sold", hover_name="Model",
                      text="Model", size_max=20,
                      color_discrete_sequence=px.colors.qualitative.Bold)
    fig5.update_traces(textposition="top center", textfont_size=8)
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       font_color="#e2e8f0", height=420, margin=dict(t=10,b=10))
    fig5.update_xaxes(gridcolor="#2d3748", title="Battery Capacity (kWh)")
    fig5.update_yaxes(gridcolor="#2d3748", title="Range (km)")
    st.plotly_chart(fig5, use_container_width=True)
