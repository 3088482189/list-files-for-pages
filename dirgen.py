import os
import time
import codecs
import hashlib
import base64
from urllib.parse import quote
import json

config=json.loads(open("dirgen_assets/config.json").read())

site_name=config["site_name"]
search_typlist=config["search_typlist"]
search_each_file_length=config["search_each_file_length"]

if(config["use_cdn"]==1): layout_mb=open("dirgen_assets/layout_cdn.html","r").read()
else: layout_mb=open("dirgen_assets/layout.html","r").read()
node_mb=open("dirgen_assets/node.html","r").read()
passwd_mb=open("dirgen_assets/passwd.html","r").read()
custom_html=open("dirgen_assets/custom.html","r").read()
search_txt=open("search.txt","w")

icon_back  ="<i   class='mdui-color-white mdui-list-item-avatar mdui-list-item-avatar mdui-icon material-icons'>arrow_back</i>"
icon_dir   ="<i   class='mdui-color-white mdui-list-item-avatar mdui-list-item-avatar mdui-icon material-icons'>folder</i>"
icon_page  ="<i   class='mdui-color-white mdui-list-item-avatar mdui-list-item-avatar mdui-icon material-icons'>web</i>"

icon_md    ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-md.svg'></img>"
icon_js    ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-js.svg'></img>"
icon_py    ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-py.svg'></img>"
icon_go    ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-go.svg'></img>"
icon_pdf   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/pdf.svg'></img>"
icon_txt   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt.svg'></img>"
icon_bin   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/bin.svg'></img>"
icon_html  ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-html.svg'></img>"
icon_css   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-css.svg'></img>"
icon_cpp   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-cpp.svg'></img>"
icon_zip   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/ar.svg'></img>"
icon_deb   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/ar-deb.svg'></img>"
icon_rpm   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/ar-rpm.svg'></img>"
icon_apk   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/ar-apk.svg'></img>"
icon_img   ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/img.svg'></img>"
icon_other ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/x.svg'></img>"
icon_video ="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/vid.svg'></img>"
icon_script="<img class='mdui-color-white mdui-list-item-avatar' src='/dirgen_assets/icon/txt-script.svg'></img>"

def file_md_time(file_path):
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(os.stat(file_path).st_mtime))
def file_size(file_path):
    fsize=os.path.getsize(file_path)
    fsize=fsize/float(1024)
    return round(fsize,8)
def is_binary_file(file_path):
    with open(file_path,'rb') as file:
        initial_bytes=file.read(8192)
        file.close()
    return not any(initial_bytes.startswith(bom) for bom in (codecs.BOM_UTF16_BE,codecs.BOM_UTF16_LE,codecs.BOM_UTF32_BE,codecs.BOM_UTF32_LE,codecs.BOM_UTF8,)
                   ) and b'\0' in initial_bytes
def is_img(file):
    typlist={'jpg','png','bmp','jpeg','rgb','svg','tif','gif'}
    file=file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0
def is_txt(file):
    typlist={'txt','in','out'}
    file=file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0
def is_zip(file):
    typlist={'zip','rar','7z','cab'}
    file=file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0
def is_video(file):
    file=file.lower()
    typlist={'mp4','mkv','flv','avi'}
    for i in typlist:
        if(file.endswith(i)):
            return 1
    typlist={'mp3','flac','wav','ogg'}
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0
def path_to_link(path):
    list=path.split('/')
    str=''
    now=''
    for i in list:
        if(i=='.'):
            continue
        now += '/'+i
        str += '/'+"<a href='"+now+"/f_index.html' style='color: #2962ff'>"+i+"</a>"
    if(str==''):
        str=site_name
    return str
def add_search(file):
    if(is_binary_file(file)):
        return
    search_txt.write(file+"|-|-|-|"+"%.2f" % file_size(file)+"|-|-|-|\n\n")
    flag=0
    for i in search_typlist:
        if(file.endswith(i)):
            flag=1
    if(flag):
        t=open(file,"r").read()
        if(len(t) > search_each_file_length):
            search_txt.write(t[0:search_each_file_length])
        else:
            search_txt.write(t)
    search_txt.write("\n\n|-|=|-|\n\n")

def get(path):
    if(os.path.exists(os.path.join(path,"index.html"))): return 1
    now=layout_mb.replace("{%SITE_NAME%}",site_name)\
                 .replace("{%PATH%}",path)\
                 .replace("{%PATH_and_LINK%}",path_to_link(path))\
                 .replace("{%CUSTOM_HTML%}",custom_html)
    index=open(os.path.join(path,"f_index.html"),"w")
    exists_passwd=os.path.exists(os.path.join(path,".passwd"))
    Folders='''
<li class="mdui-subheader-inset">Folders</li>
<li href="../f_index.html" class="mdui-list-item mdui-ripple">
    <i class="mdui-list-item-avatar mdui-color-white"><img src="/dirgen_assets/icon/folder-parent.svg"></i>
    <a href="../f_index.html" class="mdui-list-item-content">..</a>
</li>
'''
    Files="<li class='mdui-subheader-inset'>Files</li>"

    list=os.listdir(path)
    list.sort()
    for file in list:
        if(file[0]=='.' or file=="f_index.html"):
            continue
        to=os.path.join(path,file)
        if(os.path.isdir(to)):
            if(get(to)):
                link=file+"/index.html"
                icon=icon_page
            else:
                link=file+"/f_index.html"
                icon=icon_dir
            Folders+=node_mb.replace("{%ICON%}",icon)\
                            .replace("{%NAME%}",file)\
                            .replace("{%LINK%}",link)\
                            .replace("{%SIZE%}","")\
                            .replace("{%MD_DATE%}",file_md_time(to))

    for file in list:
        if(file[0]=='.' or file=="f_index.html"):
            continue
        to=os.path.join(path,file)
        if(not os.path.isdir(to)):
            link=file
            if to.lower().endswith(".cpp"):
                icon=icon_cpp
                link="javascript:viewcode('cpp','"+file+"')"
            elif to.lower().endswith(".go"):
                icon=icon_go
                link="javascript:viewcode('go','"+file+"')"
            elif to.lower().endswith(".pdf"):
                icon=icon_pdf
            elif to.lower().endswith(".sh"):
                icon=icon_script
                link="javascript:viewcode('bash','"+file+"')"
            elif is_txt(to):
                icon=icon_txt
                link="javascript:viewcode('plain','"+file+"')"
            elif to.lower().endswith(".md"):
                icon=icon_md
                link="javascript:viewmd('"+file+"')"
            elif to.lower().endswith(".py"):
                link="javascript:viewcode('python','"+file+"')"
                icon=icon_py
            elif to.lower().endswith(".js"):
                icon=icon_js
                link="javascript:viewcode('javascript','"+file+"')"
            elif to.lower().endswith(".css"):
                icon=icon_css
                link="javascript:viewcode('css','"+file+"')"
            elif to.lower().endswith(".html"):
                icon=icon_html
            elif to.lower().endswith(".deb"):
                icon=icon_deb
            elif to.lower().endswith(".rpm"):
                icon=icon_rpm
            elif to.lower().endswith(".apk"):
                icon=icon_apk
            elif is_zip(to):
                icon=icon_zip
            elif is_img(to):
                icon=icon_img
                link="javascript:viewimg('"+file+"')"
            elif is_binary_file(to):
                icon=icon_bin
            elif is_video(to):
                icon=icon_video
            else: icon=icon_other

            Files+=node_mb.replace("{%ICON%}",icon)\
                          .replace("{%NAME%}",file)\
                          .replace("{%LINK%}",link)\
                          .replace("{%SIZE%}","%.2fKB"%file_size(to))\
                          .replace("{%MD_DATE%}",file_md_time(to))
            if(exists_passwd==0): add_search(to)

    if(exists_passwd):
        passwd=open(os.path.join(path,".passwd"),"r").read()
        tmp=passwd_mb.\
            replace("{%SITE_NAME%}",site_name).\
            replace("{%PASSWD_MD5%}",hashlib.md5(passwd.encode(encoding='UTF-8')).hexdigest()).\
            replace("{%ENCRYPT%}",str(base64.b64encode(quote(Folders+Files,'utf-8').encode('utf-8')),'utf-8').replace('w',passwd[::-1]))
        now=now.replace("{%FILELIST%}",tmp)

    else: now=now.replace("{%FILELIST%}",Folders+Files)
    if(config["htmlmin"]): 
        import htmlmin
        now=htmlmin.minify(now)
    index.write(now)
    index.close()
    return 0

get(".")
search_txt.close()