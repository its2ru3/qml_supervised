"""Metric and result aggregation utilities for the VQC paper reproduction project."""

import numpy as np
from sklearn.metrics import accuracy_score


def compute_paper_accuracy(y_true, y_pred_paper):
    """Compute the accuracy reported by the paper from its predicted labels."""
    return accuracy_score(y_true, y_pred_paper)


def compare_with_paper(our_accuracy, paper_accuracy, tolerance=0.05):
    """Compare our accuracy with the paper's. Returns a dict with match status and delta."""
    delta = our_accuracy - paper_accuracy
    return {
        "our_accuracy": our_accuracy,
        "paper_accuracy": paper_accuracy,
        "delta": delta,
        "match": abs(delta) < tolerance,
        "status": "✓" if abs(delta) < tolerance else "✗",
    }


def aggregate_results(results_dict, key_names=None):
    """Aggregate results across dataset splits and/or depths.
    results_dict: dict keyed by (set_name, depth) or set_name, each containing
                  at minimum 'our_accuracy' and 'paper_accuracy'.
    Returns a summary dict with mean and std of accuracies."""
    our_accs = []
    paper_accs = []

    for key, val in results_dict.items():
        if "our_accuracy" in val:
            our_accs.append(val["our_accuracy"])
        if "paper_accuracy" in val:
            paper_accs.append(val["paper_accuracy"])

    summary = {
        "our_mean": np.mean(our_accs) if our_accs else None,
        "our_std": np.std(our_accs) if our_accs else None,
        "paper_mean": np.mean(paper_accs) if paper_accs else None,
        "paper_std": np.std(paper_accs) if paper_accs else None,
        "n_results": len(our_accs),
    }
    return summary


def print_comparison_table(results_dict, group_by="depth"):
    """Print a formatted comparison table of our results vs paper.
    group_by: 'depth' groups by depth across sets, 'set' groups by set across depths."""
    if group_by == "depth":
        print("\n" + "=" * 70)
        print(f"{'Depth':<8} {'Our Acc (mean±std)':>20} {'Paper Acc (mean±std)':>22} {'Match':>8}")
        print("=" * 70)
        for d in sorted(set(k[1] if isinstance(k, tuple) else k for k in results_dict)):
            our, pap = [], []
            for k, v in results_dict.items():
                if isinstance(k, tuple) and k[1] == d:
                    our.append(v.get("our_accuracy", 0))
                    pap.append(v.get("paper_accuracy", 0))
            if our:
                match = "✓" if abs(np.mean(our) - np.mean(pap)) < 0.05 else "✗"
                print(f"{d:<8} {np.mean(our):.4f}±{np.std(our):.4f}      {np.mean(pap):.4f}±{np.std(pap):.4f}        {match}")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print(f"{'Set':<8} {'Our Acc':>12} {'Paper Acc':>12} {'Match':>8}")
        print("=" * 70)
        for set_name in ["I", "II", "III"]:
            if set_name in results_dict:
                v = results_dict[set_name]
                our = v.get("our_accuracy", 0)
                pap = v.get("paper_accuracy", 0)
                match = "✓" if abs(our - pap) < 0.05 else "✗"
                print(f"{set_name:<8} {our:>12.4f} {pap:>12.4f} {match:>8}")
        print("=" * 70)
