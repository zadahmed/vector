FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libssl-dev
RUN  apt-get install  -y gcc libpq-dev python3-dev python3-pip python3-venv python3-wheel curl
RUN apt-get install -y python3-opencv
RUN pip install opencv-python
RUN apt-get -y upgrade
ENV TZ=Asia/Dubai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8000
WORKDIR /
COPY ./requirements.txt .
COPY ./ocr/ /
COPY . .
RUN pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
RUN pip install ./APP_OCR-0.1.0-py3-none-any.whl
RUN pip install -r requirements.txt

# Run the application in the port 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]