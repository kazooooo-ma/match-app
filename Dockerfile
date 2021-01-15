# ココで前述のベースイメージを指定している
FROM joyzoursky/python-chromedriver

# - Vi・Vim が入っていないのでインストールする
# - pip をアップデートして pipienv をインストールする
RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  pip install --upgrade pip && \
  pip install pipenv \
  pip install requests \
  pip install selenium \
  pip install discordwebhook

# Japanese
RUN apt-get install -y locales task-japanese
RUN locale-gen ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8

WORKDIR /root/app/
#COPY *.py /root/app/

#CMD ["python", "toukare.py"]
