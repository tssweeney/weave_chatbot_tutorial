"""
This is a simple chatbot that uses OpenAI's API to generate responses to user messages.

The scaffolding is from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps,
and the added tracing uses the Weave library.
"""

import json
from openai import OpenAI
import streamlit as st

# 1. Initialize Weave
# This will begin to automatically track calls to many common LLM providers and orchestrators.
# In this case, all calls to `client.chat.completions.create` will be traced.
import weave

weave_client = weave.init("weave-chatbot-tutorial-b")


class ChatbotModel(weave.Model):
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
    def invoke(self, user_message, messages):
        # Add system prompt and user message to the messages list
        messages = [
            {"role": "system", "content": self.system_prompt},
            *messages,
            {"role": "user", "content": user_message},
        ]

        # Process the user input
        response = OpenAI().chat.completions.create(
            model=self.model_name,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)


def handle_feedback(call_id, feedback):
    print(f"Feedback: {feedback} for call_id: {call_id}")
    weave_client.get_call(call_id).feedback.add_reaction("👍" if feedback else "👎")
    for i, message in enumerate(st.session_state.messages):
        if "call_id" in message and message["call_id"] == call_id:
            st.session_state.messages[i]["feedback"] = feedback
            break


def main():
    model = ChatbotModel()
    # Initialize the Streamlit session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Print out a Title
    st.title("Apple Customer Support Chatbot")

    # Display the current session messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "call_id" in message:
                st.button(
                    "👍",
                    key=f"positive-{message['call_id']}",
                    on_click=handle_feedback,
                    args=[message["call_id"], True],
                    type="primary"
                    if "feedback" in message and message["feedback"] == True
                    else "secondary",
                )
                st.button(
                    "👎",
                    key=f"negative-{message['call_id']}",
                    on_click=handle_feedback,
                    args=[message["call_id"], False],
                    type="primary"
                    if "feedback" in message and message["feedback"] == False
                    else "secondary",
                )

    # Wait for user input
    if user_message := st.chat_input("What is up?"):
        # Display the user input
        with st.chat_message("user"):
            st.markdown(user_message)

        # Process the user input
        with weave.attributes(dict(env="demo")):
            res, call = model.invoke.call(
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
            st.button(
                "👍",
                key=f"positive-{call.id}",
                on_click=handle_feedback,
                args=[call.id, True],
            )
            st.button(
                "👎",
                key=f"negative-{call.id}",
                on_click=handle_feedback,
                args=[call.id, False],
            )

        # Add the user message to the session state
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Add the response to the session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
                "call_id": call.id,
                "feedback": None,
            }
        )


if __name__ == "__main__":
    main()
