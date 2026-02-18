# Sydney House Price Prediction

### Project Overview
This project focuses on predicting the selling prices of residential properties across Sydney using historical and socio-economic data. The goal is to assist buyers, sellers, and policy makers by providing a data-driven estimate of housing values.

### Objective
Build a robust regression model capable of predicting house prices based on features such as rent prices, number of rooms, distance to CBD, property size, and other housing attributes.

### Dataset Description
- **Source**: Publicly available government and real estate data
- **Size**: ~11,100 observations
- **Key Variables**:
  - Median house and apartment rent
  - Median apartment price (2020)
  - Distance to CBD (by transport and driving)
  - Property attributes (bedrooms, bathrooms, parking, type)
  - Property inflation index

### Methodology
1. Basic Cleaning and Standardisation
2. Exploratory Data Analysis (EDA)
3. Outlier Treatment and Feature Transformation
4. Multicollinearity Filtering
5. Encoding Categorical Features
6. Baseline Linear Regression
7. Feature Interactions
8. Regularisation (Ridge, Lasso, ElasticNet)
9. Tree-Based Models (Decision Tree, Random Forest)
10. Model Evaluation and Comparison

### Model Performance
| Model                       | RMSE   | MAE    | R²     |
|-----------------------------|--------|--------|--------|
| Linear Regression           | 0.2361 | 0.1743 | 0.8149 |
| Linear + Interactions       | 0.2358 | 0.1741 | 0.8153 |
| Ridge Regression            | 0.2357 | 0.1740 | 0.8155 |
| Lasso Regression            | 0.2358 | 0.1740 | 0.8153 |
| ElasticNet Regression       | 0.2358 | 0.1740 | 0.8153 |
| Decision Tree               | 0.2798 | 0.2019 | 0.7400 |
| Tuned Decision Tree         | 0.2527 | 0.1831 | 0.7880 |
| Random Forest               | 0.2157 | 0.1524 | 0.8455 |

### Insights & Observations
- Linear models perform strongly when combined with interaction terms and regularisation.
- Random Forest outperforms all other models across every metric, capturing complex nonlinear relationships.
- Features like distance to CBD and rental price show high predictive power.

### Requirements
- Python 3.10+
- pandas, numpy, matplotlib, seaborn
- scikit-learn

Install via:
```bash
pip install -r requirements.txt
```

### How to Run
Open the notebook house_price_predictions.ipynb and execute the cells sequentially. Final model comparison and evaluation are at the model

### Future Work
- Make the model universal using pipelines
- Model deployment  using Flask/Streamlit
- Predict on future datasets with different feature distributions

### Author
Atharva Katkar

[GitHub](https://github.com/atharvakatkar) | [LinkedIn](www.linkedin.com/in/ankatkar)