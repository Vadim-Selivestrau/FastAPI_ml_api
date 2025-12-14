import streamlit as st
import requests

API_URL = "http://app:8000/process"  # через docker-compose
# API_URL = "http://localhost:8000/process"  # 

st.set_page_config(page_title="FastAPI ML Client")
st.title("FastAPI ML Client")

prompt = st.text_area("Введите текст для классификации", height=200)

if st.button("Отправить"):
    if not prompt.strip():
        st.warning("Введите текст")
    else:
        with st.spinner("Обработка..."):
            try:
                r = requests.post(
                    API_URL,
                    json={"text": prompt},
                    timeout=30
                )
                data = r.json()

                st.subheader("Результат")

                st.markdown(f"**Model:** {data.get('model')}")
                st.markdown(f"**Cached:** {data.get('cached')}")

                st.markdown("**Predictions:**")
                predictions = data.get("predictions", [])
                if predictions:
                    for p in predictions:
                        st.markdown(f"- {p['label']}: {p['probability']:.2f}")
                else:
                    st.write("Нет предсказаний")

            except Exception as e:
                st.error(f"Ошибка при запросе к серверу: {str(e)}")
