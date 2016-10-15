FROM debian:8.6


ADD sources.list /etc/apt/sources.list
RUN apt-get update -y && \
    apt-get install -y nmap && \
    apt-get install -y python-pip


RUN pip install tornado -i https://pypi.tuna.tsinghua.edu.cn/simple


COPY . /code
RUN cd /code/python-nmap && python setup.py install
CMD ["python", "/code/application.py"]
