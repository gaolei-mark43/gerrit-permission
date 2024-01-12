import Gerrit_api
import json
import datetime
import os


class Repo:
    def __init__(self, action, repo_name, bak_file=None):
        self.action = action
        self.repo_name = repo_name
        self.bak_file = bak_file

    # 封存仓库
    def seal_up_repo(self):
        if self.action == "seal":
            print("开始封存仓库{}".format(self.repo_name))
            # 封存仓库
            # 查看仓库是否存在owner权限
            result = api.permission(self.repo_name)
            result = json.loads(result)
            permission = result['{}'.format(self.repo_name)]['local']
            # 判断refs/*这个key是否存在
            if 'refs/*' in permission.keys() and 'owner' in str(permission['refs/*']):
                print("仓库{}存在owner权限，开始封存".format(self.repo_name))
                # 备份owner权限
                owner_permission = permission['refs/*']['permissions']['owner']
                user_list = []
                bak_list = []
                for key in owner_permission['rules'].keys():
                    print("开始备份{}权限".format(key))
                    bak_list.append(key)
                    user_list.append(key)
                # 新建bak目录
                if not os.path.exists("bak"):
                    os.mkdir("bak")
                os.chdir("bak")
                # 写入文件，文件名称为仓库名加时间戳
                with open(self.repo_name + "-" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".txt", "w") as f:
                    f.write(str(bak_list))
                    print("备份完成", os.listdir(os.getcwd()))
                # 删除owner权限
                print("删除人员为{}".format(user_list))
                result = api.delete_permission(self.repo_name, user_list)
                if result == "success":
                    print("删除owner权限成功")
                    # 调用state接口设置Hidden状态
                    result = api.state(self.repo_name, "HIDDEN")
                    if result[1] == 200:
                        print("封存仓库{}成功".format(self.repo_name))
                    else:
                        print("封存仓库{}失败".format(self.repo_name), "报错内容为{}".format(result[0]))
                elif result == "fail":
                    print("删除owner权限失败")

            else:
                print("仓库{}不存在owner权限，开始封存".format(self.repo_name))
                # 不存在就调用state接口设置Hidden状态
                result = api.state(self.repo_name, "HIDDEN")
                if result[1] == 200:
                    print("封存仓库{}成功".format(self.repo_name))
                else:
                    print("封存仓库{}失败".format(self.repo_name), "报错内容为{}".format(result[0]))

    # 恢复仓库
    def recover_repo(self):
        if self.action == "recover":
            # 读取文件
            with open(self.bak_file, "r") as f:
                user_list = eval(f.read())
            # 恢复权限
            print("开始恢复仓库{}权限".format(self.repo_name))
            result = api.recover_permission(self.repo_name, user_list)
            if result == "success":
                print("恢复{}权限成功".format(self.repo_name))
                # 调用state接口设置Active状态
                result = api.state(self.repo_name, "ACTIVE")
                if result[1] == 200:
                    print("恢复仓库{}成功".format(self.repo_name))
                else:
                    print("恢复仓库{}失败".format(self.repo_name), "报错内容为{}".format(result[0]))
            elif result == "fail":
                print("恢复{}权限失败".format(self.repo_name))


if __name__ == '__main__':
    api = Gerrit_api.base_api()
    # 封存temppj仓库
    # repo = Repo("seal", "temppj")
    # repo.seal_up_repo()
    # # 恢复temppj仓库
    repo = Repo("recover", "temppj", "bak/temppj-20230907153845.txt")
    repo.recover_repo()


