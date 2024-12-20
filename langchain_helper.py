from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain

load_dotenv()
llm = OpenAI(temperature=0.6)

# 0--> BaseException , No risk

# # 1 --> Very creative . 
# load_dotenv()
# llm = OpenAI(temperature=0.6)

# # name = llm(" I want to open a restaurant for Italian food.Suggest a fancy name for this ")
# # print(name)



# prompt_template_name = PromptTemplate(
#     input_variables = ['cuisine'],
#     template = " I want to open restaurant for {cuisine} food. Suggest a fancy name for this ."
# )

# # prompt_template_name.format(cuisine="Itailan")
# # chain.run('American')
# #Sequential Chain


# prompt_template_items = PromptTemplate(
#     input_variables = ['restaurant_name'],
#     template = " Suggest some menu items for {restaurant_name} . Return it as comand separated."
# )

# # name_chain = LLMChain(llm=llm,prompt=prompt_template_name)
# # food_items_chain = LLMChain(llm=llm,prompt= prompt_template_items)

# # chain = SimpleSequentialChain(chains = [name_chain,food_items_chain])
# # response = chain.run("Indian")

# # print(response)

# name_chain = LLMChain(llm=llm,prompt=prompt_template_name,output_key="restaurant_name")
# food_items_chain = LLMChain(llm=llm,prompt= prompt_template_items,output_key="menu_items")

# seqchain = SequentialChain(
#     chains=[name_chain,food_items_chain],
#     input_variables=['cuisine'],
#     output_variables=['restaurant_name','menu_items']
# )

# print(seqchain({'cuisine':'Arabic'}))


# def generate_restaurant_name_and_items(cuisine):

#     load_dotenv()
#     llm = OpenAI(temperature=0.6)

#     prompt_template_name = PromptTemplate(
#         input_variables = ['cuisine'],
#         template = " I want to open restaurant for {cuisine} food. Suggest a fancy name for this ."
#     )

#     prompt_template_items = PromptTemplate(
#         input_variables = ['restaurant_name'],
#         template = " Suggest some menu items for {restaurant_name} . Return it as comand separated."
#     )

#     name_chain = LLMChain(llm=llm,prompt=prompt_template_name,output_key="restaurant_name")
#     food_items_chain = LLMChain(llm=llm,prompt= prompt_template_items,output_key="menu_items")

#     seqchain = SequentialChain(
#         chains=[name_chain,food_items_chain],
#         input_variables=['cuisine'],
#         output_variables=['restaurant_name','menu_items']
#     )
 
#     response = seqchain({'cuisine':'Arabic'})
#     return response


# if  __name__ == "__main__":
#     print(generate_restaurant_name_and_items("Italian"))


#Illustration of connecting to different agents 
# from langchain.agents import AgentType,initialize_agent,load_tools

# tools = load_tools(["wikipedia","llm-math"],llm=llm)


# agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# agent.run("When was Elon musk born? what is his age in 2023")


# tools = load_tools(["serpapi","llm-math"],llm=llm)
# agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
# agent.run("What is the GDP of US in 2022")


#Illustration of memory 

# from langchain.memory import ConversationBufferMemory

# prompt_template_name = PromptTemplate(
#     input_variables = ['cuisine'],
#     template = " I want to open restaurant for {cuisine} food. Suggest a fancy name for this ."
# )

# memory = ConversationBufferMemory()
# chain = LLMChain(llm=llm,prompt= prompt_template_name ,memory=memory )
# name = chain.run("Mexican")
# print(name)

# name = chain.run("Indian")
# print(name)

# print(chain.memory.buffer)


# Chaion with memory included in it
# from langchain.chains import ConversationChain

# convo = ConversationChain(llm=llm)
# print(convo.prompt.template)

# convo.run("Who won the first cricket world cup")
# convo.run("What is 5+5")
# convo.run("who was the captain of winning team")
# print(convo.memory.buffer)

#Conversatpion buffer which has the abilivtyto restrict the buffer moemory

from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
# k control the history of questions
memory = ConversationBufferWindowMemory(k=1)

convo = ConversationChain(memory=memory,llm=llm)
print(convo.run("Who won the first cricket world cup"))
print(convo.run("What is 5+5"))
print(convo.run("who was the captain of winning team"))
# print(convo.memory.buffer)
