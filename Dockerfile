FROM python:3.12-slim
WORKDIR /workspace
COPY requirements_lock.txt .
RUN pip install --no-cache-dir -r requirements_lock.txt
COPY . .
ENV PYTHONPATH=/workspace/src/python
CMD ["bash", "verify_pipeline.sh"]
