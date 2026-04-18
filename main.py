from app.input_parser import MatrixInputHandler
from app.json_runner import JsonPatternRunner
from app.mac import MacCalculator


def print_menu() -> None:
    """
    프로그램 메뉴를 출력한다.
    """
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")


def run_user_input_mode() -> None:
    """
    사용자 입력 모드를 실행한다.

    처리 흐름:
    - 입력 핸들러 생성
    - 필터/패턴 입력 수집
    - 점수 계산
    - 결과 출력
    """
    handler = MatrixInputHandler()
    calculator = MacCalculator()

    print("\n=== 사용자 입력 모드 (3x3) ===")

    filter_a = handler.prompt_matrix("필터 A", 3)
    filter_b = handler.prompt_matrix("필터 B", 3)
    pattern = handler.prompt_matrix("패턴", 3)

    score_a = calculator.mac(pattern, filter_a)
    score_b = calculator.mac(pattern, filter_b)

    print("\n# [결과]")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    if score_a > score_b:
        print("판정: A")
    elif score_b > score_a:
        print("판정: B")
    else:
        print("판정: UNDECIDED")


def run_json_mode() -> None:
    """
    data.json 분석 모드를 실행한다.

    처리 흐름:
    - JSON 러너 생성
    - 패턴 분석 실행
    - 결과 요약 출력
    """
    runner = JsonPatternRunner()
    runner.run()


def main() -> None:
    """
    프로그램 진입점이다.
    """
    print_menu()
    choice = input("선택: ").strip()

    if choice == "1":
        run_user_input_mode()
        return

    if choice == "2":
        run_json_mode()
        return

    print("지원하지 않는 메뉴입니다. 1 또는 2를 선택해주세요.")


if __name__ == "__main__":
    main()