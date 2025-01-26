## Miniblink 简介

Miniblink 是 chromium的精简版,删除了音视频功能,移植使用了VC6的CRT。

[Miniblink GitHub地址](https://github.com/weolar/miniblink49)

> miniblink使用了wke的接口。wke的相关介绍可以google一下。
>
> 总的来说，miniblink的接口是纯C导出，只要使用wke.h即可加载。无需.lib。
>
> - 另外，请勿跨线程调用所有接口（除非接口有特殊申明）
> - 所有接口如果返回的是const utf8*，const wchar_t*类型的字符串，均不需要手动释放
> - miniblink暂时只支持windows系统
> - 发现错误或提供注意事项、避坑经验等请联系QQ：93527630
> - 参考项目[MBPython](https://github.com/lochen88/MBPython)。
> - MBPython使用demo请查看https://miniblink.net/views/doc/other.html
>





