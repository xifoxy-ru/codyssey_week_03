class AppConfig:
    """애플리케이션 전역 설정 상수"""

    BENCHMARK_TABLE_SIZES = (3, 5, 13, 25)
    DEFAULT_DATA_FILE = "data/data.json"
    DEFAULT_INPUT_SIZE = 3
    DEFAULT_BENCHMARK_REPEAT = 10
    EPSILON = 1e-9
    ENCODING = "utf-8"
    MILLISECONDS = 1000
    REQUIRED_FILTER_SIZES = ("size_5", "size_13", "size_25")


class JsonKey:
    """JSON 구조와 키 관련 상수"""

    FILTERS = "filters"
    PATTERNS = "patterns"
    INPUT = "input"
    EXPECTED = "expected"


class PatternRule:
    """패턴/필터 규칙 관련 상수"""

    PATTERN_KEY_REGEX = r"size_(\d+)_(\d+)"
    SIZE_KEY_TEMPLATE = "size_{size}"


class LabelValue:
    """라벨 문자열 상수"""

    CROSS = "Cross"
    X = "X"
    UNDECIDED = "UNDECIDED"
    RESULT_A = "A"
    RESULT_B = "B"
    LABEL_PLUS = "+"
    LABEL_CROSS_LOWER = "cross"
    LABEL_X_LOWER = "x"


class Text:
    """출력 문구와 오류 메시지 상수"""

    APP_TITLE = "=== Mini NPU Simulator ===\n"
    MENU_USER_INPUT = "1. 사용자 입력 (3x3)"
    MENU_JSON_ANALYSIS = "2. data.json 분석"
    MENU_PROMPT = "선택: "
    MENU_INVALID = "지원하지 않는 메뉴입니다. 1 또는 2를 선택해주세요."

    USER_INPUT_SECTION = "\n=== 사용자 입력 모드 (3x3) ==="
    RESULT_SECTION = "\n# [결과]"
    RESULT_SCORE_A = "A 점수: {score}"
    RESULT_SCORE_B = "B 점수: {score}"
    RESULT_JUDGE = "판정: {result}"

    INPUT_MATRIX_PROMPT = "\n{name} ({size}줄 입력, 공백 구분)"
    INPUT_RETRY = "다시 입력해주세요."
    INPUT_LINE_COUNT_ERROR = "입력 형식 오류: 총 {size}줄을 입력해야 합니다."
    INPUT_COLUMN_COUNT_ERROR = "입력 형식 오류: 각 줄에 {size}개의 숫자를 입력해야 합니다."
    INPUT_NUMBER_ONLY_ERROR = "입력 형식 오류: 숫자만 입력할 수 있습니다."
    INPUT_AVG_TIME = "연산 시간(평균/{repeat}회): {ms:.6f} ms"

    MATRIX_EMPTY_ERROR = "행렬은 비어 있지 않은 2차원 리스트여야 합니다."
    MATRIX_ROW_TYPE_ERROR = "행렬의 각 행은 리스트여야 합니다."
    MATRIX_SQUARE_ERROR = "NxN 정사각 행렬이어야 합니다."
    MATRIX_NUMBER_ERROR = "행렬에는 숫자만 포함되어야 합니다."
    MATRIX_SIZE_MISMATCH_ERROR = "두 행렬의 크기가 다릅니다."

    JSON_FILE_NOT_FOUND = "파일을 찾을 수 없습니다: {path}"
    JSON_TOP_LEVEL_ERROR = "JSON 최상위 구조는 객체(dict)여야 합니다."
    JSON_LOAD_FAIL = "JSON 로드 실패: {error}"
    JSON_FILTERS_REQUIRED = "JSON 구조 오류: filters 항목이 필요합니다."
    JSON_PATTERNS_REQUIRED = "JSON 구조 오류: patterns 항목이 필요합니다."
    JSON_PATTERN_KEY_ERROR = "패턴 키 형식 오류: {key}"
    JSON_FILTER_MISSING = "필터 누락: {size_key}"
    JSON_FILTER_STRUCTURE_ERROR = "필터 구조 오류: {size_key}"
    JSON_FILTER_LABEL_MISSING = "필터 라벨 누락: {size_key}"
    JSON_FILTER_SIZE_MISMATCH = "필터 크기 불일치: {size_key}"
    JSON_PATTERN_STRUCTURE_ERROR = "패턴 데이터 구조는 객체(dict)여야 합니다."
    JSON_PATTERN_INPUT_MISSING = "패턴 input 누락"
    JSON_PATTERN_EXPECTED_MISSING = "패턴 expected 누락"
    JSON_PATTERN_SIZE_MISMATCH = "패턴 크기와 키의 size 값이 일치하지 않습니다."
    JSON_LOAD_SECTION = "\n#---------------------------------------\n# [1] 필터 로드\n#---------------------------------------"
    JSON_PATTERN_STAGE = "\n#---------------------------------------\n# [2] 패턴 분석 (라벨 정규화 적용)\n#---------------------------------------"
    JSON_FILTER_LOADED = "✓ {size_key:<7} 필터 로드 완료 (Cross, X)"
    JSON_REASON_UNDECIDED = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    JSON_REASON_MISMATCH = "예측값({predicted})과 expected({expected}) 불일치"
    JSON_REQUIRED_FILTER_MISSING = "필수 필터 누락: {size_key}"
    
    JSON_PATTERN_SECTION = "\n--- {pattern_key} ---"
    JSON_SCORE_CROSS = "Cross 점수: {score}"
    JSON_SCORE_X = "X 점수: {score}"
    JSON_AVG_TIME = "평균 시간: {ms:.6f} ms"
    JSON_STATUS = "판정: {predicted} | expected: {expected} | {status}"
    JSON_FAIL = "FAIL: {error}"

    SUMMARY_SECTION = "\n# [결과 요약]"
    SUMMARY_TOTAL = "총 테스트: {total}개"
    SUMMARY_PASS = "통과: {passed}개"
    SUMMARY_FAIL = "실패: {failed}개"
    SUMMARY_FAIL_CASES = "\n실패 케이스:"
    SUMMARY_FAIL_ITEM = "- {pattern_key}: {reason}"

    BENCHMARK_SECTION = "\n# [성능 분석]"
    BENCHMARK_HEADER = "크기\t평균 시간(ms)\t연산 횟수"
    BENCHMARK_ROW = "{size}x{size}\t{avg_ms:.6f}\t{operation_count}"
    BENCHMARK_ROW_EMPTY = "{size}x{size}\t-\t{operation_count}"

    BENCHMARK_REPEAT_ERROR = "repeat는 1 이상이어야 합니다."
    LABEL_INVALID_ERROR = "지원하지 않는 라벨입니다: {label}"

    BLOCK_LINE = "#---------------------------------------"
    MODE_SECTION = "[모드 선택]\n"
    FILTER_INPUT_SECTION = "# [1] 필터 입력"
    PATTERN_INPUT_SECTION = "# [2] 패턴 입력"
    MAC_RESULT_SECTION = "# [3] MAC 결과"