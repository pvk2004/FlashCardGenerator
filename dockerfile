FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV STREAMLIT_CONFIG_DIR=/tmp/.streamlit
RUN mkdir -p /tmp/.streamlit
COPY .streamlit/config.toml /tmp/.streamlit/config.toml
EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]