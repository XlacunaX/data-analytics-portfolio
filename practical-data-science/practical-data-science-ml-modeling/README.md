# Machine Learning Modelling – Wine Quality Dataset

This project was completed as part of the **Practical Data Science (with Python)** course in the **Master of Analytics program at RMIT University**.

## Objective
Apply machine learning techniques to analyse the relationship between physicochemical attributes and wine quality.

## Dataset
The dataset contains **4781 wine samples** with physicochemical attributes and a quality score (0–10).

Features include:

- Alcohol
- Density
- pH
- Residual sugar
- Sulphates
- Acidity measures
- Other chemical attributes

## Tools Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

## Methods

### Regression
A **Simple Linear Regression model** was built to examine the relationship between alcohol and density.

Results showed a **negative relationship**, where alcohol concentration decreases as density increases.

### Classification

The following classification models were implemented:

- k-Nearest Neighbours (kNN)
- Modified kNN using PCA
- Decision Tree classifier

Results showed:

- kNN accuracy ≈ **0.47**
- kNN with PCA accuracy ≈ **0.50**
- Decision Tree accuracy ≈ **0.55**, outperforming kNN.

### Clustering

Two clustering techniques were applied:

**K-Means**
- Optimal number of clusters: **k = 2**
- Best silhouette score ≈ **0.22**

**DBSCAN**
- Selected parameters: **MinPts = 3**, **Eps = 2.0**
- Detected clusters and noise points but showed weaker performance compared to K-Means.

## Key Insights

- Alcohol and density show a strong negative relationship.
- PCA slightly improves kNN classification performance.
- Decision Trees perform better than kNN for this dataset.
- K-Means produced more compact clusters than DBSCAN.
