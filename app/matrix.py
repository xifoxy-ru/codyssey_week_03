from typing import Any

from app.constants import Text


class MatrixValidator:
    """
    행렬 검증을 담당하는 객체이다.
    """

    def validate_square_matrix(self, matrix: Any) -> list[list[float]]:
        """
        입력 데이터가 NxN 정사각 행렬인지 검증한다.
        """
        if not isinstance(matrix, list) or not matrix:
            raise ValueError(Text.MATRIX_EMPTY_ERROR)

        size = len(matrix)
        normalized: list[list[float]] = []

        for row in matrix:
            if not isinstance(row, list):
                raise ValueError(Text.MATRIX_ROW_TYPE_ERROR)

            if len(row) != size:
                raise ValueError(Text.MATRIX_SQUARE_ERROR)

            converted_row: list[float] = []

            for value in row:
                try:
                    converted_row.append(float(value))
                except (TypeError, ValueError) as exc:
                    raise ValueError(Text.MATRIX_NUMBER_ERROR) from exc

            normalized.append(converted_row)

        return normalized
