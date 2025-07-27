import streamlit as st
import tensorflow as tf
import os
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
from bsti_quiz import run_quiz  # Quiz module
from main_menu import render_main_menu
from demo_quiz import run_demo_quiz # Demo Quiz module

# --- Page Setup ---
st.set_page_config(page_title="Beaucrea Skin Analyzer", layout="centered")

with st.sidebar:
    st.markdown("""
    <style>
    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        color: white;
        background-color: #cb8ca4; /* Pink */
        padding: 14px 20px;
        margin-bottom: 0;
        border-radius: 8px 8px 0 0;
    }
    .nav-group {
        background-color: #fdf6f8;
        border: 1px solid #eee;
        border-top: none;
        border-radius: 0 0 8px 8px;
        overflow: hidden;
        margin-bottom: 24px;
    }
    .nav-button {
        background-color: #ffffff;
        padding: 12px 20px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
        font-size: 15px;
        font-weight: 500;
        color: #444;
        text-align: left;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background-color: #e4f3ef; /* Sage Green Hover */
        color: #31766d;
        font-weight: 600;
    }
    .nav-button-active {
        background-color: #d8ede9 !important; /* Active Sage Green */
        font-weight: 700;
        color: #31766d;
    }
    .sidebar-footer {
        text-align: center;
        font-size: 12px;
        color: #aaa;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Welcome to Beaucrea</div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-group'>", unsafe_allow_html=True)

    def nav_button(label, step_name, emoji="", enabled=True):
        style = (
            "opacity: 1; cursor: pointer;"
            if enabled
            else "opacity: 0.5; cursor: not-allowed;"
        )

        clicked = st.button(f"{emoji} {label}", key=f"nav_{step_name}")
        if clicked:
            if enabled:
                st.session_state.app_step = step_name
                st.rerun()
            else:
                if step_name == "upload_photo":
                    st.warning("⚠️ Please complete the BSTI Quiz first to unlock Upload.")
                elif step_name == "results":
                    st.warning("⚠️ Please upload your skin photo to view Results.")

        # Force visual disabled state
        st.markdown(
            f"""
            <style>
            button[data-testid="baseButton"][key="nav_{step_name}"] {{
                {style}
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


    # --- Navigation Buttons ---

    quiz_done = bool(st.session_state.get("bsti_type_result"))
    photo_done = bool(st.session_state.get("trait_percentages"))

    nav_button("Main Page", "start", "🏠")
    nav_button("Assessment", "quiz", "📋")
    nav_button("Demo Assessment", "demo_quiz", "🧪")
    nav_button("Skin Analysis", "upload_photo", "📸", enabled=quiz_done)
    nav_button("Results", "results", "📊", enabled=photo_done)


    # --- Copyright Footer ---
    st.markdown("<div class='sidebar-footer'>© 2025 Beaucrea. All rights reserved.</div>", unsafe_allow_html=True)


# --- Session Initialization ---
if "app_step" not in st.session_state:
    st.session_state.app_step = "start"
if "bsti_type_result" not in st.session_state:
    st.session_state.bsti_type_result = None
if "predicted_skin_traits" not in st.session_state:
    st.session_state.predicted_skin_traits = []
if "uploaded_image_display" not in st.session_state:
    st.session_state.uploaded_image_display = None

# --- Load Keras Model ---
@st.cache_resource
def load_skin_model():
    path = "mobilenetv2_skin_classification_model.keras"
    if not os.path.exists(path):
        st.error("❌ Model file not found!")
        return None
    try:
        return tf.keras.models.load_model(path)
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        return None

@st.cache_resource
def get_class_labels():
    train_dir = "C:/Users/Ideapad Gaming/OneDrive/Beaucrea Skin Classification/train"
    return sorted(os.listdir(train_dir)) if os.path.isdir(train_dir) else []

model = load_skin_model()
class_labels = get_class_labels()

# --- Load Product CSV ---
@st.cache_data
def load_product_data():
    return pd.read_csv("processed_skincare_data.csv")

product_df = load_product_data()

# --- Skincare Advice from Excel ---
@st.cache_data
def load_skincare_advice():
    advice_df = pd.read_excel("skincare_bsti_advice_updated.xlsx")
    return {
        row["Trait"]: [row["Label"], row["Description"]]
        for _, row in advice_df.iterrows()
    }

def get_skincare_routine(bsti_type):
    advice_dict = load_skincare_advice()
    recommendations = []
    for trait in bsti_type:
        if trait in advice_dict:
            recommendations.append(advice_dict[trait])
    return recommendations


# --- App Pages ---
if st.session_state.app_step == "start":
    render_main_menu()

elif st.session_state.app_step == "quiz":
    st.markdown(
    "<h1 style='text-align: center; font-size: 42px;'>📋 Step 1: Skin Type Assessment</h1>",
    unsafe_allow_html=True)
    bsti_result = run_quiz()
    if bsti_result:
        st.session_state.bsti_type_result = bsti_result
        st.success(f"Your BSTI Type: {bsti_result}")
        st.session_state.app_step = "upload_photo"
        st.rerun()

elif st.session_state.app_step == "demo_quiz":
    st.markdown(
    "<h1 style='text-align: center; font-size: 42px;'>🧪 Step 1: Skin Type Assessment (Demo)</h1>",
    unsafe_allow_html=True)
    demo_result = run_demo_quiz()
    if demo_result:
        st.session_state.bsti_type_result = demo_result
        st.success(f"Your BSTI Type: {demo_result}")
        st.session_state.app_step = "upload_photo"
        st.rerun()
elif st.session_state.app_step == "upload_photo":
    st.markdown(
        "<h1 style='text-align: center; font-size: 40px;'>📸 Step 2: Upload a Skin Photo</h1>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload a clear face photo (no makeup)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.session_state.uploaded_image_display = image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Show centered Analyze button only when image is uploaded
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔬 Analyze Image", use_container_width=True):
                if model is None or not class_labels:
                    st.error("Model or class labels not loaded.")
                else:
                    with st.spinner("Analyzing..."):
                        img = image.resize((224, 224))
                        arr = np.expand_dims(np.array(img) / 255.0, axis=0)
                        preds = model.predict(arr)[0]
                        percentages = {label: float(p * 100) for label, p in zip(class_labels, preds)}
                        st.session_state.trait_percentages = percentages
                        st.session_state.predicted_skin_traits = [
                            label for label, score in percentages.items() if score >= 50
                        ]
                        st.session_state.app_step = "results"
                        st.rerun()
    else:
        st.info("📥 Upload an image to proceed.")


elif st.session_state.app_step == "results":
    import streamlit.components.v1 as components

    # --- CSS for pink uniform tabs ---
    st.markdown("""
        <style>
        .top-nav-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            padding: 16px 12px;
            background-color: #fcfafa;
            border-bottom: 2px solid #f0eaea;
            flex-wrap: wrap;
        }

        .top-nav-button {
            background-color: #fbe4eb;
            color: #4a4a4a;
            border: 2px solid #f5c2d9;
            border-radius: 12px;
            width: 220px;
            height: 60px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out, color 0.2s;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .top-nav-button:hover {
            background-color: #f8d4e1;
        }

        .top-nav-button.active {
            background-color: #f7c1cc;
            color: #333333;
            border-color: #f7c1cc;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Tab labels ---
    tabs = ["Unique Skin Type", "Glimpse of Your Skin", "Recommended Skincare Routine", "Product Recommendations"]
    if "result_tab" not in st.session_state:
        st.session_state.result_tab = tabs[0]

    # --- Render top tab buttons ---
    st.markdown('<div class="top-nav-wrapper">', unsafe_allow_html=True)
    cols = st.columns(len(tabs))
    for i, tab in enumerate(tabs):
        with cols[i]:
            if st.button(tab, key=f"tab_{i}"):
                st.session_state.result_tab = tab
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Add active button logic ---
    st.markdown(f"""
        <script>
        const btns = window.document.querySelectorAll('[data-testid="stButton"] button');
        btns.forEach(btn => {{
            if (btn.innerText === "{st.session_state.result_tab}") {{
                btn.classList.add("top-nav-button", "active");
            }} else {{
                btn.classList.add("top-nav-button");
                btn.classList.remove("active");
            }}
        }});
        </script>
    """, unsafe_allow_html=True)

    # --- Store selected tab ---
    section = st.session_state.result_tab

 # --- Section 1: BSTI TYPE ---
    if section == "Unique Skin Type":
        st.markdown("### 🎯 Your Unique Skin Type")

        bsti_type = st.session_state.get("bsti_type_result", "N/A")

        # Main BSTI Display Box
        st.markdown(f"""
            <div style='
                background-color: #fdf2f5;
                border: 2px solid #f7c1cc;
                padding: 20px;
                border-radius: 15px;
                margin-top: 20px;
                text-align: center;
            '>
                <h2 style='margin: 0; font-size: 48px; color: #333;'>{bsti_type}</h2>
                <p style='font-weight: 500; color: #666;'>Based on Baumann Skin Type Indicator</p>
            </div>
        """, unsafe_allow_html=True)

        # Load and display description
        try:
            df = pd.read_excel("baumann_skin_types_official.xlsx", engine="openpyxl")
            match = df[df["Type"] == bsti_type]

            if not match.empty:
                st.subheader(f"📌 {match.iloc[0]['Profile']}")
                description = match.iloc[0]['Description']
                st.markdown(f"""
                    <div style='
                        margin-top: 30px;
                        padding: 18px 24px;
                        background-color: #fafafa;
                        border-left: 5px solid #f7c1cc;
                        border-radius: 10px;
                        font-size: 16px;
                        color: #333;
                    '>
                        {description}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No description found for this skin type.")
        except Exception as e:
            st.error(f"Error loading skin type description: {e}")

    # --- Section 2: Glimpse ---
    elif section == "Glimpse of Your Skin":
        st.title("🔬 Glimpse of Your Skin")

        col1, col2 = st.columns([2, 1])
        with col1:
            for label, score in st.session_state.get("trait_percentages", {}).items():
                st.write(f"**{label}**: {score:.1f}%")
                st.progress(score / 100)
        with col2:
            image = st.session_state.get("uploaded_image_display")
            if image:
                st.image(image, caption="Analyzed Image", use_container_width=True)

    # --- Section 3: Routine ---
    elif section == "Recommended Skincare Routine":
        st.title("🧴 Recommended Skincare Routine")

        advice = get_skincare_routine(st.session_state.get("bsti_type_result"))

        if advice:
            table_html = """
            <style>
            .recommendation-wrapper {
                width: 100%;
                overflow-x: auto;
                font-family: 'Segoe UI', sans-serif;
            }
            table.recommendation-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }
            table.recommendation-table th, table.recommendation-table td {
                border: 1px solid #ddd;
                padding: 12px 16px;
                text-align: left;
                vertical-align: top;
            }
            table.recommendation-table th {
                background-color: #f3f3f3;
                font-weight: 700;
            }
            table.recommendation-table tr:nth-child(even) {
                background-color: #fdf6f8;
            }
            table.recommendation-table tr:hover {
                background-color: #fbeef2;
            }
            </style>

            <div class="recommendation-wrapper">
            <table class="recommendation-table">
                <thead>
                    <tr>
                        <th>Skin Trait</th>
                        <th>Recommended Skincare Advice</th>
                    </tr>
                </thead>
                <tbody>
            """

            for trait, recommendation in advice:
                table_html += f"""
                    <tr>
                        <td>{trait}</td>
                        <td>{recommendation}</td>
                    </tr>
                """

            table_html += "</tbody></table></div>"

            # Render table using same component logic
            components.html(table_html, height=600, scrolling=True)

        else:
            st.info("No routine found for your profile.")


    # --- Section 4: Products ---
    elif section == "Product Recommendations":
        st.title("🛍 Product Recommendations")

        bsti = st.session_state.get("bsti_type_result", "")
        results = product_df[
            (product_df["skin_type"] == bsti) & (product_df["is_suitable"] == True)
        ].drop_duplicates(subset=["name"]).sort_values(by=["compatibility_score", "rating"], ascending=[False, False])

        fallback_type = None
        if "D" in bsti and "O" not in bsti:
            fallback_type = "dry"
        elif "O" in bsti and "D" not in bsti:
            fallback_type = "oily"

        if results.empty and fallback_type:
            results = product_df[
                (product_df[fallback_type] == 1) &
                (product_df["dry"] != product_df["oily"]) &
                (product_df["is_suitable"] == True)
            ].drop_duplicates(subset=["name"]).sort_values(by=["compatibility_score", "rating"], ascending=[False, False])

        if results.empty:
            st.error("Still no suitable product found. Please try again later.")
        else:
            top5 = results.head(5).copy()

            table_html = """
            <style>
            .recommendation-wrapper {
                width: 100%;
                overflow-x: auto;
                font-family: 'Segoe UI', sans-serif;
            }
            table.recommendation-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }
            table.recommendation-table th, table.recommendation-table td {
                border: 1px solid #ddd;
                padding: 12px 16px;
                text-align: left;
                vertical-align: top;
            }
            table.recommendation-table th {
                background-color: #f3f3f3;
                font-weight: 700;
            }
            .buy-link {
                background-color: #ff5c5c;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: 600;
                display: inline-block;
                text-align: center;
                text-decoration: none;
            }
            .buy-link:hover {
                background-color: #e04b4b;
            }
            </style>

            <div class="recommendation-wrapper">
            <table class="recommendation-table">
                <thead>
                    <tr>
                        <th>Product Name</th>
                        <th>Brand</th>
                        <th>Category</th>
                        <th>Price (USD)</th>
                        <th>Rating ⭐</th>
                        <th>Why It's Recommended</th>
                        <th>Buy Link</th>
                    </tr>
                </thead>
                <tbody>
            """

            for _, row in top5.iterrows():
                product_link = (
                    row.get("product_url")
                    or row.get("shop_link")
                    or f"https://shopee.com.my/search?keyword={row['name'].replace(' ', '%20')}"
                )
                table_html += f"""
                    <tr>
                        <td>{row['name']}</td>
                        <td>{row['brand']}</td>
                        <td>{row['category']}</td>
                        <td>${row['price']:.2f}</td>
                        <td>{row['rating']:.1f}</td>
                        <td>{row['compatibility_reasons']}</td>
                        <td><a class="buy-link" href="{product_link}" target="_blank">Buy Now</a></td>
                    </tr>
                """

            table_html += "</tbody></table></div>"
            components.html(table_html, height=1000, scrolling=False)

    # --- Restart Button ---
    if st.button("🔁 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
