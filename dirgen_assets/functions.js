document.onreadystatechange=function(){NProgress.start();}
window.onload=function(){
    if(getCookie("theme")=="night")night();
    NProgress.done();
}
function md_turn(input,output){
    var text=window.document.getElementById(input).value.trim(),res="";
    var list=text.split("$$");
    for(i in list){
        if(i&1)res+=katex.renderToString(list[i],{displayMode:true});
        else{
            var LIST=list[i].split('$'),now="";
            for(j in LIST){
                if(j&1)now+='<latex>'+katex.renderToString(LIST[j])+'</latex>';
                else now+=LIST[j];
            }
            res+=marked(now);
        }
    }window.document.getElementById(output).innerHTML=res;
}
function setCookie(cname,cval,exdays=0.5){
    var d=new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires="expires="+d.toUTCString();
    document.cookie=cname+"="+cval+";"+expires+";path=/";
}
function getCookie(cname){
    var name=cname+"=",decodedCookie=decodeURIComponent(document.cookie),ca=decodedCookie.split(';'),c;
    for(i in ca){
        c=ca[i];
        while(c.charAt(0)==' ')c=c.substring(1);
        if(c.indexOf(name)==0)return c.substring(name.length, c.length);
    }return "";
}
function night(){
    if(document.getElementById('nightmode').innerHTML==""){
        setCookie("theme","night");
        document.cookie=document.cookie.replace("daymode","nightmode");
        document.querySelector('html').classList.add("mdui-theme-layout-dark");
        document.querySelector('body').classList.add("mdui-theme-layout-dark");
        document.getElementById("content-left").classList.add("mdui-theme-layout-dark");
        document.getElementById("content-right").classList.add("mdui-theme-layout-dark");
        document.getElementById('nightmode').innerHTML="<style>\
            .mdui-color-white{background-color: #0000 !important;color: #fff !important;}\
            code{background-color: #0000 !important;color: #66ccff}</style>"
        var hl=document.createElement('link');
        hl.href="/dirgen_assets/nord.min.css";
        hl.type='text/css';
        hl.rel='stylesheet';
        document.getElementById('nightmode').appendChild(hl);
    }else{
        setCookie("theme","day");
        document.cookie=document.cookie.replace("nightmode","daymode");
        document.getElementById('nightmode').innerHTML="";
        document.querySelector('html').classList.remove("mdui-theme-layout-dark");
        document.querySelector('body').classList.remove("mdui-theme-layout-dark");
        document.getElementById("content-left").classList.remove("mdui-theme-layout-dark");
        document.getElementById("content-right").classList.remove("mdui-theme-layout-dark");
    }
}
function show(val){document.querySelector(val).hidden=0;}
function hide(val){document.querySelector(val).hidden=1;}
function viewmd(file){
    var link=new XMLHttpRequest();
    document.getElementById("download_file_name").innerHTML="下载"+file;
    document.getElementById("preview-raw").href='/'+document.getElementById("path").innerHTML+"/"+file
    close_preview();
    link.onreadystatechange=function(){
        show("#loading");
        show("#preview-raw");
        show("#close_preview");
        NProgress.start();
        if(link.readyState==4){
            if(link.responseText.length <= 819200)
                document.getElementById("md_source").innerHTML=link.responseText;
            else document.getElementById("md_source").innerHTML=link.responseText.substr(0,819200)+ "\n\n ### 文件过大,请下载查看";
            md_turn('md_source','md_out');
            document.querySelectorAll('pre code').forEach((block)=>{hljs.highlightBlock(block);});
            hljs.initCopyButtonOnLoad();
            hljs.initLineNumbersOnLoad();
            hide("#loading");
            show("#md_out");
            NProgress.done();
        }
    }
    link.open('GET',file,true);
    link.send();
}
function viewcode(typ,file){
    var link=new XMLHttpRequest();
    document.getElementById("download_file_name").innerHTML="下载"+file;
    document.getElementById("preview-raw").href='/'+document.getElementById("path").innerHTML+"/"+file
    close_preview();
    link.onreadystatechange=function(){
        show("#loading");
        show("#preview-raw");
        show("#close_preview");
        NProgress.start();
        if(link.readyState==4){
            if(link.responseText.length <= 819200)
                document.getElementById("md_out").innerHTML="<pre><code class='language-"+typ+"'>"+link.responseText.replace(/[<>&"]/g,function(c){
                    return {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c];
                  })+"</code></pre>";
            else document.getElementById("md_out").innerHTML="<pre><code class='language-"+typ+"'>"+link.responseText.substr(0,819200).replace(/[<>&"]/g,function(c){
                return {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c];
              })+"</code></pre><p>文件较大,请下载查看</p>";
            document.querySelectorAll('pre code').forEach((block)=>{hljs.highlightBlock(block);});
            hljs.initCopyButtonOnLoad();
            hljs.initLineNumbersOnLoad();
            hide("#loading");
            show("#md_out");
            NProgress.done();
        }
    }
    link.open('GET',file,true);
    link.send();
}
function viewimg(file){
    document.getElementById("md_out").innerHTML="<img src="+file+" title="+file+"></img>";
}
function close_preview(){
    hide("#preview-raw");
    hide("#close_preview");
    hide("#md_out");
}
function filter(){
    var obj=document.querySelectorAll(".obj"),
        arr=document.getElementById('filter_input').value.trim().split('|');
    for(i in obj){
        obj[i].hidden=1;
        var flag=1;
        for(x in arr)if(obj[i].innerHTML.toLowerCase().indexOf(arr[x].toLowerCase())==-1){flag=0;break;}
        if(flag)obj[i].hidden=0;
    }
}
var icon_other="<img src='/dirgen_assets/icon/x.svg'></img>",
    icon_pdf  ="<img src='/dirgen_assets/icon/pdf.svg'></img>",
    icon_md   ="<img src='/dirgen_assets/icon/txt-md.svg'></img>",
    icon_txt  ="<img src='/dirgen_assets/icon/txt.svg'></img>",
    icon_bin  ="<img src='/dirgen_assets/icon/bin.svg'></img>",
    icon_html ="<img src='/dirgen_assets/icon/txt-html.svg'></img>",
    icon_css  ="<img src='/dirgen_assets/icon/txt-css.svg'></img>",
    icon_js   ="<img src='/dirgen_assets/icon/txt-js.svg'></img>",
    icon_py   ="<img src='/dirgen_assets/icon/txt-py.svg'></img>",
    icon_shell="<img src='/dirgen_assets/icon/txt-script.svg'></img>",
    icon_cpp  ="<img src='/dirgen_assets/icon/txt-cpp.svg'></img>",
    icon_go   ="<img src='/dirgen_assets/icon/txt-go.svg'></img>",
    icon_img  ="<img src='/dirgen_assets/icon/img.svg'></img>",
    icon_zip  ="<img src='/dirgen_assets/icon/ar.svg'></img>",
    icon_deb  ="<img src='/dirgen_assets/icon/ar-deb.svg'></img>",
    icon_rpm  ="<img src='/dirgen_assets/icon/ar-rpm.svg'></img>",
    icon_apk  ="<img src='/dirgen_assets/icon/ar-apk.svg'></img>",
    icon_video="<img src='/dirgen_assets/icon/video.svg'></img>";
function search(){
    hide("#filelist");
    show("#searchlist");
    var dir=document.getElementById('path').innerHTML,
        text=document.getElementById('search_input').value.split('|'),
        tot=0,res="<li class='mdui-list-item'></li>";
    document.getElementById("return_to_filelist").hidden=0;
    var LINK=new XMLHttpRequest();
    LINK.onreadystatechange=function(){
        NProgress.start();
        if(LINK.readyState==4){
            NProgress.done();
            var items=LINK.responseText.split("|-|=|-|");
            for(i in items){
                node=items[i];
                var tmp=node.split("|-|-|-|"),
                    path=tmp[0],size=tmp[1],content=tmp[2],filename;
                tmp=path.split("/");
                filename=tmp[tmp.length-1];
                if(path.indexOf(dir)!=-1){
                    var flag=1;
                    for(j in text)if((path.indexOf(text[j])==-1) && (content.indexOf(text[j])==-1))flag=0;
                    if(flag==0)continue;
                    ++tot;
                    var link=path,icon=icon_other;
                    if(filename.indexOf("cpp")!=-1)icon=icon_cpp,link="javascript:viewcode('cpp','/"+path+"')";
                    else if(filename.indexOf("md")!=-1)icon=icon_md,link="javascript:viewmd('/"+path+"')";
                    link=link.replace('\n','');
                    res+="\
<li href=\""+link+"\" class='mdui-list-item mdui-ripple obj'>\
<i class='mdui-list-item-avatar mdui-color-white'>"+icon+"</i>\
<a href=\""+link+"\" class='mdui-list-item-content'>\
<div class='mdui-list-item-title'>"+filename+"</div>\
</a>\
<i class='mdui-list-item'>"+size+"KB</i>\
</li>";
                }
            }
            // document.getElementById("path_and_link").innerHTML="在"+path_and_link_backup+"的搜索结果,共"+tot+"个";
            document.getElementById("searchlist").innerHTML=res;
            mdui.snackbar({message: "共找到"+tot+"个文件",position: "left-top"});
        }
    }
    LINK.open('GET',"/search.txt",true);
    LINK.send();
}