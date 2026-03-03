import os
from crewai import Agent, Crew, Task
from langchain_openai import ChatOpenAI
import streamlit as st

# التأكد من المفتاح
os.environ["OPENAI_API_KEY"] = "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"

st.set_page_config(page_title="Haneena`s AI", layout="centered")

# CSS بسيط وناعم
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #21d4fd; text-align: center; font-size: 26px !important; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #7b2ff7, #21d4fd); color: white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Haneena`s AI Support")
    st.markdown("---")

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("Client Name")
    with c2:
        language = st.selectbox("Language", ["Arabic", "English"])

    query = st.text_area("How can we help?")

    if st.button("🚀 Run Haneena`s Team"):
        if customer_name and query:
            # وكيل الدعم
            support_agent = Agent(
                role="Technical Specialist",
                goal="Solve issues",
                backstory=f"Part of Haneena`s team assisting {customer_name}",
                llm=llm,
                verbose=True
            )
            # وكيل الجودة
            qa_agent = Agent(
                role="QA Reviewer",
                goal="Refine solution",
                backstory="Ensures high quality for Haneena`s clients",
                llm=llm,
                verbose=True
            )

            # المهام
            task1 = Task(description=query, expected_output="Technical draft", agent=support_agent)
            task2 = Task(description=f"Refine in {language}", expected_output="Final response", agent=qa_agent, context=[task1])

            crew = Crew(agents=[support_agent, qa_agent], tasks=[task1, task2])
            
            with st.spinner("Processing..."):
                result = crew.kickoff()
            
            st.info(result)
            st.download_button("📥 Download", str(result), file_name="Report.txt")
        else:
            st.warning("Fill all fields!")

if __name__ == "__main__":
    main()