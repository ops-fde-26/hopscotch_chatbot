import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.set_page_config(page_title="Hopscotch Support", page_icon="🛍️")
st.title("Hopscotch Support")
st.caption("Return and refund help based on store policy")

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("Missing OPENROUTER_API_KEY. Add it to a .env file (see .env.example) and restart.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
MODEL = "openai/gpt-4o-mini"

POLICY = (Path(__file__).parent / "hopscotch_policy.md").read_text(encoding="utf-8")
SYSTEM_PROMPT = f"""You are a customer support assistant for Hopscotch, a kids fashion store in Mumbai.
Be warm and short.

=== RETURN POLICY ===
{POLICY}
=== END POLICY ===

Rules:
- Answer only from the policy. Do not invent rules.
- If you need delivery date, item condition, or order value, ask for it.
- For any Section 4 case, do not decide. Say a human agent will review it.
- For defect claims, ask for photos.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

with st.sidebar:
    if st.button("Clear chat"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()
    st.markdown("**Try asking**")
    st.write("Bought a dress 10 days ago, never worn, tags on — can I return it?")
    st.write("Sole of my son's sneakers peeled off after 3 weeks of school")
    st.write("A button came off and my toddler nearly put it in his mouth")
    st.write("My order was ₹7,200, I want a refund")

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

if user_text := st.chat_input("Ask about returns, refunds, or defects"):
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                temperature=0.3,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(reply)
        except Exception as e:
            st.error(str(e))
            st.session_state.messages.pop()
