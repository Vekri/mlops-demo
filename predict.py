import sys
import joblib

FLOWERS = {0: "setosa", 1: "versicolor", 2: "virginica"}


def main():
    if len(sys.argv) != 5:
        print("Usage: python predict.py sepal_length sepal_width petal_length petal_width")
        print("Example: python predict.py 6.7 3.0 5.2 2.3")
        sys.exit(1)

    features = [float(value) for value in sys.argv[1:]]
    model = joblib.load("model.pkl")
    prediction = int(model.predict([features])[0])
    print(f"features: {features}")
    print(f"prediction: {prediction}")
    print(f"flower_class: {FLOWERS.get(prediction, 'unknown')}")


if __name__ == "__main__":
    main()
