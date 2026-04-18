from typing import Any


class MatrixValidator:
    """
    행렬 검증을 담당하는 객체이다.
    """

    def validate_square_matrix(self, matrix: Any) -> list[list[float]]:
        """
        입력 데이터가 NxN 정사각 행렬인지 검증한다.

        Args:
            matrix: 검증할 입력 데이터

        Returns:
            숫자형 NxN 행렬

        Raises:
            ValueError: 형식이 잘못된 경우
        """
        if not isinstance(matrix, list) or not matrix:
            raise ValueError("행렬은 비어 있지 않은 2차원 리스트여야 합니다.")

        size = len(matrix)
        normalized: list[list[float]] = []

        for row in matrix:
            if not isinstance(row, list):
                raise ValueError("행렬의 각 행은 리스트여야 합니다.")

            if len(row) != size:
                raise ValueError("NxN 정사각 행렬이어야 합니다.")

            converted_row: list[float] = []

            for value in row:
                try:
                    converted_row.append(float(value))
                except (TypeError, ValueError) as exc:
                    raise ValueError("행렬에는 숫자만 포함되어야 합니다.") from exc

            normalized.append(converted_row)

        return normalized
