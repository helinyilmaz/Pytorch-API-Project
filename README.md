# PyTorch Sentiment Analysis API

A scalable, production-style NLP prediction API built with FastAPI and DistilBERT, featuring Redis caching, containerization with Docker, and deployment on Kubernetes with load testing and monitoring.

---

## 📌 Project Overview

This project implements an end-to-end machine learning inference service for sentiment analysis. A DistilBERT model is packaged for efficient CPU-based inference and exposed through a REST API built with FastAPI.

To support production-like workloads, the system includes Redis caching to reduce repeated model inference, Docker for containerization, Kubernetes for orchestration, and AWS for cloud deployment. Load testing is performed with k6, and performance metrics are visualized using Grafana.

---

## 🚀 Features

- REST API for sentiment prediction using FastAPI
- DistilBERT model for NLP sentiment analysis (HuggingFace, PyTorch)
- Dependency management with Poetry
- Redis-based response caching
- Dockerized application
- Kubernetes deployment (EKS)
- Load testing with k6
- Performance monitoring with Grafana
- Automated testing with pytest

---

## 🧠 Model

- **Model:** DistilBERT
- **Task:** Sentiment analysis
- **Framework:** PyTorch
- **Source:** HuggingFace Transformers

The model is optimized for CPU-based inference and loaded at container build time to reduce cold-start latency.

---

## 📥 API Usage

### Request Format

```json
{
  "text": ["example sentence 1", "example sentence 2"]
}
```

### Response Format

```json
{
  "predictions": [
    [
      {"label": "POSITIVE", "score": 0.71},
      {"label": "NEGATIVE", "score": 0.29}
    ],
    [
      {"label": "POSITIVE", "score": 0.72},
      {"label": "NEGATIVE", "score": 0.28}
    ]
  ]
}
```

---

## 🛠️ Tech Stack

- **API:** FastAPI
- **ML:** PyTorch, HuggingFace Transformers
- **Caching:** Redis
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Cloud:** AWS (EKS)
- **Testing:** pytest, k6
- **Monitoring:** Grafana
- **Dependency Management:** Poetry

---

## 🧪 Load Testing

Load testing is performed using k6 to evaluate throughput and latency under concurrent requests.

**Metrics collected include:**
- Average and median response time
- 90th, 95th, and 99th percentile latency
- Request throughput under load

---

## 📊 Monitoring

Grafana dashboards visualize:
- API request volume
- Response latency
- Cache performance
- Resource utilization

This allows for performance analysis and identification of system bottlenecks.

---

## 📦 Deployment

The application is packaged using Docker and deployed on AWS using Kubernetes (EKS).

**Redis is used to:**
- Reduce repeated model inference
- Improve response times
- Protect the API from abuse

The system is designed to scale horizontally under load.

---

## 📎 Notes

This project was originally developed in a private academic workspace and republished here for portfolio purposes.

---

## 👩‍💻 Author

**Helin Yilmaz**
