"""
ETL Pipeline Runner
"""

import argparse
from pathlib import Path

from etl.config import DEFAULT_XML_PATH, DASHBOARD_JSON_PATH


def run_etl_pipeline(xml_path: Path = DEFAULT_XML_PATH):
    """
    Run the complete ETL pipeline
    
    Args:
        xml_path: Path to input XML file
    """
    print("Starting ETL Pipeline...")
    
    # TODO: Implement pipeline steps:
    # 1. Parse XML
    # 2. Clean and normalize
    # 3. Categorize
    # 4. Load to database
    # 5. Generate dashboard JSON
    
    print("ETL Pipeline completed!")


def main():
    """
    Main CLI entry point
    """
    parser = argparse.ArgumentParser(description='Run MoMo SMS ETL Pipeline')
    parser.add_argument(
        '--xml',
        type=str,
        default=str(DEFAULT_XML_PATH),
        help='Path to XML input file'
    )
    
    args = parser.parse_args()
    xml_path = Path(args.xml)
    run_etl_pipeline(xml_path)


if __name__ == '__main__':
    main()
