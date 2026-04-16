import time

from app.mac import MacCalculator


class MacBenchmark:
    """
    MAC 성능 측정을 담당하는 객체이다.
    """

    def __init__(self) -> None:
        """
        벤치마크 객체를 초기화한다.
        """
        self.calculator = MacCalculator()

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

        Raises:
            ValueError: repeat가 1 미만인 경우
        """
        if repeat < 1:
            raise ValueError("repeat는 1 이상이어야 합니다.")

        start = time.perf_counter()

        for _ in range(repeat):
            self.calculator.mac(matrix_a, matrix_b)

        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000

        return elapsed_ms / repeat