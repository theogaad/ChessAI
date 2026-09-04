from src.chess.case import Case
import pytest

@pytest.mark.parametrize("line, column", [(0, 0), (2, 3), (3, 2), (7, 7)])
def test_case_creation(line, column) -> None:
    case = Case(line, column)
    assert case.line == line
    assert case.column == column
    assert case.content is None

@pytest.mark.parametrize("line, column", [(-1, 0), (0, -1), (8, 0), (0, 8)])
def test_case_creation_invalid_position(line, column) -> None:
    with pytest.raises(ValueError):
        Case(line, column)
        