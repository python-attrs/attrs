FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
RUN pip install pytest
CMD ["/bin/bash"]
