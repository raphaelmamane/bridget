import streamlit as st




def sidebar():
    with st.sidebar:

        st.image('/Users/raphael/bridget/images/bridget.png')
        st.markdown(
            "## Hi, I’m Bridget!\n"
            "I’m your Nexar AI-analyst,\n"
            "here to bridge the gap between \n"
            "data and people.\n\n"
            "**Upload** a pdf, doc or txt file, choose a dataset, ask a question…\n"
            "Get an analysis"
            "in real-time!\n"
        )


        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "Bridget was developed at the Nexar 2023 GenAI Hackathon by the awesome team made of:\n "
            "documents and get accurate answers with instant citations. "
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/mmz-001/knowledge_gpt) "  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("---")
