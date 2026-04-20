"""Data loading utilities for the VQC paper reproduction project."""

import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_paper_csv(filepath):
    """Load one of the paper's CSV files. Columns are: index, feature_1, feature_2, Label (+1/-1).
    Returns X (n_samples, 2) and y (n_samples,) with labels as integers {+1, -1}."""
    df = pd.read_csv(filepath, header=0, index_col=0)
    df.columns = ["feature_1", "feature_2", "label"] + list(df.columns[3:])
    df = df.dropna(how="all")
    X = df[["feature_1", "feature_2"]].values
    y = df["label"].values.astype(int)
    return X, y


def load_paper_classification(filepath):
    """Load a classification results CSV. Has extra columns: Test Result, Testing Success.
    Returns X, y_true, y_pred."""
    df = pd.read_csv(filepath, header=0, index_col=0)
    df.columns = ["feature_1", "feature_2", "label", "test_result"] + list(df.columns[4:])
    df = df.dropna(how="all")
    X = df[["feature_1", "feature_2"]].values
    y_true = df["label"].values.astype(int)
    y_pred = df["test_result"].values.astype(int)
    return X, y_true, y_pred


def load_all_kernel_sets():
    """Load all three kernel dataset splits (Sets I, II, III).
    Returns a dict keyed by set name, each containing
    X_train, y_train, X_test, y_test, y_pred_paper."""
    kernel_sets = {}
    for set_name in ["I", "II", "III"]:
        train_path = os.path.join(DATA_DIR, f"Direct_Kernel_Set_{set_name}_Training.csv")
        test_path = os.path.join(DATA_DIR, f"Direct_Kernel_Set_{set_name}_Classifications_ResultsOnly.csv")

        X_train, y_train = load_paper_csv(train_path)
        X_test, y_true, y_pred_paper = load_paper_classification(test_path)

        kernel_sets[set_name] = {
            "X_train": X_train,
            "y_train": y_train,
            "X_test": X_test,
            "y_test": y_true,
            "y_pred_paper": y_pred_paper,
        }
    return kernel_sets


def load_all_variational_sets():
    """Load all variational dataset splits for depths 0-4 and Sets I, II, III.
    The CSV filenames use pattern: Variational_Set_{I,II,III}_d{0-4}_*.csv
    Returns a nested dict keyed by (set_name, depth) containing
    X_train, y_train, X_test, y_test, paper_accuracy."""
    depths = [0, 1, 2, 3, 4]
    set_names = ["I", "II", "III"]
    variational_data = {}

    for set_name in set_names:
        for d in depths:
            train_path = os.path.join(DATA_DIR, f"Variational_Set_{set_name}_d{d}_Training.csv")
            test_path = os.path.join(
                DATA_DIR, f"Variational_Set_{set_name}_d{d}_Classifications_ResultsOnly.csv"
            )

            # Training data
            df_train = pd.read_csv(train_path, header=0, index_col=0)
            df_train.columns = ["feature_1", "feature_2", "label"] + list(df_train.columns[3:])
            df_train = df_train.dropna(how="all")
            X_train = df_train[["feature_1", "feature_2"]].values
            y_train = df_train["label"].values.astype(int)

            # Test data with paper's predictions
            X_test, y_test, y_pred_paper = load_paper_classification(test_path)
            paper_acc = accuracy_score(y_test, y_pred_paper)

            variational_data[(set_name, d)] = {
                "X_train": X_train,
                "y_train": y_train,
                "X_test": X_test,
                "y_test": y_test,
                "y_pred_paper": y_pred_paper,
                "paper_accuracy": paper_acc,
            }

    return variational_data
