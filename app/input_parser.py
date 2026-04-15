from app.matrix import MatrixValidator


class MatrixInputHandler:
    """
    사용자 입력 처리 스켈레톤 코드
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
        pass

    def prompt_matrix(self, name: str, size: int) -> list[list[float]]:
        """
        사용자에게 행렬 입력을 받아 반환한다.

        Args:
            name: 입력 안내용 이름
            size: 기대하는 행렬 크기

        Returns:
            검증된 행렬
        """
        pass
