from app.constants import Text
from app.matrix import MatrixValidator


class MatrixInputHandler:
    """
    사용자 입력 처리 객체이다.
    """

    def __init__(self) -> None:
        self.validator = MatrixValidator()

    def parse_matrix_from_lines(
        self,
        lines: list[str],
        expected_size: int,
    ) -> list[list[float]]:
        """
        여러 줄 문자열을 행렬로 변환한다.
        """
        if len(lines) != expected_size:
            raise ValueError(Text.INPUT_LINE_COUNT_ERROR.format(size=expected_size))

        matrix: list[list[float]] = []

        for line in lines:
            parts = line.strip().split()

            if len(parts) != expected_size:
                raise ValueError(Text.INPUT_COLUMN_COUNT_ERROR.format(size=expected_size))

            row: list[float] = []

            for part in parts:
                try:
                    row.append(float(part))
                except ValueError as exc:
                    raise ValueError(Text.INPUT_NUMBER_ONLY_ERROR) from exc

            matrix.append(row)

        return self.validator.validate_square_matrix(matrix)

    def prompt_matrix(self, name: str, size: int) -> list[list[float]]:
        """
        사용자에게 행렬 입력을 받아 반환한다.
        """
        while True:
            print(Text.INPUT_MATRIX_PROMPT.format(name=name, size=size))
            lines: list[str] = []

            for _ in range(size):
                lines.append(input().rstrip())

            try:
                return self.parse_matrix_from_lines(lines, size)
            except ValueError as exc:
                print(exc)
                print(Text.INPUT_RETRY)
