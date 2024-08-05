import os
import openai

openai.api_key = "sk-SFXiex2MCespk9H83d766aE49cCd4cFd8a5b4dEbAb728507"

# all client options can be configured just like the `OpenAI` instantiation counterpart
openai.base_url = "https://free.gpt.ge/v1/"
openai.default_headers = {"x-foo": "true"}

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Hello world!",
        },
    ],
)
print(completion.choices[0].message.content)

# 正常会输出结果：Hello there! How can I assist you today ?
