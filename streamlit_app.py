from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

FLOWERS = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
PRESETS = {
    "Setosa": (5.1, 3.5, 1.4, 0.2),
    "Versicolor": (6.0, 2.9, 4.5, 1.5),
    "Virginica": (6.7, 3.0, 5.2, 2.3),
}

st.set_page_config(page_title="Iris predictor", page_icon="🌸", layout="centered")


@st.cache_resource
def load_model():
    path = Path(__file__).resolve().parent / "model.pkl"
    if not path.exists():
        return None
    return joblib.load(path)


def show_prediction(model, features):
    prediction = int(model.predict([features])[0])
    probabilities = model.predict_proba([features])[0]
    flower, class_id = st.columns(2)
    flower.metric("Flower", FLOWERS[prediction])
    class_id.metric("Class", prediction)
    st.bar_chart(
        pd.DataFrame(
            {"probability": probabilities},
            index=["Setosa", "Versicolor", "Virginica"],
        )
    )
    st.caption(
        "Sepal length, sepal width, petal length, petal width: "
        + ", ".join(f"{value:.1f} cm" for value in features)
    )


def apply_features(values):
    (
        st.session_state.sepal_length,
        st.session_state.sepal_width,
        st.session_state.petal_length,
        st.session_state.petal_width,
    ) = values


st.title("Iris flower predictor")
st.write("Type the four measurements, or paste them as 6.7, 3.0, 5.2, 2.3. The prediction updates from those inputs.")

model = load_model()
if model is None:
    st.error("model.pkl is missing. In this folder, run: python train.py")
    st.stop()

if "sepal_length" not in st.session_state:
    st.session_state.sepal_length = 5.1
    st.session_state.sepal_width = 3.5
    st.session_state.petal_length = 1.4
    st.session_state.petal_width = 0.2

st.subheader("Input parameters")
typed = st.text_input(
    "Four numbers: sepal length, sepal width, petal length, petal width",
    placeholder="6.7, 3.0, 5.2, 2.3",
)
if st.button("Use these numbers", type="primary"):
    cleaned = typed.replace("[", "").replace("]", "")
    try:
        entered = [float(part.strip()) for part in cleaned.split(",")]
        if len(entered) != 4:
            raise ValueError
    except ValueError:
        st.error("Enter exactly 4 numbers, for example 6.7, 3.0, 5.2, 2.3")
    else:
        apply_features(entered)
        st.rerun()

sample_columns = st.columns(3)
for column, (name, values) in zip(sample_columns, PRESETS.items()):
    if column.button(name, use_container_width=True):
        apply_features(values)
        st.rerun()

left, right = st.columns(2)
left.number_input("Sepal length (cm)", min_value=0.0, max_value=10.0, step=0.1, key="sepal_length")
right.number_input("Sepal width (cm)", min_value=0.0, max_value=10.0, step=0.1, key="sepal_width")
left.number_input("Petal length (cm)", min_value=0.0, max_value=10.0, step=0.1, key="petal_length")
right.number_input("Petal width (cm)", min_value=0.0, max_value=10.0, step=0.1, key="petal_width")

features = [
    st.session_state.sepal_length,
    st.session_state.sepal_width,
    st.session_state.petal_length,
    st.session_state.petal_width,
]

st.subheader("Prediction")
show_prediction(model, features)
