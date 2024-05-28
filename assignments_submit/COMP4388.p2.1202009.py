import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix,roc_curve, auc
from chefboost import Chefboost as chef



def load_data():
    url = "C:\Data.csv"
    data = pd.read_csv(url)
    return data


def plot_class_distribution(data):
    plt.figure(figsize=(8, 6))
    data['Smoker'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Distribution of Smoker Class Label')
    plt.xlabel('Smoker')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.show()


def plot_age_density(data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data['Age'], fill=True, color='skyblue', alpha=0.7)
    plt.title('Density Plot for Age')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.show()


def plot_bmi_density(data):
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data['BMI'], fill=True, color='orange', alpha=0.7)
    plt.title('Density Plot for BMI')
    plt.xlabel('BMI')
    plt.ylabel('Density')
    plt.show()


def plot_scatter_by_region(data):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Age', y='BMI', hue='Region', data=data, palette='viridis')
    plt.title('Scatter Plot of Age vs BMI, Colored by Region')
    plt.xlabel('Age')
    plt.ylabel('BMI')
    plt.show()


def split_data(data):
    data_encoded = pd.get_dummies(data, columns=['Gender', 'Region', 'Smoker'], drop_first=True)
    X = data_encoded.drop('Smoker_yes', axis=1)
    y = data_encoded['Smoker_yes']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def knn_evaluation(X_train, X_test, y_train, y_test, k_values):
    results_table = pd.DataFrame(columns=['K', 'Accuracy', 'AUC', 'Confusion Matrix'])

    for k in k_values:
        knn_model = KNeighborsClassifier(n_neighbors=k)
        knn_model.fit(X_train, y_train)
        y_pred = knn_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, knn_model.predict_proba(X_test)[:, 1])
        cm = confusion_matrix(y_test, y_pred)

        result_row = pd.DataFrame({
            'K': [k],
            'Accuracy': [accuracy],
            'AUC': [auc],
            'Confusion Matrix': [cm]
        })
        result_row = result_row.astype({'K': int, 'Accuracy': float, 'AUC': float, 'Confusion Matrix': object})
        results_table = pd.concat([results_table, result_row], ignore_index=True)
    plot_knn_results(results_table)

    return results_table

def plot_knn_results(results_table):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(results_table['K'], results_table['Accuracy'], marker='o', label='Accuracy')
    plt.xlabel('K')
    plt.ylabel('Accuracy')
    plt.title('KNN - Accuracy vs K')

    plt.subplot(1, 2, 2)
    plt.plot(results_table['K'], results_table['AUC'], marker='o', label='AUC')
    plt.xlabel('K')
    plt.ylabel('AUC')
    plt.title('KNN - AUC vs K')

    plt.tight_layout()
    plt.show()


def decision_tree(X_train, X_test, y_train, y_test, config=None):
    target_column = 'Smoker_yes'
    train_data = pd.concat([X_train, y_train], axis=1).reset_index(drop=True)
    if config is None:
        config = {
            'algorithm': 'C4.5',
            'split_criterion': 'gini',
            'max_depth': 5
        }
    model = chef.fit(train_data, config=config, target_label=target_column)
    test_data = pd.concat([X_test, y_test], axis=1).reset_index(drop=True)
    predictions = test_data.apply(lambda row: chef.predict(model, row), axis=1)
    cm = confusion_matrix(y_test, predictions)
    print("Confusion Matrix:")
    print(cm)
    fpr, tpr, _ = roc_curve(y_test, predictions)
    auc_val = auc(fpr, tpr)
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy:", accuracy)
    print("AUC:", auc_val)
    return
def naive_bayes(X_train, X_test, y_train, y_test):
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    y_pred = nb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    y_prob = nb_model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    results_table = pd.DataFrame({
        'Model': ['Naive Bayes'],
        'Accuracy': [accuracy],
        'AUC': [auc_score],
        'Confusion Matrix': [cm]
    })
    plot_nb_results(results_table)
    return results_table




def plot_nb_results(results_table):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.heatmap(results_table['Confusion Matrix'].iloc[0], annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Naive Bayes - Confusion Matrix')

    plt.subplot(1, 2, 2)
    plt.bar(['Accuracy', 'AUC'], results_table[['Accuracy', 'AUC']].iloc[0])
    plt.ylim(0, 1)
    plt.title('Naive Bayes - Accuracy and AUC')

    plt.tight_layout()
    plt.show()

def ann(X_train, X_test, y_train, y_test):
    ann_model = MLPClassifier(hidden_layer_sizes=(50,), activation='logistic', max_iter=500, random_state=42)
    ann_model.fit(X_train, y_train)
    y_pred = ann_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, ann_model.predict_proba(X_test)[:, 1])
    cm = confusion_matrix(y_test, y_pred)

    results_table = pd.DataFrame({
        'Model': ['ANN'],
        'Accuracy': [accuracy],
        'AUC': [auc],
        'Confusion Matrix': [cm]
    })

    plot_ann_results(results_table)

    return results_table

def plot_ann_results(results_table):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.heatmap(results_table['Confusion Matrix'].iloc[0], annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('ANN - Confusion Matrix')

    plt.subplot(1, 2, 2)
    plt.bar(['Accuracy', 'AUC'], results_table[['Accuracy', 'AUC']].iloc[0])
    plt.ylim(0, 1)
    plt.title('ANN - Accuracy and AUC')

    plt.tight_layout()
    plt.show()

def basic_statistics(data):
    print("\nBasic Statistics:")
    print(data.describe())

def main():
    data = load_data()

    while True:
        print("\nMenu:")
        print("1. Plot Distribution of Smoker Class Label")
        print("2. Plot Density for Age")
        print("3. Plot Density for BMI")
        print("4. Visualize Scatter Plot by Region")
        print("5. Split Dataset into Training and Test Sets")
        print("6. Compare KNN with Different Values of K")
        print("7. Run Naive Bayes")
        print("8. Run ANN")
        print("9. Run Decision Tree")
        print("10. Display Basic Statistics")
        print("11. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10/11): ")

        if choice == '1':
            plot_class_distribution(data)
        elif choice == '2':
            plot_age_density(data)
        elif choice == '3':
            plot_bmi_density(data)
        elif choice == '4':
            plot_scatter_by_region(data)
        elif choice == '5':
            X_train, X_test, y_train, y_test = split_data(data)
            print("Dataset split into training and test sets.")
        elif choice == '6':
            if 'X_train' not in locals():
                print("Please split the dataset first (Option 5) before comparing KNN.")
            else:
                k_values = [3, 5, 10]  # You can adjust these values
                results_table = knn_evaluation(X_train, X_test, y_train, y_test, k_values)
                print("\nResults for KNN:")
                print(results_table)
        elif choice == '7':
            if 'X_train' not in locals():
                print("Please split the dataset first (Option 5) before running Naive Bayes.")
            else:
                results_table = naive_bayes(X_train, X_test, y_train, y_test)
                print("\nResults for Naive Bayes:")
                print(results_table)
        elif choice == '8':
            if 'X_train' not in locals():
                print("Please split the dataset first (Option 5) before running ANN.")
            else:
                results_table = ann(X_train, X_test, y_train, y_test)
                print("\nResults for ANN:")
                print(results_table)
        elif choice == '9':
            if 'X_train' not in locals():
                print("Please split the dataset first (Option 5) before running Decision Trees.")
            else:
                results_table = decision_tree(X_train, X_test, y_train, y_test)
                print("\nResults for Decision Trees:")
                print(results_table)
        elif choice == '10':
            basic_statistics(data)
        elif choice == '11':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, or 11.")


if __name__ == "__main__":
    main()