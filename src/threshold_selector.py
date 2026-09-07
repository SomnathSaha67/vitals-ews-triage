def choose_best_threshold(scores: list[int], actual_labels: list[str]) -> int:
    """
    Choose the threshold that gives the highest agreement with the dataset labels.

    A score greater than or equal to the threshold is classified as High Risk.
    A score below the threshold is classified as Low Risk.
    """

    if not scores:
        raise ValueError("Cannot choose a threshold without scores.")

    if len(scores) != len(actual_labels):
        raise ValueError("Scores and labels must have the same length.")

    possible_thresholds = range(min(scores), max(scores) + 2)

    best_threshold = None
    best_accuracy = -1.0

    for threshold in possible_thresholds:
        correct_predictions = 0

        for score, actual_label in zip(scores, actual_labels):
            predicted_label = (
                "High Risk" if score >= threshold else "Low Risk"
            )

            if predicted_label == actual_label:
                correct_predictions += 1

        accuracy = correct_predictions / len(scores)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold

    return best_threshold