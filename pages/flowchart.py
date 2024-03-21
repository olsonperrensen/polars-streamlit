import streamlit as st

if "token" not in st.session_state:
    st.switch_page("pages/login.py")

if st.session_state.token:  # Check if token is present
    st.title("Polars Expression Graph")

    expression = st.text_input(
        """Enter Polars expressions separated by semicolons: example below\n 
        DataFrame({
            'col1': ['string_' + str(i) for i in range(10)],
            'col2': ['another_string_' + str(i) for i in range(10)]
        }).lazy()        
        """,
        key="input_key",
    )

    if expression:
        nodes = []
        inside_method_call = False
        current_node = ""

        for char in expression:
            if char == "(":
                inside_method_call = True

            if char == ")":
                inside_method_call = False

            if char == ";" and not inside_method_call:
                nodes.append(current_node.strip())
                current_node = ""
            else:
                current_node += char

        # Append the last node after loop ends
        nodes.append(current_node.strip())

        if len(nodes) > 0:
            graph_string = "digraph {"
            for i, node in enumerate(nodes):
                graph_string += f'"{node}";'

            graph_string += "}"

        st.graphviz_chart(graph_string)
else:
    st.warning("Please log in")
