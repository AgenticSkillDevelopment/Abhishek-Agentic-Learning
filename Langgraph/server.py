# # import os
# # import json
# # import httpx
# # from mcp.server.fastmcp import FastMCP

# # mcp = FastMCP(name="currency_checker", host="0.0.0.0", port=8010)

# # API_HOST = "http://localhost:8000/check_for_datasets/"
# # API_HOST_2 = "http://localhost:8000/last_update_id/"

# # @mcp.tool()
# # async def check_for_datasets() -> str:
# #     """Check dataset availability via API."""
# #     try:
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(API_HOST)
# #             response.raise_for_status()
# #             result = response.json()
# #         return json.dumps(result)
# #     except Exception as e:
# #         return f"⚠️ Error fetching datasets: {e}"

# # @mcp.tool()
# # async def check_last_update_id() -> str:
# #     """Fetch last update ID via API."""
# #     try:
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(API_HOST_2)
# #             response.raise_for_status()
# #             result = response.json()
# #         return json.dumps(result)
# #     except Exception as e:
# #         return f"⚠️ Error fetching last update ID: {e}"

# # if __name__ == "__main__":
# #     mcp.run(transport="streamable-http")
# import os
# import json
# import re
# import httpx
# from mcp.server.fastmcp import FastMCP
# import aiohttp
# from langchain.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq  # Or use your preferred LLM
# from dotenv import load_dotenv
# from Payload import *
# import numpy as np
# import pandas as pd
# import os
# from datetime import datetime
# import json
# import logging
# import asyncio
# # Ensure environment variables are loaded
# load_dotenv()
# groq_api_key = os.getenv("GROQ_API_KEY")

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# # Set LLM
# llm = ChatGroq(model="qwen/qwen3-32b", api_key=groq_api_key, temperature=0)

# # Prompt template to convert SQL query + columns into a structured payload
# parse_prompt = ChatPromptTemplate.from_template("""
# Given the available columns: {columns_json}
# And the query: "{query}"

# Generate a JSON payload with the following keys:
# - columns: list of selected columns
# - conditions: {{"where": ..., "on": ...}} (use null if not present)
# - groupby: list of columns for grouping
# - aggregation: optional dict like {{"function": "sum", "column": "salary"}}
# - sorting: list of dicts like [{{"column": "age", "direction": "desc"}}]

# Only return valid JSON. Do not include any explanation.
# """)

# # Create MCP server
# mcp = FastMCP(name="currency_checker", host="0.0.0.0", port=8010)

# # Update this to match your actual backend API URL
# API_HOST = "http://192.168.1.163:8000/check_for_datasets/"
# API_HOST_2 = "http://192.168.1.163:8000/last_update_id/"
# API_HOST_DATA = "http://192.168.1.163:8000/query_data/"

# # @mcp.tool()
# # async def check_for_datasets() -> str:
# #     """Checks for datasets using external API."""
# #     try:
# #         print("API_HOSTlknfjknndfglndfglgk")
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(API_HOST)
# #             print(response)
# #             response.raise_for_status()
# #             result = response.json()
# #         if "error" in result:
# #             return f"❌ API Error: {result['error']}"
# #         return json.dumps(result)
# #     except Exception as e:
# #         return f"⚠️ Failed to assess currencies: {e}"

# # @mcp.tool()
# # async def check_last_update_id() -> str:
# #     """Checks for last updated id using external API."""
# #     print("🚀 check_last_update_id tool invoked")
# #     try:
# #         print("📡 About to call external API:", API_HOST_2)
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(API_HOST_2)
# #             print(f"📥 Response received: {response.status_code}")
# #             response.raise_for_status()
# #             result = response.json()
# #             print(f"✅ Parsed result: {result}")
# #         if "error" in result:
# #             return f"❌ API Error: {result['error']}"
# #         return str(result)
# #     except Exception as e:
# #         print(f"❌ Exception in tool: {e}")
# #         return f"⚠️ Failed to assess currencies: {e}"

# # @mcp.tool()
# # async def get_data_with_llm(columns_json: str, query: str) -> str:
# #     """
# #     Fetch for data on input type query

# #     args:
# #         query: normal string
# #     """
# #     print("mnxcbjkbbjkzbnxcjkz km,nnnnn  ............................")
# #     try:
# #         # Parse the columns JSON
# #         try:
# #             columns_json = ""
# #             columns_data = json.loads(columns_json)
# #             print(f'{columns_data=}')
# #             valid_columns = columns_data.get("columns", [])
# #             print(f'{valid_columns=}')
# #             if not valid_columns:
# #                 return "⚠️ Error: No columns provided in columns_json"
# #         except json.JSONDecodeError:
# #             return "⚠️ Error: Invalid columns_json format"

# #         # Parse the SQL-like query
# #         payload = {
# #             "columns": [],
# #             "conditions": {"where": None, "on": None},
# #             "groupby": [],
# #             "aggregation": None,
# #             "sorting": []
# #         }

# #         # Regular expressions to parse query components
# #         select_pattern = r"select\s+(.+?)(?:\s+where|\s+group by|\s+order by|$)"
# #         where_pattern = r"where\s+(.+?)(?:\s+group by|\s+order by|$)"
# #         groupby_pattern = r"group by\s+(.+?)(?:\s+order by|$)"
# #         orderby_pattern = r"order by\s+(.+)$"
# #         agg_pattern = r"(sum|count|avg|max|min)\((.+?)\)"

# #         # Extract SELECT columns
# #         select_match = re.search(select_pattern, query.lower(), re.IGNORECASE)
# #         if select_match:
# #             columns = [col.strip() for col in select_match.group(1).split(",")]
# #             # Validate columns against columns_json
# #             payload["columns"] = [col for col in columns if col in valid_columns]
# #             if not payload["columns"]:
# #                 return "⚠️ Error: No valid columns in query"

# #         # Extract WHERE conditions
# #         where_match = re.search(where_pattern, query.lower(), re.IGNORECASE)
# #         if where_match:
# #             payload["conditions"]["where"] = where_match.group(1).strip()

# #         # Extract GROUP BY
# #         groupby_match = re.search(groupby_pattern, query.lower(), re.IGNORECASE)
# #         if groupby_match:
# #             payload["groupby"] = [col.strip() for col in groupby_match.group(1).split(",") if col.strip() in valid_columns]

# #         # Extract ORDER BY
# #         orderby_match = re.search(orderby_pattern, query.lower(), re.IGNORECASE)
# #         if orderby_match:
# #             sort_items = orderby_match.group(1).split(",")
# #             for item in sort_items:
# #                 parts = item.strip().split()
# #                 if len(parts) >= 1 and parts[0] in valid_columns:
# #                     direction = parts[1].lower() if len(parts) > 1 and parts[1].lower() in ["asc", "desc"] else "asc"
# #                     payload["sorting"].append({"column": parts[0], "direction": direction})

# #         # Extract aggregation functions
# #         agg_match = re.search(agg_pattern, query.lower(), re.IGNORECASE)
# #         if agg_match:
# #             payload["aggregation"] = {"function": agg_match.group(1), "column": agg_match.group(2)}

# #         # Send payload to API
# #         # async with httpx.AsyncClient() as client:
# #         #     response = await client.post(API_HOST_DATA, json=payload)
# #         #     response.raise_for_status()
# #         #     result = response.json()
# #         result = process_payload(payload)
# #         return json.dumps({"data": result})
        
# #     except Exception as e:
# #         return f"⚠️ Failed to process query: {e}"



# # @mcp.tool()
# # async def get_data_with_llm(columns_json: str, query: str) -> str:
# #     """Process an SQL-like query using an LLM to generate a JSON payload and send it to the data API."""
# #     try:
# #         # Step 1: Parse and validate columns_json
# #         print("tool called..................")
# #         try:

# #             columns_data = json.loads(columns_json)
# #             valid_columns = columns_data.get("columns", [])
# #             if not valid_columns:
# #                 return "❌ Error: No columns provided in columns_json"
# #         except json.JSONDecodeError:
# #             return "❌ Error: Invalid columns_json format"

# #         # Step 2: Use LLM to generate JSON payload
# #         chain = parse_prompt | llm
# #         response = await chain.ainvoke({"columns_json": columns_json, "query": query})

# #         try:
# #             payload = json.loads(response.content)
# #         except json.JSONDecodeError:
# #             return "❌ Error: LLM returned invalid JSON"

# #         # Step 3: Validate columns in payload
# #         if "columns" in payload:
# #             payload["columns"] = [col for col in payload["columns"] if col in valid_columns]
# #             if not payload["columns"]:
# #                 return "❌ Error: No valid columns in query"

# #         # Step 4: POST payload to external API
# #         result = process_payload(payload)
# #         return result
# #     except Exception as e:
# #         return f" Failed to process query: {e}"


# # @mcp.tool()
# # async def get_data_with_llm(columns_json: str, query: str) -> str:
# #     """Process an SQL-like query using an LLM to generate a JSON payload and process it locally."""
# #     # logger.debug(f"get_data_with_llm called with columns_json: {columns_json}, query: {query}")
# #     print("tool called..................")
# #     async def attempt_llm_call(attempts=3, base_delay=1):
# #         for attempt in range(attempts):
# #             try:
# #                 chain = parse_prompt | llm
# #                 response = await chain.ainvoke({"columns_json": columns_json, "query": query})
# #                 # logger.debug(f"LLM response: {response.content}")
# #                 try:
# #                     payload = json.loads(response.content)
# #                     # logger.debug(f"Parsed payload: {payload}")
# #                 except json.JSONDecodeError:
# #                     # logger.error("LLM returned invalid JSON")
# #                     return " Error: LLM returned invalid JSON"
# #                 return payload
# #             except Exception as e:
# #                 if "Rate limit reached" in str(e):
# #                     retry_after = float(str(e).split("Please try again in ")[1].split("s")[0]) if "Please try again in" in str(e) else base_delay * (2 ** attempt)
# #                     # logger.warning(f"Rate limit hit, retrying after {retry_after}s (attempt {attempt + 1}/{attempts})")
# #                     await asyncio.sleep(retry_after)
# #                 else:
# #                     # logger.error(f"LLM error: {e}")
# #                     return f" Error: LLM call failed: {e}"
# #         # logger.error("Max retry attempts reached")
# #         return " Error: Max retry attempts reached for LLM call"

# #     try:
# #         # Validate columns_json
# #         try:
# #             columns_data = json.loads(columns_json)
# #             valid_columns = columns_data.get("columns", [])
# #             if not valid_columns:
# #                 # logger.error("No columns provided in columns_json")
# #                 return " Error: No columns provided in columns_json"
# #         except json.JSONDecodeError:
# #             # logger.error("Invalid columns_json format")
# #             return " Error: Invalid columns_json format"

# #         # Get payload from LLM with retry logic
# #         result = await attempt_llm_call()
# #         if isinstance(result, str) and result.startswith(" Error"):
# #             return result
# #         payload = result

# #         # Validate columns in payload
# #         if payload.get("columns"):
# #             payload["columns"] = [col for col in payload["columns"] if col in valid_columns]
# #             if not payload["columns"]:
# #                 # logger.error("No valid columns in query")
# #                 return " Error: No valid columns in query"
# #         # logger.debug(f"Validated columns: {payload['columns']}")

# #         # Process payload locally
# #         result = process_payload(payload)
# #         # logger.debug(f"Process payload result: {result}")
# #         return result

# #     except Exception as e:
# #         # logger.error(f"Failed to process query: {e}")
# #         return f" Failed to process query: {e}"




    

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")

import os
import json
import httpx
import numpy as np
import pandas as pd

from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="currency_checker", port=8010)
OUTPUT_DIR = "output_dataframes"
OUTPUT_DIR_ABS = os.path.abspath(OUTPUT_DIR)  
DATA_FILE = os.path.abspath("data.csv")
# Update this to match your actual backend API URL
API_HOST = "http://0.0.0.0:8000/check_for_datasets/"
API_HOST_2 = "http://0.0.0.0:8000/last_update_id/"

@mcp.tool()
async def check_for_datasets() -> str:
    """Checks for datasets using external API."""
    try:
        print("API_HOST")
        async with httpx.AsyncClient() as client:
            response = await client.get(API_HOST)
            print(response)
            response.raise_for_status()
            result = response.json()
        if "error" in result:
            return f"❌ API Error: {result['error']}"
        return json.dumps(result)
    except Exception as e:
        return f"⚠️ Failed to assess currencies: {e}"

@mcp.tool()
async def check_last_update_id() -> str:
    """Checks for last updated id using external API."""
    try:
        print("API_HOST")
        async with httpx.AsyncClient() as client:
            response = await client.get(API_HOST_2)
            print(response)
            response.raise_for_status()
            result = response.json()
            print(f"result: {result}")
        if "error" in result:
            return f"❌ API Error: {result['error']}"
        return str(result)
    except Exception as e:
        return f"⚠️ Failed to assess currencies: {e}"

@mcp.tool()
async def get_data(columns: str, query: str) -> str:
    """Processes SQL-like query to create and save a DataFrame locally based on columns and query conditions."""
    try:
        # Parse the input query to extract components
        
        payload = await create_payload(columns, query)
        
        # Process the payload and create DataFrame
        result = process_query(payload)
        
        # Save the DataFrame locally
    
        output_path = f"output_dataframe_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output_path = os.path.join(OUTPUT_DIR_ABS, output_path)
        result.to_csv(output_path, index=False)
        
        return f"✅ DataFrame created and saved to {output_path}"
    except Exception as e:
        return f"⚠️ Failed to process query: {str(e)}"

async def create_payload(columns: str, query: str) -> dict:
    """Creates a JSON payload from columns and SQL-like query."""
    try:
        # Split columns into a list
        column_list = [col.strip() for col in columns.split(',')]
        
        # Initialize payload structure
        payload = {
            "columns": column_list,
            "conditions": [],
            "groupby": [],
            "aggregation": {},
            "sorting": []
        }
        
        # Parse query (simplified parsing for demonstration)
        query = query.lower()
        
        # Extract WHERE conditions
        if "where" in query:
            where_clause = query.split("where")[1].split("group by")[0] if "group by" in query else query.split("where")[1]
            conditions = where_clause.split("and")
            payload["conditions"] = [cond.strip() for cond in conditions]
        
        # Extract GROUP BY
        if "group by" in query:
            groupby_clause = query.split("group by")[1].split("order by")[0] if "order by" in query else query.split("group by")[1]
            payload["groupby"] = [col.strip() for col in groupby_clause.split(",")]
        
        # Extract ORDER BY (sorting)
        if "order by" in query:
            orderby_clause = query.split("order by")[1]
            sort_items = orderby_clause.split(",")
            for item in sort_items:
                parts = item.strip().split()
                col = parts[0]
                direction = parts[1].upper() if len(parts) > 1 else "ASC"
                payload["sorting"].append({"column": col, "direction": direction})
        
        # Extract aggregation functions (e.g., COUNT, SUM, AVG)
        if any(agg in query for agg in ["count(", "sum(", "avg("]):
            for agg in ["count", "sum", "avg"]:
                if f"{agg}(" in query:
                    agg_start = query.index(f"{agg}(")
                    agg_end = query.index(")", agg_start)
                    col = query[agg_start + len(agg) + 1:agg_end].strip()
                    payload["aggregation"][col] = agg.upper()
        
        return payload
    except Exception as e:
        raise Exception(f"Failed to create payload: {str(e)}")
     
def process_query(payload: dict) -> pd.DataFrame:
    """Processes the payload to create a DataFrame using NumPy and pandas."""
    try:
        # Simulate data for demonstration (replace with actual data source)
        # For example, assume we have some sample data
        # data = {
        #     "id": np.array([1, 2, 3, 4, 5]),
        #     "value": np.array([10, 20, 30, 40, 50]),
        #     "category": np.array(["A", "B", "A", "B", "A"]),
        #     "date": np.array(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"])
        # }
        # with open("data.json", "r") as f:
        #     data= json.load(f)
        # df = pd.DataFrame(data)   
        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError(f"Data file not found at {DATA_FILE}")
        df = pd.read_csv(DATA_FILE)
        print(f'{df.head(10)=}')
        
        
        
        # base_dir = os.path.dirname(__file__)  # Gets the directory of the current script
        # csv_path = os.path.join(base_dir, "data.csv")
        # df=pd.DataFrame(csv_path)
        
        
        
        # Select specified columns
        selected_columns = [col for col in payload["columns"] if col in df.columns]
        if not selected_columns:
            raise ValueError("No valid columns selected")
        df = df[selected_columns]
        
        # Apply WHERE conditions
        for condition in payload["conditions"]:
            # Simple condition parsing (e.g., "value > 20")
            if ">=" in condition:
                col, val = condition.split(">=")
                df = df[df[col.strip()] >= float(val.strip())]
            elif "<=" in condition:
                col, val = condition.split("<=")
                df = df[df[col.strip()] <= float(val.strip())]
            elif "=" in condition:
                col, val = condition.split("=")
                df = df[df[col.strip()] == val.strip().strip("'")]
            elif ">" in condition:
                col, val = condition.split(">")
                df = df[df[col.strip()] > float(val.strip())]
            elif "<" in condition:
                col, val = condition.split("<")
                df = df[df[col.strip()] < float(val.strip())]
        
        # Apply GROUP BY and aggregations
        if payload["groupby"]:
            agg_funcs = {}
            for col, agg in payload["aggregation"].items():
                if agg == "COUNT":
                    agg_funcs[col] = "count"
                elif agg == "SUM":
                    agg_funcs[col] = "sum"
                elif agg == "AVG":
                    agg_funcs[col] = "mean"
            if agg_funcs:
                df = df.groupby(payload["groupby"]).agg(agg_funcs).reset_index()
        
        # Apply sorting
        for sort in payload["sorting"]:
            df = df.sort_values(by=sort["column"], ascending=(sort["direction"] == "ASC"))
        
        return df
    except Exception as e:
        raise Exception(f"Failed to process query: {str(e)}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")