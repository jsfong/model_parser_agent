# model_parser_agent
## Introduction
This is python AI agent that will use model_parser_mcp tool at `MCP_URL`.

## Pre-requisite
1. model_parser_mcp is running. Refer to section below on how to setup model_parser_mcp.
2. google adk is install https://google.github.io/adk-docs/get-started/python/#installation
3. Create a .env file. This file contain mandatory environment variables.
    - `GOOGLE_API_KEY` Google Gemini API key

## Setting Up model_parser_mcp 
### Pre-requisite
Create a .env file. This file contain mandatory environment variables.
Configure
- `DATABASE_URL=postgres://postgres:admin@localhost/modelruntime` //Targeting DB that contained savedModel
- `CACHE_SIZE=5` //Cache size

### Docker-compose
Create a .env file and run the docker compose file as below:
```
version: '3'
services:
  model_query:
    image: "jsfong/model-parser-mcp:latest"
    ports:
      - "8001:8001"
    volumes:
      - ./.env:/.env
```
### Release page
https://hub.docker.com/repository/docker/jsfong/model-parser-mcp/general



## Configuration
### Environment Variable
|  Var |  Remarks |
|---------|----------|
|MCP_URL| Set url of mcp tool in `agent.py` (only support SSE) |

### Instruction
Edit the **instruction** variable in `agent.py`.

## How to run
```
cd ../
adk web
```