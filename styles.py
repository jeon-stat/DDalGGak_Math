# styles.py
# 앱 전역 CSS를 이 파일에서만 관리합니다.
# 스타일 수정이 필요하면 app.py를 건드리지 말고 이 파일만 열면 됩니다.

APP_CSS = """
<style>
:root {
    --dd-border: rgba(128, 128, 128, 0.22);
    --dd-border-strong: rgba(128, 128, 128, 0.36);
    --dd-muted: rgba(128, 128, 128, 0.82);
    --dd-soft-shadow: 0 18px 45px rgba(0, 0, 0, 0.06);
}

.stApp {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.3rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color) !important;
    border-right: 1px solid var(--dd-border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

h1, h2, h3, h4 {
    letter-spacing: 0 !important;
}

p, li, label, div {
    letter-spacing: 0 !important;
}

.dd-shell {
    width: 100%;
}

.dd-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 11%, transparent);
    border: 1px solid color-mix(in srgb, var(--primary-color) 22%, transparent);
    border-radius: 999px;
    padding: 0.32rem 0.62rem;
    margin-bottom: 1rem;
}

.dd-hero {
    padding: 3rem 0 2.6rem;
    border-bottom: 1px solid var(--dd-border);
    margin-bottom: 2.3rem;
}

.dd-hero h1 {
    font-size: clamp(2.3rem, 5vw, 4.6rem);
    line-height: 1.03;
    font-weight: 820;
    margin: 0 0 1rem;
    letter-spacing: 0 !important;
}

.dd-hero p {
    max-width: 680px;
    font-size: 1.08rem;
    line-height: 1.7;
    color: var(--dd-muted);
    margin: 0;
}

.dd-section {
    margin: 2.4rem 0;
}

.dd-section-title {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 1rem;
    border-bottom: 1px solid var(--dd-border);
    padding-bottom: 0.9rem;
    margin-bottom: 1rem;
}

.dd-section-title h2,
.dd-section-title h3 {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 760;
}

.dd-section-title p {
    margin: 0;
    font-size: 0.92rem;
    color: var(--dd-muted);
}

.dd-panel {
    background: var(--secondary-background-color);
    border: 1px solid var(--dd-border);
    border-radius: 8px;
    padding: 1.2rem;
}

.dd-panel-quiet {
    border: 1px solid var(--dd-border);
    border-radius: 8px;
    padding: 1.2rem;
}

.dd-feature {
    min-height: 180px;
    border-top: 1px solid var(--dd-border);
    padding: 1.25rem 0.2rem 0.8rem;
}

.dd-feature-kicker {
    color: var(--primary-color);
    font-size: 0.78rem;
    font-weight: 760;
    margin-bottom: 0.65rem;
}

.dd-feature h3,
.dd-feature h4 {
    font-size: 1.08rem;
    font-weight: 760;
    margin: 0 0 0.55rem;
}

.dd-feature p {
    color: var(--dd-muted);
    font-size: 0.92rem;
    line-height: 1.62;
    margin: 0;
}

.dd-stat-row {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1px;
    border: 1px solid var(--dd-border);
    border-radius: 8px;
    overflow: hidden;
    background: var(--dd-border);
    margin-top: 1.7rem;
}

.dd-stat {
    background: var(--secondary-background-color);
    padding: 1rem;
}

.dd-stat strong {
    display: block;
    font-size: 1.45rem;
    margin-bottom: 0.25rem;
}

.dd-stat span {
    font-size: 0.82rem;
    color: var(--dd-muted);
}

.dd-sidebar-brand {
    border-bottom: 1px solid var(--dd-border);
    padding-bottom: 1.2rem;
    margin-bottom: 1.2rem;
}

.dd-sidebar-brand h2 {
    margin: 0 0 0.25rem;
    font-size: 1.25rem;
    font-weight: 820;
}

.dd-sidebar-brand p {
    margin: 0;
    color: var(--dd-muted);
    font-size: 0.82rem;
}

.dd-location {
    font-size: 0.78rem;
    color: var(--dd-muted);
    border: 1px solid var(--dd-border);
    border-radius: 8px;
    padding: 0.65rem 0.75rem;
    background: var(--background-color);
}

.dd-page-header {
    border-bottom: 1px solid var(--dd-border);
    padding-bottom: 1.1rem;
    margin-bottom: 1.4rem;
}

.dd-page-header h1 {
    font-size: 2.1rem;
    line-height: 1.15;
    font-weight: 820;
    margin: 0 0 0.55rem;
}

.dd-page-header p {
    margin: 0;
    max-width: 760px;
    color: var(--dd-muted);
    line-height: 1.65;
}

.dd-workflow {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin: 1rem 0 1.6rem;
}

.dd-workflow-step {
    border: 1px solid var(--dd-border);
    border-radius: 8px;
    padding: 1rem;
    background: var(--secondary-background-color);
}

.dd-workflow-step strong {
    display: block;
    margin-bottom: 0.35rem;
}

.dd-workflow-step span {
    color: var(--dd-muted);
    font-size: 0.88rem;
    line-height: 1.55;
}

.stButton > button {
    border-radius: 8px !important;
    min-height: 2.8rem;
    font-weight: 760 !important;
}

.stTextArea textarea,
.stTextInput input,
.stSelectbox [data-baseweb="select"],
.stRadio,
.stSlider {
    color: var(--text-color) !important;
}

.stTextArea textarea,
.stTextInput input {
    background-color: var(--secondary-background-color) !important;
    border: 1px solid var(--dd-border-strong) !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] {
    background: var(--secondary-background-color);
    border: 1px dashed var(--dd-border-strong);
    border-radius: 8px;
    padding: 0.9rem;
}

iframe {
    display: block;
    margin: 0 auto !important;
    border: none !important;
}

@media (max-width: 800px) {
    .block-container {
        padding-top: 1.35rem;
    }

    .dd-hero {
        padding-top: 1.6rem;
    }

    .dd-stat-row,
    .dd-workflow {
        grid-template-columns: 1fr;
    }
}
</style>
"""
