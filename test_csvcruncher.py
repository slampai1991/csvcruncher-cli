import pytest
import csvcruncher

# Sample data for tests
data = [
    {"id": "1", "name": "A", "price": "10.5", "qty": "2"},
    {"id": "2", "name": "B", "price": "20.0", "qty": "5"},
    {"id": "3", "name": "C", "price": "15.0", "qty": "1"},
    {"id": "4", "name": "A", "price": "5.0", "qty": "10"},
]

def test_filter_by_lt():
    result = csvcruncher.filter_by(data, "price<15")
    assert len(result) == 2
    assert all(float(row["price"]) < 15 for row in result)

def test_filter_by_gt():
    result = csvcruncher.filter_by(data, "qty>2")
    assert len(result) == 2
    assert all(int(row["qty"]) > 2 for row in result)

def test_filter_by_eq():
    result = csvcruncher.filter_by(data, "name=A")
    assert len(result) == 2
    assert all(row["name"] == "A" for row in result)

def test_aggregate_avg():
    result = csvcruncher.aggregate(data, "price", "avg")
    assert result is not None
    assert result["avg"] == round((10.5+20.0+15.0+5.0)/4, 2)

def test_aggregate_min():
    result = csvcruncher.aggregate(data, "qty", "min")
    assert result is not None
    assert result["min"] == 1.0

def test_aggregate_max():
    result = csvcruncher.aggregate(data, "qty", "max")
    assert result is not None
    assert result["max"] == 10.0

def test_aggregate_invalid_column():
    result = csvcruncher.aggregate(data, "notacol", "avg")
    assert result is None

def test_aggregate_invalid_op():
    result = csvcruncher.aggregate(data, "qty", "sum")
    assert result is None

def test_sort_by_asc():
    result = csvcruncher.sort_by(data, "price=asc")
    prices = [float(row["price"]) for row in result]
    assert prices == sorted(prices)

def test_sort_by_desc():
    result = csvcruncher.sort_by(data, "qty=desc")
    qtys = [int(row["qty"]) for row in result]
    assert qtys == sorted(qtys, reverse=True)

def test_csv_reader(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("id,name,price,qty\n1,A,10.5,2\n2,B,20.0,5\n")
    result = csvcruncher.csv_reader(str(file))
    assert isinstance(result, list)
    assert result[0]["name"] == "A"
    assert result[1]["price"] == "20.0"
