# MP1: Command-Line Data Pipeline

DS 3500 — Jake Lawler

## Overview

This project is a command-line data pipeline that loads a data file, validates it,
cleans it, and saves the result as a CSV. Data moves through four stages in order:
it is **loaded** from disk, **validated** against the expected columns and types,
**processed** to remove duplicates, missing values, and outliers, and finally
**saved** to an output path. Every cleaning decision is driven by `config/config.yaml`
rather than hard-coded, so the same pipeline can be pointed at a different dataset
by editing the config instead of the code. `pipeline.py` sits at the top level and
coordinates the stages, while the reusable modules live in `src/`. Each module logs
its own activity under its module name, so the output shows which stage produced
each message.

## Project Structure

| File | Responsibility |
| --- | --- |
| `pipeline.py` | Parses command-line arguments and runs the four stages in order |
| `src/utils.py` | Configures logging and checks that input paths exist |
| `src/data_loaders.py` | Reads CSV, JSON, and YAML files based on file extension |
| `src/data_validator.py` | Checks required columns exist and drops rows with non-numeric values |
| `src/data_processor.py` | Removes duplicates, missing values, and outliers per the config |
| `src/data_output.py` | Creates the output directory and writes the cleaned CSV |
| `config/config.yaml` | Controls which columns are validated and which cleaning steps run |
| `fixtures/` | Sample data files used for testing |

## Usage

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example Output

```text
12:42:32 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
12:42:32 INFO     src.utils — Input file validated: fixtures/sample_data.csv
12:42:32 INFO     src.utils — Input file validated: config/config.yaml
12:42:32 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
12:42:32 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
12:42:32 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
12:42:32 DEBUG    src.data_validator — Validation: 100 -> 98 rows
12:42:32 INFO     __main__ — Validation complete: 100 -> 98 rows
12:42:32 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
12:42:32 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
12:42:32 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
12:42:32 INFO     __main__ — Processing complete: 98 -> 92 rows
12:42:32 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
12:42:32 INFO     __main__ — Saved cleaned data to output\clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```

Running without `--verbose` shows only the INFO lines and the final report.