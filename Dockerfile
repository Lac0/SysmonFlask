FROM python:3.8.10
EXPOSE 5000
WORKDIR /flaskapp
COPY ./sysmon /flaskapp
RUN pip3 install Flask  
RUN pip3 install psutil
CMD ["python","flaskapp.py"]