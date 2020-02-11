import os
import time
import codecs

icon_back = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/folder-parent.svg\"></img></i>"
icon_dir = "<i class=\"mdui-list-item-avatar mdui-color-white mdui-icon material-icons\">folder</i>"
icon_web_dir = "<i class=\"mdui-list-item-avatar mdui-color-white mdui-icon material-icons\">web</i>"

icon_other = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/x.svg\"></img></i>"
icon_pdf = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/x-pdf.svg\"></img></i>"
icon_markdown = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-md.svg\"></img></i>"
icon_txt = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt.svg\"></img></i>"
icon_bin = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/bin.svg\"></img></i>"
icon_html = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-html.svg\"></img></i>"
icon_css = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-css.svg\"></img></i>"
icon_js = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-js.svg\"></img></i>"
icon_py = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-py.svg\"></img></i>"
icon_shell = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-script.svg\"></img></i>"
icon_cpp = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-cpp.svg\"></img></i>"
icon_go = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/txt-go.svg\"></img></i>"
icon_photo = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/img.svg\"></img></i>"
icon_video = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/vid.svg\"></img></i>"
icon_zip = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/ar.svg\"></img></i>"
icon_deb = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/ar-deb.svg\"></img></i>"
icon_rpm = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/ar-rpm.svg\"></img></i>"
icon_apk = "<i class=\"mdui-list-item-avatar mdui-color-white\"><img src=\"/add/icon/ar-apk.svg\"></img></i>"

content_right=open("dirgen-content-right.txt","r").read()

search=open("search.txt","w")

def file_md_time(file_path):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(os.stat(file_path).st_mtime))

def file_size(file_path):
    fsize = os.path.getsize(file_path)
    fsize = fsize/float(1024)
    return round(fsize, 8)


def is_binary_file(file_path):
    with open(file_path, 'rb') as file:
        initial_bytes = file.read(8192)
        file.close()
    return not any(initial_bytes.startswith(bom) for bom in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE, codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF8,)
                   ) and b'\0' in initial_bytes


def is_img(file):
    typlist = {'jpg', 'png', 'bmp', 'jpeg', 'rgb', 'svg', 'tif', 'gif'}
    file = file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0


def is_txt(file):
    typlist = {'txt', 'in', 'out'}
    file = file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0


def is_zip(file):
    typlist = {'zip', 'rar', '7z', 'cab'}
    file = file.lower()
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0


def is_video(file):
    file = file.lower()
    typlist = {'mp4', 'mkv', 'flv', 'avi'}
    for i in typlist:
        if(file.endswith(i)):
            return 1
    typlist = {'mp3', 'flac', 'wav', 'ogg'}
    for i in typlist:
        if(file.endswith(i)):
            return 1
    return 0

def path_to_link(path):
    list=path.split('/')
    str=''
    now=''
    for i in list:
        if(i=='.'): continue
        now+='/'+i
        str+='/'+"<a href='"+now+"/f_index.html' style='color: #2962ff'>"+i+"</a>"
    if(str==''): str="zcmimi's files"
    return str

def add_search(file): 
    if(is_binary_file(file)): return
    search.write(file+"\n|-|-|-|\n"+"%.2f"%file_size(file)+"\n|-|-|-|\n")
    flag=0
    typlist = {"md", "cpp"}
    for i in typlist:
        if(file.endswith(i)): 
            flag=1
    if(flag): 
        search.write(open(file,"r").read())
    search.write("|-|=|-|\n")

def get(path):
    if(os.path.exists(os.path.join(path, "index.html"))):
        return 1
    index = open(os.path.join(path, "f_index.html"), "w")

    index.write("<!DOCTYPE html><html>")
    index.write(
        "<head><title>zcmimi的文件床</title><subtitle>"+path+"</subtitle><link rel=\"stylesheet\" href=\"/add/mdui/css/mdui.min.css\" /></head>")
    # index.write("<link rel=\"stylesheet\" href=\"https://cdnjs.loli.net/ajax/libs/mdui/0.4.3/css/mdui.min.css\">")
    # index.write("<script src=\"https://cdnjs.loli.net/ajax/libs/mdui/0.4.3/js/mdui.min.js\"></script>")

    index.write("<body class='mdui-theme-accent-blue padding-top'>")

    index.write("<div id=\"content-left\" class='left-body mdui-appbar-with-toolbar padding-top'>")

    index.write("<div class='mdui-appbar mdui-shadow-2 mdui-appbar-fixed' style='width: 30%'>\
                <div class='mdui-toolbar mdui-color-white'>\
                    <a href='/f_index.html' class='mdui-btn mdui-btn-icon'><i class='mdui-icon material-icons'>home</i></a>\
					<span class='mdui-text' id='path' style='text-overflow: clip !important;overflow: scroll;'>"+path_to_link(path)+"</span>\
					<div class='mdui-toolbar-spacer'></div>\
                    <button id='filter_button' class='mdui-btn mdui-btn-icon mdui-ripple' onclick='view_filter_textfield()'>\
                        <i class='mdui-icon material-icons'>filter_list</i>\
                    </button>\
                    <div id='filter_textfield' class='mdui-textfield' style='display: none;'>\
                        <input id='filter_input' class='mdui-textfield-input' placeholder='筛选,多关键词请用|分割'>\
                    </div>\
                    <button id='search_button' class='mdui-btn mdui-btn-icon mdui-ripple' onclick='view_search_textfield()'>\
                        <i class='mdui-icon material-icons'>search</i>\
                    </button>\
                    <div id='search_textfield' class='mdui-textfield' style='display: none;'>\
                        <input id='search_input' class='mdui-textfield-input' placeholder='搜索,多关键词请用|分割'>\
                    </div>\
                </div>\
            </div><p></p>")

    index.write("<ul class=\"mdui-list\">")    
    
    index.write("<li class=\"mdui-subheader-inset\">Folders</li>")
    index.write("<li href=\"../f_index.html\" class=\"mdui-list-item mdui-ripple\">" +
                icon_back+"<a href=\"../f_index.html\" class=\"mdui-list-item-content\">"+"..</a></li>")

    list = os.listdir(path)
    list.sort()
    for file in list:
        if(file[0] == '.' or file == "f_index.html"):
            continue
        to = os.path.join(path, file)
        if(os.path.isdir(to)):
            if(get(to)):
                to_idx = file+"/index.html"
                icon = icon_web_dir
            else:
                to_idx = file+"/f_index.html"
                icon = icon_dir
            index.write("<li href=\""+to_idx +
                        "\" class=\"mdui-list-item mdui-ripple obj\">")
            index.write(icon)
            index.write("<a href=\""+to_idx +
                        "\" class=\"mdui-list-item-content\">")
            index.write("<div class=\"mdui-list-item-title\">"+file+"</div>")
            index.write("<div class=\"mdui-list-item-text\">" +
                        file_md_time(to)+"</div>")
            index.write("</a>")
            index.write("</li>")

    index.write("<li class=\"mdui-subheader-inset\">Files</li>")
    for file in list:
        if(file[0] == '.' or file == "f_index.html"):
            continue
        to = os.path.join(path, file)
        if(not os.path.isdir(to)):
            link=file
            if to.lower().endswith(".cpp"):
                icon = icon_cpp
                link="javascript:viewcode('cpp','"+file+"')"
            elif to.lower().endswith(".go"):
                icon = icon_go
                link="javascript:viewcode('go','"+file+"')"
            elif to.lower().endswith(".pdf"):
                icon = icon_pdf
            elif to.lower().endswith(".sh"):
                icon = icon_shell
                link="javascript:viewcode('bash','"+file+"')"
            elif is_txt(to):
                icon = icon_txt
                link="javascript:viewcode('plain','"+file+"')"
            elif to.lower().endswith(".md"):
                icon = icon_markdown
                link="javascript:viewmd('"+file+"')"
            elif to.lower().endswith(".py"):
                link="javascript:viewcode('python','"+file+"')"
                icon = icon_py
            elif to.lower().endswith(".js"):
                icon = icon_js
                link="javascript:viewcode('javascript','"+file+"')"
            elif to.lower().endswith(".css"):
                icon = icon_css
                link="javascript:viewcode('css','"+file+"')"
            elif to.lower().endswith(".html"):
                icon = icon_html
            elif to.lower().endswith(".deb"):
                icon = icon_deb
            elif to.lower().endswith(".rpm"):
                icon = icon_rpm
            elif to.lower().endswith(".apk"):
                icon = icon_apk
            elif is_img(to):
                icon = icon_photo
            elif is_zip(to):
                icon = icon_zip
            elif is_binary_file(to):
                icon = icon_bin
            elif is_video(to):
                icon = icon_video
            else:
                icon = icon_other

            index.write("<li href=\""+link +
                        "\" class=\"mdui-list-item mdui-ripple obj\">")
            index.write(icon)
            index.write("<a href=\""+link +
                        "\" class=\"mdui-list-item-content\">")
            index.write("<div class=\"mdui-list-item-title\">"+file+"</div>")
            index.write("<div class=\"mdui-list-item-text\">" +
                        file_md_time(to)+"</div>")
            index.write("</a>")
            index.write("<i class='mdui-list-item'>%.2fKB</i>"%file_size(to))
            index.write("</li>")
            
            add_search(to)

    index.write("</ul>")

    index.write("<script src=\"/add/mdui/js/mdui.min.js\"></script>")

    index.write("</div>")

    index.write(content_right)

    index.write("</body>")
    index.write("</html>")
    index.close()
    return 0


get(".")
search.close()