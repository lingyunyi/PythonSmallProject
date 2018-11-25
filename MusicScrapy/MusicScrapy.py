# 导入requests爬虫数据库
import requests
# 导入正则库
import re
# 导入系统库
import sys
# 导入OS库
import os
class MusicScrapy(object):
    '''
    音乐爬虫类
    '''
    def __init__(self):
        # 歌手名字
        self.singer = None
        # 歌手链接
        self.singerUrl = None
        # 歌手头像链接
        self.singerImgUrl = None
        # 当前工作路径
        self.workPath = None
        # 执行获取当前目录函数
        self.selectFolder()
        # 歌手所有页面的页面
        self.singerListLength = None
        # 歌手名字列表
        self.singerNameList = []
    def selectFolder(self):
        '''
        以当前文件夹为一个根目录并创建一个子文件夹，以子文件夹为下载目录，返回一个文件夹给下载函数
        :return:
        '''
        # 获得当前文件执行的文件目录
        newPath = os.getcwd()
        # 判断是否存在子文件夹
        childPath = os.path.join(newPath,"img")
        # 如果子文件夹img存在
        if os.path.exists(childPath):
            # 进入该目录
            os.chdir(childPath)
            newPath = os.getcwd()
        else:
            # 如果不存在将创建该文件夹
            os.mkdir(childPath)
            # 并且也选择该文件夹
            os.chdir(childPath)
            # 最后在获取当前文件工作路径
            newPath = os.getcwd()
        # 返回工作路径
        self.workPath = newPath
        return self.workPath
    def singerSearch(self,musicName):
        '''
        输入搜索歌曲名，返回其歌手以及歌手链接
        :param musicName:音乐名字
        :return:歌手名字，歌手链接
        '''
        # 请求头设置
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://sou.kuwo.cn/ws/NSearch?type=all&catalog=yueku2016&key=%s" %str(musicName)
        # 提交搜索数据获得回应
        respond = requests.get(url,headers=headers)
        # 获取回应中的html代码
        musicHtml = respond.content.decode("utf-8")
        # 利用正则过滤文件搜索出歌手姓名以及歌手对应的连接
        singerAndUrl = re.findall(r'<p class="s_name"><a href="(.*?)" target="_blank" title="(.*?)">', musicHtml)[0]
        # 将歌手名字以及链接区分开来
        (singer,singerUrl) = singerAndUrl[1],singerAndUrl[0]
        # 将其赋值给类变量
        (self.singer,self.singerUrl) = singer,singerUrl
        self.getSingerImgUrl()
        return self.singer,self.singerUrl
    def getSingerImgUrl(self):
        '''
        通过传入的歌手链接，返回歌手图像图片
        :param singerUrl:
        :return:
        '''
        # 如果歌手链接不等于空执行
        if self.singerUrl != None:
            # 设置请求头
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
            # 提交搜索数据获得回应
            respond = requests.get(self.singerUrl,headers=headers)
            # 获取回应中的html代码
            singerHtml = respond.content.decode("utf-8")
            # 利用正则匹配图片链接
            singerImg = re.findall(r'<img.*?data-src="(.*?)".*?class="lazyLoad" />', singerHtml)[0]
            # 获得图片并修改起大小
            singerImgUrl = singerImg.replace("180","150")
            self.singerImgUrl = singerImgUrl
            return self.singerImgUrl
        else:
            # 否则返回错误，代表singer搜索函数未执行
            return False
    def downLoadImg(self):
        '''
        通过传入的图像连接进行下载
        :param singer:
        :param singerImgUrl:
        :return:
        '''
        # 设置请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        # 提交搜索数据获得回应
        respond = requests.get(self.singerImgUrl, headers=headers)
        # 保存照片内容
        img = respond.content
        # 创建文件并且保存照片
        # 选择下级路径
        # 如果选择路径函数执行成功则执行
        if self.workPath != None:
            os.chdir(self.workPath)
            fp = open(self.singer + ".jpg", 'wb')
            fp.write(img)
            fp.close()
            # 返回下载成功
            return True
        else:
            # 否则下载失败
            return False
    def getSingerListLength(self):
        '''
        获取该页面的页面数
        :return:
        '''
        # 请求头设置
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.kuwo.cn/artist/index"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        singerHtml = respond.content.decode("utf-8")
        # 利用正则过滤文件搜索出歌手姓名以及歌手对应的连接
        singerListLength = re.findall(r'<div class="page" data-page="(.*?)"></div>', singerHtml)[0]
        self.singerListLength = int(singerListLength)
        return self.singerListLength
    def getSingerNameList(self):
        '''
        获取所有的歌手，并返回一个列表
        :return: 歌手名字列表
        '''
        # 获取歌手页面长度
        self.getSingerListLength()
        # 获取歌手名字
        if self.singerListLength != None:
            # 遍历歌手页面长度
            for i in range(self.singerListLength):
                # 请求头设置
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
                # catepgory为种类，0为全部，pn为页面数
                url = r"http://www.kuwo.cn/artist/indexAjax?category=0&prefix=&pn=%s" %(i)
                # 提交搜索数据获得回应
                respond = requests.get(url, headers=headers)
                # 获取回应中的html代码
                singeNameHtml = respond.content.decode("utf-8")
                # 利用正则过滤文件搜索出歌手姓名以及歌手对应的连接
                singerName = re.findall(r'<a href="/artist/content\?name=(.*?)" class="a_name">', singeNameHtml)
                # 将名字添加入名字列表中
                self.singerNameList.extend(singerName)
        return self.singerNameList
    def bySingerGetSingerId(self,singerName):
        '''
        通过输入歌手名字返回歌手姓名
        :param singerName: 歌手姓名
        :return:
        '''
        # 设置搜索参数
        params = {
            "name" : str(singerName)
        }
        url = "http://www.kuwo.cn/artist/content?"
        # 设置请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers, params=params)
        # 获取回应中的html代码
        singerPageHtml = respond.content.decode("utf-8")
        # 获取歌手活动ID
        singerArtistId = re.findall(r'<div class="artistTop" data-artistid="(.*?)">', singerPageHtml)
        singerMusicPage = re.findall(r'<div class="page" data-page="(.*?)"></div>', singerPageHtml)
        self.singerArtistId = int(singerArtistId[0])
        self.singerMusicPage = int(singerMusicPage[0])
        # 返回歌手ID以及歌手音乐列表数
        return self.singerArtistId, self.singerMusicPage
    def bySingergetMusicList(self, singerName):
        self.singerMusicList = []
        self.bySingerGetSingerId(singerName)
        # 地址
        url = "http://www.kuwo.cn/artist/contentMusicsAjax?"
        # 设置搜索参数
        # 设置请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        # 只获取五页
        for i in range(5):
            params = {
                "artistId" : self.singerArtistId,
                # "&pn" : int(self.singerMusicPage), 该条命令为取完所有的歌曲目录
                "&pn": i,
                "&rn" : 15
            }
            # 提交搜索数据获得回应
            respond = requests.get(url, headers=headers, params=params)
            # 获取回应中的html代码
            musicListHtml = respond.content.decode("utf-8")
            # 获取连接以及歌曲名字
            musicList = re.findall(r'<div class="name"><a href="(.*?)" target="_blank">(.*?)</a></div>', musicListHtml)
            for i in musicList:
                musicName = i[1]
                musicUrl = str(i[0]).replace(i[0],"http://www.kuwo.cn%s"%(i[0]))
                self.singerMusicList.extend([(musicName,musicUrl)])
        return self.singerMusicList
if __name__ == "__main__":
    oneMusic = MusicScrapy()