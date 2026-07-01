import streamlit as st
from PIL import Image
from pathlib import Path
from io import BytesIO

def define_style() :
    # --- STYLE CARDS USED TO DESCRIBE X-RAY --- #

    st.markdown(
        """
    <style>
        /* Hauteur fixe partagée pour l'image et la box conclusion */
        .sync-height {
            height: 250px !important;
        }

        .report-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* Distribue l'espace proprement à l'intérieur */
        }
        
        .card-title {
            color: #1e3a8a;
            font-weight: bold;
            font-size: 1.2rem;
            text-transform: capitalize;
            margin: 0;
        }
        
        .predicted-class {
            font-weight: bold;
            font-size: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 10px 0;
        }
        
        .confidence-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.95rem;
            font-weight: 500;
            color: #475569;
            margin-top: auto;
        }
        
        .progress-bg {
            background-color: #f1f5f9;
            border-radius: 9999px;
            width: 100%;
            height: 10px;
            margin-top: 8px;
        }
        
        .progress-fill {
            background-color: #2563eb;
            height: 10px;
            border-radius: 9999px;
        }
        
        .text-content {
            color: #334155;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .warning-box {
            background-color: #fef2f2;
            border: 1px solid #fca5a5;
            border-radius: 8px;
            padding: 12px;
            color: #991b1b;
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 20px;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            background-color: #e0f2fe;
            color: #0369a1;
            margin-top: 6px;
        }
        
        /* Forçage absolu du comportement et de la hauteur de l'image */
        [data-testid="stImage"] {
            height: 250px !important;
            width: 100% !important;
            overflow: hidden !important;
            border-radius: 12px;
            display: block !important;
        }
        [data-testid="stImage"] * {
            width: 100% !important;
            height: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }
        [data-testid="stImage"] img {
            object-fit: cover !important;
            object-position: center !important;
            border-radius: 12px;
        }

        [data-testid="column"]:has([data-testid="stImage"]) {
            width: 100% !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def display_image_dec(image, json) :
    define_style()
    # --- PREMIÈRE LIGNE : IMAGE & CONCLUSION ---
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, use_container_width=True)
    with col2:
        conf_val = json.get("confidence", 0.0)
        conf_pct = int(conf_val * 100)
        img_quality = json.get("image_quality", "N/A")

        pred_class = json.get("predicted_class", "unknown")
        class_color = (
            "#10b981" if pred_class.lower() == "normal" else "#ef4444"
        )

        st.markdown(
            f"""
        <div class="report-card sync-height">
            <div>
                <div class="card-title">Conclusion</div>
                <span class="badge">Qualité: {img_quality}</span>
            </div>
            <div class="predicted-class" style="color: {class_color};">Résultat : Scan {pred_class}</div>
            <div>
                <div class="confidence-container">
                    <span>Confiance : </span>
                    <span>{conf_pct} %</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {conf_pct}%;"></div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # --- DEUXIÈME LIGNE : VISUAL EVIDENCE ---
    st.markdown(
        f"""
    <div class="report-card">
        <div class="card-title">Visual Evidence</div>
        <div class="text-content">{json.get('visual_evidence', '')}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # --- TROISIÈME LIGNE : REASONING & JUSTIFICATION CÔTE À CÔTE ---
    col_reasoning, col_justification = st.columns(2)

    with col_reasoning:
        st.markdown(
            f"""
        <div class="report-card">
            <div class="card-title">Reasoning</div>
            <div class="text-content">{json.get('reasoning', '')}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_justification:
        st.markdown(
            f"""
        <div class="report-card">
            <div class="card-title">Justification</div>
            <div class="text-content">{json.get('justification', '')}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # --- QUATRIÈME LIGNE : LIMITATIONS ---
    limitations = json.get("limitations", "None identified.")
    if limitations and limitations.lower() != "none identified.":
        st.markdown(
            f"""
        <div class="report-card">
            <div class="card-title">Limitations</div>
            <div class="text-content">{limitations}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # --- CINQUIÈME LIGNE : WARNING ---
    st.markdown(
        f"""
    <div class="warning-box">
        ⚠️ {json.get('warning', 'Outil pédagogique uniquement.')}
    </div>
    """,
        unsafe_allow_html=True,
    )


def upload_user_image_to_directory(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) :
    UPLOAD_DIR = Path("./assets/images/user_images")

    safe_name = uploaded_file.name

    dest_path = UPLOAD_DIR / safe_name

    # uploaded_file is file-like: write its bytes to disk
    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return dest_path