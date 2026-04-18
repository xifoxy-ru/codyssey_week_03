from app.constants import AppConfig, Text
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


def run_user_input_mode() -> None:
    handler = MatrixInputHandler()
    calculator = MacCalculator()
    judge = ScoreJudge()
    benchmark = MacBenchmark()

    print(f'\n{Text.BLOCK_LINE}')
    print(Text.FILTER_INPUT_SECTION)
    print(Text.BLOCK_LINE)
    filter_a = handler.prompt_matrix("필터 A", AppConfig.DEFAULT_INPUT_SIZE)
    filter_b = handler.prompt_matrix("필터 B", AppConfig.DEFAULT_INPUT_SIZE)

    print(f'\n{Text.BLOCK_LINE}')
    print(Text.PATTERN_INPUT_SECTION)
    print(f'{Text.BLOCK_LINE}')
    pattern = handler.prompt_matrix("패턴", AppConfig.DEFAULT_INPUT_SIZE)

    score_a = calculator.mac(pattern, filter_a)
    score_b = calculator.mac(pattern, filter_b)
    result = judge.judge_scores(score_a, score_b)
    average_ms = benchmark.benchmark_mac(pattern, filter_a)

    print(f'\n{Text.BLOCK_LINE}')
    print(Text.MAC_RESULT_SECTION)
    print(f'{Text.BLOCK_LINE}\n')
    print(Text.RESULT_SCORE_A.format(score=score_a))
    print(Text.RESULT_SCORE_B.format(score=score_b))
    print(Text.INPUT_AVG_TIME.format(
        repeat=AppConfig.DEFAULT_BENCHMARK_REPEAT,
        ms=average_ms,
    ))
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
