# main_menu.py

import streamlit as st

def render_main_menu():
    # --- Styling ---
    st.markdown("""
        <style>
            html, body, [class*="css"]  {
                background-color: #fef6f8;
            }
            .hero {
                background-color: #fde8ef;
                border-radius: 12px;
                padding: 40px 30px;
                text-align: center;
                margin: 40px auto 20px;
                max-width: 700px;
            }
            .hero h1 {
                font-size: 42px;
                color: #3b3b3b;
            }
            .hero p {
                color: #555;
                font-size: 16px;
            }
            .feature-grid {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
                margin-top: 40px;
            }
            .feature-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                width: 220px;
                text-align: center;
            }
            .feature-card h3 {
                font-size: 18px;
                margin-top: 10px;
                margin-bottom: 6px;
                color: #333;
            }
            .feature-card p {
                font-size: 14px;
                color: #777;
            }
            .how-it-works {
                text-align: center;
                margin-top: 60px;
            }
            .step {
                margin-top: 30px;
            }
            .step-circle {
                width: 40px;
                height: 40px;
                background: #fbd3dc;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                margin-bottom: 8px;
                color: #b23656;
            }
            .cta-button {
                margin-top: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown("""
    <div class="hero">
        <h1>beaucrea</h1>
        <p><em>where your beauty meets science</em><br>
        Uncover the creature within — uniquely you.<br>
        From skin traits to tailored care, we empower your natural beauty with AI-powered insight and dermatological trust.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Call to Action ---
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        st.markdown(
            """
            <style>
            button[data-testid="baseButton"] {
                background-color: #d5ede4 !important;  /* Sage green */
                color: #2f645e !important;             /* Deep sage text */
                font-weight: 600;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            button[data-testid="baseButton"]:hover {
                background-color: #c2e5d8 !important;
                color: #1f4d45 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if st.button("🌿 Start Your Skin Journey"):
            st.session_state.app_step = "quiz"
            st.rerun()


    # --- Feature Cards ---
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div style="font-size: 30px;">🧪</div>
            <h3>BSTI Quiz</h3>
            <p>Scientific 64-question assessment to determine your exact skin type.</p>
        </div>
        <div class="feature-card">
            <div style="font-size: 30px;">✨</div>
            <h3>AI Recommendations</h3>
            <p>Personalized product suggestions based on your unique skin profile.</p>
        </div>
        <div class="feature-card">
            <div style="font-size: 30px;">👩‍⚕️</div>
            <h3>Expert Insights</h3>
            <p>Access dermatologist-approved advice and skincare routines.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- How It Works ---
    st.markdown("""
    <style>
    .how-it-works {
        text-align: center;
        margin-top: 60px;
    }
    .steps-row {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        gap: 60px;
        flex-wrap: nowrap;
        margin-top: 30px;
    }
    .step {
        width: 250px;
    }
    .step-circle {
        width: 40px;
        height: 40px;
        background: #fbd3dc;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 10px;
        color: #b23656;
    }
    </style>

    <div class="how-it-works">
        <h2>How It Works</h2>
        <div class="steps-row">
            <div class="step">
                <div class="step-circle">1</div>
                <p><strong>Take the BSTI Quiz</strong><br>
                Answer 64 scientifically-designed questions about your skin</p>
            </div>
            <div class="step">
                <div class="step-circle">2</div>
                <p><strong>Get Your Skin Type</strong><br>
                Receive your personalized BSTI classification and detailed analysis</p>
            </div>
            <div class="step">
                <div class="step-circle">3</div>
                <p><strong>Discover Products</strong><br>
                Get AI-powered recommendations tailored to your unique needs</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
