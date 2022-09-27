FROM python:3.8-alpine

RUN apk update && \
	apk add gcc g++ cmake && \
	pip install -U pip && \
	pip install -U setuptools
	
RUN pip install --user \
	argparse numpy matplotlib opencv-python pillow face_recognition 

COPY ./haarcascades .
COPY ./Celebs .
COPY crm.py .

CMD [ "python", "./crm.py", "1" ]