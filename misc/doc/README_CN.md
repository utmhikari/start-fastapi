# start-fastapi

2021版，简易Web后端开发框架，基于[FastAPI](https://github.com/tiangolo/fastapi)

定位是快速实现效率工具（比如各类测试工具）、轻量级内容管理/数据处理后端

整个框架在fastapi基础上梳理了目录结构、配置等容易踩坑的内容，做了一些约定，这样业务就能基本专心写crud了

有兴趣的同学，也可以使用[2020版](https://github.com/utmhikari/start-fastapi/tree/v2020_final)

## 环境需求

- python 3.6+ (类型检查用)
- `pip3 install -r ./requirements.txt`
- idea/pycharm (推荐) + venv

## 项目结构

整个项目结构基于洋葱圈模型组织：

![onion](http://www.zyiz.net/upload/202006/15/202006150525428099.png)

目录结构如下:

- app: 业务逻辑的部分，以`__init__.py`为入口
    - handler: 控制器（controller）
    - middleware: web中间件
    - model: 各类数据结构及其内在逻辑（尽量与业务无关）
    - service: 业务逻辑服务
- cfg: 各运行环境的配置
    - dev: 开发环境配置
        - app.cfg: 形式为[python-dotenv](https://github.com/theskumar/python-dotenv)，fastapi的配置
        - uvicorn.json: [uvicorn](https://www.uvicorn.org/)的配置
        - logger.json: uvicorn日志配置，参考：[logging cfg](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py)
    - prod: 生产环境配置
- core: 底层逻辑的部分, 以`__init__.py`为入口。
    - handler
    - lib: 底层的library，与业务/数据结构无关，相当于框架内部的支持接口
    - model
    - service
        - trans: **事务服务**, 用于管理运行在后台的任务
- misc: 各种杂项，比如构建脚本、文档等
    - build: 构建脚本
    - dev: 开发期用的一些资源
        - gen_code.py: 生成代码的脚本
    - doc: 文档
    - test: 测试脚本
- main.py: 主入口
- requirements.txt: python包列表

## 快速上手

### 启动应用

运行 `./main.py`，可以启动范例project，包括以下内容:

- core核心模块: 健康检查接口、基础数据结构等
- [cors](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)跨域检查web中间件（当前全部为*）
- 一个简单的买卖市场的模型，包括产品product、消费者customer与购买逻辑

运行的机制如下:

- `./main.py`根据传入cmd args去读取`./cfg/{env}`里的配置, 调用`uvicorn.run`接口从`./app/__init__.py`启动fastapi应用
- 在`./app/__init__.py`的`startup`回调中，初始化core核心模块以及app文件夹下用户定义的业务模块

如果需要自定义启动脚本，可以统一放在`./misc/build`下

### 代码编写指南

可以遵循以下的约定编写代码：

- `./main.py`默认以dev环境启动，有热加载机制，方便开发
- handler/controller都放到`./app/handler`下, 注意在`./app/__init__.py`增加对应handler的`import`以及`APP.include_router`逻辑
- 在`./app/model`下定义相关的数据结构, 在`./app/service`下编写业务服务
- 如果需要[web中间件](https://fastapi.tiangolo.com/tutorial/middleware/)，在`./app/middleware`下编写

一些编写的tips:

- 调用GET `/docs`，可以快速调试各个handler
- 在fastapi应用中尽量避免出现协程（async def），因为主循环默认是asyncio，如果用协程可能阻塞主eventloop
- core的开发需要注意，一是得与业务无关，二是保证尽量无缝复用到其它项目中。比如各数据库/缓存的client逻辑、微信/钉钉机器人的service，都可以放到core里
- 可以自定义`./misc/dev/gen_code.py`去快速生成业务代码模板（在项目根目录下运行）
- 数据结构尽量继承`pydantic.BaseModel`，有很多值得挖掘的地方（序列化/反序列化是最常用的）

### HTTP返回数据

一般HTTP的返回数据，状态码200加上一个body就够用了

在handler逻辑中，可以用`./core/model/handler.py`的`Resp`去生成response body的模板，细节如下:

```text
{
  "success": bool,
  "message": str,
  "code": IntEnum,
  "data": Any,
}
```

用`Resp.ok`生成成功的，用`Resp.err`生成失败的

## 其它杂项

### WebSocket

例子里的handler：`./app/handler/test.py`，包括了一些websocket的例子

需要知道更多，可以参考：[websocket documentation](https://fastapi.tiangolo.com/advanced/websockets/)

### 部署

执行`./misc/build/pack.sh`可以把项目内容打包到`./misc/build/start-fastapi.tar.gz`

如果要部署到docker，可以参考这个：`./misc/build/Dockerfile`
