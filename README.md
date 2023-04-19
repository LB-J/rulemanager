# rulemanager

#### 介绍
用于配置 prometheus 告警规则，通过邮件、企业微信等告警渠道进行发送告警。
结合了 thanos rule，alertmanager。
并通过定时任务的方式，将告警规则同步到 thanos rule 所在节点中。

#### 软件架构
##### 语言：python3.7
##### 架构：rest-framework django

#### 安装教程
##### 采用docker-compose 进行部署，已经将依赖的mysql、redis、python环境，通过docker-compose 进行集成。并放在仓库的 docker-compose中。
##### 下载代码并将代码放置 docker-compose/rulemanager/server/rulemanager/ 下。
##### docker-comse up -d 进行启动。

#### 部署说明
##### 1，部署说明详见 docker-compose/README.txt

#### 功能模块
##### 1，用户管理模块，实现告警接收用户/用户组的配置；规则分组：实现告警规则分组和用户组关联功能；
##### 2，规则管理：进行规则的管理（新增、删除、启用/停用等）
####  3，告警管理，展示当前正在发生的告警信息，以及ack功能（告警确认）。


