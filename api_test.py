import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')
prompt = ""
response = model.generate_content(prompt, stream=True)
for chunk in response:
    print(chunk.text)
    print("_" * 80)
