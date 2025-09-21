pipeline {
  agent any

  environment {
    APP_ID = "a0QtXXT23YRgkKFhyPzzh"
  }

  parameters {
    string(name: 'DEPLOY_URL_CRED_ID', defaultValue: 'DEPLOY_URL', description: 'Credentials ID for the deployment URL (Secret Text)')
    string(name: 'DEPLOY_KEY_CRED_ID', defaultValue: 'DEPLOY_KEY', description: 'Credentials ID for the deployment API key (Secret Text)')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Env setup') {
      steps {
        sh 'python3 -m venv .venv'
      }
    }

    stage('Install requirements') {
      steps {
        sh '.venv/bin/pip install -r requirements.txt'
      }
    }

    stage('Migrations') {
      steps {
        sh '.venv/bin/python manage.py makemigrations'
        sh '.venv/bin/python manage.py migrate'
      }
    }

    stage('Unit Tests') {
      steps {
        sh '.venv/bin/python manage.py test'
      }
    }

    stage('Start Server') {
      steps {
        sh '.venv/bin/python manage.py runserver 0.0.0.0:8000 &'
        sh 'sleep 5' // wait for server to boot
      }
    }

    stage('API Test') {
      steps {
        sh '.venv/bin/python check.py'
      }
    }
  }

  post {
    success {
      echo "✅ Tests passed, triggering deployment API..."
      withCredentials([
        string(credentialsId: params.DEPLOY_URL_CRED_ID, variable: 'DEPLOY_URL'),
        string(credentialsId: params.DEPLOY_KEY_CRED_ID, variable: 'DEPLOY_KEY')
      ]) {
        sh '''
          curl -X POST \
            "$DEPLOY_URL" \
            -H "accept: application/json" \
            -H "Content-Type: application/json" \
            -H "x-api-key: $DEPLOY_KEY" \
            -d "{\"applicationId\": \"$APP_ID\"}"
        '''
      }
    }

    failure {
      echo "❌ Pipeline failed, sending error email..."
    }
  }
}
