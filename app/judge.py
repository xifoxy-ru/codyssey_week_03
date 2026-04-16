from app.constants import AppConfig, LabelValue


class ScoreJudge:
    """
    점수 비교와 판정을 담당하는 객체이다.
    """

    def __init__(self, epsilon: float = AppConfig.EPSILON) -> None:
        self.epsilon = epsilon

    def judge_scores(self, score_a: float, score_b: float) -> str:
        """
        두 점수를 비교하여 A, B, UNDECIDED 중 하나를 반환한다.
        """
        if abs(score_a - score_b) < self.epsilon:
            return LabelValue.UNDECIDED

        if score_a > score_b:
            return LabelValue.RESULT_A

        return LabelValue.RESULT_B
