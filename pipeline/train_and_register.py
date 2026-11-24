import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Iris-Classification-Experiment")

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
model_name = "IrisClassifier"

with mlflow.start_run() as run:
    clf = RandomForestClassifier(n_estimators=50, random_state=42).fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    mlflow.log_param("n_estimators", 50)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(
        sk_model=clf,
        name="iris-model",
        registered_model_name=model_name,
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )
    print(f"Logged model with accuracy: {acc:.4f}")

client = MlflowClient()
version = client.get_latest_versions(model_name, stages=["None"])[0].version
client.transition_model_version_stage(name=model_name, version=version, stage="Staging")
client.transition_model_version_stage(name=model_name, version=version, stage="Production")
print(f"Model {model_name} v{version} transitioned to Production!")
