from app.constants import LabelValue, Text


class LabelNormalizer:
    """
    라벨 정규화를 담당하는 객체이다.
    """

    def normalize_label(self, label: str) -> str:
        """
        입력 라벨을 내부 표준 라벨로 정규화한다.
        """
        value = str(label).strip().lower()

        if value in {LabelValue.LABEL_PLUS, LabelValue.LABEL_CROSS_LOWER}:
            return LabelValue.CROSS

        if value == LabelValue.LABEL_X_LOWER:
            return LabelValue.X

        raise ValueError(Text.LABEL_INVALID_ERROR.format(label=label))
