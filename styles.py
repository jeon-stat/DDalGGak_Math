# styles.py
# 앱 전역 CSS를 이 파일에서만 관리합니다.
# 스타일 수정이 필요하면 app.py를 건드리지 말고 이 파일만 열면 됩니다.

APP_CSS = """
<style>
.stApp {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}
[data-testid="stSidebar"] {
    background-color: var(--background-color) !important;
    border-right: 2px solid rgba(128, 128, 128, 0.25) !important;
}
</style>
"""
