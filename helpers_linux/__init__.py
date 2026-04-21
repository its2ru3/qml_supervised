"""Helper modules for the VQC paper reproduction project."""
import importlib

# Import submodules
from . import data, visualization, circuits, noise, metrics

# Reload submodules (this runs every time helpers is reloaded)
importlib.reload(data)
importlib.reload(visualization)
importlib.reload(circuits)
importlib.reload(noise)
importlib.reload(metrics)

# Re-export fresh references
# ---- data ----
load_paper_csv = data.load_paper_csv
load_paper_classification = data.load_paper_classification
DATA_DIR = data.DATA_DIR
load_all_kernel_sets = data.load_all_kernel_sets
load_all_variational_sets = data.load_all_variational_sets

# ---- visualization ----
plot_kernel_matrix = visualization.plot_kernel_matrix
plot_data = visualization.plot_data
plot_decision_boundary = visualization.plot_decision_boundary
plot_accuracy_vs_depth = visualization.plot_accuracy_vs_depth
plot_loss_convergence = visualization.plot_loss_convergence
plot_kernel_comparison = visualization.plot_kernel_comparison
plot_classification_histogram = visualization.plot_classification_histogram
plot_data_with_labels = visualization.plot_data_with_labels

# ---- circuits ----
build_paper_feature_map = circuits.build_paper_feature_map
build_paper_ansatz = circuits.build_paper_ansatz
parity_interpret = circuits.parity_interpret
build_custom_rx_zz_circuit = circuits.build_custom_rx_zz_circuit

# ---- noise ----
create_noisy_sampler = noise.create_noisy_sampler
apply_readout_mitigation = noise.apply_readout_mitigation
zero_noise_extrapolation = noise.zero_noise_extrapolation

# ---- metrics ----
compute_paper_accuracy = metrics.compute_paper_accuracy
compare_with_paper = metrics.compare_with_paper
aggregate_results = metrics.aggregate_results