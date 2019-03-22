weather-forecasting
====

Pythonを使って天気予測をやってみる。
numpy, keras等を使って試行錯誤しています。

## Description

## Demo

## VS. 

## Requirement

- python3
- numpy
- tensorflow
- keras

## Usage

## Install

Amazon Linux2でのインストール手順です。

python3, pip3, virtualenvをインストールする。
```bash
sudo yum install python3
sudo yum install python3-pip
pip3 install virtualenv
```

virtualenvで仮想環境を作成する。
```bash
virtualenv --no-site-packages weather_forecasting
```

仮想環境を有効にする。
```bash
cd weather_forecasting
source bin/activate
```

仮想環境にnumpyをインストールする。
```bash
pip3 install numpy
pip3 install tensorflow
pip3 install keras
```

GitHubからリポジトリをクローンする。
```bash
git clone 'https://github.com/predora005/weather-forecasting'
```

作業が終わったら仮想環境を無効にする。
```bash
deactivate
```

## Contribution

## Licence

[MIT](https://github.com/predora005/weather-forecasting/blob/master/LICENSE)

## Author

[predora005](https://github.com/predora005)
