import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Haneena AI", layout="centered")
st.title("🤖 Haneena's Engineering AI")

# وضع خانة السؤال خارج شروط الـ IF لتظهر دائماً
user_query = st.text_input("How can I help you, Engineer?", placeholder="Type here...")

if user_query:
    # الآن نتحقق من المفتاح فقط عند محاولة الإرسال
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("⚠️ Key missing! Go to App Settings > Secrets and add: GOOGLE_API_KEY = 'your_key'")
    else:
        with st.status("🚀 Processing...", expanded=False) as status:
            try:
                # تعريف الـ LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=st.secrets["GOOGLE_API_KEY"],
                    version="v1"
                )

                # تعريف العميل
                agent = Agent(
                    role='Engineer Expert',
                    goal='Technical support',
                    backstory='Expert AI assistant.',
                    llm=llm,
                    verbose=False
                )

                task = Task(description=user_query, agent=agent, expected_output="Technical answer")
                crew = Crew(agents=[agent], tasks=[task])
                
                result = crew.kickoff()
                status.update(label="✅ Done!", state="complete")
                
                st.markdown("### 🤖 Response:")
                st.info(result.raw)

            except Exception as e:
                st.error(f"Error: {e}")
                status.update(label="❌ Failed", state="error")
