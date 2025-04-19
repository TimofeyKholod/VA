task= 'Привет, придумай КОРОТКОЕ приветствие в стиле Джарвиса из марвел В ОТВЕТЕ НАПИШИ ТОЛЬКО ПРИВЕТСТВИЕ'
import g4f
from g4f.client import Client
client = Client()
response = client.chat.completions.create(
                model="gpt-4o-mini",
                provider=g4f.Provider.OIVSCode,
                messages=[{"role": "user", "content": task}]
            )
result = response.choices[0].message.content
gen_text(result)
# Client Start