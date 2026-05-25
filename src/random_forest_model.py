# data manipulation
import pandas as pd
# numerical operations
import numpy as np
# split datasets into training and testing subsets
from sklearn.model_selection import train_test_split
# mean of 0 and a variance of 1
from sklearn.preprocessing import StandardScaler, LabelEncoder
# random forest model for classification
from sklearn.ensemble import RandomForestClassifier  # Import Random Forest Classifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Load the first dataset (heart.csv)
data1 = pd.read_csv(r'C:\users\nitin\Downloads\heart.csv')

# Load the second dataset (cardiovascular.csv), specifying the correct delimiter
data2 = pd.read_csv(r'C:\users\nitin\Downloads\cardio_train.csv', delimiter=';')

# Process the first dataset (data1) with 'Cholesterol' (capital C)
data1['high_risk'] = ((data1['Cholesterol'] > 240) |  
                      (data1['RestingBP'] > 140) |
                      (data1['ExerciseAngina'] == 'y')).astype(int)

# Encode categorical columns for data1
label_encoder = LabelEncoder()
data1['Sex'] = label_encoder.fit_transform(data1['Sex'])  # Encode gender
data1['ChestPainType'] = label_encoder.fit_transform(data1['ChestPainType'])
data1['RestingECG'] = label_encoder.fit_transform(data1['RestingECG'])
data1['ExerciseAngina'] = label_encoder.fit_transform(data1['ExerciseAngina'])
data1['ST_Slope'] = label_encoder.fit_transform(data1['ST_Slope'])

# Splitting features and target for data1
X1 = data1.drop('high_risk', axis=1)
y1 = data1['high_risk']

# Process the second dataset (data2) with 'cholesterol' (lowercase c)
data2['high_risk'] = ((data2['cholesterol'] > 1) |  
                      (data2['ap_hi'] > 140) |
                      (data2['ap_lo'] > 90)).astype(int)

# Encode categorical columns for data2
data2['gender'] = label_encoder.fit_transform(data2['gender'])  # Encode 'Gender'

# Splitting features and target for data2
X2 = data2.drop('high_risk', axis=1)
y2 = data2['high_risk']

# Function to process a dataset
def process_dataset(X, y):
    # Separate train-test splits for each dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled

# Process both datasets
X1_train, X1_test, y1_train, y1_test, X1_train_scaled, X1_test_scaled = process_dataset(X1, y1)
X2_train, X2_test, y2_train, y2_test, X2_train_scaled, X2_test_scaled = process_dataset(X2, y2)

# Function to evaluate the Random Forest model
def evaluate_model(X_train, y_train, X_test, y_test, dataset_name):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)  # Train the model
    y_pred = model.predict(X_test)  # Make predictions

    print(f"Classification Report for {dataset_name}:")
    print(classification_report(y_test, y_pred))
    
    return y_pred, model

# Evaluate Random Forest model for Dataset 1
y1_pred, model1 = evaluate_model(X1_train_scaled, y1_train, X1_test_scaled, y1_test, "Dataset 1")

# Evaluate Random Forest model for Dataset 2
y2_pred, model2 = evaluate_model(X2_train_scaled, y2_train, X2_test_scaled, y2_test, "Dataset 2")

# Visualization of classification reports
def plot_classification_reports(report, title):
    metrics = ['precision', 'recall', 'f1-score']
    df = pd.DataFrame(report).transpose().iloc[:-1]  # Remove last row

    plt.figure(figsize=(10, 5))
    
    # Plotting metrics
    for metric in metrics:
        plt.plot(df.index, df[metric], marker='o', label=f'{metric}')

    # Customize the plot
    plt.title(title)
    plt.xticks(rotation=0)
    plt.ylim(0, 1)
    plt.ylabel('Score')
    plt.xlabel('Classes')
    plt.legend(title='Metrics', loc='lower right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Plot performance for Dataset 1
plot_classification_reports(classification_report(y1_test, y1_pred, output_dict=True),
                            'Dataset 1: Random Forest Model Performance')

# Plot performance for Dataset 2
plot_classification_reports(classification_report(y2_test, y2_pred, output_dict=True),
                            'Dataset 2: Random Forest Model Performance')


# graphing importance chart
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Ensure that `X1` and `y1` are your features and target for Dataset 1
# Repeat similar steps for Dataset 2 if you want a separate graph for it

# Split data into training and test sets for Dataset 1
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

# Train the Random Forest model on Dataset 1
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Get feature importances
feature_importances = model.feature_importances_

# Create a DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': X1.columns,  # X1.columns gets the feature names from Dataset 1
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# Plot feature importances
plt.figure(figsize=(10, 8))
sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
plt.title('Feature Importance for Predicting Heart Disease (Dataset 1)')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

# Optional: Print the importance values
print(importance_df)
