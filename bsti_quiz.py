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
            ("How does your T-zone feel throughout the day?", "Tight or dry", "Normal", "Slightly oily", "Very oily"),
            ("How long does your skin feel tight/dry after washing?", "All day", "1–3 hrs", "Less than 1 hr", "Not at all"),
            ("How often do you see blackheads or clogged pores?", "Never", "Rarely", "Often", "Always"),
            ("How does your skin feel without moisturizer?", "Tight/flaky", "Normal", "Slightly oily", "Greasy"),
            ("How often do you experience flaking or rough patches?", "Never", "Rarely", "Often", "Always"),
            ("How easily does your skin absorb moisturizer?", "Very quickly", "Quickly", "Normal", "Slowly/Greasy film"),
            ("How does your skin feel after a hot shower?", "Tight", "Slightly dry", "Normal", "Slick/Oily"),
            ("How often do you get shiny areas on your face?", "Never", "Sometimes", "Often", "Always"),
            ("Do you feel the need to reapply moisturizer during the day?", "Yes, multiple times", "Yes, once", "Rarely", "Never"),
            ("Does your makeup cling to dry patches?", "Always", "Sometimes", "Rarely", "Never"),
            ("How does your skin feel in air conditioning?", "Very dry", "Slightly dry", "Normal", "Oily"),
            ("How does your skin behave during flights?", "Dry/tight", "Slightly dry", "Normal", "Oily/shiny")
        ]
    },
    "SR": {
        "label": "🔥 Sensitive vs. Resistant",
        "questions": [
            ("Do skincare products sting or burn your skin?", "Never", "Rarely", "Often", "Always"),
            ("Do you get redness or irritation easily?", "Never", "Occasionally", "Frequently", "Always"),
            ("Do you react to fragrance or essential oils?", "Never", "Rarely", "Often", "Always"),
            ("Does your skin get red after exfoliation?", "Never", "Sometimes", "Often", "Always"),
            ("Do you get hives or rashes frequently?", "Never", "Sometimes", "Often", "Always"),
            ("Is your skin affected by weather changes?", "Not at all", "Slightly", "Moderately", "Severely"),
            ("Do you break out after trying new products?", "Never", "Occasionally", "Often", "Always"),
            ("Do you experience flushing after eating spicy foods?", "Never", "Sometimes", "Often", "Always"),
            ("Is your skin reactive to touch or pressure?", "Not at all", "Slightly", "Moderately", "Extremely"),
            ("Do you have eczema or rosacea history?", "No", "Mild", "Moderate", "Severe"),
            ("Do you find sunscreen irritating?", "Never", "Rarely", "Often", "Always"),
            ("Is your skin sensitive during stress or hormonal change?", "Never", "Occasionally", "Often", "Always"),
            ("Do you avoid products due to sensitivity?", "Never", "Sometimes", "Often", "Always"),
            ("Does your skin react to chlorine or salt water?", "Never", "Mildly", "Moderately", "Severely"),
            ("Do you experience skin itchiness?", "Never", "Occasionally", "Often", "Always"),
            ("Do you feel your skin barrier is weak?", "Not at all", "Slightly", "Moderately", "Very weak")
        ]
    },
    "PN": {
        "label": "☀️ Pigmented vs. Non-Pigmented",
        "questions": [
            ("Do you have freckles or sun spots?", "None", "Few", "Some", "Many"),
            ("Do you tan easily?", "Never", "Sometimes", "Often", "Very easily"),
            ("Do you get uneven skin tone or dark patches?", "Never", "Occasionally", "Often", "Always"),
            ("Do you get post-acne dark marks?", "Never", "Sometimes", "Often", "Always"),
            ("Do you use skin-lightening products?", "Never", "Rarely", "Often", "Regularly"),
            ("Do you have melasma or pigmentation issues?", "No", "Mild", "Moderate", "Severe"),
            ("Do you wear sunscreen daily?", "Always", "Usually", "Sometimes", "Never"),
            ("Is your skin darker in some areas (knees, armpits)?", "No", "Slightly", "Noticeably", "Significantly"),
            ("Do you have under-eye darkness?", "None", "Mild", "Moderate", "Severe"),
            ("Does hyperpigmentation stay for long?", "Not at all", "Weeks", "Months", "Years"),
            ("Do you avoid sun due to pigmentation risk?", "Never", "Sometimes", "Often", "Always"),
            ("Do you notice sunspots on your face?", "No", "Few", "Several", "Many"),
            ("Do you have darker areas on your elbows/knees?", "No", "Slightly", "Moderately", "Very noticeable"),
            ("Do you use vitamin C or niacinamide regularly?", "Always", "Often", "Sometimes", "Never"),
            ("Do scars become darker on your skin?", "Never", "Occasionally", "Often", "Always"),
            ("Do you find it hard to achieve an even tone?", "Never", "Slightly", "Often", "Very often")
        ]
    },
    "WT": {
        "label": "⏳ Wrinkled vs. Tight",
        "questions": [
            ("Do you have fine lines when you smile?", "Never", "Occasionally", "Often", "Always"),
            ("Does your skin feel thin or fragile?", "Never", "Slightly", "Moderately", "Very"),
            ("Do you get lines around your eyes?", "Never", "Sometimes", "Often", "Always"),
            ("Do you have forehead lines?", "None", "Few", "Several", "Many"),
            ("Do you use anti-aging products?", "Always", "Often", "Rarely", "Never"),
            ("Do you smoke or were exposed to smoke?", "Never", "Rarely", "Occasionally", "Frequently"),
            ("Do you sleep on your side?", "Never", "Sometimes", "Often", "Always"),
            ("Is your skin elastic when pinched?", "Very", "Moderately", "Slightly", "Not at all"),
            ("Do you have crow’s feet?", "None", "Few", "Visible", "Deep"),
            ("Has your skin lost plumpness over time?", "Not at all", "Slightly", "Moderately", "Severely"),
            ("Do you get wrinkles from facial expressions?", "Never", "Occasionally", "Often", "Always"),
            ("Do you wear sunscreen for aging prevention?", "Always", "Often", "Rarely", "Never"),
            ("Has your skin changed with age?", "Not at all", "Slightly", "Moderately", "Significantly"),
            ("Do you get wrinkles from dehydration?", "Never", "Occasionally", "Often", "Always"),
            ("Do you drink plenty of water daily?", "Always", "Often", "Sometimes", "Rarely"),
            ("Do you have vertical lip lines?", "None", "Few", "Noticeable", "Deep")
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
    return {"OD": "O", "SR": "S", "PN": "P", "WT": "W"}[trait] if score >= 64 else {"OD": "D", "SR": "R", "PN": "N", "WT": "T"}[trait]

def run_quiz():
    init_state()
    trait_keys = list(TRAITS.keys())
    page = st.session_state.quiz_step
    trait_index = page // 3
    local_page = page % 3
    qpp = 6

    if trait_index >= len(trait_keys):
        return finalize_quiz()

    trait_key = trait_keys[trait_index]
    label = TRAITS[trait_key]["label"]
    questions = TRAITS[trait_key]["questions"]
    start = local_page * qpp
    end = start + qpp

    st.markdown(f"<div style='text-align:center;'><h2>{label}</h2><p>Page {local_page+1} of 3</p></div>", unsafe_allow_html=True)
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

        if page < 11:
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
