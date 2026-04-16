class ScoreJudge:
    """
    점수 비교와 판정을 담당하는 객체이다.
    """

    def __init__(self, epsilon: float = 1e-9) -> None:
        """
        판정 객체를 초기화한다.

        Args:
            epsilon: 동점 판정을 위한 허용오차
        """
        self.epsilon = epsilon

    def judge_scores(self, score_a: float, score_b: float) -> str:
        """
        두 점수를 비교하여 A, B, UNDECIDED 중 하나를 반환한다.

        Args:
            score_a: 첫 번째 점수
            score_b: 두 번째 점수

        Returns:
            판정 결과 문자열
        """
        if abs(score_a - score_b) < self.epsilon:
            return "UNDECIDED"

        if score_a > score_b:
            return "A"

        return "B"