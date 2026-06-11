# 📌 WHAT: Base image — Python 3.11 on slim Linux
# 🎯 WHY: Slim version is smaller than full Python image
#         — faster to download and deploy
# 💼 INTERVIEW: "I used Python slim image to minimize
#         container size — smaller images deploy faster"
FROM python:3.11-slim

# 📌 WHAT: Sets working directory inside container
# 🎯 WHY: All commands run from this folder
# 💼 INTERVIEW: "Standard practice to isolate app
#         files in a dedicated directory"
WORKDIR /app

# 📌 WHAT: Copies and installs dependencies FIRST
# 🎯 WHY: Docker caches this layer — if code changes
#         but requirements don't, it skips reinstalling
# 💼 INTERVIEW: "I copy requirements first to leverage
#         Docker's layer caching — speeds up rebuilds"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📌 WHAT: Copies our application code
# 🎯 WHY: Done AFTER pip install for better caching
# 💼 INTERVIEW: "Code changes more often than
#         dependencies — this ordering optimizes
#         build time significantly"
COPY . .

# 📌 WHAT: Documents which port our app uses
# 🎯 WHY: Tells Docker to expose port 8000
# 💼 INTERVIEW: "EXPOSE documents the port — 
#         required for cloud deployments"
EXPOSE 8000

# 📌 WHAT: Command that runs when container starts
# 🎯 WHY: Starts our FastAPI server
# 💼 INTERVIEW: "I use 0.0.0.0 so the API is
#         accessible from outside the container"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]