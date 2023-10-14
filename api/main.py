import fastapi
from fastapi import BackgroundTasks, FastAPI, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from dataclasses import dataclass
import re
from typing import Optional, Callable, Annotated
import io
from pydantic import BaseModel
import openai

app = fastapi.FastAPI()





class TextInput(BaseModel):
    text: str


@dataclass
class GPTConfig():
  model: str = "gpt-3.5-turbo"
  temperature: float = 0
  max_tokens: int = 3096
  top_p: float = 1
  presence_penalty: float = 0
  frequency_penalty: float = 0

def get_azure_deployment_id(model: str) -> str:
    conversion_dictionary = {
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-35",
    }
    deployment_id = conversion_dictionary.get(model)
    if deployment_id is None:
        raise ValueError(f"model {model} is not supported in azure")

    return deployment_id

def create_chat(messages,
                gpt_config: GPTConfig = GPTConfig(),
                clean_output = True):
    print("------------------------------------")
    print(messages)
    print("------------------------------------")

    result = openai.ChatCompletion.create(
      messages=messages,
      model=gpt_config.model if openai.api_type == "open_ai" else None,
      deployment_id = get_azure_deployment_id(gpt_config.model) if openai.api_type == "azure" else None,
      top_p=gpt_config.top_p,
      presence_penalty=gpt_config.presence_penalty,
      frequency_penalty=gpt_config.frequency_penalty,
      max_tokens=gpt_config.max_tokens,
      temperature=gpt_config.temperature
    )
    print(result['choices'][0].message.content)
    if clean_output:
      return result['choices'][0].message.content.strip()
    else:
      return result['choices'][0].message.content

class ParsingError(Exception):
    pass

def generate_and_parse(gpt_function: Callable[[GPTConfig], str], parsing_function: Callable[[str], any], gpt_config, max_tries=2):
    # run gpt function until parsable.
    for i in range(max_tries):
        output = gpt_function(gpt_config)
        try:
            parsed_output = parsing_function(output)
            break
        except:
            if gpt_config.temperature < 0.3:
                gpt_config.temperature += 0.1
            pass
    else:
        raise ParsingError(f"Failed to parse output. GPT output: \n{output}")

    return parsed_output

def create_chat_and_parse(messages, parsing_function: Callable, gpt_config: GPTConfig = GPTConfig(), clean_output = True, max_tries=2):
    return generate_and_parse(gpt_function=lambda gpt_config: create_chat(messages, gpt_config, clean_output),
                       parsing_function=parsing_function,
                       gpt_config=gpt_config,
                       max_tries=max_tries)

@app.post("/get_example_sentence")
def get_example_sentence(text_input: TextInput):
    messages = [ { "role": "user", "content": f"Generate one example sentence for the word {text_input.text}" } ]
    example_sentence = create_chat(messages)
    return {"result": {
        "example_sentence": example_sentence,
        "image_link": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
        }}


@app.get("/health")
def health():
    return {"status": "ok"}
