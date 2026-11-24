pipeline {
    agent any
    environment {
        MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Compile Kubeflow Pipeline') { steps { sh '/home/esha/mlops-venv/bin/python pipeline/iris_pipeline.py' } }
        stage('Train & Register in MLflow') { steps { sh '/home/esha/mlops-venv/bin/python pipeline/train_and_register.py' } }
        stage('Deploy to K8s') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl rollout status deployment/iris-model-deployment'
            }
        }
    }
}
