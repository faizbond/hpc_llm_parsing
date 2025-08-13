# seaborn_plot.py

import seaborn as sns
import matplotlib.pyplot as plt

# Load example dataset
df = sns.load_dataset("penguins")

# Create a simple seaborn scatter plot
sns.set(style="whitegrid")
plot = sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm", hue="species")

# Save the plot
plt.title("Penguin Bill Dimensions")
plt.savefig("penguin_plot.png")
print("Plot saved as penguin_plot.png")

# numpy_compute.py

import numpy as np

# Create two random matrices
A = np.random.rand(1000, 1000)
B = np.random.rand(1000, 1000)

# Perform matrix multiplication
C = np.matmul(A, B)

# Print summary statistics
print("Matrix multiplication complete.")
print(f"Result matrix shape: {C.shape}")
print(f"Mean of result: {C.mean():.4f}, Std Dev: {C.std():.4f}")