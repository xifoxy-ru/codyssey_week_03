from app.constants import AppConfig, InputValue, LabelValue, Text
from app.enums import MenuOption
from app.input_parser import MatrixInputHandler
from app.judge import ScoreJudge
from app.json_runner import JsonPatternRunner
from app.mac import MacCalculator
from app.benchmark import MacBenchmark


def print_menu() -> None:
    print(Text.APP_TITLE)
    print(Text.MODE_SECTION)
    print(Text.MENU_USER_INPUT)
    print(Text.MENU_JSON_ANALYSIS)

def format_cell(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def print_matrix(matrix: list[list[float]]) -> None:
    for row in matrix:
        print(" ".join(format_cell(value) for value in row))


def confirm_filters(
    filter_a: list[list[float]],
    filter_b: list[list[float]],
) -> bool:
    print()
    print(Text.BLOCK_LINE)
    print(Text.FILTER_CONFIRM_SECTION)
    print(Text.BLOCK_LINE)

    print(Text.FILTER_A)
    print_matrix(filter_a)
    print()
    print(Text.FILTER_B)
    print_matrix(filter_b)

    while True:
        choice = input(Text.FILTER_CONFIRM_PROMPT).strip().lower()

        if choice in InputValue.YES:
            return True

        if choice in InputValue.NO:
            return False

        print(Text.FILTER_CONFIRM_INVALID)


def run_user_input_mode() -> None:
    handler = MatrixInputHandler()
    calculator = MacCalculator()
    judge = ScoreJudge()
    benchmark = MacBenchmark()

    while True:
        print()
        print(Text.BLOCK_LINE)
        print(Text.FILTER_INPUT_SECTION)
        print(Text.BLOCK_LINE)

        filter_a = handler.prompt_matrix(Text.FILTER_A, AppConfig.DEFAULT_INPUT_SIZE)
        filter_b = handler.prompt_matrix(Text.FILTER_B, AppConfig.DEFAULT_INPUT_SIZE)

        if confirm_filters(filter_a, filter_b):
            break

    print()
    print(Text.BLOCK_LINE)
    print(Text.PATTERN_INPUT_SECTION)
    print(Text.BLOCK_LINE)

    pattern = handler.prompt_matrix(Text.PATTERN, AppConfig.DEFAULT_INPUT_SIZE)

    score_a = calculator.mac(pattern, filter_a)
    score_b = calculator.mac(pattern, filter_b)
    result = judge.judge_scores(score_a, score_b)
    average_ms = benchmark.benchmark_mac(pattern, filter_a)

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

def run_json_mode() -> None:
    runner = JsonPatternRunner()
    runner.run()


def main() -> None:
    print_menu()
    choice = input(Text.MENU_PROMPT).strip()

    if choice == str(MenuOption.USER_INPUT):
        run_user_input_mode()
        return

    if choice == str(MenuOption.JSON_ANALYSIS):
        run_json_mode()
        return

    print(Text.MENU_INVALID)


if __name__ == "__main__":
    main()
