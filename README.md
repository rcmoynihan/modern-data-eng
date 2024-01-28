# The Modern Data Engineering Stack
Accompaniment repository for The Modern Data Engineering Stack presentation.

**Contents:**
- [Pre-Lecture Setup](#pre-lecture-setup)
- [In-Lecture Reference](#in-lecture-reference)

# Pre-Lecture Setup

This section outlines the steps required to set up your environment before attending the lecture. It includes instructions for installations, configurations, and verifications of various tools and technologies. The commands are split for Mac and Windows users where necessary.

## Installations

### 1. Git
- **Mac:** Use Homebrew to install Git. Open a terminal and run:
  ```
  brew install git
  ```
- **Windows:** Download and install Git from [Git for Windows](https://gitforwindows.org/). Follow the installation wizard steps.

### 2. Pyenv and Python 3.10.10
- **Mac:**
  ```
  brew install pyenv
  pyenv install 3.10.10
  ```
- **Windows:** Use [pyenv-win](https://github.com/pyenv-win/pyenv-win) via PowerShell:
  ```
  pyenv install 3.10.10
  ```

### 3. Poetry
- **Mac and Windows:** Install Poetry using the same command for both platforms:
  ```
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### 4. Docker Desktop
- **Mac and Windows:** Download Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop) and follow the installation instructions.

### 5. LocalStack Desktop Client
- **Mac and Windows:** Create a LocalStack account (recommended to use Github as an auth provider) after following [this link](https://app.localstack.cloud/sign-up). Then under [LocalStack Desktop](https://app.localstack.cloud/download) download the client that suits your OS.

### 6. DBeaver and ClickHouse Drivers
- **Mac and Windows:** Download DBeaver from the [DBeaver website](https://dbeaver.io/download/). Install ClickHouse drivers via DBeaver's GUI:
  - Open DBeaver.
  - Navigate to Database > Driver Manager.
  - Find and install the ClickHouse driver.
- _Alternatively_, any DB client that supports ClickHouse is fine (e.g. DataGrip, Looker). You can also just use the [ClickHouse CLI](https://clickhouse.com/docs/en/interfaces/cli) if you prefer a command line interface.

## Configuration

### 1. Clone Repository
- **Mac and Windows:** Open a terminal or command prompt and run:
  ```
  git clone https://github.com/rcmoynihan/modern-data-eng
  ```

### 2. Set Python Version
- **Mac and Windows:** Set your shell to use Python 3.10.10:
  ```
  pyenv global 3.10.10
  ```

### 3. Setup Poetry Environment
- Navigate to the cloned repository:
  ```
  cd modern-data-eng
  ```
- Create, install, and activate the poetry environment:
  ```
  poetry install
  poetry shell
  ```

### 4. Launch Docker Stack
- Navigate to the cloned repository:
  ```
  cd modern-data-eng
  ```
- Run the command:
  ```
  docker-compose up --build
  ```
  This may take a while (5-10 minutes depending on internet speed) on the first run as Docker needs to download all specified containers. Subsequent runs will be faster.

- Use `Crtl + C` to bring the stack down.

## Verify Setup

To ensure that your setup is correct, perform the following verifications _after activating your poetry environment_:

1. **Git Version:** Check Git installation:
   ```
   git --version
   ```
2. **Python Version:** Verify Python version:
   ```
   python --version
   ```
   It should display `Python 3.10.10`.

3. **Poetry Version:** Check Poetry installation:
   ```
   poetry --version
   ```
4. **Docker Version:** Ensure Docker is running:
   ```
   docker --version
   docker-compose --version
   ```
5. **AWS CLI Local:** Confirm awslocal CLI is working:
   ```
   awslocal --version
   ```
6. **DBeaver:** Open DBeaver and ensure ClickHouse drivers are visible in the Driver Manager.

## Troubleshooting
### General Issues
- **An installed CLI tool cannot be found:** Try exiting your terminal completely and reopening a new window to reload. Then, ensure your poetry environment is installed and running properly.

### Python / Poetry Issues
- **Pyenv has issues on newer Macs:** Macs running the M1 chip and later sometimes have issues installing pyenv. See [this article](https://laict.medium.com/install-python-on-macos-11-m1-apple-silicon-using-pyenv-12e0729427a9) for details on how to fix.
- **Poetry issues:** First, ensure that pyenv is running 3.10.10 by checking `python --version` in your current shell. Otherwise, try uninstalling (see command below) and installing with an [alternative method](https://python-poetry.org/docs/#installing-with-pipx).
  ```
  curl -sSL https://install.python-poetry.org | python3 - --uninstall
  ```
### Docker Issues
- **If on Windows:** Ensure WSL2 is configured to work with Docker properly. See this [documentation](https://docs.docker.com/desktop/wsl/) for details.
- **`docker-compose` command not found:** Check you have the most up to date version of Docker Desktop. Alternatively, see this [documentation on ensuring you are on Compose V2](https://docs.docker.com/compose/migrate/).


## Overview of Technologies

Installed manually:
- **Git:** Version control system for tracking changes in source code during software development.
- **Pyenv:** Tool to easily switch between multiple versions of Python.
- **Python 3.10.10:** Our specific version of Python for this setup.
- **Poetry:** Tool for managing dependencies, virtual environments, and packaging in Python.
- **Docker:** Application for building and sharing containerized applications and microservices.
- **Docker Compose:** A tool that allows you to define and manage multi-container Docker applications.
- **LocalStack:** A fully functional local AWS cloud stack for testing and mocking cloud development.
- **awslocal CLI:** A command-line tool to interact with LocalStack services.
- **DBeaver:** Universal database tool for developers, SQL programmers, and database administrators.


Installed via docker-compose:
- **Apache Airflow:** An open-source platform used for orchestrating complex computational workflows and data processing pipelines. In your setup, Airflow is customized with specific configurations for the executor, database connections, SMTP for email notifications, and user setup.
- **PostgreSQL:** A powerful, open-source object-relational database system that uses and extends the SQL language. It's being used here as the database for Apache Airflow.
- **ClickHouse:** An open-source column-oriented database management system capable of real-time generation of analytical data reports.
- **Great Expectations (GX):** Data quality validation tool.
- **MailDev:** An easy-to-use SMTP server for development purposes. It's used here to test email notifications from Airflow.
- **ZooKeeper:** A centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
- **Redis:** An open-source, in-memory data structure store, used as a database, cache, and message broker.


# In-Lecture Reference
Below are certain commands and links that we will be using during the presentation. They are provided here for convienence so that you can simply copy and paste instead of typing things out and making hard to spot typos.

Ensure you are `cd`'d into the project root directory (`modern-data-eng/`) before running commands.

## Links
- [Airflow](http://localhost:8080/)
- [Maildev](http://localhost:1080/)

## Docker Commands
**Launch Docker stack:**
  ```bash
  docker-compose up --build
  ```
## Poetry Commands
**Activate poetry environment:**
  ```bash
  poetry shell
  ```

## AWS Commands
### Batch
**Create Cloudformation stack:**
  ```bash
  awslocal cloudformation create-stack --stack-name modern-data-eng-stack --template-body file://batch/infra.yaml
  ```

**Seed S3 with page view data:**
  ```bash
  python seed_s3.py
  ```

**Package Lambda function code for deployment:**
  ```bash
  python package_lambda.py batch/batch_transform/lambda_function.py batch/batch_transform/requirements.txt batch/batch_transform/batch_transform.zip
  ```

**Update Lambda function code:**
  ```bash
  awslocal lambda update-function-code --function-name [function_name] --zip-file fileb://batch/batch_transform/batch_transform.zip
  ```

### Real Time
**Update Cloudformation stack:**
  ```bash
  awslocal cloudformation update-stack --stack-name modern-data-eng-stack --template-body file://real_time/infra.yaml
  ```

**Package Lambda function code for deployment (S3 Processor):**
  ```bash
  python package_lambda.py real_time/s3_event_processor/lambda_function.py real_time/s3_event_processor/requirements.txt real_time/s3_event_processor/s3_event_processor.zip
  ```

**Update Lambda function code (S3 Processor):**
  ```bash
  awslocal lambda update-function-code --function-name [function_name] --zip-file fileb://real_time/s3_event_processor/s3_event_processor.zip
  ```

**Package Lambda function code for deployment (Price Adjuster):**
  ```bash
  python package_lambda.py real_time/price_adjuster/lambda_function.py real_time/price_adjuster/requirements.txt real_time/price_adjuster/price_adjuster.zip
  ```

**Update Lambda function code (Price Adjuster):**
  ```bash
  awslocal lambda update-function-code --function-name [function_name] --zip-file fileb://real_time/price_adjuster/price_adjuster.zip
  ```

**Display live Redis values:**
  ```bash
  python real_time/poll_redis.py
  ```

**Upload one file to S3:**
  ```bash
  python seed_s3.py --num-records 1
  ```