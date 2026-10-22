# MLOps demo: from `model.pkl` to a public page

One iris classifier is trained, saved as `model.pkl`, and then used by every later step: the command-line predictor, the FastAPI service, Docker, the Streamlit page, GitHub Actions, and Streamlit Community Cloud.

| | |
|---|---|
| Project | https://github.com/Vekri/mlops-demo |
| GitHub Actions | https://github.com/Vekri/mlops-demo/actions |
| Public Streamlit page | https://mlops-demo-pu2vzxx8rafyqsavaglcbr.streamlit.app/ |

## What you will learn

1. Train a scikit-learn Random Forest and save it as `model.pkl`.
2. Record that run in MLflow.
3. Change the four flower measurements and predict again without training.
4. Serve the same file with FastAPI.
5. Give those inputs a page in Streamlit.
6. Package the API and `model.pkl` with Docker.
7. Read request counts in Prometheus and chart them in Grafana.
8. Keep versions with Git and share them on GitHub.
9. Let GitHub Actions check every push.
10. Publish the Streamlit page on Streamlit Community Cloud.

## The four numbers

Every prediction uses four measurements, in centimeters, in this order:

1. Sepal length
2. Sepal width
3. Petal length
4. Petal width

| Example | Flower | Class |
|---|---|---|
| `5.1, 3.5, 1.4, 0.2` | Setosa | 0 |
| `6.0, 2.9, 4.5, 1.5` | Versicolor | 1 |
| `6.7, 3.0, 5.2, 2.3` | Virginica | 2 |

Changing the numbers does not train a new model. The saved forest votes on the new row and returns one of the three classes plus a probability for each class.

## What happens when you open the public page

1. Your browser opens the Streamlit Cloud address.
2. Streamlit Cloud already copied the `main` branch from GitHub. It does not read your laptop, and opening the link does not start GitHub Actions.
3. It runs `mlops_iris_predictor.py`.
4. That file loads `model.pkl` with `joblib` and caches it. It does not fit a new forest.
5. The page starts at `5.1, 3.5, 1.4, 0.2` and shows Setosa, class 0.
6. You paste four numbers and click **Use these numbers**, or you type into the four boxes.
7. Streamlit checks that there are exactly four numbers, reruns the page, and calls `predict` and `predict_proba` on `model.pkl`.
8. The flower name, class number, and three probability bars update.

A later `git push` to `main` does two separate things: GitHub Actions checks that commit, and Streamlit Cloud redeploys the page.

## Files

| File | Job |
|---|---|
| `train.py` | Train on an 80/20 split and write `model.pkl` |
| `train_mlflow.py` | Train again and record the run in `mlflow.db` |
| `predict.py` | Predict one flower from the command line |
| `app.py` | FastAPI service: `/`, `/health`, `POST /predict`, `/metrics` |
| `test_api.py` | API tests used locally and in GitHub Actions |
| `mlops_iris_predictor.py` | Streamlit page. This is the Cloud entry file |
| `model.pkl` | The saved Random Forest used by every predictor |
| `Dockerfile` | API image. Copies `app.py` and `model.pkl` |
| `docker-compose.yml` | API, Prometheus, and Grafana together |
| `prometheus.yml` | Tells Prometheus to scrape `/metrics` every 5 seconds |
| `.github/workflows/ci.yml` | The check that runs on every push to `main` |
| `requirements.txt` | Python packages for the laptop, Actions, Docker, and Cloud |

`model.pkl` is in the repository on purpose. Streamlit Cloud can only use files that were pushed. `mlflow.db` and screenshots stay on the laptop.

## Run it on your laptop

Open PowerShell in this folder before each command:

```powershell
cd C:\Users\Raja Reddy\mlops-demo
```

The same folder is also `C:\Users\Raja Reddy\Desktop\Oct2026\Deploy1\mlops-demo`.

### 1. Train the model

```powershell
python train.py
```

You should see `Accuracy: 1.0` and a new `model.pkl`. The script uses a Random Forest of 100 trees, `random_state=42`, and a 20 percent test split.

### 2. Track the experiment

```powershell
python train_mlflow.py
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000. Choose **Model training**, then **Experiments**, then **iris-classifier**. The training run is `iris_rf_production`. The MCP registry screen is a different page.

### 3. Predict with new numbers

```powershell
python predict.py 6.7 3.0 5.2 2.3
```

Replace the four numbers every time. This command only loads `model.pkl`.

### 4. Open the Streamlit page

```powershell
python -m streamlit run mlops_iris_predictor.py
```

Open the local URL printed in the terminal. If port 8501 is already in use, Streamlit prints another port. Paste `6.7, 3.0, 5.2, 2.3` and click **Use these numbers**.

If the page says `model.pkl` is missing, run `python train.py` in this folder and start Streamlit again.

### 5. Serve the API

```powershell
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs. In **POST /predict**, edit `features` and click **Execute**. The response contains `prediction`, `flower_class`, and `latency_ms`. http://127.0.0.1:8000/metrics is the Prometheus text.

### 6. Run the API in Docker

Stop the local API with `Ctrl+C` first. The local server and the container both want port 8000.

```powershell
docker build -t mlops-demo .
docker run --rm -p 8000:8000 mlops-demo
```

Rebuild after you change `app.py`, `model.pkl`, or `requirements.txt`.

### 7. Start monitoring

Stop the single container with `Ctrl+C`, then:

```powershell
docker compose up -d
```

| Service | Address | Login |
|---|---|---|
| API | http://127.0.0.1:8000/docs | none |
| Prometheus | http://127.0.0.1:9090 | none |
| Grafana | http://127.0.0.1:3000 | `admin` / `admin` |

In Prometheus, open **Graph** and run `http_requests_total`. Grafana starts empty. Add a Prometheus data source at `http://prometheus:9090`, then create a panel. Stop the stack with `docker compose down`.

## GitHub Actions is the check

Every push or pull request to `main` starts a fresh Ubuntu machine. That machine:

1. Checks out that exact commit.
2. Installs `requirements.txt`.
3. Runs `train_mlflow.py`.
4. Stops the job if accuracy is below `0.90`.
5. Runs `pytest test_api.py`.
6. Starts `mlops_iris_predictor.py` and waits for a healthy response.
7. Builds the Docker image.
8. Calls `POST /predict` inside the container.
9. Deletes the machine and leaves the green or red result on the commit.

Open the workflow here: https://github.com/Vekri/mlops-demo/actions

For a manual run, open **MLOps CI**, click **Run workflow**, and enter four comma-separated numbers such as `6.7,3.0,5.2,2.3`.

## CI and CD in this project

CI is the GitHub Actions check. It answers: does this commit train, pass the tests, start Streamlit, and answer a prediction from Docker?

CD is the publish step. Streamlit Community Cloud watches `main` and republishes `mlops_iris_predictor.py`. The Docker image is built during the check and then removed. This workflow does not give the FastAPI service its own public address.

## Docker and Streamlit Cloud

| | Docker | Streamlit Cloud |
|---|---|---|
| What people open | API docs on port 8000 | The public `.streamlit.app` page |
| Program | `app.py` | `mlops_iris_predictor.py` |
| Model | `model.pkl` copied into the image | `model.pkl` loaded from the GitHub repo |
| When it updates | When you rebuild or when Actions builds it | When you push to `main` |
| Who can use it | Your machine, or the temporary Actions runner | Anyone with the link |

## Deploy the page yourself

The live page is already deployed from this repository. To create it again:

1. Open https://share.streamlit.io and sign in with GitHub.
2. Choose **Create app**, then **Yup, I have an app**.
3. Repository: `Vekri/mlops-demo`. Branch: `main`. Main file path: `mlops_iris_predictor.py`.
4. Click **Deploy**.

Cloud installs `requirements.txt`, starts `mlops_iris_predictor.py`, and loads `model.pkl`. It does not use the Dockerfile.
