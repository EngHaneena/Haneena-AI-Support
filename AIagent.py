# ... (الجزء العلوي من الكود كما هو)

    # 3. تعريف المحرك (تأكدي من استخدام Flash للسرعة إذا لم يظهر خطأ 404)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=google_api_key,
        temperature=0.3 # تقليل الـ temperature يجعل الرد أسرع وأكثر مباشرة
    )

    # 4. تعريف العميل (إيقاف verbose=False للسرعة)
    support_agent = Agent(
        role='Fast Technical Support',
        goal='Provide quick and accurate technical answers.',
        backstory='You are a high-speed AI assistant.',
        llm=llm,
        allow_delegation=False,
        verbose=False # تم التغيير لـ False لتقليل وقت المعالجة
    )

    # ... (بقية الكود)

    if user_query:
        with st.status("🚀 Engineer AI is working...", expanded=True) as status:
            try:
                task = Task(description=user_query, agent=support_agent, expected_output="Short technical answer.")
                crew = Crew(agents=[support_agent], tasks=[task], verbose=False)
                result = crew.kickoff()
                status.update(label="✅ Answer Ready!", state="complete", expanded=False)
                
                st.markdown("### 🤖 Response:")
                st.write(result.raw)
