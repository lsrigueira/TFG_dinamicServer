FROM ubuntu:18.04

WORKDIR /code
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y 
RUN apt-get install python3-pip -y
RUN pip3 install cython 
RUN pip3 install scipy==1.3.0  
RUN pip3 install scikit-learn==0.21.2  
RUN pip3 install matplotlib==3.1.0
RUN pip3 install XlsxWriter==1.1.8 
RUN pip3 install pandas==0.24.2 
RUN pip3 install seaborn==0.9.0
RUN pip3 install plotly==3.10.0
RUN pip3 install Cython==0.29.12 

RUN mkdir ./src
ADD ./src ./src


