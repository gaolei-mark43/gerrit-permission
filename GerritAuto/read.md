## 自动化新建Gerrit到Gitee仓库replication配置

### 拆分工作逻辑

1. **创建仓库**
   - 使用Gerrit命令行或API创建新的仓库。

2. **删除服务器上的Git实际存储目录**
   - 使用脚本或命令行删除刚刚创建的仓库的物理存储目录。

3. **克隆Gitee镜像库**
   - 在刚刚的目录下使用以下命令克隆Gitee仓库的镜像版本：
     ```
     git clone --bare gitee镜像库
     ```

4. **新增replication.config配置**
   - 在Gerrit的`etc`目录下，创建或修改`replication.config`文件以配置复制规则。这可以通过脚本或手动操作完成。

5. **重启Gerrit Replication插件**
   - 使用SSH连接到Gerrit服务器，执行以下命令以重新加载Replication插件：
     ```
     ssh -p 29418 leigao6@codereview.test.com gerrit plugin reload replication
     ```

6. **修改仓库权限**
   - 使用Gerrit命令行或API修改仓库的权限，将其改为继承EPD_QQZW_XXJ/ACESS_PJ。这可能需要编写脚本以自动化此过程，并确保将权限规则写成Markdown格式。
