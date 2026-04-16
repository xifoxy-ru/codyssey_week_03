from app.matrix import MatrixValidator


class MacCalculator:
    """
    MAC 연산을 담당하는 객체이다.
    """

    def __init__(self) -> None:
        """
        MAC 계산기를 초기화한다.
        """
        self.validator = MatrixValidator()

    def mac(
        self,
        matrix_a: list[list[float]],
        matrix_b: list[list[float]],
    ) -> float:
        """
        두 NxN 행렬에 대해 MAC 연산을 수행한다.

        Args:
            matrix_a: 첫 번째 행렬
            matrix_b: 두 번째 행렬

        Returns:
            MAC 점수

        Raises:
            ValueError: 두 행렬 크기가 맞지 않는 경우
        """
        normalized_a = self.validator.validate_square_matrix(matrix_a)
        normalized_b = self.validator.validate_square_matrix(matrix_b)

        if len(normalized_a) != len(normalized_b):
            raise ValueError("두 행렬의 크기가 다릅니다.")

        size = len(normalized_a)
        total = 0.0

        for row in range(size):
            for col in range(size):
                total += normalized_a[row][col] * normalized_b[row][col]

        return total
