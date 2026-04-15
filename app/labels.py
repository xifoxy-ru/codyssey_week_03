class LabelNormalizer:
    """
    라벨 정규화를 담당하는 객체 스켈레톤 코드
    """

    def normalize_label(self, label: str) -> str:
        """
        입력 라벨을 내부 표준 라벨로 정규화한다.

        예:
            '+' -> 'Cross'
            'cross' -> 'Cross'
            'x' -> 'X'

        Args:
            label: 원본 라벨 문자열

        Returns:
            정규화된 라벨 문자열

        Raises:
            ValueError: 지원하지 않는 라벨인 경우
        """
        pass
