import streamlit as st

score_map = {"A": 0, "B": 2, "C": 5, "D": 8}

TRAITS = {
    "OD": {
        "label": "🌿 Oily vs. Dry",
        "questions": [
            ("How often does your skin feel greasy or shiny by midday?", "Rarely", "Sometimes", "Often", "Always"),
            ("How visible are your pores, especially on the cheeks or nose?", "Barely visible", "Slightly visible", "Noticeable", "Very large"),
            ("How often do you blot or powder your skin during the day?", "Never", "1x per day", "2 to 3x per day", "4+ times per day"),
            ("After cleansing, how quickly does your skin become oily again?", "Over 8 hrs", "4 to 8 hrs", "2 to 4 hrs", "Less than 2 hrs"),
        ]
    },
    "SR": {
        "label": "🔥 Sensitive vs. Resistant",
        "questions": [
            ("Do skincare products sting or burn your skin?", "Never", "Rarely", "Often", "Always"),
            ("Do you get redness or irritation easily?", "Never", "Occasionally", "Frequently", "Always"),
            ("Do you react to fragrance or essential oils?", "Never", "Rarely", "Often", "Always"),
            ("Does your skin get red after exfoliation?", "Never", "Sometimes", "Often", "Always"),
        ]
    },
    "PN": {
        "label": "☀️ Pigmented vs. Non-Pigmented",
        "questions": [
            ("Do you have freckles or sun spots?", "None", "Few", "Some", "Many"),
            ("Do you tan easily?", "Never", "Sometimes", "Often", "Very easily"),
            ("Do you get uneven skin tone or dark patches?", "Never", "Occasionally", "Often", "Always"),
            ("Do you get post-acne dark marks?", "Never", "Sometimes", "Often", "Always"),
        ]
    },
    "WT": {
        "label": "⏳ Wrinkled vs. Tight",
        "questions": [
            ("Do you have fine lines when you smile?", "Never", "Occasionally", "Often", "Always"),
            ("Does your skin feel thin or fragile?", "Never", "Slightly", "Moderately", "Very"),
            ("Do you get lines around your eyes?", "Never", "Sometimes", "Often", "Always"),
            ("Do you have forehead lines?", "None", "Few", "Several", "Many"),
        ]
    }
}


def init_state():
    if "quiz_step" not in st.session_state:
        st.session_state.quiz_step = 0
    for key in TRAITS:
        num_questions = len(TRAITS[key]["questions"])
        if key not in st.session_state or len(st.session_state[key]) != num_questions:
            st.session_state[key] = [None] * num_questions
            
def calc_score(answers):
    return sum(score_map.get(ans.split(".")[0], 0) for ans in answers if ans)

def classify(score, trait):
    max_score = len(TRAITS[trait]["questions"]) * 8  # max per question is 8
    percentage = (score / max_score) * 100
    return {"OD": "O", "SR": "S", "PN": "P", "WT": "W"}[trait] if percentage >= 50 else {"OD": "D", "SR": "R", "PN": "N", "WT": "T"}[trait]


def run_demo_quiz():
    init_state()
    trait_keys = list(TRAITS.keys())
    page = st.session_state.quiz_step
    trait_index = page
    qpp = 4


    if trait_index >= len(trait_keys):
        return finalize_quiz()

    trait_key = trait_keys[trait_index]
    label = TRAITS[trait_key]["label"]
    questions = TRAITS[trait_key]["questions"]
    start = 0
    end = start + qpp

    st.markdown(f"<div style='text-align:center;'><h2>{label}</h2><p>Page {page+1} of 4</p></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='height: 8px; background: linear-gradient(to right, #eecbf3, #b5d2f6); border-radius: 5px; margin-bottom: 20px;'>
            <div style='height: 100%; width: {(page+1)/12*100:.1f}%; background-color: #9b59b6; border-radius: 5px;'></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .block-container {
            padding: 2rem 4rem !important; /* top/bottom 2rem, left/right 4rem */
            max-width: 95% !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for row in range(2):
        row_cols = st.columns([1, 1, 1], gap="large")
        for col_index in range(3):
            q_idx = row * 3 + col_index
            i = start + q_idx
            if i >= len(questions):
                continue


            qkey = f"{trait_key}_{i}"
            qtext, *opts = questions[i]
            options = [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"]

            with row_cols[col_index]:
                st.markdown(f"""
                    <div style='
                        background-color: #ffffff;
                        border: 1px solid #ddd;
                        border-radius: 12px;
                        padding: 14px 16px;
                        margin-bottom: 16px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                    '>
                    <p style='font-weight: 600; font-size: 18px; margin-bottom: 16px;'>{qtext}</p>
                """, unsafe_allow_html=True)

                with st.container():
                    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                    # Fetch previously selected answer, if exists
                    previous_answer = st.session_state[trait_key][i]

                    selected = st.radio(
                        label="",
                        options=options,
                        key=qkey,
                        index=options.index(previous_answer) if previous_answer in options else None,
                        label_visibility="collapsed",
                        horizontal=False,
                    )

                    # Save back to session state
                    st.session_state[trait_key][i] = selected

        # Centered buttons in a single row with spacing
    col_back, col_spacer, col_next = st.columns([1, 6, 1])

    with col_back:
        if st.button("⬅ Back", use_container_width=True, disabled=page == 0):
            st.session_state.quiz_step -= 1
            st.rerun()

    with col_next:
        unanswered = [ans for ans in st.session_state[trait_key][start:end] if ans is None]

        if page < len(trait_keys) - 1:
            if st.button("Next ➡", use_container_width=True):
                if unanswered:
                    st.warning("⚠️ Please answer all questions before continuing.")
                else:
                    st.session_state.quiz_step += 1
                    st.rerun()
        else:
            if st.button("Submit Quiz", use_container_width=True):
                if unanswered:
                    st.warning("⚠️ Please complete all questions before submitting.")
                else:
                    return finalize_quiz()

def finalize_quiz():
    scores = {k: calc_score(st.session_state[k]) for k in TRAITS}
    bsti = "".join([classify(scores[k], k) for k in TRAITS])
    st.success(f"🎉 Your BSTI Skin Type is: **{bsti}**")
    st.session_state.quiz_results = scores
    st.session_state.bsti_result = bsti
    return bsti
