FROM centos:latest
COPY abcd.py /root/abcd.py
RUN yum -y install epel-release
RUN yum -y install python-pip
RUN yum -y install git
RUN pip install --upgrade pip
RUN pip install PyGithub
RUN pip install requests==2.7.0
RUN yum install --assumeyes wget unzip git

RUN wget https://releases.hashicorp.com/vault/0.10.1/vault_0.10.1_linux_amd64.zip
RUN unzip vault_0.10.1_linux_amd64.zip

RUN export PATH=$PATH:${PWD}
RUN exec $shell

CMD ["/bin/bash"]
