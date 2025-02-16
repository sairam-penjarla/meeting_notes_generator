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



class Utilities:
    def __init__(self):
        logger.debug("initializing utilities")
        self.config = get_config()
        self.session_utils = SessionUtilities()

        self.client = OpenAI()

    def get_user_msg(
        self,
        question,
    ):
        logger.debug("getting user message")

        return {
            "role": "user",
            "content": question,
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

    def extract_text(self, file_content, file_type, max_length=5000):
        def process_part(part):
            messages = self.get_previous_messages("shorter_transcript_prompt")
            part = self.invoke_llm(messages=messages + [self.get_user_msg(part)])
            return part

        # Ensure the file type starts with a dot
        file_type = file_type.lower().strip()
        logger.info(f"File type: {file_type}")

        if file_type == ".txt":
            # Decode the file content and return as a string
            text = file_content.decode("utf-8")
            logger.info("Decoded .txt file content")

        elif file_type == ".docx":
            # Parse the .docx content using python-docx with an in-memory file
            with io.BytesIO(file_content) as file_stream:
                doc = Document(file_stream)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info("Parsed .docx file content")

        elif file_type == ".vtt":
            # Parse the .vtt content directly using webvtt
            with io.BytesIO(file_content) as file_stream:
                text = "\n".join(
                    [caption.text for caption in webvtt.read_buffer(file_stream)]
                )
            logger.info("Parsed .vtt file content")

        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        logger.info(f"Initial text length: {len(text)}")
        # print(f"Initial text length: {len(text)}")

        # Split the text if it exceeds the max_length
        if len(text) > max_length:
            parts = [process_part(text[i:i + max_length]) for i in range(0, len(text), max_length)]
            logger.info("Text split into parts and processed")
        else:
            parts = [text]

        # Process each part and concatenate the results
        processed_text = "".join(parts)
        logger.info(f"Processed text length: {len(processed_text)}")
        # print(f"Processed text length: {len(processed_text)}")

        # Re-process if the final size is above 6000
        while len(processed_text) > 6000:
            logger.info("Processed text length exceeds 6000, re-processing")
            parts = [process_part(processed_text[i:i + max_length]) for i in range(0, len(processed_text), max_length)]
            processed_text = "".join(parts)
            logger.info(f"Re-processed text length: {len(processed_text)}")
            # print(f"Re-processed text length: {len(processed_text)}")

        return processed_text

    def process_transcript(self, transcript, max_length=5000):
        def process_part(part):
            messages = self.get_previous_messages("shorter_transcript_prompt")
            part = self.invoke_llm(messages=messages + [self.get_user_msg(f"Instructions: Make sure that you reduce the transcript into half of it's length. transcript: {part}")])
            return part

        logger.info(f"Initial transcript length: {len(transcript)}")
        # print(f"Initial transcript length: {len(transcript)}")

        # Split the transcript if it exceeds the max_length
        if len(transcript) > max_length:
            parts = [transcript[i:i + max_length] for i in range(0, len(transcript), max_length)]
            logger.info("Transcript split into parts")
        else:
            parts = [transcript]

        # Process each part and concatenate the results
        processed_transcript = "".join([process_part(part) for part in parts])
        logger.info(f"Processed transcript length: {len(processed_transcript)}")
        # print(f"Processed transcript length: {len(processed_transcript)}")

        # Re-process if the final size is above 6000
        while len(processed_transcript) > 6000:
            logger.info("Processed transcript length exceeds 6000, re-processing")
            parts = [process_part(processed_transcript[i:i + max_length]) for i in range(0, len(processed_transcript), max_length)]
            processed_transcript = "".join(parts)
            logger.info(f"Re-processed transcript length: {len(processed_transcript)}")
            # print(f"Re-processed transcript length: {len(processed_transcript)}")

        return processed_transcript