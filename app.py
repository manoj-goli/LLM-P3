from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.example_selectors import LengthBasedExampleSelector
llm = OpenAI(temperature=.9, model="gpt-3.5-turbo-instruct")

#UI starts here

import streamlit as st

st.set_page_config(
    page_title="I am a ManBot",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

user_input = st.text_input("Type the query", "Type the quety here")
todo = st.selectbox(
    "What would you like to do",
    ("Explain", "Poem", "Funny comment"),
)
character = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Kid]", "***Adult***", "Senior"],
    index=None,
)
verbose = st.slider("Adjust verbose here", 0, 100, 10)
submit = st.button("Generate", type="primary")

examples = []

if character == ":rainbow[Kid]":
    examples = [
        {
            "query": "What is a street light?",
            "answer": "It's like a giant nightlight that helps cars see where to go when it's dark!"
        },
        {
            "query": "Why do trees have leaves?",
            "answer": "So they can wear their green clothes and make yummy oxygen for us!"
        },
        {
            "query": "How does a rainbow appear?",
            "answer": "It's like the sky is painting with colors after the rain takes a little nap!"
        },
        {
            "query": "What makes the stars twinkle?",
            "answer": "They're winking at us from far away in the night sky!"
        },
        {
            "query": "Why do birds sing?",
            "answer": "They're having fun singing happy songs to greet the morning sun!"
        }
    ]

elif character == "***Adult***":
    examples = [
        {
            "query": "What is a street light?",
            "answer": "A street light is a public lighting fixture found on streets and roads. It provides illumination to improve visibility for drivers and pedestrians during nighttime or low-light conditions."
        },
        {
            "query": "Why do trees have leaves?",
            "answer": "Trees have leaves to perform photosynthesis, which is the process of converting sunlight, carbon dioxide, and water into glucose and oxygen. Leaves also play a role in regulating water loss and providing shade."
        },
        {
            "query": "How does a rainbow appear?",
            "answer": "A rainbow appears when sunlight is refracted, dispersed, and reflected inside water droplets in the atmosphere. This process separates the light into its constituent colors, creating the multicolored arc we see."
        },
        {
            "query": "What makes the stars twinkle?",
            "answer": "Stars appear to twinkle due to the Earth's atmosphere. As starlight passes through different layers of air with varying temperatures and densities, it bends slightly, causing the light to fluctuate and create a twinkling effect."
        },
        {
            "query": "Why do birds sing?",
            "answer": "Birds sing for various reasons, including attracting mates, defending their territory, and communicating with other birds. Their songs can convey information about their presence, reproductive status, and more."
        }
    ]

elif character == "Senior":
    examples = [
        {
            "query": "What is a street light?",
            "answer": "A street light is a lamp post that illuminates our streets at night, ensuring that both pedestrians and drivers can navigate safely after dark."
        },
        {
            "query": "Why do trees have leaves?",
            "answer": "Trees have leaves to carry out photosynthesis, which is essential for producing the oxygen we breathe and providing shade and shelter in our environment."
        },
        {
            "query": "How does a rainbow appear?",
            "answer": "A rainbow forms when sunlight passes through raindrops, bending and splitting into its constituent colors, creating that beautiful arc we all admire after a storm."
        },
        {
            "query": "What makes the stars twinkle?",
            "answer": "Stars appear to twinkle because their light passes through Earth's turbulent atmosphere, causing slight variations in brightness and position as seen from the ground."
        },
        {
            "query": "Why do birds sing?",
            "answer": "Birds sing for various reasons, such as attracting mates, marking their territory, and communicating with each other. Their songs add life and vibrancy to our mornings."
        }
    ]

example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template="Query: {query}\nOutput: {answer}"
)

example_selector = LengthBasedExampleSelector(
    # The examples it has available to choose from.
    examples=examples,
    # The PromptTemplate being used to format the examples.
    example_prompt=example_prompt,
    # The maximum length that the formatted examples should be.
    # Length is measured by the get_text_length function below.
    max_length=100
    # The function used to get the length of a string, which is used
    # to determine which examples to include. It is commented out because
    # it is provided as a default value if none is specified.
    # get_text_length: Callable[[str], int] = lambda x: len(re.split("\n| ", x))
)

dynamic_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="{todo} as a {character}. Below are some examples and followed by the user's input ",
    suffix="Input: {user_input}\nOutput:",
    input_variables=["todo", "character", "user_input"]
)

if submit:
    response = llm.invoke(dynamic_prompt.format(user_input=user_input,todo=todo,character=character))
    print(response)
    st.write(response)


