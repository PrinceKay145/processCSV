import csv
from tabulate import tabulate
import argparse
import re
# @todo 1. write a script to filter and do aggregate operations on the data
# expecting the condition from terminal
# filter can be for numbers or letters
# aggregation on numbers
# argparse and csv can be used 
# tabulate can be used for a better output

def parse_condition(condition: str) -> tuple:
    """
    split into column, operator and value using regex
    """
    match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)(>|<|=)(.+)$", condition)

    # validate condition (expecting valid inputs)
    if not match:
        raise ValueError(f"Invalid condition format:{condition}. Expected format: column=value, column>value, or column<value ")
    (column, operator, value) = match.groups()
    return (column, operator, value)
def apply_filter(data: list, condition:str, headers:list) -> list:
    """
    apply filter on data based on given condition
    """
    column, operator, value = parse_condition(condition)

    #validate column exists (expecting valid inputs)
    if column not in headers:
        raise ValueError(f"Column {column} not found in CSV. Available columnds: {', '.join(headers)}")
    filtered_data=[]
    for row in data:
        try:
            cell_value = float(row[column]) #numerical condition
            condition_value=float(value)
        except(ValueError, TypeError):
            cell_value=str(row[column])     #string condition
            condition_value=str(value)

        if operator == "=" and cell_value == condition_value:
            filtered_data.append(row)
        elif operator == ">" and cell_value > condition_value:
            filtered_data.append(row)
        elif operator == "<" and cell_value < condition_value:
            filtered_data.append(row)
    return filtered_data

def compute_aggregate(data:list, column:str, operation:str, headers:list) -> float:
    """
    compute aggregate on data based on given column and operation
    """
    #Although valid inputs are expected 
    #validate column exists 
    if column not in headers:
        raise ValueError(f"Column {column} not found in CSV. Available columnds: {', '.join(headers)}")
    # Validate operation
    if operation not in ["avg", "min", "max"]:
        raise ValueError(f"Invalid operation '{operation}'. Supported operations: avg, min, max")
    
    if not data:
        raise ValueError("No data available for aggregation after filtering")

    if operation == "avg":
        return sum(float(row[column]) for row in data)/len(data)
    elif operation == "max":
        return max(float(row[column]) for row in data)
    elif operation == "min":
        return min(float(row[column]) for row in data)

def process_csv(file_path: str, condition: str = None, aggregate: str = None):
    """
    Main processing function that handles CSV processing
    """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        data = list(reader)

    #Apply filtering if condition is provided
    if condition:
        filtered_data = apply_filter(data, condition, headers)
    else:
        filtered_data = data

    #Apply aggregation if aggregate is provided
    if aggregate:
        column, operation = aggregate.split("=")
        result = compute_aggregate(filtered_data, column, operation, headers)
        return(tabulate([[result]], headers=[operation], tablefmt="fancy_grid"))
    else:
        table_data = [[row[column]for column in headers] for row in filtered_data]
        return(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help='Path to CSV file') #for file name
    parser.add_argument("--where", type=str, default=None, help = 'Filter condition') #for filtering of data
    parser.add_argument("--aggregate", type=str, default=None, help = 'Aggregaton condition ') #for aggregation of data
    args = parser.parse_args()

    result = process_csv(args.file, args.where, args.aggregate)
    print(result)

if __name__ == '__main__':
    main()