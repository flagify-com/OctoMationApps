# 山石云瞻.威胁情报应用（基于API）

## 介绍
- 版本：v 1.1.1
- 作者：[wzfukui](https://github.com/wzfukui)
- 发布：2024-07-30
- 更新：2024-08-02
- 编程语言：Python 3.6+
- 依赖库：requests

## 功能

根据[山石云瞻威胁情报](https://ti.hillstonenet.com.cn/apihelp)官方API实现，可针对IP、域名、文件HASH、URL进行威胁情报查询。因为高级信息接口返回的信息包括基础信息，因此直接对接了高级接口。

*注意1：免费版API有使用限制：6次/分钟，1500次/天*
*注意2：部分数组类型的返回数据可能为空，取值时需要注意，可能取不到数据，例如:rdns_list*
*注意3: 风险等级包括malicious， normal，suspicious，unknown，以及unreported（山石中没有查到数据，人工赋予）
*注意4: 支持作战室中以日志模式执行，查看原始数据返回结果。

## API KEY获取方式

注册账号，访问山石云服务后台，https://cloud.hillstonenet.com.cn/console/account/subscription-management/management?type=1，点击【应用订阅与管理】，点击进入山石云瞻威胁情报中心【授权管理】。

## 返回码说明

| 状态码 | 说明           |
|--------|----------------|
| 1      | 未查询到报告   |
| 0      | OK             |
| -1     | 鉴权错误       |
| -2     | 查询总量超限   |
| -3     | 查询频率过高   |
| -4     | 查询值异常     |
| -5     | 请求无效       |

## 威胁类型汇总

| 英文标签           | 中文标签           | 中文描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bogon              | 未启用IP           | Bogon是RFC 1918，RFC 5735和RFC 6598定义的私有和保留地址和尚未由Internet分配号码机构分配给区域Internet注册表（RIR）的网块。Fullbogon是一个更大的集合，其中还包括已分配给RIR但未被该RIR分配给实际ISP或其他最终用户的IP空间。                                                                                                                                                |
| Whitelist          | 白名单             | 白名单广泛用于信息安全的各种场景，是指明确允许某些实体能够进行特定操作的做法。在威胁情报中，白名单是指已知的安全的IP地址或者域名。                                                                                                                                                                                                                                                                                                                |
| DGA                | DGA域名            | 由域名生成算法生成的域名。恶意软件会利用这类算法会生成大量的伪随机域名，用来和命令与控制服务器进行通信，以规避常规安全检测手段，隐藏攻击者身份。                                                                                                                                                                                                                                                                                                |
| CnC                | CnC                | 僵尸网络命令与控制服务器。僵尸网络是指采用一种或多种传播手段，将大量主机感染恶意程序，从而在控制者和被感染主机之间所形成的一个可一对多控制的网络。攻击者通过各种途径传播恶意程序感染互联网上的大量主机，而被感染的主机将通过一个控制信道接收攻击者命令与控制服务器的指令，组成一个僵尸网络。                                                                                                         |
| Sinkhole           | Sinkhole           | Sinkhole（DNS沉洞）一般指被安全厂商或者安全设备接管的已知恶意域名，用以阻止恶意软件进一步从命令与控制服务器接收指令。Sinkhole技术将用户路径从恶意或不可访问内容替代到不同的资源，以便安全分析人员可以捕获和分析它。                                                                                                                                                                                                                     |
| BruteForcer        | 暴力破解器         | 暴力破解是一种不断试错的方法，通过不停使用字典中的大量字符串进行尝试，直到获取正确的用户名密码或其他目标字符串的做法。暴力破解器是指存在SSH或其他暴力破解行为的主机。                                                                                                                                                                                                                                                  |
| Compromised        | 失陷主机           | 失陷主机是指被黑客攻击并被成功控制的主机。                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Scanner            | 扫描器             | 扫描器能够对网络中的IP，端口，操作系统，服务版本等进行大批量扫描，来收集信息，供后续攻击行为使用。                                                                                                                                                                                                                                                                                                                                                  |
| Botnet             | 僵尸网络           | 僵尸网络是指采用一种或多种传播手段，将大量主机感染恶意程序，从而在控制者和被感染主机之间所形成的一个可一对多控制的网络。攻击者通过各种途径传播恶意程序感染互联网上的大量主机，而被感染的主机将通过一个控制信道接收攻击者命令与控制服务器的指令，组成一个僵尸网络。                                                                                                         |
| APT                | APT攻击            | 高级可持续性攻击，又称APT攻击，通常由国家背景的相关攻击组织进行攻击的活动。APT攻击常用于国家间的网络攻击行动。主要通过向目标计算机投放特种木马，实施窃取国家机密信息、重要企业的商业信息、破坏网络基础设施等活动，具有强烈的政治、经济目的。                                                                                                                                                                                 |
| CredentialStuffing | 撞库攻击           | 自动化的使用被盗的用户名密码对受害服务器进行尝试性的登录。                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Miner              | 挖矿               | Miner是指存在数字货币挖矿行为的地址。数字货币被越来越多的被用于黑产交易，攻击者通过植入挖矿病毒，使受害系统成为Miner，占用受害系统硬件资源为攻击者挖矿，获取数字货币。                                                                                                                                                                                                                                                   |
| Proxy              | 代理服务器         | 代理服务器是一种服务器应用程序或设备，它为客户端的请求充当中介，将请求转发给服务器端，包括HTTP代理、SOCKS代理、VPN节点等。代理服务器可以用来隐藏客户端真实身份。                                                                                                                                                                                                                                                                          |
| TorNode            | 暗网节点           | Tor是洋葱路由器的缩写，通过接入Tor网络，用户可以隐藏自己的真实地址。Tor可以被应用于合法目的上，也可应用于非法目的上。犯罪企业、黑客组织会为了各种目的而使用Tor。                                                                                                                                                                                                                                                                        |
| DropSite           | 外泄数据站点       | 存放外泄数据的站点                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| DriveBySrc         | 路过式下载         | 路过式下载是一个在未经用户同意或用户未知的情况下自动下载到用户的计算机上的程序。利用浏览器漏洞的恶意软件会通过html注入的方式在用户不知情的情况下从属于该分类的IP地址或者域名下载恶意内容。                                                                                                                                                                                                                                    |
| EXESource          | 可执行程序源       | 可疑的可执行程序下载站点                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| MalwareSite        | 恶意软件站点       | 和恶意软件相关的站点。某些恶意软件代码中包含该站点，或者会访问该站点。                                                                                                                                                                                                                                                                                                                                                                                                            |
| Private            | 私有地址           | 协议中规定的私有IP地址。该类地址一般不会被路由到广域网中。                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Reserved           | 保留地址           | 协议中规定的保留IP地址。该类地址一般不会被路由到广域网中。                                                                                                                                                                                                                                                                                                                                                                                                                       |
| others             | 其它               | 其它                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Trojan             | 木马               | 特洛伊木马（Trojan Horse）常被简称木马，在计算机领域中指的是一种后门程序，是黑客用来盗取其他用户的个人信息，甚至是远程控制对方的计算机而加壳制作，然后通过各种手段传播或者骗取目标用户执行该程序，以达到盗取密码等各种数据资料等目的。该地址和木马相关。                                                                                                                            |
| Backdoor           | 后门               | 后门是一种恶意软件，可以绕过安全性限制来获得对计算机系统的未经授权的访问。 换句话说，后门是一段代码，它允许他人进入和退出系统而不会被检测到。该地址和后门软件相关。                                                                                                                                                                                                                                                             |
| Worm               | 蠕虫               | 计算机蠕虫是一种恶意软件，可将其自身的副本在计算机之间传播。 蠕虫可以在没有任何人工干预的情况下进行自我复制，并且不需要将其附加到软件程序中即可造成损害。该地址和蠕虫相关。                                                                                                                                                                                                                                                      |
| Malware            | 恶意软件           | 恶意软件是故意设计成对计算机，服务器，客户端或计算机网络造成损害的任何软件。 存在多种类型的恶意软件，包括计算机病毒，蠕虫，特洛伊木马，勒索软件，间谍软件，广告软件，流氓软件和恐吓软件。该地址和恶意软件相关。                                                                                                                                                                                                                             |
| Ransomware         | 勒索软件           | 勒索软件（Ransomware）是指黑客用来劫持用户资产或资源并以此为条件向用户勒索钱财的一种恶意软件。该地址和勒索软件相关。                                                                                                                                                                                                                                                                                                                                                          |
| AdWare             | 广告软件           | 恶意广告软件（Adware）是指未经用户允许，下载并安装或与其他软件捆绑通过弹出式广告或以其他形式进行商业广告宣传的程序。安装广告软件之后，往往造成系统运行缓慢或系统异常。一些恶意广告软件可能会集成间谍软件 ，如键盘记录程序和隐私盗取软件等其它恶意程序。该地址和广告软件相关。                                                                                                                                                         |
| FakeAV             | 伪杀毒软件         | 伪杀毒软件（FakeAV）是一种伪装成杀毒软件的恶意程序，在安装后会假装进行扫描系统然后报出很多病毒让用户进行购买。该地址和伪杀毒软件相关。                                                                                                                                                                                                                                                                                                                                          |
| GrayWare           | 灰色软件           | 灰色软件（GrayWare）不是病毒或者木马，但可能对用户有害或者会引起用户反感。该地址和灰色软件相关。                                                                                                                                                                                                                                                                                                                                                                                  |
| RiskWare           | 风险软件           | 风险软件（RiskWare）是合法程序，如果被恶意用户利用，它们可能会造成破坏，从而删除，阻止，修改或复制数据，并破坏计算机或网络的性能。该地址和风险软件相关。                                                                                                                                                                                                                                                                                                               |
| HackTool           | 黑客工具           | 黑客工具（HackTool）是一类攻击者或恶意代码作者所使用的工具。黑客工具一般没有主动传播自身、感染其他文件和直接损害当前主机安全的行为，一般仅作为攻击者收集目标信息、进行探测或反制安全软件的工具。其设计的目的是用于配合网络攻击和恶意代码的生产与传播。部分黑客工具可以与恶意代码组合使用充当其功能模块，也可以用于构造和修改恶意代码。该地址和黑客工具相关。                                             |
| Phishing           | 网络钓鱼           | 网络钓鱼是通过伪装成电子通信中的可信赖实体来获取用户名，密码和信用卡详细信息等敏感信息的欺诈性尝试。 通常通过电子邮件欺骗或即时消息传递来执行，它通常会指导用户在这类与合法网站的外观和风格相匹配的假网站上输入个人信息。                                                                                                                                                                                                                                        |
| Spam               | 发送垃圾邮件       | 该地址会在未经接收者允许的情况下大量、重复发送无用的广告信息给接收者。                                                                                                                                                                                                                                                                                                                                                                                                         |
| DoS                | 拒绝服务攻击       | 拒绝服务攻击（DOS）工具,会导致目标服务中止。此类程序会对目标发送大量畸形数据包，阻塞目标网络带宽。该类别包括发动拒绝服务攻击或者分布式拒绝服务攻击（DDoS）的地址。                                                                                                                                                                                                                                                                                   |
| Exploit            | 漏洞利用           | 漏洞利用(Exploit)，通常可以获得远程主机的root权限和远程shell,此类工具通常针对某一个特定服务，利用该服务程序的边界检查不完善等漏洞，溢出获得系统权限。该类地址和漏洞利用相关。                                                                                                                                                                                                                                                       |
| TestFile           | 引擎测试程序       | 反病毒测试文件，该地址和反病毒测试文件相关。                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| DDNS               | 动态DNS            | 动态DNS（DDNS）是一种实时自动更新域名系统（DNS）中名称服务器的主机名                                                                                                                                                                                                                                                                                                                                                                                                              |
| EngineCrawler      | 搜索引擎爬虫       | 搜索引擎通过爬虫访问和下载页面，并进一步分析提取链接从而发现新的网页。                                                                                                                                                                                                                                                                                                                                                                                                             |
| InternetMapping    | 网络空间测绘       | 网络空间测绘通过探测、采集、分析和处理，发现识别网络空间设施、服务和资源，基于地理信息和逻辑关系进行图形绘制，直观展现网络空间资产、属性、状态和安全态势等。                                                                                                                                                                                                                                                                                               |
| WebAttacker        | Web攻击            | Web攻击是基于HTTP流量的攻击，包含多种攻击技术，例如跨站脚本注入，SQL注入等，攻击成功可能给用户带来巨大危害。                                                                                                                                                                                                                                                                                                                                                                   |
| DNS/NTPServer      | DNS/NTP服务器      | DNS/NTP服务器为网络基础设施，提供域名解析/时间同步服务。由于响应包比请求包大，攻击者可以利用此特点伪造请求源IP进行反射攻击。                                                                                                                                                                                                                                                                                                                                                   |
| BlackMarket        | 黑灰产             | 通过人工方式或者技术手段实施的操纵网络信息内容，获取违法利益、破坏网络生态秩序的行为                                                                                                                                                                                                                                                                                                                                                                                              |


## 典型数据返回结果示例

### IP查询
```json
{
  "msg": "",
  "code": 200,
  "data": {
    "risk_level": "suspicious",
    "err_msg": "",
    "err_code": 0,
    "threat_type": [
      
    ],
    "detail": {
        "result": "suspicious",
        "rdns_list": [
          {
            "domain_name": "web.salvrp.com",
            "lookup_time": 1629412235065
          }
        ],
        "basic_info": {
          "carrier": "FranTech Solutions",
          "location": {
            "country": "United States",
            "country_code": "US",
            "province": "Nevada",
            "city": "Las Vegas",
            "latitude": 36.171909,
            "longitude": -115.139969
          },
          "network": "199.19.224.0/22"
        },
        "current_domains": [
          
        ],
        "connect_files": [
          
        ],
        "history_domains": [
          {
            "date": 1636980029000,
            "domain_name": "v.lczp.cf"
          },
          {
            "date": 1626480000000,
            "domain_name": "web.rmog.us"
          }
        ],
        "ip_address": "199.19.224.129",
        "ports": [
          
        ],
        "referer_files": [
          
        ],
        "download_files": [
          
        ]
      }
  }
}
```

### 域名查询

```json
{
  "msg": "",
  "code": 200,
  "data": {
    "risk_level": "normal",
    "err_msg": "",
    "err_code": 0,
    "threat_type": [
      
    ],
    "detail": {
        "result": "normal",
        "history_ips": [
          {
            "date": 1670112000000,
            "ip_address": "140.82.121.3"
          },
          {
            "date": 1670112000000,
            "ip_address": "20.205.243.166"
          },
          {
            "date": 1670025600000,
            "ip_address": "13.229.188.59"
          },
          {
            "date": 1670025600000,
            "ip_address": "192.30.253.113"
          },
          {
            "date": 1669939200000,
            "ip_address": "52.74.223.119"
          },
          {
            "date": 1669939200000,
            "ip_address": "192.30.253.112"
          },
          {
            "date": 1660242112000,
            "ip_address": "20.27.177.113"
          },
          {
            "date": 1660052421000,
            "ip_address": "20.207.73.82"
          },
          {
            "date": 1659219665000,
            "ip_address": "20.200.245.247"
          },
          {
            "date": 1656534922000,
            "ip_address": "20.248.137.48"
          }
        ],
        "domain_name": "github.com",
        "domain_siblings": [
          
        ],
        "current_whois": "Admin Country: US\nAdmin Organization: GitHub, Inc.\n...Updated Date: 2022-09-07T09:10:44+0000\nUpdated Date: 2022-09-07T09:10:44Z",
        "dns_records": [
          "ns-1707.awsdns-21.co.uk",
          "dns4.p08.nsone.net"
        ],
        "sub_domains": [
          "ivaynberg.github.com",
          "jonthornton.github.com"
        ],
        "connect_files": [
          "821bcc4fd35ed62784bf991768376baf",
          "895030b037fd8b1aa02bc036d6ae964a"
        ],
        "referer_files": [
          "30abc67b8797791b806a30e86e0e8466",
          "eb63bc2e399b0746a1168aa227304593709944e64528e1c5d73dc4908f3d5af1"
        ],
        "current_ips": [
          "20.205.243.166",
          "140.82.116.3"
        ],
        "download_files": [
          "2064a3b61ffb6841f930cad9e9cac665",
          "93e69c2ad0af362c07acc9b7533afe87"
        ]
      }
  }
}
```

### URL查询

```json
{
  "msg": "",
  "code": 200,
  "data": {
    "risk_level": "normal",
    "err_msg": "",
    "err_code": 0,
    "threat_type": [
      
    ],
    "detail": {
        "result": "normal",
        "hash_sha256": "996e1f714b08e971ec79e3bea686287e66441f043177999a13dbc546d8fe402a",
        "related_files": [
          "c26ae551673da969c6619688a5752a10",
          "07d4d97803f409818821ae052de4dc62"
        ],
        "related_domains": [
          
        ],
        "related_ips": [
          
        ],
        "url": "https://github.com"
      }
  }
}
```
### 文件查询

```json
{
  "msg": "",
  "code": 200,
  "data": {
    "risk_level": "malicious",
    "err_msg": "",
    "err_code": 0,
    "threat_type": [
      "Miner"
    ],
    "detail": {
        "basic_info": {
          "first_seen": 1590605043000,
          "last_seen": 1590605043000,
          "file_type": "Win32 EXE",
          "scan_date": 1591248854000,
          "file_size": 6392320
        },
        "sha256": "14883d4357a0ed3fffb57a1990f18b5f266eec1c349750b8f2302a18422a1664",
        "referer_ips": [
          "0.1.1.1",
          "127.0.0.1",
          "223.255.255.255",
          "239.255.255.250"
        ],
        "tags": [
          
        ],
        "result": "malicious",
        "sha1": "f81536f9e1213c9278840c512a01cf203e2944e5",
        "connect_ips": [
          "1.83.125.62"
        ],
        "download_ips": [
          
        ],
        "threat_type": [
          "Miner"
        ],
        "connect_domains": [
          
        ],
        "download_domains": [
          
        ],
        "referer_domains": [
          "galactic-bits.ml",
          "gist.github.com",
          "github.com",
          "schemas.xmlsoap.org"
        ],
        "md5": "30abc67b8797791b806a30e86e0e8466"
      }
  }
}
```

## 更新记录

- 2024-07-30: v 1.0.0 发布
- 2024-08-02: v 1.1.0 修改查询结果的输出数据格式，增加日志模式支持
- 2024-08-02: v 1.1.1 bug修复
  - 移除healthcheck动作中sdk日志操作（context不支持）
  - 修改API KEY为密钥类型