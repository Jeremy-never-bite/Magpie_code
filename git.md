# git原理
![a](https://mmbiz.qpic.cn/mmbiz_png/uJDAUKrGC7Ksu8UlITwMlbX3kMGtZ9p0NJ4L9OPI9ia1MmibpvDd6cSddBdvrlbdEtyEOrh4CKnWVibyfCHa3lzXw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

Workspace：工作区，就是你平时存放项目代码的地方

Index / Stage：暂存区，用于临时存放你的改动，事实上它只是一个文件，保存即将提交到文件列表信息

Repository：仓库区（或本地仓库），就是安全存放数据的位置，这里面有你提交到所有版本的数据。其中HEAD指向最新放入仓库的版本

Remote：远程仓库，托管代码的服务器，可以简单的认为是你项目组中的一台电脑用于远程数据交换

# 步骤
## 1 安装git并连接到github
教程 [地址](https://blog.csdn.net/qq_42690368/article/details/82319238?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-82319238-blog-120997367.pc_relevant_3mothn_strategy_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-82319238-blog-120997367.pc_relevant_3mothn_strategy_recovery&utm_relevant_index=2)

## 2 克隆远程仓库到本地
`git clone git@github.com:Jeremy-never-bite/Magpie_code.git`


在本地有版本库的情况下，使用git pull从远程库获取最新commit 数据（如果有的话），并merge（合并）到本地
## 3 修改并增加文件


## 4 将add后的文件提交到本地仓库
将需要上传到远程仓库的文件写在add后面，将改动添加到暂存区
`git add [filename]`
为了简单可以直接写提交当前目录
`git add .`

## 5 git commit提交说明
`git commit -m ["提交的信息"]`

## 6 git push 推送到远程
`git push`
这样你就完成了向远程仓库的推送，branch 是分支名


<!-- $ git pull origin master
然后再进行：
$ git push origin master -->

## 7 分支
*  列出所有本地分支
`git branch`

*  列出所有远程分支
git branch -r

*   新建一个分支，但依然停留在当前分支
git branch [branch-name]

*  新建一个分支，并切换到该分支
git checkout -b [branch]

* 切换分支
git checkout [branch]

*   合并指定分支到当前分支
 git merge [branch]

*   删除分支
 git branch -d [branch-name]

*   删除远程分支
 git push origin --delete [branch-name]