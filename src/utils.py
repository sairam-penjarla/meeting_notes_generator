import io
import json
import os
import random
import re

import pandas as pd
import pandasql as ps
import webvtt
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

from config import get_config
from custom_logger import logger
from src.multi_shot_examples import get_examples
from src.session_utils import SessionUtilities
from src.prompt_templates import get_prompt

load_dotenv()

DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")


class Utilities:
    def __init__(self):
        logger.debug("initializing utilities")
        self.config = get_config()
        self.session_utils = SessionUtilities()

        self.client = OpenAI(api_key=DATABRICKS_TOKEN, base_url=DATABRICKS_HOST)

    def get_user_msg(
        self,
        content,
        question,
    ):
        logger.debug("getting user message")

        return {
            "role": "user",
            "content": f"Content:{content}\n\nQuestion:{question}\n\nAnswer:",
        }

    def get_session_icon(self, session_id):
        icon_name = self.session_utils.get_session_icon(session_id)
        if icon_name is None:
            icons_dir_path = "static/images/session-icons"
            random_icon = random.choice(
                [x for x in os.listdir(icons_dir_path) if x.endswith(".svg")]
            )
            return random_icon
        return icon_name

    def get_previous_messages(self, component):
        instructions = get_prompt(component)
        messages = [{"role": "system", "content": instructions}]
        messages += get_examples(component)
        return messages

    def invoke_llm(self, messages):
        llm_params = self.config.LLM_PARAMS
        llm_params["messages"] = messages
        llm_params["stream"] = False

        chat_completion = self.client.chat.completions.create(**llm_params)

        return chat_completion.choices[0].message.content

    def invoke_llm_stream(self, messages):
        logger.debug("invoking llm")
        llm_params = self.config.LLM_PARAMS
        llm_params["messages"] = messages
        llm_params["stream"] = True

        chat_completion = self.client.chat.completions.create(**llm_params)

        for chunk in chat_completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def extract_text(self, file_content, file_type):
        # Ensure the file type starts with a dot
        file_type = file_type.lower().strip()

        if file_type == ".txt":
            # Decode the file content and return as a string
            return file_content.decode("utf-8")

        elif file_type == ".docx":
            # Parse the .docx content using python-docx with an in-memory file
            with io.BytesIO(file_content) as file_stream:
                doc = Document(file_stream)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])

        elif file_type == ".vtt":
            # Parse the .vtt content directly using webvtt
            with io.BytesIO(file_content) as file_stream:
                captions = "\n".join(
                    [caption.text for caption in webvtt.read_buffer(file_stream)]
                )
                return captions

        else:
            raise ValueError(f"Unsupported file type: {file_type}")
