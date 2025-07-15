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
    match = re.match(r"^([a-z]+)(>|<|=)(.+)$", condition)
    (column, operator, value) = match.groups()
    return (column, operator, value)
def apply_filter(data: list, condition:str) -> list:
    """
    apply filter on data based on given condition
    """
    column, operator, value = parse_condition(condition)
    filtered_data=[]
    for row in data:
        try:
            cell_value = float(row[column]) #numerical condition
            condition_value=float(value)
        except:
            cell_value=str(row[column])     #string condition
            condition_value=str(value)

        if operator == "=" and cell_value == condition_value:
            filtered_data.append(row)
        elif operator == ">" and cell_value > condition_value:
            filtered_data.append(row)
        elif operator == "<" and cell_value < condition_value:
            filtered_data.append(row)
    return filtered_data

def compute_aggregate(data:list, column:str, operation:str) -> float:
    """
    compute aggregate on data based on given column and operation
    """
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

    if condition:
        filtered_data = apply_filter(data, condition)
    else:
        filtered_data = data

    if aggregate:
        column, operation = aggregate.split("=")
        result = compute_aggregate(filtered_data, column, operation)
        return(tabulate([[result]], headers=[operation], tablefmt="fancy_grid"))
    else:
        table_data = [[row[column]for column in headers] for row in filtered_data]
        return(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True) #for file name
    parser.add_argument("--where", type=str, default=None) #for filtering of data
    parser.add_argument("--aggregate", type=str, default=None) #for aggregation of data
    args = parser.parse_args()

    result = process_csv(args.file, args.where, args.aggregate)
    print(result)

if __name__ == '__main__':
    main()