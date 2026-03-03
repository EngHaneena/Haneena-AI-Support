import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", layout="wide")
st.title("🤖 Haneena's AI Support")

# 2. التحقق من المفتاح
if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    
    # 3. تعريف المحرك (استخدام Pro لتجنب 404)
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=google_api_key,
        temperature=0.7
    )

    # 4. تعريف العميل (تأكدي من المسافات هنا)
    support_agent = Agent(
        role='Computer Engineering Expert',
        goal='Help students with technical questions',
        backstory='Expert in AI and Robotics.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    # 5. واجهة المستخدم
    user_query = st.text_input("Ask your question, Engineer:")

    if user_query:
        with st.spinner('Thinking...'):
            try:
                task = Task(
                    description=user_query,
                    agent=support_agent,
                    expected_output="A helpful technical response."
                )
                crew = Crew(agents=[support_agent], tasks=[task])
                result = crew.kickoff()
                
                st.success("Analysis Complete!")
                st.write(result.raw)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please add GOOGLE_API_KEY to Streamlit Secrets.")
