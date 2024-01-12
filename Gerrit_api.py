import requests
import json


# gerrit-api基类
class base_api:
    def __init__(self):
        url = "http://codereview.test.com:8081/a/"
        self.url = url
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic XXXXXXXXXXXXXXXXXXXXXXXX='
        }
        self.headers = headers

    # 获取所有项目
    def projects(self, is_all=None):
        if is_all is None:
            projects_url = self.url + "projects/"
        else:
            projects_url = self.url + "projects/?all"
        r = requests.get(projects_url, headers=self.headers)
        # 去掉多余的字符
        r = r.text[5:-1]
        return r

    # 获取权限
    def permission(self, project):
        # 替换project中的/为%2F
        project = project.replace("/", "%2F")
        permission_url = self.url + "access/?project=" + project
        r = requests.get(permission_url, headers=self.headers)
        r = r.text[5:-1]
        return r

    # 删除权限
    def delete_permission(self, project, user_list):
        project = project.replace("/", "%2F")
        url = self.url + "projects/" + project + "/access"
        # 执行删除
        success_list = []
        fail_list = []
        for user in user_list:
            payload = json.dumps({
                "remove": {
                    "refs/*": {
                        "permissions": {
                            "owner": {
                                "rules": {
                                    "{}".format(user): {
                                        "action": "ALLOW"
                                    }
                                }
                            }
                        }
                    }
                }
            })
            print(payload)
            r = requests.post(url, headers=self.headers, data=payload)
            if r.status_code == 200:
                print("删除{}权限成功".format(user))
                success_list.append(user)
            else:
                print("删除{}权限失败".format(user), "报错内容为{}".format(r.text))
                fail_list.append(user)
        if len(fail_list) == 0:
            return "success"
        else:
            return "fail"

    # 恢复权限
    def recover_permission(self, project, user_list):
        project = project.replace("/", "%2F")
        url = self.url + "projects/" + project + "/access"
        # 执行恢复
        success_list = []
        fail_list = []
        for user in user_list:
            payload = json.dumps({
                "add": {
                    "refs/*": {
                        "permissions": {
                            "owner": {
                                "rules": {
                                    "{}".format(user): {
                                        "action": "ALLOW"
                                    }
                                }
                            }
                        }
                    }
                }
            })
            r = requests.post(url, headers=self.headers, data=payload)
            if r.status_code == 200:
                print("恢复{}权限成功".format(user))
                success_list.append(user)
            else:
                print("恢复{}权限失败".format(user), "报错内容为{}".format(r.text))
                fail_list.append(user)
        if len(fail_list) == 0:
            return "success"
        else:
            return "fail"

    # 设置project状态
    def state(self, project, state):
        # 替换project中的/为%2F
        project = project.replace("/", "%2F")
        url = self.url + "projects/" + project + "/config"
        state_data = ['ACTIVE', 'READ_ONLY', 'HIDDEN']
        if state in state_data:
            payload = json.dumps({"state": state})
            r = requests.put(url, headers=self.headers, data=payload)
            return r.text, r.status_code


