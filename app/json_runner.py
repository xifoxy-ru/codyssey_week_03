import json
import re
from pathlib import Path
from typing import Any

from app.benchmark import MacBenchmark
from app.judge import ScoreJudge
from app.labels import LabelNormalizer
from app.mac import MacCalculator
from app.matrix import MatrixValidator


class JsonPatternRunner:
    """
    JSON 기반 패턴 분석 객체이다.
    """

    def __init__(self, data_file: str = "data.json") -> None:
        """
        JSON 러너를 초기화한다.

        Args:
            data_file: 사용할 JSON 파일 경로
        """
        self.data_file = data_file
        self.validator = MatrixValidator()
        self.calculator = MacCalculator()
        self.judge = ScoreJudge()
        self.normalizer = LabelNormalizer()
        self.benchmark = MacBenchmark()

    def load_json_file(self, path: str | Path) -> dict[str, Any]:
        """
        JSON 파일을 로드한다.
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("JSON 최상위 구조는 객체(dict)여야 합니다.")

        return data

    def extract_size_from_pattern_key(self, key: str) -> int:
        """
        패턴 키에서 size 값을 추출한다.
        """
        match = re.fullmatch(r"size_(\d+)_(\d+)", key)

        if not match:
            raise ValueError(f"패턴 키 형식 오류: {key}")

        return int(match.group(1))

    def resolve_filter_pair(
        self,
        filters: dict[str, Any],
        size: int,
    ) -> tuple[list[list[float]], list[list[float]]]:
        """
        주어진 크기에 맞는 Cross / X 필터를 반환한다.
        """
        size_key = f"size_{size}"

        if size_key not in filters:
            raise ValueError(f"필터 누락: {size_key}")

        size_filters = filters[size_key]

        if not isinstance(size_filters, dict):
            raise ValueError(f"필터 구조 오류: {size_key}")

        if "Cross" not in size_filters or "X" not in size_filters:
            raise ValueError(f"필터 라벨 누락: {size_key}")

        cross_filter = self.validator.validate_square_matrix(size_filters["Cross"])
        x_filter = self.validator.validate_square_matrix(size_filters["X"])

        if len(cross_filter) != size or len(x_filter) != size:
            raise ValueError(f"필터 크기 불일치: {size_key}")

        return cross_filter, x_filter

    def analyze_single_pattern(
        self,
        pattern_key: str,
        pattern_data: dict[str, Any],
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        """
        단일 패턴 케이스를 분석한다.
        """
        if not isinstance(pattern_data, dict):
            raise ValueError("패턴 데이터 구조는 객체(dict)여야 합니다.")

        if "input" not in pattern_data:
            raise ValueError("패턴 input 누락")

        if "expected" not in pattern_data:
            raise ValueError("패턴 expected 누락")

        size = self.extract_size_from_pattern_key(pattern_key)
        input_matrix = self.validator.validate_square_matrix(pattern_data["input"])
        expected = self.normalizer.normalize_label(pattern_data["expected"])

        if len(input_matrix) != size:
            raise ValueError("패턴 크기와 키의 size 값이 일치하지 않습니다.")

        cross_filter, x_filter = self.resolve_filter_pair(filters, size)

        cross_score = self.calculator.mac(input_matrix, cross_filter)
        x_score = self.calculator.mac(input_matrix, x_filter)

        winner = self.judge.judge_scores(cross_score, x_score)

        if winner == "A":
            predicted = "Cross"
        elif winner == "B":
            predicted = "X"
        else:
            predicted = "UNDECIDED"

        average_ms = self.benchmark.benchmark_mac(input_matrix, cross_filter)

        return {
            "pattern_key": pattern_key,
            "size": size,
            "cross_score": cross_score,
            "x_score": x_score,
            "predicted": predicted,
            "expected": expected,
            "pass": predicted == expected,
            "average_ms": average_ms,
        }

    def print_json_summary(self, results: list[dict[str, Any]]) -> None:
        """
        JSON 분석 결과 요약을 출력한다.
        """
        total = len(results)
        passed = sum(1 for item in results if item["pass"])
        failed = total - passed

        print("\n# [결과 요약]")
        print(f"총 테스트: {total}개")
        print(f"통과: {passed}개")
        print(f"실패: {failed}개")

        if failed:
            print("\n실패 케이스:")
            for item in results:
                if not item["pass"]:
                    print(
                        f"- {item['pattern_key']}: "
                        f"predicted={item['predicted']}, expected={item['expected']}"
                    )

    def print_benchmark_summary(self, results: list[dict[str, Any]]) -> None:
        """
        크기별 성능 요약을 출력한다.
        """
        grouped: dict[int, list[float]] = {}

        for item in results:
            size = item.get("size")
            average_ms = item.get("average_ms")

            if size is None or average_ms is None:
                continue

            grouped.setdefault(size, []).append(average_ms)

        if not grouped:
            return

        print("\n# [성능 분석]")
        print("크기\t평균 시간(ms)\t연산 횟수")

        for size in sorted(grouped):
            avg_ms = sum(grouped[size]) / len(grouped[size])
            operation_count = size * size
            print(f"{size}x{size}\t{avg_ms:.6f}\t{operation_count}")

    def run(self) -> None:
        """
        data.json 분석 전체 흐름을 실행한다.
        """
        try:
            data = self.load_json_file(self.data_file)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            print(f"JSON 로드 실패: {exc}")
            return

        filters = data.get("filters")
        patterns = data.get("patterns")

        if not isinstance(filters, dict):
            print("JSON 구조 오류: filters 항목이 필요합니다.")
            return

        if not isinstance(patterns, dict):
            print("JSON 구조 오류: patterns 항목이 필요합니다.")
            return

        results: list[dict[str, Any]] = []

        for pattern_key, pattern_data in patterns.items():
            print(f"\n--- {pattern_key} ---")

            try:
                result = self.analyze_single_pattern(
                    pattern_key,
                    pattern_data,
                    filters,
                )
                results.append(result)

                status = "PASS" if result["pass"] else "FAIL"

                print(f"Cross 점수: {result['cross_score']}")
                print(f"X 점수: {result['x_score']}")
                print(f"평균 시간: {result['average_ms']:.6f} ms")
                print(
                    f"판정: {result['predicted']} | "
                    f"expected: {result['expected']} | {status}"
                )

            except ValueError as exc:
                print(f"FAIL: {exc}")
                results.append(
                    {
                        "pattern_key": pattern_key,
                        "size": None,
                        "cross_score": None,
                        "x_score": None,
                        "predicted": "ERROR",
                        "expected": "UNKNOWN",
                        "pass": False,
                        "average_ms": None,
                    }
                )

        self.print_benchmark_summary(results)
        self.print_json_summary(results)