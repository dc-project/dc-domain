## Intro

快速实现三级域名解析基于CloudXNS,dc-ctl 子项目之一

## 功能

- 初始化一个随机三级域名泛解析
- 删除指定三级域名
- 更新指定三级域名

## 使用

```angular2html
./domain.py domain -h  
usage: domain.py [-h] domain <subcommand> ...

positional arguments:
  domain        resolve domain
  <subcommand>
    init        init domain resolve
    del         del domain resolve
    update      update domain resolve

optional arguments:
  -h, --help    show this help message and exit

```

## Todo

[ ] 支持ali dns  
[ ] 支持指定初始化三级域名
[ ] 支持docker快速部署

