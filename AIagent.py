import streamlit as st
import requests
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="Haneena AI Support", page_icon="🤖")
st.title("🤖 Haneena's Engineering AI")
st.markdown("---")

# 2. التحقق من المفتاح في Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    user_query = st.text_input("How can I help you today, Engineer?", placeholder="Ask your technical question...")

    if user_query:
        with st.spinner("🚀 Direct Connection to Gemini..."):
            try:
                # 3. الاتصال المباشر عبر API (بدون مكتبات وسيطة)
                # نستخدم مسار v1 المستقر مباشرة
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": user_query}]
                    }]
                }

                response = requests.post(url, headers=headers, data=json.dumps(data))
                result = response.json()

                # 4. معالجة النتيجة وعرضها
                if response.status_code == 200:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("### 🤖 Response:")
                    st.write(answer)
                else:
                    # إظهار الخطأ القادم من قوقل بوضوح
                    error_msg = result.get('error', {}).get('message', 'Unknown Error')
                    st.error(f"Google API Error: {error_msg}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")
else:
    st.warning("⚠️ Please add GOOGLE_API_KEY to Streamlit Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("🛠️ Developed by: **Eng. Haneena**")
