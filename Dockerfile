FROM amazonlinux:2

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN yum install unzip git -y
RUN unzip awscliv2.zip
RUN ./aws/install

RUN python -m ensurepip --default-pip
RUN pip install --upgrade pip
RUN pip install  wheel pandas pandas-datareader PyMySQL Flask