from src.data_loader import load_records
from src.ews_scorer import score_vitals
from src.threshold_selector import choose_best_threshold


def calculate_score(record):
    """
    Calculate one patient's total vital-sign score.
    """
    return score_vitals(
        record.heart_rate,
        record.resp_rate,
        record.spo2,
        record.temperature,
        record.systolic_bp,
    )


def validate(csv_path):
    """
    Calculate the best threshold for the supplied dataset.
    """
    records = load_records(csv_path)

    scores = [calculate_score(record) for record in records]
    actual_labels = [record.ground_truth_risk for record in records]

    best_threshold = choose_best_threshold(scores, actual_labels)

    correct_predictions = 0

    for score, actual_label in zip(scores, actual_labels):
        predicted_label = (
            "High Risk"
            if score >= best_threshold
            else "Low Risk"
        )

        if predicted_label == actual_label:
            correct_predictions += 1

    accuracy = correct_predictions / len(records)

    print(f"Records loaded: {len(records)}")
    print(f"Automatically selected threshold: {best_threshold}")
    print(f"Agreement with dataset: {accuracy:.2%}")


if __name__ == "__main__":
    import sys

    validate(sys.argv[1])