import asyncio
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "youtube")
SLIDES = os.path.join(OUT, "slides")
AUDIO = os.path.join(OUT, "audio")
os.makedirs(SLIDES, exist_ok=True)
os.makedirs(AUDIO, exist_ok=True)

CLOUD = "https://mlops-demo-pu2vzxx8rafyqsavaglcbr.streamlit.app/"
REPO = "https://github.com/Vekri/mlops-demo"
ACTIONS = "https://github.com/Vekri/mlops-demo/actions"
VOICE = "en-US-GuyNeural"

LONG = [
    (
        "The full path",
        "MLOps, from your laptop to a public page",
        [
            "Train a model",
            "Track the run",
            "Serve an API",
            "Package it with Docker",
            "Check every push with GitHub Actions",
            "Publish the page on Streamlit Cloud",
        ],
        "This lesson follows one real iris project from the first training command to a public Streamlit page. You will see what happens on your laptop, what GitHub Actions checks, and what Streamlit Cloud serves to anyone with the link.",
    ),
    (
        "01  Train",
        "Python and scikit-learn write model.pkl",
        [
            "Command: python train.py",
            "Data: 150 iris flowers, 4 measurements",
            "Model: Random Forest, 100 trees",
            "Result you should see: Accuracy 1.0",
            "File created: model.pkl",
        ],
        "Start in the project folder and run python train.py. Scikit-learn loads the iris dataset, keeps eighty percent for training, and tests the rest. A random forest of one hundred trees learns the pattern. The program prints the accuracy and saves the trained model as model.pkl. That file is the model your later steps use.",
    ),
    (
        "02  Track",
        "MLflow records the experiment",
        [
            "Command: python train_mlflow.py",
            "Database: mlflow.db",
            "Experiment: iris-classifier",
            "Logged: n_estimators, accuracy, model",
            "Open Model training, then Experiments",
        ],
        "Run python train_mlflow.py. The same training happens again, and MLflow stores the parameters, the accuracy, and the model in a local database. Then run mlflow ui. In the browser, open Model training, then Experiments, then iris-classifier. The M C P registry page is a different screen. Your training run is under Model training.",
    ),
    (
        "03  Predict",
        "Change the four numbers any time",
        [
            "Order: sepal length, sepal width",
            "Then petal length, petal width",
            "5.1, 3.5, 1.4, 0.2 is setosa",
            "6.0, 2.9, 4.5, 1.5 is versicolor",
            "6.7, 3.0, 5.2, 2.3 is virginica",
        ],
        "The four numbers are one flower, in centimeters. Run python predict.py followed by four new numbers every time. Five point one, three point five, one point four, zero point two returns setosa. Six point seven, three point zero, five point two, two point three returns virginica. The model is not trained again. Only the input row changes.",
    ),
    (
        "04  API",
        "FastAPI serves POST /predict",
        [
            "Command: python -m uvicorn app:app --reload",
            "Docs: 127.0.0.1 port 8000 slash docs",
            "Edit the features list and click Execute",
            "Response: prediction, flower class, latency",
            "Metrics are exposed at slash metrics",
        ],
        "Start the A P I with uvicorn. Open the docs page on port 8000. Choose POST slash predict, click Try it out, and replace the four numbers. Execute sends that row to model.pkl. The reply is the class number, the flower name, and the latency. Slash metrics exposes the counters that Prometheus can read.",
    ),
    (
        "05  Streamlit",
        "Type the inputs on a web page",
        [
            "File: mlops_iris_predictor.py",
            "Command: python -m streamlit run mlops_iris_predictor.py",
            "Paste 6.7, 3.0, 5.2, 2.3",
            "Click Use these numbers",
            "The four boxes and the chart update",
        ],
        "The Streamlit page is for people who should not call an A P I. Run mlops iris predictor. Paste six point seven, three point zero, five point two, two point three, and click Use these numbers. Streamlit checks that there are exactly four numbers, copies them into the boxes, and reruns the page. The saved forest votes, and the page shows the flower, the class, and three probability bars.",
    ),
    (
        "06  Docker",
        "The API runs inside one container",
        [
            "Dockerfile starts uvicorn on port 8000",
            "It copies app.py and model.pkl",
            "Command: docker run -p 8000:8000 mlops-demo",
            "Stop the local uvicorn first",
            "Both programs want port 8000",
        ],
        "Docker packages the FastAPI app, its Python libraries, and model.pkl into one image. Build it with docker build, then run it and map port 8000. Stop the local uvicorn process first, because both want that port. The docs page looks the same, but the process now runs inside the container. Docker compose adds Prometheus on 9090 and Grafana on 3000.",
    ),
    (
        "07  Monitor",
        "Prometheus stores numbers, Grafana draws them",
        [
            "Prometheus: 127.0.0.1 port 9090",
            "It calls slash metrics every 5 seconds",
            "Try the query http_requests_total",
            "Grafana: port 3000, admin and admin",
            "Grafana starts empty until you add a chart",
        ],
        "Prometheus is the measurement database. Every five seconds it calls the A P I metrics path and stores request counts and latency. Open port 9090, choose Graph, and run http requests total. Grafana on port 3000 is the chart screen. Sign in with admin and admin. It starts empty until you connect the Prometheus address and create a panel.",
    ),
    (
        "08  Versions",
        "Git on the laptop, GitHub for the shared copy",
        [
            "git add, git commit, git push",
            "Each commit is one version of main",
            "model.pkl is included in the repository",
            "mlflow.db and the videos stay local",
            REPO,
        ],
        "Git on your laptop stores each version in the hidden git folder. Add the files, commit them with a reason, and push. That push sends the version to GitHub on the main branch. The saved model.pkl is part of that shared copy, so Streamlit Cloud, the API, and Docker can load the same file. The MLflow database and these lesson videos stay on your laptop. The project is at github.com slash Vekri slash mlops dash demo.",
    ),
    (
        "09  CI",
        "GitHub Actions checks that exact commit",
        [
            "Trigger: push or pull request to main",
            "A new Ubuntu machine checks out the code",
            "Train, accuracy gate, tests",
            "Streamlit health check",
            "Docker build, then POST slash predict",
        ],
        "Continuous integration means every push is checked before you trust it. GitHub reads the workflow file and starts a fresh Ubuntu computer. That computer checks out your commit, installs the requirements, trains the model, and stops if accuracy falls below zero point nine zero. It runs the tests, starts Streamlit long enough to see a healthy response, builds the Docker image, and calls predict. Then GitHub deletes that computer. The green check stays on the commit.",
    ),
    (
        "10  CD",
        "A passing version becomes the public page",
        [
            "CI is the check",
            "CD is the publish step",
            "Streamlit Cloud publishes this app",
            "The Docker test container is removed",
            "The A P I is not given a public server",
        ],
        "Continuous deployment means a good version is placed where people can use it. In this project, Streamlit Cloud does that for the predictor page. A push to main updates the public site. The Docker image is built during the check and then removed. The FastAPI service is tested, and it is not published to its own public server by this workflow.",
    ),
    (
        "11  Cloud",
        "Streamlit Cloud loads model.pkl from GitHub",
        [
            "Repo: Vekri/mlops-demo, branch main",
            "File: mlops_iris_predictor.py",
            "joblib loads the committed model.pkl",
            "The page does not train a new forest",
            CLOUD,
        ],
        "Streamlit Cloud does not read your laptop. It copies the main branch from GitHub and runs mlops iris predictor. That file loads model.pkl with joblib and caches the forest. It does not train a replacement model. Your browser session starts at the default measurements and shows setosa. Each new set of four numbers is predicted with that same saved model. The public page is the Streamlit app link shown on this slide.",
    ),
    (
        "12  Compare",
        "Docker and Streamlit Cloud use the same model.pkl",
        [
            "Docker: the API container on port 8000",
            "Cloud: the public Streamlit page",
            "Both load the saved model.pkl",
            "Opening the public link does not run Actions",
            "A push checks the code and updates the page",
        ],
        "Docker and Streamlit Cloud both load the same model.pkl. Use Docker when you want the API container on your machine or inside the GitHub check. Use Streamlit Cloud when you want a link anyone can open. Opening the public link does not start GitHub Actions. A push starts the check and also updates the Cloud page. They share the GitHub code and the saved model, and they serve different programs.",
    ),
    (
        "Run it",
        "Commands, GitHub, and the public page",
        [
            "python train.py",
            "python -m streamlit run mlops_iris_predictor.py",
            "docker run -p 8000:8000 mlops-demo",
            REPO,
            CLOUD,
        ],
        "To repeat the lesson, train the model, run the Streamlit file, and open the local address printed in the terminal. For the API, stop any program already using port 8000, then run the Docker image. The code is on GitHub under Vekri slash mlops dash demo. The public page is the Streamlit Cloud link. Type four measurements, click Use these numbers, and the flower name updates from model.pkl. That is the full path: train, track, serve, package, check, and publish.",
    ),
]

SHORT = [
    (
        "One model. Two ways to run it.",
        ["Train it", "Check it", "Publish the page"],
        "Here is the short version of a full machine learning operations project.",
    ),
    (
        "1. Train on your laptop",
        ["python train.py", "Accuracy 1.0", "Saved as model.pkl"],
        "Train the iris forest with python train.py. It saves model.pkl.",
    ),
    (
        "2. GitHub checks every push",
        ["Train and test", "Start Streamlit", "Build Docker and predict"],
        "Push to main. GitHub Actions trains, tests, starts Streamlit, builds Docker, and calls predict.",
    ),
    (
        "3. Streamlit Cloud publishes it",
        ["Loads model.pkl from GitHub", "File: mlops_iris_predictor.py", "Type four flower numbers"],
        "Streamlit Cloud reads that GitHub code, loads model.pkl, and serves the public predictor. Type four measurements and it returns the flower.",
    ),
    (
        "Docker is the API. Cloud is the page.",
        ["Both load model.pkl", "github.com/Vekri/mlops-demo", CLOUD],
        "Docker runs the API. Streamlit Cloud runs the public page. Both load the same model.pkl from GitHub. Same project. Two different jobs.",
    ),
]


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)


def wrap(draw, text, fnt, width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def new_canvas(w, h):
    img = Image.new("RGB", (w, h), (11, 18, 32))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 14), fill=(37, 99, 235))
    return img, draw


def draw_long(index, total, eyebrow, title, bullets):
    w, h = 1920, 1080
    img, draw = new_canvas(w, h)
    draw.text((80, 50), f"{index:02d}  /  {total:02d}", font=font(28), fill=(148, 163, 184))
    draw.text((80, 100), eyebrow.upper(), font=font(28, True), fill=(96, 165, 250))
    title_lines = wrap(draw, title, font(64, True), 1700)
    y = 160
    for line in title_lines[:2]:
        draw.text((80, y), line, font=font(64, True), fill=(248, 250, 252))
        y += 78
    y += 20
    for bullet in bullets:
        draw.rounded_rectangle((80, y, 1840, y + 78), radius=16, fill=(17, 24, 39))
        draw.ellipse((110, y + 28, 136, y + 54), fill=(59, 130, 246))
        draw.text((164, y + 18), bullet, font=font(32), fill=(241, 245, 249))
        y += 96
    path = os.path.join(SLIDES, f"long_{index:02d}.png")
    img.save(path)
    return path


def draw_short(index, total, title, bullets):
    w, h = 1080, 1920
    img, draw = new_canvas(w, h)
    draw.text((70, 80), "MLOPS LESSON", font=font(32, True), fill=(96, 165, 250))
    draw.text((70, 130), f"{index} of {total}", font=font(28), fill=(148, 163, 184))
    y = 230
    for line in wrap(draw, title, font(68, True), 920)[:4]:
        draw.text((70, y), line, font=font(68, True), fill=(248, 250, 252))
        y += 84
    y += 40
    for bullet in bullets:
        box_h = 150
        draw.rounded_rectangle((70, y, 1010, y + box_h), radius=24, fill=(17, 24, 39))
        text_y = y + 45
        for line in wrap(draw, bullet, font(36), 860)[:2]:
            draw.text((110, text_y), line, font=font(36), fill=(241, 245, 249))
            text_y += 46
        y += box_h + 28
    path = os.path.join(SLIDES, f"short_{index:02d}.png")
    img.save(path)
    return path


async def speak(name, text):
    import edge_tts
    path = os.path.join(AUDIO, f"{name}.mp3")
    await edge_tts.Communicate(text, VOICE).save(path)
    return path


def render_clip(image, audio, dest):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg, "-y", "-loop", "1", "-i", image, "-i", audio,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-shortest", dest,
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def concat(parts, dest):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    listing = os.path.join(OUT, "concat_list.txt")
    with open(listing, "w", encoding="utf-8") as handle:
        for part in parts:
            handle.write("file '" + part.replace("\\", "/") + "'\n")
    subprocess.run(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", dest],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


async def build(kind, scenes, drawer, output_name):
    clips = []
    total = len(scenes)
    for index, scene in enumerate(scenes, start=1):
        if kind == "long":
            eyebrow, title, bullets, narration = scene
            image = drawer(index, total, eyebrow, title, bullets)
        else:
            title, bullets, narration = scene
            image = drawer(index, total, title, bullets)
        audio = await speak(f"{kind}_{index:02d}", narration)
        clip = os.path.join(OUT, f"{kind}_{index:02d}.mp4")
        render_clip(image, audio, clip)
        clips.append(clip)
        print(f"Rendered {kind} scene {index}/{total}")
    dest = os.path.join(OUT, output_name)
    concat(clips, dest)
    print("Wrote", dest)


def media_duration(path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-i", path],
        capture_output=True,
        text=True,
    )
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            clock = line.split("Duration:")[1].split(",")[0].strip()
            hours, minutes, seconds = clock.split(":")
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    raise RuntimeError(f"No duration for {path}")


def clock(seconds):
    total = int(round(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def write_posting(long_clips, short_clips):
    long_marks = []
    cursor = 0.0
    for clip, scene in zip(long_clips, LONG):
        long_marks.append((clock(cursor), scene[1]))
        cursor += media_duration(clip)
    short_total = clock(sum(media_duration(clip) for clip in short_clips))
    chapters = "\n".join(f"{mark} {title}" for mark, title in long_marks)
    text = f"""Long lesson
Title: MLOps End to End: Train model.pkl, Docker, GitHub Actions, and Streamlit Cloud
File: mlops_youtube_long.mp4
Length: {clock(cursor)}

Description:
Follow one iris classifier from your laptop to a public page. Every step uses the same saved model.pkl.

You will see the exact commands and what each one produces:
- python train.py saves model.pkl
- MLflow records the experiment
- FastAPI serves POST /predict from model.pkl
- Streamlit loads model.pkl and lets you type four measurements
- Docker packages the API and model.pkl
- Prometheus and Grafana read the metrics
- Git stores each version and GitHub receives model.pkl with the push
- GitHub Actions trains, tests, checks Streamlit, and checks Docker
- Streamlit Cloud publishes the page and loads the same model.pkl

Try the public app:
{CLOUD}

Project code and README:
{REPO}

GitHub Actions:
{ACTIONS}

Chapters:
{chapters}

Tags:
MLOps, Streamlit, Docker, GitHub Actions, FastAPI, MLflow, scikit-learn, model.pkl, CI CD, machine learning

Short
Title: Train model.pkl, then publish it
File: mlops_youtube_short.mp4
Format: vertical YouTube Short
Length: {short_total}

Description:
Train model.pkl, let GitHub Actions check the push, and let Streamlit Cloud publish the page. The API and the public page both load that same file.

Try the public app:
{CLOUD}

Project code and README:
{REPO}

GitHub Actions:
{ACTIONS}

#Shorts #MLOps #Streamlit #Docker #GitHub
"""
    path = os.path.join(OUT, "POSTING.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("Wrote", path)


async def main():
    await build("long", LONG, draw_long, "mlops_youtube_long.mp4")
    await build("short", SHORT, draw_short, "mlops_youtube_short.mp4")
    long_clips = [os.path.join(OUT, f"long_{index:02d}.mp4") for index in range(1, len(LONG) + 1)]
    short_clips = [os.path.join(OUT, f"short_{index:02d}.mp4") for index in range(1, len(SHORT) + 1)]
    write_posting(long_clips, short_clips)


if __name__ == "__main__":
    asyncio.run(main())
