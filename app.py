import streamlit as st
from st_pages import show_pages, Page
from streamlit_login_auth_ui.widgets import __login__

st.set_page_config(
    page_title="PolarSpace",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://hk3lab.ai",
        "Report a bug": "https://github.com/olsonperrensen/polars-streamlit/issues",
        "About": "![image](https://hk3lab.ai/wp-content/uploads/2020/02/cropped-cropped-hk3lab-3.png) 2024 © HK3 Lab S.r.l. Via Parteli 19 38068 Rovereto (TN) - Italy - PI/CF 02572270227",
    },
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


def render_footer():
    ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
<p style='font-size: 0.875em;'>2024 © HK3 Lab S.r.l. Via Parteli 19 38068 Rovereto (TN) - Italy - PI/CF 02572270227</p>
</div>

</div>
"""
    st.write(ft, unsafe_allow_html=True)


show_pages(
    [
        Page("app.py", "About Project", "🚩"),
        Page("pages/About.py", "HK3lab", "🌇"),
        Page("pages/HExplore.py", "Explore", "📈"),
        Page("pages/Query.py", "Query", "📅"),
        Page("pages/llm.py", "Experiment", "🦄"),
        Page("pages/openapi.py", "OPENAPI", "🐲"),
        Page("pages/openapi-v2.py", "OPENAPIv2", "🐉"),
        Page("pages/history.py", "History", "🦜"),
    ]
)
st.title("🌟 Welcome to PolarSpace! 🌌")

st.write(
    "PolarSpace is a powerful and intuitive web application that empowers users to explore, analyze, and visualize data using the Polars library and Streamlit framework. 📊📈"
)
feature_tabs = st.tabs(["🎯 Features"])

with feature_tabs[0]:
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11, col12 = st.columns(3)
    col13, col14, col15 = st.columns(3)
    with col1:
        with st.expander("📁 Seamless Data Uploading"):
            st.write(
                "Users can effortlessly target their Parquet files (up to 2GB in size). The app automatically handles file validation and provides informative error messages for a smooth user experience."
            )
    with col2:
        with st.expander("🎛️ Dynamic Data Querying"):
            st.write(
                "PolarSpace offers a highly interactive and customizable data experience. Users can dynamically select columns, slice rows, and apply Polars expressions to explore and transform their data."
            )
    with col3:
        with st.expander("📝 Code Snippets and Examples"):
            st.write(
                "PolarSpace provides a collection of pre-defined code snippets and examples, making it easy for users to explore and learn the capabilities of Polars and Streamlit."
            )
    with col4:
        with st.expander("📊 Interactive Plotting"):
            st.write(
                "Dive deep into your data with interactive plotting capabilities powered by Altair and Plotly. Create stunning 2D and 3D visualizations to gain valuable insights from your datasets."
            )

    with col5:
        with st.expander("⚡ High-Performance Data Processing"):
            st.write(
                "PolarSpace leverages the power of Polars and optimized data processing techniques to handle large datasets efficiently. Experience lightning-fast data loading, filtering, and aggregation."
            )
    with col6:
        with st.expander("📜 Expression History"):
            st.write(
                "PolarSpace maintains a history of user expressions and data frame transformations, allowing users to easily track and reproduce their analysis steps."
            )

    with col7:
        with st.expander("🔒 Secure Authentication"):
            st.write(
                "PolarSpace ensures data privacy and security by implementing a robust authentication system using streamlit-login-auth-ui. Only authenticated users can access the app's features and their data."
            )
    with col8:
        with st.expander("🐍 Enhanced Security Measures"):
            st.write(
                "The codebase undergoes refactoring, static analysis, and dynamic code analysis to identify and mitigate potential security vulnerabilities. User-provided code is executed in isolated containers, ensuring a secure user experience."
            )
    with col9:
        with st.expander("☁️ Scalable Cloud Infrastructure"):
            st.write(
                "The app leverages cloud services for scalable remote code execution and data storage, ensuring optimal performance and reliability as the user base grows."
            )
    with col10:
        with st.expander("🧩 Modular and Organized Code"):
            st.write(
                "The app's codebase is structured into separate Python files, ensuring a clean and maintainable architecture. Streamlit's session state is utilized to seamlessly pass data between components."
            )
    with col11:
        with st.expander("📦 Extensibility"):
            st.write(
                "PolarSpace supports the installation of allowed pip packages, enabling users to extend the app's functionality and leverage additional libraries for advanced data analysis and visualization."
            )
    with col12:
        with st.expander("🔒 Isolated Execution"):
            st.write(
                "User-provided code is executed in isolated containers, ensuring improved safety and preventing unauthorized access to sensitive system resources."
            )
    with col13:
        with st.expander("🚨 Robust Error Handling"):
            st.write(
                "The app implements comprehensive error handling mechanisms, providing informative error messages and appropriate redirections. Custom error pages and backup displays ensure a seamless user experience."
            )
    with col14:
        with st.expander("🔍 Logging and Monitoring"):
            st.write(
                "PolarSpace incorporates logging mechanisms to track user actions and system behavior, facilitating debugging and troubleshooting processes."
            )
    with col15:
        with st.expander("🚀 Deployment Ready"):
            st.write(
                "The app is configured and optimized for deployment on Heroku, ensuring scalability and reliability."
            )
with st.expander("🎓A final word"):
    st.write(
        "PolarSpace is continuously evolving to provide an even better user experience. Get ready to unleash the power of data analysis and visualization with PolarSpace. Happy data-ing! 🌠💫"
    )


render_footer()
