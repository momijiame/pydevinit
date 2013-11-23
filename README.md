pydevinit
=========

Eclipse PyDev Plugin Project Initialize Script

# これは何？

Eclipse の PyDev プラグインが使用するプロジェクトのメタデータを記録したファイルを生成するためのスクリプトです。
通常、それらのファイルは PyDev プラグインがプロジェクトを作成する際に作られます。
しかし、既存の非 PyDev プロジェクトを PyDev プラグインで読み込む場合には、それらのファイルが存在しないため、プラグインはプロジェクトを認識できません。
pydevinit は既存の非 PyDev プロジェクトを PyDev プラグインで読み込みたい時には助けになるでしょう。

# インストール

インストールと実行には Python が必要です。

## GitHub のソースコードからインストールする

```
$ git clone https://github.com/momijiame/pydevinit.git
$ cd pydevinit
$ python setup.py install
```

## PIP でインストールする

```
$ pip install pydevinit
```

# 使い方

プロジェクトのディレクトリで pydevinit を実行します。
利用可能な全てのオプションは -h で確認できます。

```
$ pydevinit --project-name <project_name> --source-path <source_dir>
```

スクリプトを実行したディレクトリに PyDev プラグイン用のメタデータを記録した隠しファイル (.project, .pydevproject) が作成されます。

