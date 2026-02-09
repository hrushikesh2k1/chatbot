## Implementing SAST, SCA, DAST in CI/CD

# Configuring self-hosted runner
Go to settings-->Actions-->Runners
click on New self hosted runners
```bash
# Create a folder
$ mkdir actions-runner && cd actions-runner# Download the latest runner package
$ curl -o actions-runner-linux-x64-2.331.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.331.0/actions-runner-linux-x64-2.331.0.tar.gz# Optional: Validate the hash
$ echo "5fcc01bd546ba5c3f1291c2803658ebd3cedb3836489eda3be357d41bfcf28a7  actions-runner-linux-x64-2.331.0.tar.gz" | shasum -a 256 -c# Extract the installer
$ tar xzf ./actions-runner-linux-x64-2.331.0.tar.gz

# Create the runner and start the configuration experience
$ ./config.sh --url https://github.com/hrushikesh2k1/chatbot --token BT62YZBLJGBC5Q6X3FPAEODJRIRPC# Last step, run it!
$ ./run.sh

# Use this YAML in your workflow file for each job
runs-on: self-hosted
```

# YAML file
```yaml
name: CI-CD Pipeline

on:
  push:
    branches:
      - "feature"
      - "integration"
      - "main"
    paths-ignore: [".github/workflows/**", "README.md"]
  pull_request:
    branches:
      - "integration"
      - "main"
    paths-ignore: [".github/workflows/**", "README.md"]
  workflow_dispatch:

jobs:
  build-test:
    runs-on: self-hosted

    steps:
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pip install pytest
          export PYTHONPATH=.
          pytest tests/

  sonarqube-sast:
    name: SonarQube SAST Scan
    runs-on: self-hosted
    needs: build-test

    steps:
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true

      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "17"

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v2
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: http://10.0.2.15:9000

  SCA:
    name: SCAN scan (Dependencies)
    runs-on: self-hosted
    needs: sonarqube-sast
    steps:
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true
        
      - name: checkout code
        uses: actions/checkout@v4
      
      - name: set up python
        uses: actions/checkout@v4
        with:
          python-version: "3.11"
      
      - name: Install pip-audit
        run: |
          sudo apt-get install pipx -y
          pipx ensurepath
          pipx install pip-audit

      - name: Run dependency scan
        run: |
          pip-audit -r requirements.txt
  dast:
    name: DAST Scan (OWASP ZAP)
    runs-on: self-hosted
    needs: SCA   # or deploy-staging depending on where app runs

    steps:
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run OWASP ZAP Baseline Scan
        continue-on-error: true
        run: |
          docker run --rm \
          -v $(pwd):/zap/wrk:rw \
          ghcr.io/zaproxy/zaproxy:stable \
          zap-baseline.py \
          -t http://10.0.2.15:5000 \
          -r zap-report.html

      - name: Upload ZAP Report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: zap-report.html


  deploy-dev:
    if: github.ref == 'refs/heads/feature'
    needs: dast
    runs-on: self-hosted
    environment: development
    env:
      MONGO_URI: ${{ secrets.MONGO_URI }}
    steps:
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true

      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v3
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run application
        run: |
          python app.py &
          sleep 10
      - name: Test API
        run: |
          curl -X POST http://127.0.0.1:5000/ask \
          -H "Content-Type: application/json" \
          -d '{"question":"ci test"}'



  deploy-staging:
    if: github.ref == 'refs/heads/integration'
    needs: dast
    runs-on: self-hosted
    environment: staging
    env:
      MONGO_URI: ${{ secrets.MONGO_URI }}
      
    steps:
      - name: Deploy to Staging
        run: echo "Deploying to Staging"
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true

      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v3
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run application
        run: |
          python app.py &
          sleep 10
      - name: Test API
        run: |
          curl -X POST http://127.0.0.1:5000/ask \
          -H "Content-Type: application/json" \
          -d '{"question":"ci test"}'

  deploy-prod:
    if: github.ref == 'refs/heads/main'
    needs: dast
    runs-on: self-hosted
    environment: production
    env:
      MONGO_URI: ${{ secrets.MONGO_URI }}
      
    steps:
      - name: Deploy to Production
        run: echo "Deploying to Production"
  
      - name: Fix workspace permissions
        run: sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true
      - name: checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v3
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run application
        run: |
          python app.py &
          sleep 9
      - name: Test API
        run: |
          curl -X POST http://127.0.0.1:5000/ask \
          -H "Content-Type: application/json" \
          -d '{"question":"ci test"}'
```

The OWASP Zap reports are download as part of the workflow on to the self hosted runner.

```bash
sudo chown -R $USER:$USER $GITHUB_WORKSPACE || true
```
Give the current runner user ownership of all files inside the GitHub workspace so permission errors don’t happen.
