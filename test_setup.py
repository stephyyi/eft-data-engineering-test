#!/usr/bin/env python3
"""
Test script to verify all dependencies are working correctly.
"""


def test_core_dependencies():
    """Test core data processing dependencies."""
    try:
        import pandas as pd
        import numpy as np
        import sqlalchemy
        import pymysql
        print("✅ Core dependencies working:")
        print(f"  - pandas: {pd.__version__}")
        print(f"  - numpy: {np.__version__}")
        print(f"  - sqlalchemy: {sqlalchemy.__version__}")
        print(f"  - pymysql: {pymysql.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Core dependency error: {e}")
        return False


def test_transform_module():
    """Test the custom transform module."""
    try:
        from src.transform import validate_and_clean, aggregate_daily_by_bank
        print("✅ Transform module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Transform module error: {e}")
        return False

def test_mysql_connection():
    """Test MySQL database connection."""
    try:
        import sqlalchemy
        engine = sqlalchemy.create_engine("mysql+pymysql://root@localhost/analytics")
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1 as test"))
            print("✅ MySQL connection successful")
        return True
    except Exception as e:
        print(f"❌ MySQL connection error: {e}")
        return False


def test_sample_data():
    """Test loading sample data."""
    try:
        import pandas as pd
        df = pd.read_csv("data/sample_transactions.csv", parse_dates=["timestamp"])
        print(f"✅ Sample data loaded: {len(df)} transactions")
        return True
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing EFT Data Engineering Project Setup...")
    print("=" * 50)

    tests = [
        test_core_dependencies,
        test_transform_module,
        test_mysql_connection,
        test_sample_data,
    ]

    results = []
    for test in tests:
        results.append(test())
        print()

    success_count = sum(results)
    total_count = len(results)

    print(f"Test Results: {success_count}/{total_count} passed")

    if success_count == total_count:
        print("🎉 All dependencies are working correctly!")
        print("\nYou can now run:")
        print("  - Transform data: python src/transform.py --in data/sample_transactions.csv --out output.csv")
        print("  - Run SQL queries against MySQL analytics database")
    else:
        print("⚠️  Some dependencies need attention")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())