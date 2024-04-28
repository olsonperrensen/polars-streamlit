import streamlit as st
from st_pages import show_pages, Page
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(
    page_title="PolarSpace",
    page_icon="🌌",
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
        Page("app.py", "About Project", "🚩"),
        Page("pages/About.py", "About HK3lab", "🧑‍💼"),
        Page("pages/HExplore.py", "HExplore", "📈"),
        Page("pages/Query.py", "Query", "📅"),
    ]
)
st.title("🌟 Welcome to PolarSpace! 🌌")

st.write(
    "PolarSpace is a powerful and intuitive web application that empowers users to explore, analyze, and visualize data using the Polars library and Streamlit framework. 📊📈"
)
feature_tabs = st.tabs(
    ["Data Interaction", "Analysis & Visualization", "Security & Performance"]
)

with feature_tabs[0]:
    with st.expander("📁 Seamless Data Uploading"):
        st.write(
            "Users can effortlessly target their Parquet files (up to 2GB in size). The app automatically handles file validation and provides informative error messages for a smooth user experience."
        )
    with st.expander("🎛️ Dynamic Data Querying"):
        st.write(
            "PolarSpace offers a highly interactive and customizable data experience. Users can dynamically select columns, slice rows, and apply Polars expressions to explore and transform their data."
        )
    with st.expander("📝 Code Snippets and Examples"):
        st.write(
            "PolarSpace provides a collection of pre-defined code snippets and examples, making it easy for users to explore and learn the capabilities of Polars and Streamlit."
        )

with feature_tabs[1]:
    with st.expander("📊 Interactive Plotting"):
        st.write(
            "Dive deep into your data with interactive plotting capabilities powered by Altair and Plotly. Create stunning 2D and 3D visualizations to gain valuable insights from your datasets."
        )
    with st.expander("⚡ High-Performance Data Processing"):
        st.write(
            "PolarSpace leverages the power of Polars and optimized data processing techniques to handle large datasets efficiently. Experience lightning-fast data loading, filtering, and aggregation."
        )
    with st.expander("📜 Expression History"):
        st.write(
            "PolarSpace maintains a history of user expressions and data frame transformations, allowing users to easily track and reproduce their analysis steps."
        )

with feature_tabs[2]:
    with st.expander("🔒 Secure Authentication"):
        st.write(
            "PolarSpace ensures data privacy and security by implementing a robust authentication system using streamlit-login-auth-ui. Only authenticated users can access the app's features and their data."
        )
    with st.expander("🐍 Enhanced Security Measures"):
        st.write(
            "The codebase undergoes refactoring, static analysis, and dynamic code analysis to identify and mitigate potential security vulnerabilities. User-provided code is executed in isolated containers, ensuring a secure user experience."
        )
    with st.expander("☁️ Scalable Cloud Infrastructure"):
        st.write(
            "The app leverages cloud services for scalable remote code execution and data storage, ensuring optimal performance and reliability as the user base grows."
        )

with st.expander("🎓A final word"):
    st.write(
        "PolarSpace is continuously evolving to provide an even better user experience. Get ready to unleash the power of data analysis and visualization with PolarSpace. Happy data-ing! 🌠💫"
    )
