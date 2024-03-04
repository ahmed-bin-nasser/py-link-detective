import json

import pytest

from py_link_detective.detective import JsonPrinter


@pytest.fixture
def json_printer(tmp_path):
    file_path = tmp_path / "output.json"
    return JsonPrinter(file_path)

def test_print_method(json_printer, tmp_path):
    # Prepare test data
    data = {1: [1, 2, 3], 2: [4, 5, 6]}
    file_path = tmp_path / "output.json"

    # Call the print method
    json_printer.print("http://example.com", data)

    # Check if the file was created
    assert file_path.exists()

    # Check if the file contains the correct data
    with open(file_path, 'r') as json_file:
        result = json_file.read()
        assert result == json.dumps(data, indent=4)

def test_print_method_with_existing_file(json_printer, tmp_path):
    # Prepare test data
    data = {1: [1, 2, 3], 2: [4, 5, 6, 7, 8]}
    file_path = tmp_path / "output.json"

    # Create an existing file
    with open(file_path, 'w') as json_file:
        json.dump({}, json_file)

    # Call the print method
    json_printer.print("http://example.com", data)

    # Check if the file contains the correct data
    with open(file_path, 'r') as json_file:
        result = json_file.read()
        assert result == json.dumps(data, indent=4)
