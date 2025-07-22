import numpy as np
import pandas as pd
import os
from datetime import datetime
import json

# Local processor instead of HTTP call
def simulate_numpy_processing(payload: dict) -> str:
    try:
        print("🔍 Simulating NumPy processing...")
        # Use dummy data for simulation
        columns = payload.get("columns", [])
        rows = 10  # simulate 10 rows

        # Simulate numeric data if aggregation is present, else strings
        if payload.get("aggregation"):
            data = np.random.randint(10, 100, size=(rows, len(columns)))
        else:
            data = np.array([[f"{col}_{i}" for col in columns] for i in range(rows)])

        # Define filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestamp}.csv"
        filepath = os.path.join("output", filename)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        # Save as CSV
        np.savetxt(filepath, data, delimiter=",", fmt="%s", header=",".join(columns), comments="")

        return f"✅ Data saved locally at: {filepath}"
    except Exception as e:
        return f"❌ Error saving data: {e}"

def process_payload(payload: dict) -> str:
    """Process the JSON payload to extract data from a DataFrame and save it locally."""
    # logger.debug(f"Processing payload: {payload}")
    try:
        # Sample DataFrame (replace with your own data source, e.g., CSV file)
        data = {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 35, 30, 40, 28],
            "department": ["AI", "HR", "AI", "AI", "Finance"],
            "salary": [60000, 50000, 65000, 70000, 55000],
            "city": ["New York", "London", "New York", "Paris", "London"]
        }
        df = pd.DataFrame(data)
        # logger.debug(f"Initial DataFrame:\n{df}")
        # Alternatively, load from a CSV file:
        # df = pd.read_csv("data.csv")

        # Select columns
        if not payload.get("columns"):
            # logger.error("No columns specified in payload")
            return "Error: No columns specified in payload"
        df = df[payload["columns"]]
        # logger.debug(f"After selecting columns:\n{df}")

        # Apply WHERE condition
        if payload.get("conditions") and payload["conditions"].get("where"):
            try:
                where_clause = payload["conditions"]["where"]
                # logger.debug(f"Applying WHERE clause: {where_clause}")
                # Safe handling for string conditions
                if "department =" in where_clause:
                    dept_value = where_clause.split("=")[1].strip().strip("'")
                    df = df[df["department"] == dept_value]
                else:
                    df = df.query(where_clause)
                # logger.debug(f"After WHERE clause:\n{df}")
            except Exception as e:
                # logger.error(f"Error applying WHERE condition: {e}")
                return f"Error applying WHERE condition: {e}"

        # Apply GROUP BY and aggregation
        if payload.get("groupby"):
            groupby_cols = payload["groupby"]
            # logger.debug(f"Applying GROUP BY: {groupby_cols}")
            if payload.get("aggregation"):
                agg_func = payload["aggregation"]["function"].lower()
                agg_col = payload["aggregation"]["column"]
                # logger.debug(f"Applying aggregation: {agg_func} on {agg_col}")
                if agg_func not in ["sum", "count", "avg", "max", "min"]:
                    # logger.error(f"Unsupported aggregation function: {agg_func}")
                    return f"Error: Unsupported aggregation function {agg_func}"
                agg_map = {
                    "sum": np.sum,
                    "count": "count",
                    "avg": np.mean,
                    "max": np.max,
                    "min": np.min
                }
                agg_pandas = agg_map.get(agg_func)
                if not agg_pandas:
                    # logger.error(f"Invalid aggregation function: {agg_func}")
                    return f"Error: Invalid aggregation function {agg_func}"
                df = df.groupby(groupby_cols).agg({agg_col: agg_pandas}).reset_index()
                # logger.debug(f"After GROUP BY and aggregation:\n{df}")
            else:
                df = df.groupby(groupby_cols).first().reset_index()
                # logger.debug(f"After GROUP BY (no aggregation):\n{df}")

        # Apply sorting
        if payload.get("sorting"):
            sort_cols = [s["column"] for s in payload["sorting"]]
            sort_ascending = [s["direction"].lower() == "asc" for s in payload["sorting"]]
            # logger.debug(f"Applying sorting: columns={sort_cols}, ascending={sort_ascending}")
            df = df.sort_values(by=sort_cols, ascending=sort_ascending)
            # logger.debug(f"After sorting:\n{df}")

        # Save the result to a local CSV file
        output_file = "output.csv"
        df.to_csv(output_file, index=False)
        # logger.debug(f"Saved result to {output_file}")

        # Convert result to JSON
        result = df.to_dict(orient="records")
        # logger.debug(f"Final result: {result}")
        return json.dumps({"data": result, "saved_to": output_file})

    except Exception as e:
        # logger.error(f"Error processing payload: {e}")
        return f"Error processing payload: {e}"


