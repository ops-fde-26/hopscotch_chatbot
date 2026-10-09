# Hopscotch Support Chatbot

Streamlit chatbot that answers return and refund questions using `hopscotch_policy.md`.

Uses the OpenAI Python SDK against OpenRouter (`openai/gpt-4o-mini`).

## Run locally

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
# put OPENROUTER_API_KEY in .env
streamlit run app.py
```

## Streamlit Cloud

Set `OPENROUTER_API_KEY` in app secrets. Do not commit `.env`.
