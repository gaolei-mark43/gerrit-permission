# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import time
import requests


# python2.7
# 新建仓库
def createProject(groupName, projectName):
    gitPath = "/devops/review_site/git"
    # 切换目录到git仓库目录
    os.chdir(gitPath)
    # 校验即将创建的仓库是否已经存在
    if os.path.exists(groupName + "/" + projectName+".git"):
        print("git已被创建，程序退出,请检查！")
        sys.exit(0)

    # 创建仓库
    command = "ssh -p 29418 leigao6@codereview.test.com gerrit create-project %s/%s" % (groupName, projectName)
    print(command)
    # 执行命令
    subprocess.call(command, shell=True)

    # 切换目录到git仓库目录
    os.chdir(gitPath + "/" + groupName + "/")
    # ls -l
    subprocess.call("ls -l", shell=True)


# clone远程代码
def cloneGitee(groupName, projectName):
    gitPath = "/devops/review_site/git"
    # 切换目录到git仓库目录
    os.chdir(gitPath+"/"+groupName+"/")
    # ls -l
    subprocess.call("ls -l", shell=True)
    # 删除本地仓库
    print("rm -rf "+projectName+".git")
    # 校验删除命令，防止误删，当projectName为空时，不执行删除命令
    if projectName == "" or projectName is None:
        print("projectName为空，不执行删除命令，请检查")
        sys.exit(0)
    else:
        subprocess.call("rm -rf "+projectName+".git", shell=True)
    # clone远程仓库
    command = "git clone --bare ssh://git@code.iflytek.com:30004/%s/%s" % (groupName, projectName)
    # 执行命令
    print(command)
    subprocess.call(command, shell=True)
    # ls -l
    subprocess.call("ls -l", shell=True)


# 新增replication.config配置
def updateReplication(groupName, projectName):
    # 切换目录到etc目录
    confName = "replication.config"
    etcPath = "/devops/review_site/etc"
    os.chdir(etcPath)
    # ls -l
    subprocess.call("ls -l", shell=True)
    # 备份replication.config
    bakPath = etcPath+"/replication.config-bak"
    command = "cp replication.config "+bakPath + "/%s" % confName + "-" + time.strftime("%Y%m%d%H%M%S")
    # 执行命令
    print(command)
    subprocess.call(command, shell=True)
    # ls -l
    subprocess.call("ls -l %s" % bakPath, shell=True)

    # 更新replication.config
    oldField = '''

[remote "edu_qqzw/dulwich_wohui/dulwich_sso_web"]
projects = edu_qqzw/dulwich_wohui/dulwich_sso_web
url = ssh://git@code.iflytek.com:30004/edu_qqzw/dulwich_wohui/dulwich_sso_web.git
push = +refs/heads/*:refs/heads/*
push = +refs/tags/*:refs/tags/*
push = +refs/changes/*:refs/changes/*
threads = 3
mirror = true
replicationDelay = 0
    
    '''
    # 替换字符为新配置
    newField = oldField.replace("edu_qqzw/dulwich_wohui/dulwich_sso_web", "%s/%s" % (groupName, projectName))
    print("新仓库配置: "+newField)
    # 将newField写入replication.config最后一行
    with open(confName, "a") as f:
        f.write(newField)
    # 打印新配置文件
    # with open(confName, "r") as f:
    #     print(f.read())

    # 重启replication插件
    command = "ssh -p 29418 leigao6@codereview.test.com gerrit plugin reload replication"
    # 执行命令
    print(command)
    subprocess.call(command, shell=True)
    # 检查replication插件是否重启成功
    command = "ssh -p 29418 leigao6@codereview.test.com gerrit plugin ls"
    # 执行命令
    print(command)
    # 获取命令的输出
    output = subprocess.check_output(command, shell=True)
    print(output)
    # 判断是否重启成功
    if "replication                    v3.4.0     3.4.0            ENABLED  replication.jar" in output:
        print("replication插件重启成功")
    else:
        print("replication插件重启失败，请检查配置文件")
        sys.exit(0)


# 修改继承项目
def updateInherit(groupName, projectName):
    # 修改继承项目
    command = "ssh -p 29418 leigao6@codereview.test.com gerrit set-project-parent --parent EPD_QQZW_XXJ/ACESS_PJ %s/%s" % (groupName, projectName)
    # 执行命令
    print(command)
    subprocess.call(command, shell=True)
    # 查看继承项目
    url = "http://codereview.test.com:8081/a/projects/%s/access" % (groupName+"%2f"+projectName)
    headers = {
        'Authorization': 'Basic XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX='
    }
    response = requests.request("GET", url, headers=headers)
    if "EPD_QQZW_XXJ/ACESS_PJ" in response.text:
        print("继承项目修改成功")
    else:
        print("继承项目修改失败，请检查配置文件")
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("参数为空，请检查")
        print("Usage: ")
        print("python GerritMain.py STC_Opera_Group testmod")
        sys.exit(0)

    if sys.argv[1] == "" or sys.argv[2] == "":
        print("参数为空，请检查")
        print("Usage: ")
        print("python GerritMain.py STC_Opera_Group testmod")
        sys.exit(0)
    groupName = sys.argv[1]
    projectName = sys.argv[2]
    createProject(groupName, projectName)
    cloneGitee(groupName, projectName)
    updateReplication(groupName, projectName)
    updateInherit(groupName, projectName)


