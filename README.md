# MLOps demo

Train an iris classifier, track the run, serve predictions, and check the result in GitHub Actions.

Repository: https://github.com/Vekri/mlops-demo

Open PowerShell in this folder before each command:

```powershell
cd C:\Users\Raja Reddy\mlops-demo
```

## 1. Train the model

```powershell
python train.py
```

This writes `model.pkl`.

## 2. Track the experiment

```powershell
python train_mlflow.py
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Open http://127.0.0.1:5000, choose **Model training**, then **Experiments**, then **iris-classifier**.

## 3. Change the four measurements and predict

The four numbers are sepal length, sepal width, petal length, and petal width.

```powershell
python predict.py 6.7 3.0 5.2 2.3
```

Use a different set of numbers on every run.

## 4. Open the Streamlit page

```powershell
python -m streamlit run streamlit_app.py
```

Open the local URL printed in the terminal, usually http://127.0.0.1:8501. Type four numbers such as `6.7, 3.0, 5.2, 2.3` and click **Use these numbers**, or edit each measurement box. The prediction updates from those inputs.

## 5. Serve the API

```powershell
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs. In **POST /predict**, edit `features` and click **Execute**.

## 6. Run the API in Docker

Stop the local API with `Ctrl+C` first. Both use port 8000.

```powershell
docker run --rm -p 8000:8000 mlops-demo
```

Rebuild after you change `app.py` or `requirements.txt`:

```powershell
docker build -t mlops-demo .
```

## 7. Start monitoring

Stop the single container with `Ctrl+C`, then:

```powershell
docker compose up -d
```

| Service | Address | Login |
|---|---|---|
| API | http://127.0.0.1:8000/docs | none |
| Prometheus | http://127.0.0.1:9090 | none |
| Grafana | http://127.0.0.1:3000 | `admin` / `admin` |

Prometheus stores request counts and prediction latency from `/metrics`. Grafana is the chart page. It starts empty until you add Prometheus at `http://prometheus:9090` as a data source.

Stop the stack with `docker compose down`.

## 8. GitHub Actions

Every push to `main` trains the model, stops if accuracy is below 0.90, runs the API tests, builds the Docker image, and calls `/predict`.

https://github.com/Vekri/mlops-demo/actions

To send different measurements on a manual run, open **MLOps CI**, click **Run workflow**, and enter four comma-separated numbers such as `6.7,3.0,5.2,2.3`.
