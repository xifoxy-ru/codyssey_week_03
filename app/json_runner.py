import json
import re
from pathlib import Path
from typing import Any

from app.benchmark import MacBenchmark
from app.constants import AppConfig, JsonKey, LabelValue, PatternRule, Text
from app.judge import ScoreJudge
from app.labels import LabelNormalizer
from app.mac import MacCalculator
from app.matrix import MatrixValidator


class JsonPatternRunner:
    """
    JSON 기반 패턴 분석 객체이다.
    """

    def __init__(self, data_file: str = AppConfig.DEFAULT_DATA_FILE) -> None:
        self.data_file = data_file
        self.validator = MatrixValidator()
        self.calculator = MacCalculator()
        self.judge = ScoreJudge()
        self.normalizer = LabelNormalizer()
        self.benchmark = MacBenchmark()

    def load_json_file(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(Text.JSON_FILE_NOT_FOUND.format(path=file_path))

        with file_path.open("r", encoding=AppConfig.ENCODING) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError(Text.JSON_TOP_LEVEL_ERROR)

        return data
    
    def print_filter_load_stage(self, filters: dict[str, Any]) -> None:
        print(Text.JSON_LOAD_SECTION)

        for size_key, filter_value in filters.items():
            if not isinstance(filter_value, dict):
                continue

            if LabelValue.CROSS in filter_value and LabelValue.X in filter_value:
                print(Text.JSON_FILTER_LOADED.format(size_key=size_key))

    def extract_size_from_pattern_key(self, key: str) -> int:
        match = re.fullmatch(PatternRule.PATTERN_KEY_REGEX, key)

        if not match:
            raise ValueError(Text.JSON_PATTERN_KEY_ERROR.format(key=key))

        return int(match.group(1))
    
    def validate_required_filters(self, filters: dict[str, Any]) -> bool:
        is_valid = True

        for size_key in AppConfig.REQUIRED_FILTER_SIZES:
            if size_key not in filters:
                print(
                    Text.JSON_FAIL.format(
                        error=Text.JSON_REQUIRED_FILTER_MISSING.format(
                            size_key=size_key
                        )
                    )
                )
                is_valid = False
                continue

            filter_value = filters[size_key]

            if not isinstance(filter_value, dict):
                print(
                    Text.JSON_FAIL.format(
                        error=Text.JSON_FILTER_STRUCTURE_ERROR.format(
                            size_key=size_key
                        )
                    )
                )
                is_valid = False
                continue

            if LabelValue.CROSS not in filter_value or LabelValue.X not in filter_value:
                print(
                    Text.JSON_FAIL.format(
                        error=Text.JSON_FILTER_LABEL_MISSING.format(
                            size_key=size_key
                        )
                    )
                )
                is_valid = False

        return is_valid

    def resolve_filter_pair(
        self,
        filters: dict[str, Any],
        size: int,
    ) -> tuple[list[list[float]], list[list[float]]]:
        size_key = PatternRule.SIZE_KEY_TEMPLATE.format(size=size)

        if size_key not in filters:
            raise ValueError(Text.JSON_FILTER_MISSING.format(size_key=size_key))

        size_filters = filters[size_key]

        if not isinstance(size_filters, dict):
            raise ValueError(Text.JSON_FILTER_STRUCTURE_ERROR.format(size_key=size_key))

        if LabelValue.CROSS not in size_filters or LabelValue.X not in size_filters:
            raise ValueError(Text.JSON_FILTER_LABEL_MISSING.format(size_key=size_key))

        cross_filter = self.validator.validate_square_matrix(size_filters[LabelValue.CROSS])
        x_filter = self.validator.validate_square_matrix(size_filters[LabelValue.X])

        if len(cross_filter) != size or len(x_filter) != size:
            raise ValueError(Text.JSON_FILTER_SIZE_MISMATCH.format(size_key=size_key))

        return cross_filter, x_filter

    def analyze_single_pattern(
        self,
        pattern_key: str,
        pattern_data: dict[str, Any],
        filters: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(pattern_data, dict):
            raise ValueError(Text.JSON_PATTERN_STRUCTURE_ERROR)

        if JsonKey.INPUT not in pattern_data:
            raise ValueError(Text.JSON_PATTERN_INPUT_MISSING)

        if JsonKey.EXPECTED not in pattern_data:
            raise ValueError(Text.JSON_PATTERN_EXPECTED_MISSING)

        size = self.extract_size_from_pattern_key(pattern_key)
        input_matrix = self.validator.validate_square_matrix(pattern_data[JsonKey.INPUT])
        expected = self.normalizer.normalize_label(pattern_data[JsonKey.EXPECTED])

        if len(input_matrix) != size:
            raise ValueError(Text.JSON_PATTERN_SIZE_MISMATCH)

        cross_filter, x_filter = self.resolve_filter_pair(filters, size)

        cross_score = self.calculator.mac(input_matrix, cross_filter)
        x_score = self.calculator.mac(input_matrix, x_filter)

        winner = self.judge.judge_scores(cross_score, x_score)

        if winner == LabelValue.RESULT_A:
            predicted = LabelValue.CROSS
        elif winner == LabelValue.RESULT_B:
            predicted = LabelValue.X
        else:
            predicted = LabelValue.UNDECIDED

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
            "reason": "",
        }

    def print_json_summary(self, results: list[dict[str, Any]]) -> None:
        total = len(results)
        passed = sum(1 for item in results if item["pass"])
        failed = total - passed

        print(Text.SUMMARY_SECTION)
        print(Text.SUMMARY_TOTAL.format(total=total))
        print(Text.SUMMARY_PASS.format(passed=passed))
        print(Text.SUMMARY_FAIL.format(failed=failed))

        if failed:
            print(Text.SUMMARY_FAIL_CASES)
            for item in results:
                if not item["pass"]:
                    print(
                        Text.SUMMARY_FAIL_ITEM.format(
                            pattern_key=item["pattern_key"],
                            reason=item["reason"],
                        )
                    )

    def print_benchmark_summary(self, results: list[dict[str, Any]]) -> None:
        grouped: dict[int, list[float]] = {}

        for item in results:
            size = item.get("size")
            average_ms = item.get("average_ms")

            if size is None or average_ms is None:
                continue

            grouped.setdefault(size, []).append(average_ms)

        if not grouped:
            return

        print(Text.BENCHMARK_SECTION)
        print(Text.BENCHMARK_HEADER)

        for size in sorted(grouped):
            avg_ms = sum(grouped[size]) / len(grouped[size])
            operation_count = size * size
            print(
                Text.BENCHMARK_ROW.format(
                    size=size,
                    avg_ms=avg_ms,
                    operation_count=operation_count,
                )
            )

    def run(self) -> None:
        try:
            data = self.load_json_file(self.data_file)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
            print(Text.JSON_LOAD_FAIL.format(error=exc))
            return

        filters = data.get(JsonKey.FILTERS)
        patterns = data.get(JsonKey.PATTERNS)

        if not isinstance(filters, dict):
            print(Text.JSON_FILTERS_REQUIRED)
            return

        if not isinstance(patterns, dict):
            print(Text.JSON_PATTERNS_REQUIRED)
            return
        
        if not self.validate_required_filters(filters):
            return

        self.print_filter_load_stage(filters)

        results: list[dict[str, Any]] = []

        for pattern_key, pattern_data in patterns.items():
            print(Text.JSON_PATTERN_SECTION.format(pattern_key=pattern_key))

            try:
                result = self.analyze_single_pattern(pattern_key, pattern_data, filters)
                results.append(result)

                status = "PASS" if result["pass"] else "FAIL"

                print(Text.JSON_SCORE_CROSS.format(score=result["cross_score"]))
                print(Text.JSON_SCORE_X.format(score=result["x_score"]))
                print(Text.JSON_AVG_TIME.format(ms=result["average_ms"]))
                print(
                    Text.JSON_STATUS.format(
                        predicted=result["predicted"],
                        expected=result["expected"],
                        status=status,
                    )
                )
            except ValueError as exc:
                print(Text.JSON_FAIL.format(error=exc))
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
                        "reason": str(exc),
                    }
                )

        self.print_benchmark_summary(results)
        self.print_json_summary(results)
