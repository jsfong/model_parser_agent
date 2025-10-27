import litellm
import logging
import os
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import  MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.ERROR)

litellm._turn_on_debug()

# Configure model
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_QWEN_2_5 = "ollama_chat/qwen2.5:7b"
MODEL_QWEN_3 = "ollama_chat/qwen3:4b"
MODEL_PHI4 = "ollama_chat/phi4:14b"
MODEL_PHI4_MINI = "ollama_chat/phi4-mini:latest"
MODEL_PHI3 = "ollama_chat/phi3:3.8b-mini-128k-instruct-q4_K_M"
MODEL_GEMMA_2 = "ollama_chat/gemma2:9b-instruct-q3_K_M"

# Podium key
google_api_key = os.getenv('GOOGLE_API_KEY', '')
os.environ["GOOGLE_API_KEY"] = google_api_key


# Sub Agent currently only work with GEMINI Sep 3
USE_GEMINI = True
if USE_GEMINI:
    MODEL = MODEL_GEMINI_2_0_FLASH
    model = MODEL
else:
    # MODEL_ENDPOINT = "http://localhost:11434/v1"
    MODEL = LiteLlm(model=MODEL_QWEN_2_5)
    model = MODEL

    os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"


# MCP config
LOCAL_MCP_URL = "http://localhost:8001/sse"
LOCAL_DOCKER_MCP_URL = "http://host.docker.internal/sse"
MCP_URL = LOCAL_MCP_URL

mcpTool = MCPToolset(
    connection_params=SseServerParams(
        url=MCP_URL
    ),
    tool_filter=['get_model_stats', 'get_element_with_filter']
)


# Must use ollama_chat instead of ollama
# https://github.com/google/adk-python/issues/784#issuecomment-3191808433
# Model < 3b still having issue triggering tool
root_agent = Agent(
    name="model_parser_agent",
    model=model,
    description=(
        "Agent to retreive infomation regarding cubs model."
    ),
    instruction=(
        """
            You are a helpful agent who can retrieve information regarding cubs model using tool.
                        
            When user ask to: 
            Retrieve model infomation, use the following tools to extract cubs model info:
            - get_model_stats

            Query certain elements, use the following tool:
            - get_element_with_filter

            Depend on user query, fill in the filter below accordingly.
            Call get_model_stats tool first(if not call before) to get all possible type_ and nature.
            filter: {
                id: "", //Fill in element id here, to retrieve specific element with that id else fill in ""
                sub_graph_root_id: "", //If user filter for element under or inside subgraph of an root element, fill the root element id here else fill in ""
                type_ : "All", //If user search for certain type fill in the type here else "All"
                nature: "All", //If user search for certain nature fill in the nature here else "All"
            }

            Tips on how to use filter:
            - If user ask to get certain element under certain element, but didnt provide the root element as sub_graph_root_id (for example, get all storey inside / under building), then
                - use get_element_with_filter to look for building type, retrieve the id, if result contain multiple element ask user which root element user wanna search.
                - fill in the retrieve root element id as sub_graph_root_id then filter the type_ as storey

            In case page_config is needed, use the default value below:
            {
                elements_per_page: 10, //default to max 10 element per result
                page_to_get: 1, //default to get first page, unless user specify
            }
           
            Do not return the full json of the result, instead return how many element retrieve and the short format of the element in pretty json format(short format only include json field of id, name, type, nature) and ask user what they wanna know on the retrieved element.
  
            Take note:
            - Always use tool to retrive cubs model information
            - If result contain page, always tell user the total_page, current_page, total_result_count and ask if which page user want to get.
            - Always use the input user supplied for filter, do not alter the input.
            - User might mixup type_ and nature, base on result of get_model_stats try to fill the the filter type_ and nature else prompt user of invalid type_ or nature. 
            - Always output data in point form / table / natural language instead of json, unless user ask for it.
            - Don't use tool if there is no model id provided. Don't assume.
        """
    ),
    tools=[mcpTool]
)
