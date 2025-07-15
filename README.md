# Procesing CSV

This is a simple script to process CSV files and perform filtering and aggregation operations on the data.

## Usage

Expecting a valid data
Aggregate expected to be either `avg`, `max`, `min`
Filter conditions expected to come after `--where`, can be numerical or string conditions

```bash
python main.py --file <file_path> --where <condition> --aggregate <column>=<operation>
```

## Example

### 0

```bash
python main.py --file products.csv
```

![Output](<Screenshot 2025-07-15 at 13.08.29.png>)

### 1

```bash
python main.py --file products.csv --where 'brand=xiaomi'
```

![Output](<Screenshot 2025-07-15 at 12.59.13.png>)

### 2

```bash
python main.py --file products.csv --where 'price>100' --aggregate 'price=avg'
```

![Output](<Screenshot 2025-07-15 at 12.56.10.png>)

### 3

```bash
python main.py --file products.csv --aggregate 'price=max'
```

![Output](<Screenshot 2025-07-15 at 13.01.08.png>)

## Test coverage

run

```bash
python -m pytest --cov=main
```

![tesr_coverage](<Screenshot 2025-07-15 at 13.02.22.png>)
