
from app.matrix import MatrixValidator


class MatrixInputHandler:
    """
    사용자 입력 처리 객체이다.
    """

    def __init__(self) -> None:
        """
        입력 처리 객체를 초기화한다.
        """
        self.validator = MatrixValidator()

    def parse_matrix_from_lines(
        self,
        lines: list[str],
        expected_size: int,
    ) -> list[list[float]]:
        """
        여러 줄 문자열을 행렬로 변환한다.

        Args:
            lines: 사용자 입력 줄 목록
            expected_size: 기대하는 행렬 크기

        Returns:
            숫자형 행렬

        Raises:
            ValueError: 줄 수나 입력 형식이 잘못된 경우
        """
        if len(lines) != expected_size:
            raise ValueError(
                f"입력 형식 오류: 총 {expected_size}줄을 입력해야 합니다."
            )

        matrix: list[list[float]] = []

        for line in lines:
            parts = line.strip().split()

            if len(parts) != expected_size:
                raise ValueError(
                    f"입력 형식 오류: 각 줄에 {expected_size}개의 숫자를 입력해야 합니다."
                )

            row: list[float] = []

            for part in parts:
                try:
                    row.append(float(part))
                except ValueError as exc:
                    raise ValueError(
                        "입력 형식 오류: 숫자만 입력할 수 있습니다."
                    ) from exc

            matrix.append(row)

        return self.validator.validate_square_matrix(matrix)

    def prompt_matrix(self, name: str, size: int) -> list[list[float]]:
        """
        사용자에게 행렬 입력을 받아 반환한다.

        Args:
            name: 입력 안내용 이름
            size: 기대하는 행렬 크기

        Returns:
            검증된 행렬
        """
        while True:
            print(f"\n{name} ({size}줄 입력, 공백 구분)")
            lines: list[str] = []

            for _ in range(size):
                lines.append(input().rstrip())

            try:
                return self.parse_matrix_from_lines(lines, size)
            except ValueError as exc:
                print(exc)
                print("다시 입력해주세요.")