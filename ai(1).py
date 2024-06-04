import os
from dotenv import load_dotenv
import utils

# Add OpenAI import. (Add code here)
from openai import AzureOpenAI

def main(): 
        
    try:     
        load_dotenv()
        utils.initLogFile()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_model = os.getenv("AZURE_OAI_MODEL")
        azure_oai_version = "2023-12-01-preview"
        # Define Azure OpenAI client (function1-3)
        client = AzureOpenAI( azure_endpoint=azure_oai_endpoint,
                            api_key=azure_oai_key,
                            api_version=azure_oai_version,
                            )
        # Define Azure OpenAI client (function4)
        client = AzureOpenAI( base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_model}/extensions",
                            api_key=azure_oai_key,
                            api_version=azure_oai_version,
                            )
        
        

        function_map = {
            "1": function1,
            "2": function2,
            "3": function3,
            "4": function4
        }

        while True:
            print('1: Validate PoC\n' +
                  '2: Company chatbot\n' +
                  '3: Developer tasks\n' +
                  '4: Use company data\n' +
                  '\'quit\' to exit the program\n')
            command = input('Enter a number:')
            if command.strip() in function_map:
                function_map[command](client, azure_oai_model)
            elif command.strip().lower() == 'quit':
                print('Exiting program...')
                break
            else :
                print("Invalid input. Please enter number 1, 2, 3, 4, or 5.")

    except Exception as ex:
        print(ex)

# Task 1: Validate PoC
def function1(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 1: Validate PoC", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    messages=[
            {"role": "system", "content": "You are a helpful assistant." + inputText}
        ]
    

    # Define argument list (Add code here)
    apiParams = {
        "model" : aiModel,
        "messages": messages,
        
    }
    

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create( **apiParams)
    

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response

# Task 2: Company chatbot
def function2(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 2: Company chatbot", "sample-text.txt")
    
    # Build messages to send to Azure OpenAI model. (Add code here)
    messages=[
            {"role":"system", "content": "You are a helpful assistant.You must reply in English and Spanish, in a casual tone."},
            {"role":"user","content":" Where can I find the company phone number?"},
            {"role":"assistant","content":" You can find it on the footer of every page on our website. Hope that helps! Thanks for using Contoso, Ltd."  },
            {"role":"user","content":"Please reply using the following format\n###\nEnglish Reply: ......\n\nSpanish Reply......\n###" + inputText},
        ]
    

    # Define argument list (Add code here)
    apiParams = {
        "messages": messages,
        "model" : aiModel,
        "temperature": 0.5,
        "max_tokens": 1000,
    }
    

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create( **apiParams)
    

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\nHope that helps! Thanks for using Contoso, Ltd.")
    return response


def function3(aiClient, aiModel):
    while True:
        print('\n1: Add comments to my function\n' +
                '2: Write unit tests for my function\n' +
                '\"quit\" to exit the program\n')
        command = input('Enter a number to select a task:')
        if command == '1':
            file = open(file="../../legacyCode.py", encoding="utf8").read()
            newfile = "../../legacyCode.py"
            prompt = "Add comments to the following function. Return all code and comments.\n---\n" + file
            break
        elif command =='2':
            file = open(file="../../fibonacci.py", encoding="utf8").read()
            newfile = "../../fibonacci.py"
            prompt = "Write five unit tests for the following function.Return all code and comments.\n---\n" + file
            break
        else :
            print("Invalid input. Please try again.")

    inputText = utils.getPromptInput("Task 3: Developer tasks", "sample-text.txt")

    # Build messages to send to Azure OpenAI model. (Add code here)
    messages=[
            {"role":"system", "content": "You are a helpful AI assistant that helps programmers write code." + prompt}
        ]
    

    # Define argument list (Add code here)
    apiParams = {
        "messages": messages,
        "model" : aiModel
    }
    
    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create( **apiParams)
    results_file = open(file=newfile, mode="w", encoding="utf8")
    results_file.write(response.choices[0].message.content)
    
    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return response 

def function4(aiClient, aiModel):
    inputText = utils.getPromptInput("Task 4: Use company data", "sample-text.txt")


    azure_search_endpoint = os.getenv("SEARCH_ENDPOINT")
    azure_search_key = os.getenv("SEARCH_KEY")
    azure_search_index = os.getenv("SEARCH_INDEX")

    extension_config = dict(dataSources = [  
                { 
                    "type": "AzureCognitiveSearch", 
                    "parameters": { 
                        "endpoint":azure_search_endpoint, 
                        "key": azure_search_key, 
                        "indexName": azure_search_index,
                    }
                }]
                )
    # Build messages to send to Azure OpenAI model. (Add code here)
    messages = [
                {"role": "system", "content": "You are a helpful travel agent."},
                {"role": "user", "content": inputText}
            ]
    

    # Define connection and argument list (Add code here)
    apiParams = {
        "messages": messages,
        "model" : aiModel,
        "extra_body" : extension_config
    }
    

    utils.writeLog("API Parameters:\n", apiParams)

    # Call chat completion connection. Will be the same as function1 (Add code here)
    # Use the call name and **apiParams to reference our argument list
    response = aiClient.chat.completions.create( **apiParams)
    

    utils.writeLog("Response:\n", str(response))
    print("Response: " + response.choices[0].message.content + "\n")
    return


if __name__ == '__main__': 
    main()
