## Python ���g�p����ۂ̐ݒ�

* mkPyProj.bat - Visual Studio �̃X�^�[�g�A�b�v�t�@�C���iPython �p�j�̐���
```sh
% dir /b *.py*
% foo.py
% mkPyProj foo
% mkPyProj bar
% dir /b *.py*
bar.py // print('Hello World')
bar.pyproj
foo.py
foo.pyproj
% foo.pyproj // Visual Studio �N��
```
* setupVSCode.bat - Visual Studio Code �� QGIS ������ Python �̕ҏW�E���s�E�f�o�b�O���s�����߂̊��ݒ�
```sh
% setupVSCode // %APPDATA%\Code\User �� settings.json �� launch.json ��z�u
```
* setenv.cmd - �R�}���h�v�����v�g�� QGIS ������ Python ���N�����邽�߂̊��ݒ�
```sh
% setenv
% python --version
Python 3.7.0
```
* subst.bat - ������̒u���isetupVSCode �Ŏg�p�j
```sh
% type foo.txt
bar baz
% subst foo.txt b v
var vaz
```

## ���̑�

* showClip.bat - �N���b�v�{�[�h���̃e�L�X�g�̏o��

�@�@�@![xls](img/xls_snap.png)
<br>�@�@�@�@�@�@�@�@�@�@�@�@�@�@��<br>
�@�@�@![xls](img/showClip.png)