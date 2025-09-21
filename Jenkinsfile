pipeline {
  agent any

  environment {
    REMOTE_USER = "youruser"
    REMOTE_HOST = "your.server.com"
    REMOTE_PATH = "/home/youruser/app"
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
}
