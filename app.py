import streamlit as st
from st_pages import show_pages, Page
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(
    page_title="EEG Dashboard",
    page_icon="💉",
    layout="wide",
)


def logged_in():
    __login__obj = __login__(
        auth_token="courier_auth_token",
        company_name="Shims",
        width=200,
        height=250,
        logout_button_name="Logout",
        hide_menu_bool=False,
        hide_footer_bool=False,
        lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
    )

    LOGGED_IN = __login__obj.build_login_ui()
    return LOGGED_IN


show_pages(
    [
        Page("app.py", "", ""),
        Page("pages/About.py", "About", "🚩"),
        Page("pages/Explore.py", "Explore", "📈"),
        Page("pages/Query.py", "Query", "📅"),
    ]
)

st.write()
