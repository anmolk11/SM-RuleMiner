from sklearn.metrics import confusion_matrix
import numpy as np

def compute_confusion_matrix(true_labels, predicted_labels):
    # Create confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels)

    # Get class labels
    classes = np.unique(np.concatenate((true_labels, predicted_labels)))

    # Calculate evaluation metrics
    tp = np.diag(cm)
    fp = np.sum(cm, axis=0) - tp
    fn = np.sum(cm, axis=1) - tp
    tn = np.sum(cm) - (tp + fp + fn)

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)
    f1_score = 2 * (precision * recall) / (precision + recall)

    # Return confusion matrix and evaluation metrics
    return cm, classes, accuracy, precision, recall,specificity ,f1_score

import numpy as np

def merge_confusion_matrices(confusion_matrix1, confusion_matrix2):
    # Check if the input matrices have compatible dimensions
    if confusion_matrix1.shape != confusion_matrix2.shape:
        raise ValueError("The input matrices must have the same dimensions.")

    # Sum the counts in each cell to obtain the merged confusion matrix
    merged_matrix = confusion_matrix1 + confusion_matrix2

    return merged_matrix

def compute_evaluation_metrics(confusion_matrix):
    true_positive = np.diag(confusion_matrix)
    false_positive = np.sum(confusion_matrix, axis=0) - true_positive
    false_negative = np.sum(confusion_matrix, axis=1) - true_positive
    true_negative = np.sum(confusion_matrix) - (true_positive + false_positive + false_negative)

    accuracy = (true_positive + true_negative) / np.sum(confusion_matrix)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = 2 * (precision * recall) / (precision + recall)
    specificity = true_negative/(true_negative + false_positive)

    return accuracy, precision, recall,specificity, f1_score



if __name__ == "__main__":
    true_labels = [0, 1, 2, 2, 0, 1]
    predicted_labels = [0, 1, 2, 1, 0, 2]

    cm, classes, accuracy, precision, recall, f1_score = compute_confusion_matrix(true_labels, predicted_labels)

    print("Confusion Matrix:")
    print("========================================")
    print("True\\Predicted\t", end="")
    for c in classes:
        print(c, "\t", end="")
    print("\n")
    for i, c in enumerate(classes):
        print(c, "\t\t", end="")
        for j in range(len(classes)):
            print(cm[i, j], "\t", end="")
        print("\n")

    print("Evaluation Metrics:")
    print("========================================")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1_score}")
