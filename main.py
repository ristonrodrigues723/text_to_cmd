
import json, os# stored in file so user doesnt get asked for it again and again
import google.generativeai as genai
import argparse# module that parses argument from cmd line terminl shell
text='this is the start of proj txt to cli, idea is to pass cmds to terminal then have gemnini respond to it will probalbly have to refer to my brother for this'


configuration='config.json'
# os=input("your os:")
# terminal=input("yout termoinal ")

def config_exits_in_sys(configuration):
    if os.path.exists(configuration):
        with open("config.json")as f:
            return json.load(f) 
    else:
        print(f"create new config files")
        return create_config(configuration)

def create_config(configuration):
    os_name=input(f"type in your os:")
    terminal=input(f"type in your terminal type")
    api_key=input(f'your api key-(can get this from "https://aistudio.google.com/prompts/new_chat") for free:')
    config_dict={
        'os':os_name,
        'terminal':terminal,
        'api_key':api_key
    }
    with open("config.json",'w') as f:
        json.dump(config_dict,f,indent=4)
        print("saved successfully")
    return config_dict
    
config=config_exits_in_sys(configuration)
os_name=config['os']
terminal=config['terminal']
api_key=config['api_key']


parser = argparse.ArgumentParser(description=text)
# parser.add_argument('api_key',help='will be used for communjcation can get this from "https://aistudio.google.com/prompts/new_chat" for free')
parser.add_argument("string_text",nargs="+",help='pass normal text here, for this to work run this app initiallty')
args=parser.parse_args()



# print(f"{args.string_text} passed for processing")


char_string=" ".join(args.string_text)
# print(char_string)


def gen_ai_ans(char_string, os_name,terminal,api_key):
    # ggl_api_key=GOOGLE_API_KEY
    genai.configure(api_key=api_key,transport="rest")#to deal with -WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
#E0000 00:00:1741496760.125789   16180 init.cc:229] grpc_wait_for_shutdown_with_timeout() timed out.



    #the model i found in a tutorial is noyt working as intended, ok ots outdated will find new through
    # models = genai.list_models()


    # print("Available Gemini Models:")
    # for model in models:
    #     print(f"- {model.name}")
    models=genai.GenerativeModel('gemini-1.5-pro-latest')#1.5-flash-pro outdtaed wont wrk tried it,
    response = models.generate_content(
        f"You are a text-to-CLI AI. Convert the given input string '{char_string}' into its exact terminal command equivalent.\n"
        f"You need to consider the exact system and terminal commands to output.\n"

        f"Respond **only** with the command, without any explanations or additional text.\n"
        f"You will be provided with {os_name} and {terminal} variables and {char_string}.\n"
        f"Generate the corresponding command based on these inputs. Only give correct commands.\n"

        f"For example, if the user says 'move a file', and you are given OS and terminal variables, return only:\n"
        f"Move-Item -Path 'C:\\source\\file.txt' -Destination 'C:\\destination\\' \n"
        f"(for Windows PowerShell) or `mv /source/file.txt /destination/` (for Linux/macOS).\n"
    )


 #it is returning whole response for request insted of just text response so needed to go through this code it only ereturns the output
    if response and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()

#output = gen_ai_ans(char_string) - parametera were are missing , i forgot to call them judt did thaty
output=gen_ai_ans(char_string, os_name,terminal,api_key)
print(f"the corresponding command is:{output}")