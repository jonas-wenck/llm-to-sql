from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import test_data
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

hf_cache_directory = os.getenv("HF_CACHE_DIRECTORY")
print("Hugging face cache directory from ENV: " + hf_cache_directory)

model = AutoModelForCausalLM.from_pretrained("PipableAI/pip-sql-1.3b", cache_dir=hf_cache_directory)
tokenizer = AutoTokenizer.from_pretrained("PipableAI/pip-sql-1.3b", cache_dir=hf_cache_directory)

prompt = f"""<schema>{test_data.SCHEMA}</schema>
<question>{test_data.QUESTION}</question>
<sql>"""

start_time = datetime.now()
print("Start time: " + start_time.strftime("%H:%M:%S"))
print("Generating response...")

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True).split('<sql>')[1].split('</sql>')[0])

end_time = datetime.now()
print("End time: " + end_time.strftime("%H:%M:%S"))
duration = end_time - start_time
print("Response generation took " + str(duration.total_seconds()) + " seconds")
