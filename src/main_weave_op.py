"""
This is a simple chatbot that uses OpenAI's API to generate responses to user messages.

The scaffolding is from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps,
and the added tracing uses the Weave library.
"""

import json
from openai import OpenAI
import streamlit as st

import weave

weave.init("weave-chatbot-tutorial-b")


model_name: str = "gpt-3.5-turbo"
system_prompt: str = """
You are a customer support agent. You are given a transcript of a conversation between a customer and an agent.
You are asked to answer the customer's question. A few rules:

1. Always respond with JSON
2. Always respond with a JSON object with the following keys:
    - `response`: The response to the customer's question.
    - `urgency`: The urgency of the response.

Important: You work for Apple, so you should always bias towards Apple's products and services.
"""


@weave.op
def handle_user_input(user_message, messages):
    # Add system prompt and user message to the messages list
    messages = [
        {"role": "system", "content": system_prompt},
        *messages,
        {"role": "user", "content": user_message},
    ]

    # Process the user input
    response = OpenAI().chat.completions.create(
        model=model_name,
        messages=messages,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


def main():
    # Initialize the Streamlit session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Print out a Title
    st.title("Apple Customer Support Chatbot")

    # Display the current session messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Wait for user input
    if user_message := st.chat_input("What is up?"):
        # Display the user input
        with st.chat_message("user"):
            st.markdown(user_message)

        # Process the user input

        res = handle_user_input(
            user_message,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        response = res.get("response")

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add the user message to the session state
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Add the response to the session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )


if __name__ == "__main__":
    main()
