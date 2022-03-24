# Shows some system info, do steps below to run using docker

docker image build -t sysmon .

docker run -p {desired port}:5000 -t sysmon
