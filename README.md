# Shows some system info, do steps below to run using docker, or use sysmon_with_shell_output.py

docker image build -t sysmon .

docker run -p 5000:5000 -t sysmon
