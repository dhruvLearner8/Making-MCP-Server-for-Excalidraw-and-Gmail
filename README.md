# MCP Agent -- Math, Excalidraw & Gmail

An AI-powered agent built with the **Model Context Protocol (MCP)** that can solve math problems, draw shapes on **Excalidraw**, and send emails via **Gmail** -- all orchestrated by **Google Gemini 2.0 Flash**.

# Demo

https://drive.google.com/file/d/1euYWneZQ_PfEa9CHB0CtxwF8p01RJZ1b/view?usp=sharing
---

## Overview

This project demonstrates a complete MCP server-client architecture:

1. **The Agent (Client)** receives a natural-language math query, reasons through it step-by-step using an LLM, calls the appropriate MCP tools, and once the answer is found, draws a rectangle on Excalidraw and sends an email notification via Gmail.

2. **The MCP Server** exposes 20+ tools covering arithmetic, trigonometry, string manipulation, drawing on Excalidraw (via Playwright), MS Paint automation, and sending emails through the Gmail API.

```
User Query
    |
    v
 ┌──────────────────────┐
 │   Gemini 2.0 Flash   │  (LLM reasoning loop)
 └──────────┬───────────┘
            │  FUNCTION_CALL / FINAL_ANSWER
            v
 ┌──────────────────────┐       stdio        ┌──────────────────────┐
 │   MCP Client         │ ◄───────────────► │   MCP Server          │
 │   (talk2mcp.py)      │                    │   (example2.py)       │
 └──────────────────────┘                    └──────────┬───────────┘
                                                        │
                                          ┌─────────────┼─────────────┐
                                          │             │             │
                                          v             v             v
                                      Math Tools   Excalidraw    Gmail API
                                                  (Playwright)
```

---

## Features

### Math Tools
| Tool | Description |
|------|-------------|
| `add`, `subtract`, `multiply`, `divide` | Basic arithmetic |
| `power`, `sqrt`, `cbrt` | Exponentiation & roots |
| `factorial`, `log`, `remainder` | Advanced math |
| `sin`, `cos`, `tan` | Trigonometric functions |
| `add_list` | Sum all numbers in a list |
| `fibonacci_numbers` | Generate first *n* Fibonacci numbers |
| `mine` | Custom operation: `a - b - b` |

### String & Data Tools
| Tool | Description |
|------|-------------|
| `strings_to_chars_to_int` | Convert characters to ASCII values |
| `int_list_to_exponential_sum` | Sum of exponentials of a number list |
| `create_thumbnail` | Generate a 100x100 thumbnail from an image |

### Excalidraw Tools
| Tool | Description |
|------|-------------|
| `draw_rectangle_excalidraw` | Opens Excalidraw in a browser (via Playwright) and draws a rectangle at given coordinates |

### MS Paint Tools (Windows)
| Tool | Description |
|------|-------------|
| `open_paint` | Launch MS Paint on a secondary monitor |
| `draw_rectangle` | Draw a rectangle on the Paint canvas |
| `add_text_in_paint` | Insert text into Paint |

### Gmail Tools
| Tool | Description |
|------|-------------|
| `send_email` | Send an email via the Gmail API |

---

## Project Structure

```
code-1/
├── example2.py              # MCP Server -- all tools defined here
├── talk2mcp.py              # MCP Client / Agent -- LLM-driven iterative loop
├── talk2paint.py            # Lightweight client for testing Excalidraw tools
├── gmail_client.py          # Gmail API helper (auth + message creation)
├── example_mcp_server.py    # Earlier version of the MCP server
├── decorator.py             # Python decorator example (logging & timing)
├── main.py                  # Scaffold entry point
├── pyproject.toml           # Project config & dependencies
├── .gitignore               # Git ignore rules
├── .python-version          # Python 3.12
└── README.md                # You are here
```

---

## Prerequisites

- **Python 3.12+**
- **uv** package manager
- **Windows OS** (required for MS Paint tools; Excalidraw & Gmail work cross-platform)
- A **Google Cloud** project with the Gmail API enabled
- A **Gemini API key**

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Set up Gmail credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and enable the **Gmail API**.
2. Download `credentials.json` (OAuth 2.0 Client ID) and place it in the project root.
3. Run the token generation flow to create `token.json`:

```bash
uv run python generate_token.py
```

> **Note:** `credentials.json` and `token.json` are excluded from version control via `.gitignore`.

---

## Usage

### Run the full agent pipeline

This starts the MCP client, connects to the server, and runs the iterative agent loop:

```bash
uv run python talk2mcp.py
```

**What happens:**
1. The agent receives the math query (e.g., *"Find ASCII values of INDIA and return the sum of their exponentials"*).
2. Gemini reasons through the problem, calling tools like `strings_to_chars_to_int` and `int_list_to_exponential_sum`.
3. Once the final answer is reached, the agent draws a rectangle on Excalidraw and sends an email notification via Gmail.

### Run the MCP server standalone (for development)

```bash
uv run python example2.py dev
```

### Test Excalidraw drawing only

```bash
uv run python talk2paint.py
```

---

## How the Agent Loop Works

```
1.  User query is sent to Gemini with a system prompt listing all available tools.
2.  Gemini responds with either:
      - FUNCTION_CALL: tool_name|param1|param2|...   --> execute the tool, feed result back
      - FINAL_ANSWER: [value]                        --> stop iterating
3.  Results from each iteration are accumulated and fed back into the next prompt.
4.  On FINAL_ANSWER, the agent additionally:
      a. Draws a rectangle on Excalidraw (via Playwright browser automation)
      b. Sends a summary email through Gmail
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| MCP Framework | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`mcp[cli]`) |
| LLM | Google Gemini 2.0 Flash (via `google-genai`) |
| Browser Automation | Playwright |
| Windows Automation | pywinauto, win32gui |
| Email | Gmail API (`google-api-python-client`) |
| Package Manager | uv |

---

## License

This project is for educational purposes as part of the **EAG V2 - Session 4** coursework.
