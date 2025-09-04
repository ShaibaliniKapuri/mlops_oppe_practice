# Heart Disease Prediction API with ML Governance & CI/CD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

This project demonstrates a complete, end-to-end MLOps workflow for a Heart Disease Prediction service. It includes model training, a rigorous analysis of fairness and explainability, containerization with Docker, and fully automated deployment to Google Kubernetes Engine (GKE) using a GitHub Actions CI/CD pipeline.

---

## ✨ Salient Features

This project is a robust example of modern machine learning engineering, integrating several key professional practices:

* End-to-End Automation (CI/CD): The pipeline, managed by **GitHub Actions*, automates the entire lifecycle from code commit to a live production endpoint. This eliminates manual steps, reduces human error, and ensures rapid, repeatable deployments.

* Containerization and Orchestration: Using **Docker* to package the application and *Kubernetes* to deploy it ensures consistency across all environments. This approach guarantees that the model runs the same way anywhere and can be easily scaled to handle more traffic.

* Infrastructure as Code (IaC)*: The kubernetes/deployment.yaml file defines the entire production infrastructure in code, making the setup version-controlled, transparent, and easy to replicate or modify.

* Responsible AI Governance*: The project goes beyond just training a model. The MLGovernance.ipynb notebook explicitly incorporates *fairness audits, **model explainability (XAI), and **data drift detection*, which are crucial for building trustworthy and reliable AI systems.

* API-First Design: By serving the model via a **FastAPI* endpoint, the project makes the model's predictive power easily accessible to other applications and services, which is a cornerstone of MLOps.

* Automated Deployment Reporting: The use of **Continuous Machine Learning (CML)* to automatically comment on a commit with the live IP address provides immediate feedback to developers, closing the loop between deployment and validation.

---

## 🔬 Deep Dive: Model Explainability & Bias Experimentation

The MLGovernance.ipynb notebook is central to the project's commitment to responsible AI. It moves beyond simple accuracy metrics to ask critical questions: "Is the model fair?" and "Why does it make the decisions it does?"

### Model Fairness & Bias Experimentation (with Fairlearn)

The analysis uses the *Fairlearn* library to audit the model for bias across two sensitive attributes: *sex* and *age_category*.

* *Demographic Parity Difference*: This metric checks if the model predicts positive outcomes (i.e., "heart disease") at the same rate across different groups.
    * Finding: The notebook found a demographic parity difference of **0.27* for the age_category group. A value greater than zero indicates a disparity. This means that the model is *significantly more likely to predict heart disease for one age group over another*, regardless of whether it's correct. This is a clear sign of bias.

* *Equalized Odds Difference: This is a stricter fairness criterion that checks if the model's error rates—specifically the **true positive rate* and *false positive rate*—are equal across groups. A fair model should perform equally well (and make mistakes at the same rate) for everyone.
    * Finding: The analysis showed a high equalized odds difference (e.g., **0.28* for Class 0), revealing that the model's ability to correctly identify patients with and without heart disease is *unequal across different groups*.

* *MetricFrame Analysis*: This provided the most direct evidence of performance disparity.
    * Finding: For the sex attribute, the model's *balanced accuracy* was *0.41* for one group but only *0.29* for the other. This concretely shows that the model is *less accurate and less reliable for one gender group*, which could lead to harmful outcomes in a real-world medical scenario.

> Conclusion on Bias: The experimentation proves the model is *not fair*. It exhibits biases that lead to performance disparities between different demographic groups. Before deploying this model responsibly, these fairness issues would need to be addressed through techniques like data re-weighting or applying fairness-aware training algorithms.

### Model Explainability (with SHAP)

The project uses *SHAP (SHapley Additive exPlanations)* to open up the "black box" of the logistic regression model and understand its decision-making process.



* Global Explainability (Summary Plots)*: The SHAP summary plots provide a panoramic view of what the model learned. They rank features by their overall importance and show how the value of a feature impacts the prediction.
    * *Insight*: These plots reveal that features like thal (thalassemia), ca (number of major vessels), and cp (chest pain type) are the most influential drivers of the model's predictions. More importantly, they show how they influence it—for example, a high value for ca (represented by a red dot) strongly pushes the prediction away from a "no heart disease" diagnosis.

* Local Explainability (Force Plots): The force plot visualizes the reasoning for a **single, specific prediction*.
    * *Insight*: This plot shows a tug-of-war among features. For one patient, a high age might push the prediction towards "heart disease," while a normal trestbps (resting blood pressure) pulls it back. This allows a data scientist or doctor to understand and trust (or question) the model's reasoning on a case-by-case basis.

> *Conclusion on Explainability*: The SHAP analysis provides crucial transparency. It confirms that the model is focusing on medically relevant features and allows for the deep-diving of individual predictions, which is essential for debugging, building trust, and ensuring the model's logic aligns with domain expertise.

---

## 📂 Project Structure
This MLOps project is structured to automate the deployment and monitoring of a machine learning model. Here's a breakdown of the key components and the overall workflow:

```
mlops_oppe_practice/
├── .github/
│   └── workflows/
│       └── cd.yml
├── kubernetes/
│   └── deployment.yaml
├── Dockerfile
├── MLGovernance.ipynb
├── data_drift_report.html
├── model.joblib
├── requirements.txt
├── serve.py
└── train.py
```

-----

### Core Components

  * **`train.py`**: This script handles the model training process. It loads a dataset, trains a machine learning model, and then saves the trained model to the `model.joblib` file.

  * **`serve.py`**: This script is responsible for serving the trained model as an API. It loads the `model.joblib` file and creates an endpoint (likely a REST API) that can receive data and return model predictions.

  * **`model.joblib`**: This is the serialized, trained machine learning model. It's the output of `train.py` and the input for `serve.py`.

  * **`requirements.txt`**: This file lists all the Python libraries and dependencies required to run the project, ensuring a consistent environment for training and serving.

-----

### MLOps and Automation

  * **`.github/workflows/cd.yml`**: This file defines a GitHub Actions workflow for Continuous Delivery (CD). This workflow automates the process of building, testing, and deploying the model whenever changes are pushed to the repository.

  * **`Dockerfile`**: This file contains the instructions to build a Docker image. The image packages the application code (`serve.py`), the trained model (`model.joblib`), and all the necessary dependencies from `requirements.txt` into a portable container.

  * **`kubernetes/deployment.yaml`**: This is a Kubernetes configuration file that defines how the Docker container will be deployed and managed in a Kubernetes cluster. It specifies details like the number of replicas, resource allocation, and how the service will be exposed.

-----

### Governance and Monitoring

  * **`MLGovernance.ipynb`**: This Jupyter Notebook is likely used for experimentation, analysis, and documentation related to machine learning governance. This could include tasks like checking for model bias, ensuring fairness, and providing model explanations.

  * **`data_drift_report.html`**: This HTML file is a report that visualizes data drift. Data drift occurs when the statistical properties of the production data change over time, which can degrade model performance. This report is a key part of monitoring the model in production.
