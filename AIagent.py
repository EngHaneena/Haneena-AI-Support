import streamlit as st
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. إعداد الصفحة والتصميم
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖", layout="centered")

st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. التحقق من وجود المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    
    # 3. إظهار خانة السؤال دائماً
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask about AI, Robotics, or Computer Architecture...")

    if user_query:
        with st.status("🚀 Engineer AI is processing...", expanded=False) as status:
            try:
                # 4. تعريف المحرك (تعديل المسار لحل خطأ 404 نهائياً)
                llm = ChatGoogleGenerativeAI(
                    model="models/gemini-1.5-flash",
                    google_api_key=google_api_key,
                    version="v1",
                    temperature=0.3
                )

                # 5. تعريف العميل (Agent)
                support_agent = Agent(
                    role='Computer Engineering Expert',
                    goal='Provide fast and accurate technical support for engineering students.',
                    backstory='You are a professional AI mentor with deep knowledge in Computer Engineering.',
                    llm=llm,
                    allow_delegation=False,
                    verbose=False
                )

                # 6. تعريف المهمة (Task)
                task = Task(
                    description=user_query,
                    agent=support_agent,
                    expected_output="A concise and professional technical response in the same language as the question."
                )

                # 7. تشغيل الفريق (Crew)
                crew = Crew(
                    agents=[support_agent],
                    tasks=[task],
                    verbose=False
                )
                
                result = crew.kickoff()
                
                # تحديث الحالة عند الانتهاء
                status.update(label="✅ Success!", state="complete")
                
                # 8. عرض النتيجة
                st.markdown("### 🤖 Response:")
                st.info(result.raw)
                
            except Exception as e:
                # إذا ظهر خطأ 404 مرة أخرى، سنظهر رسالة واضحة للمستخدم
                st.error(f"System Error: {e}")
                status.update(label="❌ Failed", state="error")

else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

# تذييل الصفحة في القائمة الجانبية
st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
st.sidebar.info("Model: Gemini 1.5 Flash")
