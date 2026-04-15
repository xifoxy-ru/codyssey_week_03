"""
Mini NPU Simulator entry point
"""

from app.input_parser import MatrixInputHandler
from app.json_runner import JsonPatternRunner


def print_menu() -> None:
    """
    프로그램 메뉴를 출력한다.
    """
    pass


def run_user_input_mode() -> None:
    """
    사용자 입력 모드를 실행한다.

    처리 흐름:
    - 입력 핸들러 생성
    - 필터/패턴 입력 수집
    - 점수 계산
    - 결과 출력
    """
    pass


def run_json_mode() -> None:
    """
    data.json 분석 모드를 실행한다.

    처리 흐름:
    - JSON 러너 생성
    - 패턴 분석 실행
    - 결과 요약 출력
    """
    pass


def main() -> None:
    """
    프로그램 진입점이다.
    """
    pass


if __name__ == "__main__":
    main()
