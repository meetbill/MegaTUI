# megatui

megacli 终端界面管理工具

![Screenshot](images/lvinfo.png)

## 使用手册

> * [使用手册](https://github.com/BillWang139967/megacli_tui/wiki)

## 相关项目

> * megacli 库 [megacli-python](https://github.com/m4ce/megacli-python)
> * python TUI 库 [py_menu](https://github.com/BillWang139967/py_menu)

## 版本发布

版本号根据 `three_page.py` 程序而定

* v1.0.8，2017-11-02，更新：物理磁盘输出内容中新增 `device_ID`,添加获取磁盘的 rebuild 进度信息
* v1.0.7，2017-10-29，更新：物理硬盘输出内容中新增 `vd` 列，以确定不同槽位的硬盘隶属的 raid 组
* v1.0.6，2017-10-21，更新：支持单台服务器多个 `raid` 卡检测
* v1.0.5，2017-10-16，新增：查询物理硬盘时会输出硬盘背板 ID(enclosure ID)。
* v1.0.4，2017-10-16，新增：部署后使用 `megatui` 命令调用此程序。
* v1.0.3，2017-10-11，新增：修复无创建 raid 组时查询虚拟磁盘失败问题。
* v1.0.2，2017-04-06，新增：虚拟磁盘查询。
* v1.0.1，2017-03-22，新增：发布初始版本。
