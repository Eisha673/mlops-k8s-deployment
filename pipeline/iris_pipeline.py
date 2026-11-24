from kfp import dsl, compiler

@dsl.component(base_image="python:3.11-slim", packages_to_install=["scikit-learn", "pandas"])
def load_and_preprocess(dataset_path: dsl.OutputPath("CSV")):
    import pandas as pd
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    df = iris.frame
    df.to_csv(dataset_path, index=False)
    print(f"Dataset saved with shape: {df.shape}")

@dsl.component(base_image="python:3.11-slim", packages_to_install=["scikit-learn", "pandas", "joblib"])
def train_model(dataset_path: dsl.InputPath("CSV"), model_path: dsl.OutputPath("Model"), test_data_path: dsl.OutputPath("CSV")):
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv(dataset_path)
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    joblib.dump(clf, model_path)
    test_df = X_test.copy()
    test_df["target"] = y_test
    test_df.to_csv(test_data_path, index=False)
    print("Model trained successfully.")

@dsl.component(base_image="python:3.11-slim", packages_to_install=["scikit-learn", "pandas", "joblib"])
def evaluate_model(model_path: dsl.InputPath("Model"), test_data_path: dsl.InputPath("CSV")) -> float:
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score

    clf = joblib.load(model_path)
    test_df = pd.read_csv(test_data_path)
    X_test = test_df.drop(columns=["target"])
    y_test = test_df["target"]

    preds = clf.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    print(f"Model Evaluation Accuracy: {acc:.4f}")
    return acc

@dsl.pipeline(name="iris-classification-pipeline", description="End-to-end Iris ML pipeline")
def iris_pipeline():
    prep_task = load_and_preprocess()
    train_task = train_model(dataset_path=prep_task.outputs["dataset_path"])
    eval_task = evaluate_model(
        model_path=train_task.outputs["model_path"],
        test_data_path=train_task.outputs["test_data_path"]
    )

if __name__ == "__main__":
    compiler.Compiler().compile(iris_pipeline, "pipeline/iris_pipeline.yaml")
    print("Compiled pipeline/iris_pipeline.yaml successfully!")
