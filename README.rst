# berycker
**Docker-like tool to set up a headless RaspberryPi or linux**

ヘッドレスでのRaspberryPiやlinuxの初期設定をdockerライクにする、コマンドラインツールです。

# 使い方
## init
```
berycker init
```
wifiやsshの設定を行います。
イメージを作ったあと、イメージを焼いたドライブを挿入した状態で実行してください。
## build
```
berycker build
```
ラズパイが起動した後に実行してください。

# beryckerfile
shファイルと同じように書けば問題ないです。`#`でコメントアウトできます。
shファイルと違うのは、中括弧で囲むことで変数を定義できることです。
```
# ssh key setting
echo {pub_key} >> .ssh/authorized_keys
```

パスワードなどのファイルに記入することがはばかられる値や、マシンごとに値が異なる所（ホスト名など）を変数として定義できます。
beryckerfile内で定義した変数は、ビルドするときにインタラクティブに入力できます。

beryckerfileの例はexampleディレクトリにあります。

