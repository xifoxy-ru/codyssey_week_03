from app.constants import Text
from app.matrix import MatrixValidator


class MacCalculator:
    """
    MAC 연산을 담당하는 객체이다.
    """

    def __init__(self) -> None:
        self.validator = MatrixValidator()

    def mac(
        self,
        matrix_a: list[list[float]],
        matrix_b: list[list[float]],
    ) -> float:
        """
        두 NxN 행렬에 대해 MAC 연산을 수행한다.
        """
        normalized_a = self.validator.validate_square_matrix(matrix_a)
        normalized_b = self.validator.validate_square_matrix(matrix_b)

        if len(normalized_a) != len(normalized_b):
            raise ValueError(Text.MATRIX_SIZE_MISMATCH_ERROR)

        size = len(normalized_a)
        total = 0.0

        for row in range(size):
            for col in range(size):
                total += normalized_a[row][col] * normalized_b[row][col]

        return total
