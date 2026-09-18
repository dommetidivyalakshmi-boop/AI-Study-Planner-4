import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random
import math


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM PASTEL UI
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        linear-gradient(
            135deg,
            #FDF4F5 0%,
            #F3F7FC 45%,
            #EEF8F4 100%
        );
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* Header */
.hero {
    background: linear-gradient(
        135deg,
        #DCCEF9,
        #CFEAF6,
        #D7F1E5
    );

    padding: 30px;
    border-radius: 28px;
    margin-bottom: 25px;

    box-shadow:
        0 10px 30px rgba(100, 100, 150, 0.10);

    border: 1px solid rgba(255,255,255,0.8);
}

.hero h1 {
    color: #2E3559;
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    color: #59617D;
    font-size: 17px;
}


/* Cards */
.card {
    background: rgba(255,255,255,0.78);
    padding: 22px;
    border-radius: 22px;

    border: 1px solid rgba(255,255,255,0.9);

    box-shadow:
        0 8px 25px rgba(80, 90, 130, 0.08);

    margin-bottom: 18px;
}


/* Metric cards */
.metric-card {
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #F8F5FF
    );

    padding: 20px;
    border-radius: 20px;

    text-align: center;

    border: 1px solid #E8E2F7;

    box-shadow:
        0 6px 20px rgba(80, 80, 120, 0.07);
}

.metric-title {
    color: #777A91;
    font-size: 14px;
}

.metric-value {
    color: #303653;
    font-size: 30px;
    font-weight: 700;
}


/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #E9E0F7,
        #DCEFF5,
        #E2F4EA
    );
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #303653;
}


/* Buttons */
.stButton > button {
    border-radius: 14px;

    border: none;

    background: linear-gradient(
        135deg,
        #B8A4E8,
        #9CCFE0
    );

    color: white;

    font-weight: 700;

    padding: 12px 20px;

    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 7px 18px rgba(100,100,150,0.18);
}


/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    border-radius: 12px !important;
}


/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
}


/* Info box */
.info-box {
    background: #EEF4FF;

    border-left: 5px solid #9BBCE5;

    padding: 15px;

    border-radius: 12px;

    color: #46516D;

    margin-bottom: 15px;
}


/* Priority */
.priority-high {
    background: #FDE2E4;
    padding: 7px 12px;
    border-radius: 20px;
    color: #9B4653;
    font-weight: 600;
}

.priority-medium {
    background: #FFF1D6;
    padding: 7px 12px;
    border-radius: 20px;
    color: #98702D;
    font-weight: 600;
}

.priority-low {
    background: #E1F4EA;
    padding: 7px 12px;
    border-radius: 20px;
    color: #39765A;
    font-weight: 600;
}


/* Footer */
.footer {
    text-align: center;
    padding: 30px;
    color: #7C8195;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "plan" not in st.session_state:
    st.session_state.plan = None

if "generated" not in st.session_state:
    st.session_state.generated = False

if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="hero">

<h1>📚 AI Study Planner</h1>

<p>
Smart • Personalized • Priority-Aware • Weekly Study Planning
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎯 Study Inputs")

    st.markdown(
        "Enter your study requirements and generate a personalized plan."
    )

    st.divider()

    start_date = st.date_input(
        "📅 Start Date",
        value=date.today()
    )

    exam_date = st.date_input(
        "🎓 Examination Date",
        value=date.today() + timedelta(days=14),
        min_value=start_date
    )

    available_hours = st.number_input(
        "⏰ Study Hours Per Day",
        min_value=1.0,
        max_value=12.0,
        value=4.0,
        step=0.5
    )

    subjects_text = st.text_area(
        "📚 Subjects",
        value="Python, Database, Artificial Intelligence, Blockchain",
        height=100
    )

    priority_text = st.text_area(
        "⭐ Priority Topics",
        value="Artificial Intelligence, Python",
        height=100
    )

    difficulty = st.select_slider(
        "📈 Study Intensity",
        options=["Light", "Balanced", "Focused", "Intensive"],
        value="Balanced"
    )

    session_length = st.select_slider(
        "⏱️ Preferred Session",
        options=[30, 45, 60, 90, 120],
        value=60
    )

    include_breaks = st.checkbox(
        "☕ Include Breaks",
        value=True
    )

    st.divider()

    generate_button = st.button(
        "✨ Generate Study Plan",
        use_container_width=True
    )

    regenerate_button = st.button(
        "🔄 Regenerate Plan",
        use_container_width=True
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_list(text):
    items = []

    for item in text.split(","):
        item = item.strip()

        if item and item not in items:
            items.append(item)

    return items


def priority_level(subject, priority_topics):

    subject_lower = subject.lower()

    for topic in priority_topics:

        if topic.lower() in subject_lower:
            return "High"

    return "Medium"


def generate_topics(subject):

    topic_templates = [
        "Introduction & Fundamentals",
        "Core Concepts",
        "Important Definitions",
        "Examples & Applications",
        "Practice Questions",
        "Problem Solving",
        "Revision",
        "Mock Test"
    ]

    return topic_templates


def create_plan(
    start_date,
    exam_date,
    subjects,
    priority_topics,
    available_hours,
    session_length,
    include_breaks,
    difficulty
):

    total_days = (exam_date - start_date).days + 1

    # Keep weekly planner manageable
    total_days = min(total_days, 14)

    records = []

    random.seed(st.session_state.generation_count)

    # --------------------------------------------------------
    # Task decomposition
    # --------------------------------------------------------

    task_pool = []

    for subject in subjects:

        level = priority_level(
            subject,
            priority_topics
        )

        topics = generate_topics(subject)

        for topic in topics:

            task_pool.append({
                "Subject": subject,
                "Topic": topic,
                "Priority": level
            })


    # Priority sorting
    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    task_pool.sort(
        key=lambda x: priority_order[x["Priority"]]
    )


    # --------------------------------------------------------
    # Generate schedule
    # --------------------------------------------------------

    task_index = 0

    for day_number in range(total_days):

        current_date = start_date + timedelta(days=day_number)

        remaining_hours = available_hours

        while remaining_hours > 0.1:

            if task_index >= len(task_pool):

                task_index = 0

            task = task_pool[task_index]

            # Session size
            session_hours = min(
                session_length / 60,
                remaining_hours
            )

            # Slight variation for realistic planning
            if session_hours > 0.5:

                variation = random.choice(
                    [0, 0, 0.25, -0.25]
                )

                session_hours = max(
                    0.5,
                    min(
                        session_hours,
                        remaining_hours
                    )
                )

            records.append({
                "Date": current_date,
                "Day": current_date.strftime("%A"),
                "Subject": task["Subject"],
                "Topic": task["Topic"],
                "Priority": task["Priority"],
                "Hours": round(session_hours, 2),
                "Type": "Study"
            })

            remaining_hours -= session_hours

            task_index += 1

            # Avoid too many sessions
            if len(records) > total_days * 8:
                break


        # Add break
        if include_breaks:

            records.append({
                "Date": current_date,
                "Day": current_date.strftime("%A"),
                "Subject": "Break",
                "Topic": "Rest & Refresh",
                "Priority": "Low",
                "Hours": 0.5,
                "Type": "Break"
            })


    df = pd.DataFrame(records)

    return df


def calculate_metrics(df):

    study_df = df[df["Type"] == "Study"]

    total_hours = study_df["Hours"].sum()

    high_priority_hours = study_df[
        study_df["Priority"] == "High"
    ]["Hours"].sum()

    subjects = study_df["Subject"].nunique()

    study_days = study_df["Date"].nunique()

    return (
        total_hours,
        high_priority_hours,
        subjects,
        study_days
    )


def validate_plan(df, available_hours):

    study_df = df[df["Type"] == "Study"]

    daily_hours = (
        study_df
        .groupby("Date")["Hours"]
        .sum()
    )

    violations = []

    for day, hours in daily_hours.items():

        if hours > available_hours + 0.01:

            violations.append(
                f"{day}: {hours:.1f} hours"
            )

    return violations


# ============================================================
# GENERATE PLAN
# ============================================================

if generate_button or regenerate_button:

    subjects = clean_list(subjects_text)

    priority_topics = clean_list(priority_text)

    if not subjects:

        st.error(
            "Please enter at least one subject."
        )

    elif exam_date < start_date:

        st.error(
            "Exam date must be after the start date."
        )

    else:

        if regenerate_button:

            st.session_state.generation_count += 1

        else:

            st.session_state.generation_count = 0


        with st.spinner(
            "Creating your personalized study plan..."
        ):

            df = create_plan(
                start_date,
                exam_date,
                subjects,
                priority_topics,
                available_hours,
                session_length,
                include_breaks,
                difficulty
            )

            st.session_state.plan = df

            st.session_state.generated = True


# ============================================================
# MAIN DASHBOARD
# ============================================================

if st.session_state.generated and st.session_state.plan is not None:

    df = st.session_state.plan

    total_hours, high_hours, subject_count, study_days = (
        calculate_metrics(df)
    )

    violations = validate_plan(
        df,
        available_hours
    )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    st.markdown("### 📊 Your Study Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Study Hours</div>
                <div class="metric-value">{total_hours:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Priority Hours</div>
                <div class="metric-value">{high_hours:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Subjects</div>
                <div class="metric-value">{subject_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Study Days</div>
                <div class="metric-value">{study_days}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    st.markdown("### ✅ Constraint Validation")

    if not violations:

        st.success(
            "All daily study-hour constraints are satisfied."
        )

    else:

        st.warning(
            "Some daily constraints need adjustment."
        )

        for violation in violations:

            st.write(
                f"⚠️ {violation}"
            )


    # --------------------------------------------------------
    # Tabs
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📅 Weekly Plan",
            "🧩 Task Decomposition",
            "📈 Analytics",
            "🎯 Priority Focus",
            "💡 Study Tips"
        ]
    )


    # ========================================================
    # TAB 1
    # ========================================================

    with tab1:

        st.markdown("### 📅 Personalized Schedule")

        display_df = df.copy()

        display_df["Date"] = display_df[
            "Date"
        ].astype(str)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Study Plan",
            data=csv_data,
            file_name="AI_Study_Plan.csv",
            mime="text/csv",
            use_container_width=True
        )


    # ========================================================
    # TAB 2
    # ========================================================

    with tab2:

        st.markdown("### 🧩 Task Decomposition")

        st.markdown(
            """
            <div class="info-box">

            The planner breaks the study workload into smaller tasks:

            <b>Subject → Topic → Study Session → Revision → Practice</b>

            This follows the task decomposition concept from the syllabus.

            </div>
            """,
            unsafe_allow_html=True
        )


        for subject in df[
            df["Type"] == "Study"
        ]["Subject"].unique():

            subject_df = df[
                df["Subject"] == subject
            ]

            with st.expander(
                f"📚 {subject}"
            ):

                for _, row in subject_df.iterrows():

                    st.write(
                        f"• {row['Topic']} — "
                        f"{row['Hours']} hour(s) — "
                        f"{row['Priority']} Priority"
                    )


    # ========================================================
    # TAB 3
    # ========================================================

    with tab3:

        st.markdown("### 📈 Study Analytics")

        study_df = df[
            df["Type"] == "Study"
        ]

        daily_summary = (
            study_df
            .groupby("Date")["Hours"]
            .sum()
            .reset_index()
        )

        daily_summary["Date"] = (
            daily_summary["Date"]
            .astype(str)
        )

        st.bar_chart(
            daily_summary.set_index("Date")
        )


        subject_summary = (
            study_df
            .groupby("Subject")["Hours"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.markdown(
            "#### 📚 Hours by Subject"
        )

        st.bar_chart(
            subject_summary
        )


    # ========================================================
    # TAB 4
    # ========================================================

    with tab4:

        st.markdown("### 🎯 Priority Focus")

        priority_summary = (
            df[
                df["Type"] == "Study"
            ]
            .groupby("Priority")["Hours"]
            .sum()
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            high = priority_summary.get(
                "High",
                0
            )

            st.markdown(
                f"""
                <div class="card">

                <h3>🔴 High Priority</h3>

                <h2>{high:.1f} hrs</h2>

                <p>Focus on these topics first.</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            medium = priority_summary.get(
                "Medium",
                0
            )

            st.markdown(
                f"""
                <div class="card">

                <h3>🟡 Medium Priority</h3>

                <h2>{medium:.1f} hrs</h2>

                <p>Maintain steady progress.</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:

            low = priority_summary.get(
                "Low",
                0
            )

            st.markdown(
                f"""
                <div class="card">

                <h3>🟢 Low Priority</h3>

                <h2>{low:.1f} hrs</h2>

                <p>Use remaining study time.</p>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # TAB 5
    # ========================================================

    with tab5:

        st.markdown("### 💡 Smart Study Suggestions")

        suggestions = [
            "⭐ Start each day with a high-priority topic.",
            "🧠 Use active recall instead of only reading notes.",
            "✍️ Practice questions after completing each topic.",
            "☕ Take short breaks between study sessions.",
            "🔄 Reserve time for revision before the exam.",
            "📊 Track completed topics every evening.",
            "🎯 Focus on one subject during each study session.",
            "📝 Use mock tests during the final preparation days."
        ]

        for suggestion in suggestions:

            st.info(suggestion)


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.markdown("""
    <div class="card">

    <h2>👋 Welcome to your Smart Study Planner</h2>

    <p>
    Enter your subjects, available study hours,
    exam date and priority topics from the sidebar.
    </p>

    <p>
    Then click <b>✨ Generate Study Plan</b>
    to create your personalized schedule.
    </p>

    </div>
    """, unsafe_allow_html=True)


    # Feature cards

    a, b, c = st.columns(3)

    with a:

        st.markdown("""
        <div class="card">

        <h3>🧩 Task Decomposition</h3>

        <p>
        Break large subjects into smaller
        manageable study tasks.
        </p>

        </div>
        """, unsafe_allow_html=True)


    with b:

        st.markdown("""
        <div class="card">

        <h3>⭐ Priority Handling</h3>

        <p>
        Important topics receive more
        attention in the schedule.
        </p>

        </div>
        """, unsafe_allow_html=True)


    with c:

        st.markdown("""
        <div class="card">

        <h3>🔄 Iterative Refinement</h3>

        <p>
        Regenerate the plan to create
        another schedule variation.
        </p>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

📚 AI Study Planner • Academic Project

<br>

Built with Python + Streamlit

<br><br>

Task Decomposition • Structured Planning • Iterative Refinement

</div>
""", unsafe_allow_html=True)