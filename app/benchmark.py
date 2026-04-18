import time

from app.constants import AppConfig, Text
from app.mac import MacCalculator


class MacBenchmark:
    """
    MAC 성능 측정을 담당하는 객체이다.
    """

    def __init__(self) -> None:
        self.calculator = MacCalculator()

    def benchmark_mac(
        self,
        matrix_a: list[list[float]],
        matrix_b: list[list[float]],
        repeat: int = AppConfig.DEFAULT_BENCHMARK_REPEAT,
    ) -> float:
        """
        MAC 연산 평균 수행 시간(ms)을 측정한다.
        """
        if repeat < 1:
            raise ValueError(Text.BENCHMARK_REPEAT_ERROR)

        start = time.perf_counter()

        for _ in range(repeat):
            self.calculator.mac(matrix_a, matrix_b)

        end = time.perf_counter()
        elapsed_ms = (end - start) * AppConfig.MILLISECONDS

        return elapsed_ms / repeat
