from app.benchmark import MacBenchmark
from app.constants import AppConfig, InputValue, LabelValue, Text
from app.enums import MenuOption
from app.input_parser import MatrixInputHandler
from app.judge import ScoreJudge
from app.json_runner import JsonPatternRunner
from app.mac import MacCalculator


class MiniNpuApp:
    def __init__(self) -> None:
        self.handler = MatrixInputHandler()
        self.calculator = MacCalculator()
        self.judge = ScoreJudge()
        self.benchmark = MacBenchmark()
        self.json_runner = JsonPatternRunner()

    def run(self) -> None:
        self._print_menu()
        choice = self._safe_input(Text.MENU_PROMPT).strip()

        if choice == str(MenuOption.USER_INPUT):
            self._run_user_input_mode()
            return

        if choice == str(MenuOption.JSON_ANALYSIS):
            self._run_json_mode()
            return

        print(Text.MENU_INVALID)

    def _safe_input(self, prompt: str = "") -> str:
        while True:
            try:
                return input(prompt)
            except (KeyboardInterrupt, EOFError):
                print()
                print(Text.INPUT_INTERRUPTED_RETRY)

    def _print_menu(self) -> None:
        print(Text.APP_TITLE)
        print()
        print(Text.MODE_SECTION)
        print()
        print(Text.MENU_USER_INPUT)
        print(Text.MENU_JSON_ANALYSIS)

    def _run_user_input_mode(self) -> None:
        while True:
            print()
            print(Text.BLOCK_LINE)
            print(Text.FILTER_INPUT_SECTION)
            print(Text.BLOCK_LINE)

            filter_a = self.handler.prompt_matrix(
                "필터 A",
                AppConfig.DEFAULT_INPUT_SIZE,
            )
            filter_b = self.handler.prompt_matrix(
                "필터 B",
                AppConfig.DEFAULT_INPUT_SIZE,
            )

            if self._confirm_filters(filter_a, filter_b):
                break

        print()
        print(Text.BLOCK_LINE)
        print(Text.PATTERN_INPUT_SECTION)
        print(Text.BLOCK_LINE)

        pattern = self.handler.prompt_matrix(
            "패턴",
            AppConfig.DEFAULT_INPUT_SIZE,
        )

        score_a = self.calculator.mac(pattern, filter_a)
        score_b = self.calculator.mac(pattern, filter_b)
        result = self.judge.judge_scores(score_a, score_b)
        average_ms = self.benchmark.benchmark_mac(pattern, filter_a)

        print()
        print(Text.BLOCK_LINE)
        print(Text.MAC_RESULT_SECTION)
        print(Text.BLOCK_LINE)
        print(Text.RESULT_SCORE_A.format(score=score_a))
        print(Text.RESULT_SCORE_B.format(score=score_b))
        print(
            Text.INPUT_AVG_TIME.format(
                repeat=AppConfig.DEFAULT_BENCHMARK_REPEAT,
                ms=average_ms,
            )
        )

        if result == LabelValue.UNDECIDED:
            print(Text.RESULT_UNDECIDED.format(epsilon=AppConfig.EPSILON))
        else:
            print(Text.RESULT_JUDGE.format(result=result))

    def _run_json_mode(self) -> None:
        self.json_runner.run()

    def _confirm_filters(
        self,
        filter_a: list[list[float]],
        filter_b: list[list[float]],
    ) -> bool:
        print()
        print(Text.BLOCK_LINE)
        print(Text.FILTER_CONFIRM_SECTION)
        print(Text.BLOCK_LINE)

        print("필터 A")
        self._print_matrix(filter_a)
        print()
        print("필터 B")
        self._print_matrix(filter_b)

        while True:
            choice = self._safe_input(Text.FILTER_CONFIRM_PROMPT).strip().lower()

            if choice in InputValue.YES:
                return True

            if choice in InputValue.NO:
                return False

            print(Text.FILTER_CONFIRM_INVALID)

    def _print_matrix(self, matrix: list[list[float]]) -> None:
        for row in matrix:
            print(" ".join(self._format_cell(value) for value in row))

    @staticmethod
    def _format_cell(value: float) -> str:
        if float(value).is_integer():
            return str(int(value))
        return str(value)