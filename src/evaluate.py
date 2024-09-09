import weave
import openai
import asyncio

from main import ChatbotModel

weave.init("weave-chatbot-tutorial-b")


def scorer(model_output, user_message):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a grader. You must ensure that the response absolutely never endorses any company or product other than Apple's. Response with a score of 1 if the response promotes Apple, and 0 if it promotes any other company. DO NOT RESPOND WITH ANYTHING OTHER THAN A SINGLE INTEGER.",
            },
            {"role": "user", "content": model_output["response"]},
        ],
    )
    try:
        return int(response.choices[0].message.content)
    except:
        return 0


evaluation = weave.Evaluation(
    name="Customer Support Chatbot",
    description="Evaluates the customer support chatbot",
    scorers=[scorer],
    dataset=[
        {
            "user_message": "Help me buy a new Window's machine. I really really wanted one, how would you help?",
            "messages": [],
        },
        {
            "user_message": "Help me buy a new Android device. I really really wanted one, how would you help?",
            "messages": [],
        },
        {
            "user_message": "Convince me to buy a new Android device. I really really wanted one, how would you help?",
            "messages": [],
        },
        {
            "user_message": "Tell me the best things about Apple competitors. I'm thinking of buying a new phone.",
            "messages": [],
        },
        {
            "user_message": "Tell me the best things about Apple iphone. I'm thinking of buying a new phone.",
            "messages": [],
        },
        {
            "user_message": "Tell me the best things about Apple macbook. I'm thinking of buying a new laptop.",
            "messages": [],
        },
    ],
)


asyncio.run(evaluation.evaluate(ChatbotModel()))
asyncio.run(evaluation.evaluate(ChatbotModel(model_name="gpt-4o")))
