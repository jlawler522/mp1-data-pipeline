"""
Data Processing Pipeline
DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load, validate, clean, and save data from the command line."
    )
    parser.add_argument("-i", "--input", required=True,
                        help="Path to the input file")
    parser.add_argument("-o", "--output", required=True,
                        help="Path to the output file")
    parser.add_argument("--config", required=True,
                        help="Path to the YAML configuration file")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config,
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    validation = config["validation"]
    required_columns = validation["required_columns"]
    numeric_columns = validation["numeric_columns"]

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)

    logger.info(
        "Validation complete: %d -> %d rows",
        rows_before_validation, len(data),
    )

    original = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, data)
    logger.info(
        "Processing complete: %d -> %d rows",
        report["rows_before"], report["rows_after"],
    )

    output_path = save_data(data, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    print("Cleaning report:")
    print(report)


if __name__ == "__main__":
    main()