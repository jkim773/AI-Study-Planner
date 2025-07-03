import openai
import GoogleCalendarExtract

# Replace with your actual API key
with open("../openai_api_key.txt", "r") as f:
    api_key = f.read().strip()




def ask_chatgpt(output_requirement, prompt_text=""):
    client = openai.OpenAI(api_key=api_key)  # ✅ Pass it directly here

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": output_requirement},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = input("Ask ChatGPT: ")
    answer = ask_chatgpt(user_input)
    print("\nChatGPT says:\n" + answer)


