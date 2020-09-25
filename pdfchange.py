import sys
import os
from tkinter import *
import tkinter.filedialog

import glob
from os import path
from aip import AipOcr
from PIL import Image

import importlib
importlib.reload(sys)
 
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

root = Tk() #创建主窗口
root.title("功能选择") #设置窗口标题
root.geometry("400x120")

def baiduOCR(picfile, outfile):
    """利用百度api识别文本，并保存提取的文字
    picfile:    图片文件名
    outfile:    输出文件
    """
    filename = path.basename(picfile)
    
    
    APP_ID = '22677263';
    API_KEY = 'LouAYK67hg7EyWNCQ4g0x1Rw';
    SECRECT_KEY  = 'R9ZOlG9nedblGIV8BiWZAlj8pyopsMvS'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    
    i = open(picfile, 'rb')
    img = i.read()
    #print("正在识别图片：\t" + filename)
    message = client.basicGeneral(img)   # 通用文字识别，每天 50 000 次免费
    #message = client.basicAccurate(img)   # 通用文字高精度识别，每天 800 次免费
    #print("识别成功！")
    i.close();
    
    with open(outfile, 'a+') as fo:
        fo.writelines("+" * 60 + '\n')
        fo.writelines("识别图片：\t" + filename + "\n" * 2)
        fo.writelines("文本内容：\n")
        # 输出文本内容
        for text in message.get('words_result'):
            fo.writelines(text.get('words') + '\n')
        fo.writelines('\n'*2)
    #print("文本导出成功！")
    #print()

 
# 解析pdf文件函数
def parse(pdf_path):
    fp = open(pdf_path, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
 
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
 
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
 
        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0
 
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            num_page += 1  # 页面增一
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if isinstance(x,LTImage):  # 图片对象
                    num_image += 1
                if isinstance(x,LTCurve):  # 曲线对象
                    num_curve += 1
                if isinstance(x,LTFigure):  # figure对象
                    num_figure += 1
                if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                    num_TextBoxHorizontal += 1  # 水平文本框对象增一
                    # 保存文本内容
                    with open(r'test.doc', 'a',encoding='utf-8') as f:    #生成doc文件的文件名及路径
                        results = x.get_text()
                        f.write(results)
                        f.write('\n')
        print('对象数量：\n','页面数：%s\n'%num_page,'图片数：%s\n'%num_image,'曲线数：%s\n'%num_curve,'水平文本框：%s\n'
              %num_TextBoxHorizontal)

def pic():
    picfile = tkinter.filedialog.askopenfilename(initialdir='C',title='选择图片',filetypes=(("所有图片",("*.jpg","*.jpeg","*.png")),('All file','*.*')))

    if picfile != '':
        lb.config(text = "开始文字识别处理...");

        outfile = 'result.txt'
        if path.exists(outfile):
            os.remove(outfile)

        lb.config(text = "图片识别...");
        baiduOCR(picfile, outfile)
        lb.config(text = "图片文本提取结束！文本输出结果位于"+outfile+"文件中");
        
    else:
        lb.config(text = "您未选择文件！");

def pdf():
    file = tkinter.filedialog.askopenfilename(initialdir='C',title='选择PDF文件',filetypes=(("PDF文件",("*.pdf")),('All file','*.*')))
    if file != '':
        parse(file)
        lb1.config(text = "图片文本提取结束！文本输出结果位于test.doc文件中");
    else:
        lb1.config(text = "您未选择文件！");
lb = Label(root,text = '')
lb.pack()
btn1 = Button(root,text='图片识别文字提取',command = pic)
btn1.pack()
lb1 = Label(root,text = '')
lb1.pack()
btn2 = Button(root,text='PDF转WORD文档',command = pdf)
btn2.pack()
root.mainloop()
