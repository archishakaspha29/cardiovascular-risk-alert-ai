# AI-Assisted Cardiovascular Risk-Alert Tool for Underserved Communities 

## Overview 

This project is an AI-assisted cardiovascular risk-alert prototype designed to support early care-seeking for underserved communities. The goal is to help users better understand possible cardiovascular risk factors and recognize when they may need to seek attention.
This project uses machine learning to analyze cardiovascular health indicators and provide a risk-alert output. It is designed as an educational and decision-support prototype, not as a replacement for a physician.

## Medical Disclaimer

This project is not a medical diagnosis tool. It does not replace professonal medical care, diagonsis, or treatment. If a used is experiencing cheat pain, shortness of breath, fainting, servere weakness, or other emergency symptoms, they should seek emergency medical help immediately

## Problem Statement

Many low-income families and underserved communities may not always have timely access to healthcare. In serios situations, delayed care can increase health risks. Cardovascular disease is one of the leading causes of death globally, so early awareness of risk factors can help people seek care sooner.

This project explore how artificial intelligence can be used responsibly to support risk awareness, especially for people who may face barriers to healthcare access.

## Project Goal

The goal of this project is to build a machine-learning based cardiovascular risk-alert tool that:

- Identifies possible cardiovascular risk patterns
- Supports early care-seeking behavior
- Uses public health datasets
- Considers fairness, bias, and underrepresentation in healthcare data
- Provides explainable results through feature importance

## Tools and Libraries Used:

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest Classifier
- Matplotlib
- Seaborn
- Kaggl public datasets

## Methodology:

The project uses public cardiovascular health datasets to train and evaluate a machine learning model

Main steps:

1. Load cardiovascular datasets
2. Clean and preprocess the data
3. Encode categorical variables
4. Engineer a high-risk label using clinically relevant indicators
5. Split the data into training and testing sets
6. Train a Random Forest classification model
7. Evaluate the model using accuracy, precision, recall, and F1-score
8. Visualize model performance and feature importance
9. Review bias, fairness, and ethical concerns

## Machine Learning Model

The main model used is a Random Forest Classifier. This model was selected because it can handle multiple health-related features and provide feature importance, which helps explain which factors contribute most to the model's prediction.

## Ethical AI and Bias Considerations

This project considers ethical AI issues in healthcare, including:

- Bias in training data
- Underrepresentation of certain demogrpahic groups
- Tranparency and explainability
- Privacy and consent
- Fair access to healthcare tools
- Responsible use of sensitive demographic information

Synthetic data and guardrails are considered as possible strategies to reduce underepresentation and improve fairness. Race and demographic variables should be treated carefully, as they may reflect social, environmental, and healthcare-access disparities rather than direct biological causes.

## Results 

The model showed strong performance on the available public test datasets. Evaluation metrics included accuracy, precision, recall, and F1-score

The results are based only on the available public datasets and should not be interpreted as clinical validation. Future testing with larger, more diverse and medically reviewed datasets is needed before real-world use.

As of now the model has achieved very high performance on the available public datasets, but these results should be interpreted carefully because the risk label was engineered using clinically relevant indicators. Future work includes external validation on larger, more diverse datasets.

## Limitations

This project has several limitations:

- It uses public datasets, which may not fully represent all populations
- The model has not been clinically validated
- The tool should not be used for diagonsis or treatment decisions
- More diverse datasets are needed to improve fairness
- Medical expert review is needed befpre any real-world deployment

  ## Future Work

  Future improvements may include:

  - Building a user-friendly web or mobile app
  - Adding a cleared risk explanation for users
  - Testing the model on larger and more diverse datasets
  - Adding fairness metrics by demographic group
  - Improving the user interface for accessibility
  - Getting feedback from healthcare professionals
  - Adding emergency-care guidance and safety guardrails
  - Publishing the app as a health education and risk awareness tool
    
## Project Status

This project is currently a prototype. The longterm goal is to develop it into a safer, more polished cardiovascular risk-awareness app that can support underserved communities while following responsible AI, privacy, and medical safety guidelines.
