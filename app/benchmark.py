class MacBenchmark:
    """
    MAC 성능 측정을 담당하는 객체 스켈레톤 코드
    """

    def benchmark_mac(
        self,
        matrix_a: list[list[float]],
        matrix_b: list[list[float]],
        repeat: int = 10,
    ) -> float:
        """
        MAC 연산 평균 수행 시간(ms)을 측정한다.

        Args:
            matrix_a: 첫 번째 행렬
            matrix_b: 두 번째 행렬
            repeat: 반복 횟수

        Returns:
            평균 수행 시간(ms)
        """
        pass
