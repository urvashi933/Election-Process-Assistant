# -----------------------------
# 🐍 BASE IMAGE
# -----------------------------
# Using slim version to reduce the final image size
FROM python:3.11-slim

# -----------------------------
# 📁 WORKDIR
# -----------------------------
WORKDIR /app

# -----------------------------
# ⚙️ ENV SETTINGS
# -----------------------------
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures console output is sent directly to the terminal (important for logs)
ENV PYTHONUNBUFFERED=1

# -----------------------------
# 📦 INSTALL DEPENDENCIES
# -----------------------------
# Copy requirements first to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 📂 COPY PROJECT
# -----------------------------
# Copy the rest of the application code
COPY . .

# -----------------------------
# 🔐 NON-ROOT USER (SECURITY)
# -----------------------------
# It is a security risk to run your app as root in production
RUN useradd -m appuser
USER appuser

# -----------------------------
# 🌐 PORT
# -----------------------------
# FastAPI standard port for your setup
EXPOSE 8080

# -----------------------------
# 🚀 START SERVER
# -----------------------------
# Standard uvicorn command as defined in your project structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]