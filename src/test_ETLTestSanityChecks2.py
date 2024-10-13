import pytest
import pandas as pd
import functools


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"File not found: {args[0]}")
        except pd.errors.EmptyDataError:
            print(f"File is empty: {args[0]}")
        except AssertionError as ae:
            print(f"Assertion failed: {ae}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return wrapper


# Fixture to provide the CSV file path
@pytest.fixture
def csv_file_path():
    # Replace with your actual file path
    return './data/in/decadal-deaths-disasters-type.csv'


@handle_exceptions
def test_check_duplicates(csv_file_path):
    df = pd.read_csv(csv_file_path)
    assert not df.empty, "The CSV file is empty."
    duplicates = df[df.duplicated()]
    assert duplicates.empty, f"Found {len(duplicates)} duplicate rows."
    print("No duplicate rows found.")


@handle_exceptions
@pytest.mark.parametrize("column_name", [None, 'Year', 'Code'])
def test_check_null_values(csv_file_path, column_name):
    df = pd.read_csv(csv_file_path)
    if column_name is None:
        null_values = df.isnull().sum()
        null_columns = null_values[null_values > 0]
        assert null_columns.empty, f"Columns with null values: {
            null_columns.to_dict()}"
        print("No null values found in any columns.")
    else:
        assert column_name in df.columns, f"Column '{
            column_name}' does not exist in the CSV."
        null_count = df[column_name].isnull().sum()
        assert null_count == 0, f"Found {
            null_count} null values in column '{column_name}'."
        print(f"No null values found in column '{column_name}'.")


@handle_exceptions
@pytest.mark.parametrize("column_name", ['Year', 'Code'])
def test_check_unique_column(csv_file_path, column_name):
    df = pd.read_csv(csv_file_path)
    assert column_name in df.columns, f"Column '{
        column_name}' does not exist in the CSV."
    unique_count = df[column_name].nunique()
    total_count = len(df[column_name])
    assert unique_count == total_count, f"Column '{
        column_name}' contains duplicate values."
    print(f"All values in column '{column_name}' are unique.")
