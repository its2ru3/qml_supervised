"""Visualization utilities for the VQC paper reproduction project."""

import numpy as np
import matplotlib.pyplot as plt


def plot_kernel_matrix(kernel_matrix, title="Quantum Kernel Matrix", ax=None):
    """Plot a heatmap of the quantum kernel matrix."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(kernel_matrix, cmap="Blues", vmin=0, vmax=1)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Sample index")
    ax.set_ylabel("Sample index")
    plt.colorbar(im, ax=ax, label="Fidelity")
    if ax is None:
        plt.tight_layout()
        plt.show()


def plot_data(X, y, title="Dataset"):
    """Scatter plot of 2D data colored by label."""
    fig, ax = plt.subplots(figsize=(6, 5))
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors="k", s=50)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Feature $x_1$")
    ax.set_ylabel("Feature $x_2$")
    plt.tight_layout()
    plt.show()


def plot_decision_boundary(classifier, X, y, title="Decision Boundary", grid_steps=30):
    """Plot decision boundary for a 2D classifier (QSVC or VQC)."""
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, grid_steps),
                         np.linspace(y_min, y_max, grid_steps))
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = classifier.predict(grid_points)
    Z = Z.reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdBu)
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors="k", s=50)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Feature $x_1$")
    ax.set_ylabel("Feature $x_2$")
    plt.tight_layout()
    plt.show()


def plot_accuracy_vs_depth(depths, our_test_accs, paper_accs, our_train_accs=None, title="VQC Accuracy vs. Depth",
                           train_errs=None, test_errs=None, paper_errs=None):
    """Plot accuracy vs depth with two or three curves (our test, paper test, optional our train).
    Optionally include error bars (standard error of mean) when multiple splits are provided."""
    fig, ax = plt.subplots(figsize=(9, 6))

    if our_train_accs is not None:
        ax.errorbar(depths, our_train_accs, yerr=train_errs, fmt='o-', label="Our VQC (train)",
                    color="#2ecc71", linewidth=2, markersize=8, capsize=4)
    ax.errorbar(depths, our_test_accs, yerr=test_errs, fmt='s-', label="Our VQC (test)",
                color="#3498db", linewidth=2, markersize=8, capsize=4)
    ax.errorbar(depths, paper_accs, yerr=paper_errs, fmt='D--', label="Paper (test)",
                color="#e74c3c", linewidth=2, markersize=8, capsize=4)

    ax.set_xlabel("Feature Map Depth $d$", fontsize=12)
    ax.set_ylabel("Accuracy", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(depths)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_loss_convergence(loss_histories, depths, title="VQC Training Loss Convergence"):
    """Plot training loss curves for each depth on the same axes with a legend.
    loss_histories: dict mapping depth -> list of loss values, or list of lists."""
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(depths)))

    for d, color in zip(depths, colors):
        hist = loss_histories[d] if isinstance(loss_histories, dict) else loss_histories[depths.index(d)]
        if len(hist) > 0:
            ax.plot(range(1, len(hist) + 1), hist, label=f"d={d}", color=color, linewidth=1.5)

    ax.set_xlabel("Optimizer Iteration", fontsize=12)
    ax.set_ylabel("Loss", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(title="Feature Map Depth", fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_kernel_comparison(kernels_ideal, kernels_noisy, titles=None):
    """Side-by-side comparison of ideal vs noisy kernel matrices (reproduces Fig. 4 from the paper).
    kernels_ideal and kernels_noisy can be single matrices or lists of matrices."""
    if not isinstance(kernels_ideal, list):
        kernels_ideal = [kernels_ideal]
        kernels_noisy = [kernels_noisy]

    n = len(kernels_ideal)
    fig, axes = plt.subplots(n, 2, figsize=(12, 5 * n))
    if n == 1:
        axes = axes.reshape(1, 2)

    for i in range(n):
        title_ideal = titles[i] if titles and i < len(titles) else f"Set {i+1}"
        im0 = axes[i, 0].imshow(kernels_ideal[i], cmap="Blues", vmin=0, vmax=1)
        axes[i, 0].set_title(f"{title_ideal} — Ideal", fontsize=12)
        plt.colorbar(im0, ax=axes[i, 0], label="Fidelity")

        im1 = axes[i, 1].imshow(kernels_noisy[i], cmap="Blues", vmin=0, vmax=1)
        axes[i, 1].set_title(f"{title_ideal} — Noisy + Mitigated", fontsize=12)
        plt.colorbar(im1, ax=axes[i, 1], label="Fidelity")

        # Compute max deviation
        max_dev = np.max(np.abs(kernels_ideal[i] - kernels_noisy[i]))
        axes[i, 1].set_xlabel(f"Max |ΔK| = {max_dev:.4f}", fontsize=10)

    plt.suptitle("Kernel Matrix Comparison: Ideal vs Noisy+Mitigated", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_classification_histogram(accuracies_per_set, depths, paper_accuracies):
    """Histogram of classification success rates across test sets for each depth,
    matching Fig. 3c from the paper. Each depth gets a subplot showing the distribution
    of test accuracies, with mean marked as a dot and paper accuracy as a vertical line.
    accuracies_per_set: dict mapping depth -> list of test accuracies (one per set)."""
    n_depths = len(depths)
    fig, axes = plt.subplots(1, n_depths, figsize=(4 * n_depths, 5), sharey=True)
    if n_depths == 1:
        axes = [axes]

    for idx, d in enumerate(depths):
        accs = accuracies_per_set[d]
        mean_acc = np.mean(accs)

        axes[idx].hist(accs, bins=10, range=(0, 1), color="#3498db", alpha=0.7, edgecolor="white")
        axes[idx].axvline(mean_acc, color="#2ecc71", linewidth=2, linestyle="-",
                          label=f"Mean={mean_acc:.3f}")
        axes[idx].axvline(paper_accuracies[idx], color="#e74c3c", linewidth=2, linestyle="--",
                          label=f"Paper={paper_accuracies[idx]:.3f}")
        axes[idx].set_title(f"Depth $d={d}$", fontsize=12)
        axes[idx].set_xlabel("Test Accuracy", fontsize=10)
        if idx == 0:
            axes[idx].set_ylabel("Count", fontsize=10)
        axes[idx].legend(fontsize=8)
        axes[idx].set_xlim(0, 1.05)

    plt.suptitle("Classification Success Rate Distribution (Fig. 3c)", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_data_with_labels(X, y, support_vectors=None, title=""):
    """Scatter plot of 2D data with optional support vector highlighting (green circles),
    matching Fig. 3b from the paper."""
    fig, ax = plt.subplots(figsize=(7, 6))

    # Plot all data points
    mask_pos = y == 1
    mask_neg = y == -1
    ax.scatter(X[mask_pos, 0], X[mask_pos, 1], c="#e74c3c", edgecolors="k", s=50, label="Class +1")
    ax.scatter(X[mask_neg, 0], X[mask_neg, 1], c="#3498db", edgecolors="k", s=50, label="Class -1")

    # Highlight support vectors if provided
    if support_vectors is not None:
        ax.scatter(support_vectors[:, 0], support_vectors[:, 1],
                   s=200, facecolors="none", edgecolors="#2ecc71", linewidths=2,
                   label="Support Vectors")

    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Feature $x_1$")
    ax.set_ylabel("Feature $x_2$")
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.show()
