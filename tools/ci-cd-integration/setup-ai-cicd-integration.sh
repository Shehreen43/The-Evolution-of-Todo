#!/bin/bash
# Script to integrate AI agents into CI/CD pipeline

echo "Setting up AI Agent Integration for CI/CD Pipeline..."

# Create directory structure for CI/CD integration
mkdir -p .github/workflows
mkdir -p .gitlab

# Create a sample GitHub Actions workflow with AI integration
cat << 'EOF' > .github/workflows/ai-enhanced-ci.yml
name: AI-Enhanced CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  docker-ai-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup Docker
      uses: docker/setup-docker-action@v3

    - name: Install Docker AI Agent (Gordon)
      run: |
        # Download and install Gordon
        curl -sSL https://raw.githubusercontent.com/your-repo/gordon-installer/main/install.sh | bash

    - name: Review Dockerfile with Gordon
      env:
        DOCKERFILE_PATH: ./Dockerfile
      run: |
        if [ -f "$DOCKERFILE_PATH" ]; then
          echo "Reviewing Dockerfile with Gordon..."
          gordon review-dockerfile "$DOCKERFILE_PATH"
          gordon optimize-image "$DOCKERFILE_PATH"
        else
          echo "Dockerfile not found at $DOCKERFILE_PATH"
          exit 1
        fi

  k8s-ai-validation:
    runs-on: ubuntu-latest
    needs: docker-ai-review
    if: github.ref == 'refs/heads/main' || github.event_name == 'pull_request'
    steps:
    - uses: actions/checkout@v4

    - name: Setup Kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'

    - name: Install kubectl-ai
      run: |
        # Install kubectl-ai plugin
        # This would be adapted based on actual kubectl-ai installation method
        curl -sSL https://raw.githubusercontent.com/itaysk/kubectl-ai/main/install.sh | bash

    - name: Validate Kubernetes Manifests
      run: |
        # Validate manifests using kubectl-ai
        if [ -d "./k8s/manifests" ]; then
          for manifest in ./k8s/manifests/*; do
            echo "Validating $manifest with kubectl-ai..."
            kubectl ai "validate -f $manifest"
          done
        fi

    - name: Deploy to Test Environment
      if: github.ref == 'refs/heads/main'
      run: |
        # Deploy to test environment using kubectl-ai
        kubectl ai "apply -f ./k8s/manifests/ --namespace=test"
        sleep 30
        kubectl ai "check if all deployments are ready in namespace test"

  ai-security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Security Scan with Gordon
      run: |
        # Build image for security scanning
        if [ -f "./Dockerfile" ]; then
          docker build -t ai-test-app:${{ github.sha }} .

          # Use Gordon for security scanning
          gordon scan-vulnerabilities ai-test-app:${{ github.sha }}
        fi
EOF

# Create a sample GitLab CI configuration with AI integration
cat << 'EOF' > .gitlab/ai-ci-cd.yml
# AI-Enhanced CI/CD Pipeline for GitLab

.docker-ai-review:
  stage: review
  before_script:
    - apt-get update && apt-get install -y curl
    - # Install Gordon (Docker AI Agent)
  script:
    - if [ -f "./Dockerfile" ]; then
        echo "Reviewing Dockerfile with Gordon...";
        gordon review-dockerfile ./Dockerfile;
        gordon optimize-image ./Dockerfile;
      else
        echo "Dockerfile not found";
        exit 1;
      fi
  artifacts:
    reports:
      dotenv: REVIEW_OUTPUT.env

.k8s-ai-validation:
  stage: test
  before_script:
    - # Install kubectl-ai
  script:
    - if [ -d "./k8s/manifests" ]; then
        for manifest in ./k8s/manifests/*; do
          echo "Validating $manifest with kubectl-ai...";
          kubectl ai "validate -f $manifest";
        done
      fi
    - # Deploy to test environment
    - kubectl ai "apply -f ./k8s/manifests/ --namespace=gitlab-test"
    - sleep 30
    - kubectl ai "check if all deployments are ready in namespace gitlab-test"

docker-ai-review-job:
  extends: .docker-ai-review
  only:
    - main
    - merge_requests

k8s-ai-validation-job:
  extends: .k8s-ai-validation
  only:
    - main
  dependencies:
    - docker-ai-review-job
EOF

# Create a sample Jenkins pipeline with AI integration
cat << 'EOF' > jenkins-pipeline/Jenkinsfile-ai.groovy
pipeline {
    agent any

    stages {
        stage('Docker AI Review') {
            steps {
                script {
                    if (fileExists('./Dockerfile')) {
                        sh '''
                            # Install Gordon (Docker AI Agent)
                            ./tools/ai-integration/install-docker-ai-agent.sh

                            # Review Dockerfile with Gordon
                            gordon review-dockerfile ./Dockerfile
                            gordon optimize-image ./Dockerfile
                        '''
                    } else {
                        error("Dockerfile not found")
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh '''
                        # Build Docker image
                        docker build -t ai-test-app:${env.BUILD_NUMBER} .

                        # Scan image with Gordon
                        gordon scan-vulnerabilities ai-test-app:${env.BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('K8s AI Validation') {
            when {
                branch 'main'
            }
            steps {
                script {
                    if (fileExists('./k8s/manifests')) {
                        sh '''
                            # Install kubectl-ai
                            ./tools/k8s-utilities/install-kubectl-ai.sh

                            # Validate manifests with kubectl-ai
                            kubectl ai "apply -f ./k8s/manifests/ --dry-run=server"

                            # Deploy to test environment
                            kubectl ai "apply -f ./k8s/manifests/ --namespace=jenkins-test"

                            # Wait and validate
                            sleep 30
                            kubectl ai "check if all deployments are ready in namespace jenkins-test"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup
                sh '''
                    kubectl ai "delete namespace jenkins-test --ignore-not-found=true"
                ''' || true
            }
        }
    }
}
EOF

# Create a script to run AI-enhanced CI/CD locally for testing
cat << 'EOF' > tools/ci-cd-integration/run-ai-cicd-local.sh
#!/bin/bash
# Script to run AI-enhanced CI/CD pipeline locally for testing

echo "Running AI-Enhanced CI/CD Pipeline Locally..."

# Function to check if required tools are available
check_requirements() {
    local missing_tools=()

    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi

    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi

    if ! command -v gordon &> /dev/null; then
        echo "Installing Gordon (Docker AI Agent)..."
        ./tools/ai-integration/install-docker-ai-agent.sh
    fi

    if ! kubectl ai --help &> /dev/null; then
        echo "Installing kubectl-ai..."
        ./tools/k8s-utilities/install-kubectl-ai.sh
    fi

    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo "Missing required tools: ${missing_tools[*]}"
        echo "Please install them before running this script."
        exit 1
    fi
}

# Function to run Docker AI review
run_docker_ai_review() {
    echo "=== Running Docker AI Review ==="

    if [ -f "./Dockerfile" ]; then
        echo "Found Dockerfile, running Gordon review..."
        gordon review-dockerfile ./Dockerfile
        gordon optimize-image ./Dockerfile
    else
        echo "No Dockerfile found in current directory, skipping Docker review"
    fi
}

# Function to run Kubernetes AI validation
run_k8s_ai_validation() {
    echo "=== Running Kubernetes AI Validation ==="

    if [ -d "./k8s/manifests" ]; then
        echo "Found Kubernetes manifests, validating with kubectl-ai..."
        for manifest in ./k8s/manifests/*; do
            if [ -f "$manifest" ]; then
                echo "Validating $manifest..."
                kubectl ai "validate -f $manifest" 2>&1 || echo "Validation may have warnings or errors for $manifest"
            fi
        done
    else
        echo "No Kubernetes manifests found, skipping K8s validation"
    fi
}

# Function to run security scan
run_security_scan() {
    echo "=== Running Security Scan ==="

    # Build a test image if Dockerfile exists
    if [ -f "./Dockerfile" ]; then
        IMAGE_NAME="local-ai-test:$(date +%s)"
        echo "Building image $IMAGE_NAME for security scanning..."
        docker build -t "$IMAGE_NAME" . 2>/dev/null || {
            echo "Docker build failed, using a sample image for testing..."
            docker pull alpine:latest
            IMAGE_NAME="alpine:latest"
        }

        echo "Scanning image $IMAGE_NAME with Gordon..."
        gordon scan-vulnerabilities "$IMAGE_NAME"

        # Clean up test image
        docker rmi "$IMAGE_NAME" 2>/dev/null || true
    else
        echo "No Dockerfile found, skipping security scan"
    fi
}

# Main execution
main() {
    echo "Starting AI-Enhanced CI/CD Pipeline..."

    check_requirements
    run_docker_ai_review
    run_k8s_ai_validation
    run_security_scan

    echo "=== AI-Enhanced CI/CD Pipeline Complete ==="
    echo "Review the output above for AI-generated insights and recommendations."
    echo "Implement suggested changes before committing your code."
}

# Run main function
main "$@"
EOF

# Make the local CI/CD script executable
chmod +x tools/ci-cd-integration/run-ai-cicd-local.sh

echo "AI Agent Integration for CI/CD Pipeline has been set up!"
echo ""
echo "Files created:"
echo "- .github/workflows/ai-enhanced-ci.yml - GitHub Actions workflow"
echo "- .gitlab/ai-ci-cd.yml - GitLab CI configuration"
echo "- jenkins-pipeline/Jenkinsfile-ai.groovy - Jenkins pipeline example"
echo "- tools/ci-cd-integration/run-ai-cicd-local.sh - Local execution script"
echo ""
echo "To run the AI-enhanced CI/CD pipeline locally:"
echo "  ./tools/ci-cd-integration/run-ai-cicd-local.sh"
echo ""
echo "For production deployment, adapt these templates to your specific CI/CD system and security requirements."
EOF