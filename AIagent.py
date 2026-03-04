import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖")
st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your technical question...")

    if user_query:
        with st.spinner("🚀 Connecting to Gemini v1..."):
            try:
                # 3. الحل الذهبي: تحديد الموديل والنسخة v1 لضمان التوافق
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro", # استخدام النسخة الاحترافية الأحدث
                    google_api_key=api_key,
                    version="v1",          # إجبار المكتبة على استخدام المسار المستقر وليس beta
                    temperature=0.3
                )

                # 4. الحصول على الإجابة
                response = llm.invoke([HumanMessage(content=user_query)])
                
                # 5. العرض
                st.success("### 🤖 Response:")
                st.write(response.content)
                
            except Exception as e:
                # محاولة تلقائية أخيرة في حال وجود خلل في تعريف الموديل
                st.error(f"Error: {e}")
                st.info("🔄 Try refreshing the page if the error persists.")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
