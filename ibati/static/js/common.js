//存cookie
function setCookie(name, value)
{
	expires = new Date();
	expires.setTime(expires.getTime() + (1000 * 86400 * 365));
	document.cookie = name + "=" + value + "; expires=" + expires.toGMTString() + "; path=/";
}
//删除cookies
function deleteCookie(name, path, domain){
    if (GetCookie(name))
        document.cookie = name + "=" + ((path) ? "; path=" + path : "") + ((domain) ? "; domain=" + domain : "") + "; expires=Thu, 01-Jan-70 00:00:01 GMT";
}
//取cookies函数   
function getCookie(name)     
{
    var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
     if(arr != null) return unescape(arr[2]); return null;
}
//取对象
function get(id){
	return document.getElementById(id);
}
//取Url参数
function GetQueryString(name)
{    
	var reg=new RegExp("(^|&)"+name+"=([^&]*)(&|$)","i");
	var r=window.location.search.substr(1).match(reg);
	if(r!=null)
	{
		return unescape(r[2])
	}
	return null;     
}
//判断该对象是否存在
function ChkObjectIsExists(id)
{
    try
    {
        var iframeList = document.getElementById(id);
        if(iframeList == null|| iframeList == "undefined")
        {
            return false;
        }
        return true;
    }
    catch(e)
    {
        return false;
    }
}
//实现js版的endWith
String.prototype.endWith=function(str){
    if(str==null||str==""||this.length==0||str.length>this.length){
          return false;
    }
    if(this.substring(this.length-str.length)==str){
          return true;
    }else{
          return false;
    }
    return true;
}
//实现js版的startWith
String.prototype.startWith=function(str){
    if(str==null||str==""||this.length==0||str.length>this.length) {
        return false;
    }
    if(this.substr(0,str.length)==str) {
        return true;
    }else{
        return false;
    }
    return true;
}
//替换所有
String.prototype.ReplaceAll = function(searchArray, replaceArray )
{
	var replaced = this ;

	for ( var i = 0 ; i < searchArray.length ; i++ )
	{
		replaced = replaced.replace( searchArray[i], replaceArray[i] ) ;
	}

	return replaced ;
}
//去除所有html标签
String.prototype.RemoveHtml = function()
{
        return this.replace(/(<[^>]*>)/g, "").replace(/(<[^>]*>)/g, "");
}
//去除左边的空格
String.prototype.LTrim = function()
{
        return this.replace(/(^\s*)/g, "");
}
//去除右边的空格
String.prototype.Rtrim = function()
{
        return this.replace(/(\s*$)/g, "");
}
//去除前后空格
String.prototype.Trim = function()
{
        return this.replace(/(^\s*)|(\s*$)/g, "");
}
//去除所有空格
String.prototype.TrimAllBlank = function()
{
        return this.replace(/\s*/g,'');
}
// 校验手机号码
String.prototype.isMobile = function() {
 var patrn = /^0?1((3[0-9]{1})|(59)){1}[0-9]{8}$/;
 return patrn.test(this);
};
// 校验电话号码
String.prototype.isPhone = function() {
 var patrn = /^(0[\d]{2,3}-)?\d{6,8}(-\d{3,4})?$/;
 return patrn.test(this);
};
// 校验URL地址
String.prototype.isUrl = function() {
 var patrn = /^http[s]?:\/\/[\w-]+(\.[\w-]+)+([\w-\.\/?%&=]*)?$/;
 return patrn.test(this);
};
// 校验电邮地址
String.prototype.isEmail = function() {
 var patrn = /^[\w-]+@[\w-]+(\.[\w-]+)+$/;
 return patrn.test(this);
};
// 校验邮编
String.prototype.isZipCode = function() {
 var patrn = /^\d{6}$/;
 return patrn.test(this);
};
//得到左边的字符串
String.prototype.Left = function(len)
{
        if(isNaN(len)||len==null)
        {
                len = this.length;
        }
        else
        {
                if(parseInt(len)<0||parseInt(len)>this.length)
                {
                        len = this.length;
                }
        }
        return this.substr(0,len);
}
//得到右边的字符串
String.prototype.Right = function(len)
{
        if(isNaN(len)||len==null)
        {
                len = this.length;
        }
        else
        {
                if(parseInt(len)<0||parseInt(len)>this.length)
                {
                        len = this.length;
                }
        }
        return this.substring(this.length-len,this.length);
}
//得到中间的字符串,注意从0开始
String.prototype.Mid = function(start,len)
{
        return this.substr(start,len);
}
//在字符串里查找另一字符串:位置从0开始
String.prototype.InStr = function(str)
{
        if(str==null)
        {
                str = "";
        }
        return this.indexOf(str);
}
//在字符串里反向查找另一字符串:位置0开始
String.prototype.InStrRev = function(str)
{
        if(str==null)
        {
                str = "";
        }
        return this.lastIndexOf(str);
}
//是否是有汉字
String.prototype.existChinese = function()
{
        //[\u4E00-\u9FA5]為漢字﹐[\uFE30-\uFFA0]為全角符號
        return /^[\x00-\xff]*$/.test(this);
}
//转换成全角
String.prototype.toCase = function()
{
        var tmp = "";
        for(var i=0;i<this.length;i++)
        {
                if(this.charCodeAt(i)>0&&this.charCodeAt(i)<255)
                {
                        tmp += String.fromCharCode(this.charCodeAt(i)+65248);
                }
                else
                {
                        tmp += String.fromCharCode(this.charCodeAt(i));
                }
        }
        return tmp
}
//对字符串进行Html编码
String.prototype.toHtmlEncode = function()
{
        var str = this;
        str=str.replace(/&/g,"&amp;");
        str=str.replace(/</g,"&lt;");
        str=str.replace(/>/g,"&gt;");
        str=str.replace(/\'/g,"&apos;");
        str=str.replace(/\"/g,"&quot;");
        str=str.replace(/\n/g,"<br>");
        str=str.replace(/\ /g,"&nbsp;");
        str=str.replace(/\t/g,"&nbsp;&nbsp;&nbsp;&nbsp;");
        return str;
}
//转换成日期
String.prototype.toDate = function()
{
	try
	{
			return new Date(this.replace(/-/g, "\/"));
	}
	catch(e)
	{
			return new Date();
	}
}
//格式化时间eg:format="yyyy-MM-dd hh:mm:ss"
String.prototype.format = function(format){
	var thisDate=this.toDate();
	var o = {  
	   "M+" :thisDate.getMonth() + 1,
	   "d+" :thisDate.getDate(),
	   "h+" :thisDate.getHours(),
	   "m+" :thisDate.getMinutes(),
	   "s+" :thisDate.getSeconds(),
	   "q+" :Math.floor((thisDate.getMonth() + 3) / 3),
	   "S" :thisDate.getMilliseconds()
   }
   if (/(y+)/.test(format)) {
	   format = format.replace(RegExp.$1, (thisDate.getFullYear() + "")
			   .substr(4 - RegExp.$1.length));
   }
   for (var k in o) {
	   if (new RegExp("(" + k + ")").test(format)) {
		   format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k]
				   : ("00" + o[k]).substr(("" + o[k]).length)); 
	   }
   }
   return format;
}
//渲染分页
function renderDcmsPager(first,prev,next,last)
{
	var TotalPage=0;
	if(!isNaN(getCookie("TotalPage")))
	{
		TotalPage=parseInt(getCookie("TotalPage"));
	}
	var CurrentPage=1;
	if(isNaN(GetQueryString("page")))
	{
		CurrentPage=1;
	}
	else
	{
		CurrentPage=GetQueryString("page");
	}
	if(CurrentPage>TotalPage)
	{
		CurrentPage=TotalPage;
	}
	if(CurrentPage<=0)
	{
		CurrentPage=1;
	}
	CurrentPage=parseInt(CurrentPage);
	var PageName="/";
	var urlsplitArr=window.location.href.split("/");
	var urlsplitArrLen=urlsplitArr.length;
	if(urlsplitArrLen>3)
	{
		PageName=urlsplitArr[urlsplitArrLen-1];
	}
	if(PageName.indexOf('search')<0&&window.location.search.indexOf('model=')!=-1)
	{
		PageName="search.aspx"+window.location.search;
	}
	PageName=PageName.replace(/page=(-*)(\d+)/i,"");
	if(PageName.indexOf('?')>=0)
	{
		if(PageName.endWith("&")||PageName.endWith("?"))
		{
			PageName=PageName+"page=";
		}
		else
		{
			PageName=PageName+"&page=";
		}
	}
	else
	{
		PageName=PageName+"?page=";
	}
	
	var dcmspager="<div class=pages>\n";
	var startpager="<a class=pgNext href=\""+PageName+"1\">"+first+"</a>\n<a class=pgNext href=\""+PageName+(CurrentPage-1)+"\">"+prev+"</a>\n";
	if(CurrentPage==1)
	{
		startpager="<a class=\"pgnext pgempty\">"+first+"</li>\n<a class=\"pgnext pgempty\">"+prev+"</a>\n";
	}
	dcmspager=dcmspager+startpager;
	var beginI=1;
	if(CurrentPage>5&&TotalPage>9)
	{
		beginI=CurrentPage-4;
	}
	var loopi=0;
	for(var i=beginI;i<=TotalPage;i++)
	{
		if(i==CurrentPage)
		{
			dcmspager=dcmspager+"<a class=\"pgcurrent\">"+i+"</a>";
		}
		else
		{
			dcmspager=dcmspager+"<a href=\""+PageName+i+"\">"+i+"</a>";
		}
		loopi++;
		if(loopi==9) break;
	}
	
	var endpager="<a class=pgNext href=\""+PageName+(CurrentPage+1)+"\">"+next+"</a>\n<a class=pgNext href=\""+PageName+TotalPage+"\">"+last+"</a>\n";
	//alert(parseInt(TotalPage));
	if(CurrentPage>=TotalPage)
	{
		endpager="<a class=\"pgnext pgempty\">"+next+"</a>\n<a class=\"pgnext pgempty\">"+last+"</a>\n";
	}
	dcmspager=dcmspager+endpager;
	dcmspager=dcmspager+"</div>";
	get("dcms_pager").innerHTML=dcmspager;
}
function renderDcmsPager5(first,prev,next,last)
{
	var TotalPage=0;
	if(!isNaN(getCookie("TotalPage")))
	{
		TotalPage=parseInt(getCookie("TotalPage"));
	}
	var CurrentPage=1;
	if(isNaN(GetQueryString("page")))
	{
		CurrentPage=1;
	}
	else
	{
		CurrentPage=GetQueryString("page");
	}
	if(CurrentPage>TotalPage)
	{
		CurrentPage=TotalPage;
	}
	if(CurrentPage<=0)
	{
		CurrentPage=1;
	}
	CurrentPage=parseInt(CurrentPage);
	var PageName="/";
	var urlsplitArr=window.location.href.split("/");
	var urlsplitArrLen=urlsplitArr.length;
	//alert(urlsplitArrLen);
	if(urlsplitArrLen>3)
	{
		PageName=urlsplitArr[urlsplitArrLen-1];
	}
	if(PageName.indexOf('tesp')<0)
	{
		PageName="testp.aspx"+window.location.search;
	}
	
	//alert(PageName);
	PageName=PageName.replace(/page=(-*)(\d+)/i,"");
	if(PageName.indexOf('?')>=0)
	{
		if(PageName.endWith("&")||PageName.endWith("?"))
		{
			PageName=PageName+"page=";
		}
		else
		{
			PageName=PageName+"&page=";
		}
	}
	else
	{
		PageName=PageName+"?page=";
	}
	
	var dcmspager="<div class=pages>\n";
	var startpager="<a class=pgNext href=\""+PageName+"1\">"+first+"</a>\n<a class=pgNext href=\""+PageName+(CurrentPage-1)+"\">"+prev+"</a>\n";
	if(CurrentPage==1)
	{
		startpager="<a class=\"pgnext pgempty\">"+first+"</li>\n<a class=\"pgnext pgempty\">"+prev+"</a>\n";
	}
	dcmspager=dcmspager+startpager;
	var beginI=1;
	if(CurrentPage>5&&TotalPage>9)
	{
		beginI=CurrentPage-4;
	}
	var loopi=0;
	for(var i=beginI;i<=TotalPage;i++)
	{
		if(i==CurrentPage)
		{
			dcmspager=dcmspager+"<a class=\"pgcurrent\">"+i+"</a>";
		}
		else
		{
			dcmspager=dcmspager+"<a href=\""+PageName+i+"\">"+i+"</a>";
		}
		loopi++;
		if(loopi==9) break;
	}
	
	var endpager="<a class=pgNext href=\""+PageName+(CurrentPage+1)+"\">"+next+"</a>\n<a class=pgNext href=\""+PageName+TotalPage+"\">"+last+"</a>\n";
	//alert(parseInt(TotalPage));
	if(CurrentPage>=TotalPage)
	{
		endpager="<a class=\"pgnext pgempty\">"+next+"</a>\n<a class=\"pgnext pgempty\">"+last+"</a>\n";
	}
	dcmspager=dcmspager+endpager;
	dcmspager=dcmspager+"</div>";
	get("dcms_pager").innerHTML=dcmspager;
}
//豪华版渲染分页
function renderDcmsPager2(first,prev,next,last)
{
	var TotalPage=0;
	
	
	if(!isNaN(getCookie("TotalPage")))
	{
		TotalPage=parseInt(getCookie("TotalPage"));
	}
	var TotalRecord;
	if(!isNaN(getCookie("TotalRecord")))
	{
		TotalRecord=parseInt(getCookie("TotalRecord"));
	}
	var CurrentPage=1;
	if(isNaN(GetQueryString("page")))
	{
		CurrentPage=1;
	}
	else
	{
		CurrentPage=GetQueryString("page");
	}
	if(CurrentPage>TotalPage)
	{
		CurrentPage=TotalPage;
	}
	if(CurrentPage<=0)
	{
		CurrentPage=1;
	}
	CurrentPage=parseInt(CurrentPage);
	var PageName="/";
	var urlsplitArr=window.location.href.split("/");
	var urlsplitArrLen=urlsplitArr.length;
	if(urlsplitArrLen>3)
	{
		PageName=urlsplitArr[urlsplitArrLen-1];
	}
	PageName=PageName.replace(/page=(-*)(\d+)/i,"");
	if(PageName.indexOf('?')>=0)
	{
		if(PageName.endWith("&")||PageName.endWith("?"))
		{
			PageName=PageName+"page=";
		}
		else
		{
			PageName=PageName+"&page=";
		}
	}
	else
	{
		PageName=PageName+"?page=";
	}
	
	var dcmspager="<div class=pages>\n";
	
	dcmspager=dcmspager+"共有："+TotalRecord+"条&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
	var startpager="<a class=pgNext href=\""+PageName+"1\">"+first+"</a>\n<a class=pgNext href=\""+PageName+(CurrentPage-1)+"\">"+prev+"</a>\n";
	if(CurrentPage==1)
	{
		startpager="<a class=\"pgnext pgempty\">"+first+"</li>\n<a class=\"pgnext pgempty\">"+prev+"</a>\n";
	}
	dcmspager=dcmspager+startpager;
	var beginI=1;
	if(CurrentPage>5&&TotalPage>9)
	{
		beginI=CurrentPage-4;
	}
	var loopi=0;
	for(var i=beginI;i<=TotalPage;i++)
 	{
		if(i==CurrentPage)
		{
		dcmspager=dcmspager+"<a class=\"pgcurrent\">"+i+"</a>";
		}
		else
  	{
			dcmspager=dcmspager+"<a href=\""+PageName+i+"\">"+i+"</a>";
		}
		loopi++;
		if(loopi==9) break;
	  }
	
	var endpager="<a class=pgNext href=\""+PageName+(CurrentPage+1)+"\">"+next+"</a>\n<a class=pgNext href=\""+PageName+TotalPage+"\">"+last+"</a>\n";
	//alert(parseInt(TotalPage));
	if(CurrentPage>=TotalPage)
	{
		endpager="<a class=\"pgnext pgempty\">"+next+"</a>\n<a class=\"pgnext pgempty\">"+last+"</a>\n";
	}
	dcmspager=dcmspager+endpager;
	
	dcmspager=dcmspager+"页次:"+CurrentPage+"/"+TotalPage+"页";
	
	//dcmspager=dcmspager+"<select onchange='location.href=\""+PageName+"this.value\"'>";
	dcmspager=dcmspager+"<select onchange='location.href=\""+PageName+"\"+this.value'>";
	for(var i=beginI;i<=TotalPage;i++)
	{
         if(i==CurrentPage)
		 {
     	 dcmspager=dcmspager+"<option value='"+i+"' selected=\"selected\">"+i+"</option>";
     	 }
     	 else
     	 {
     	   dcmspager=dcmspager+"<option value='"+i+"'>"+i+"</option>";
     	 }
	}
	
	dcmspager=dcmspager+"</select>";
	dcmspager=dcmspager+"</div>";
	get("dcms_pager").innerHTML=dcmspager;
}
//英文豪华版渲染分页
function renderDcmsPager3(first,prev,next,last)
{
	var TotalPage=0;
	
	
	if(!isNaN(getCookie("TotalPage")))
	{
		TotalPage=parseInt(getCookie("TotalPage"));
	}
	var TotalRecord;
	if(!isNaN(getCookie("TotalRecord")))
	{
		TotalRecord=parseInt(getCookie("TotalRecord"));
	}
	var CurrentPage=1;
	if(isNaN(GetQueryString("page")))
	{
		CurrentPage=1;
	}
	else
	{
		CurrentPage=GetQueryString("page");
	}
	if(CurrentPage>TotalPage)
	{
		CurrentPage=TotalPage;
	}
	if(CurrentPage<=0)
	{
		CurrentPage=1;
	}
	CurrentPage=parseInt(CurrentPage);
	var PageName="/";
	var urlsplitArr=window.location.href.split("/");
	var urlsplitArrLen=urlsplitArr.length;
	if(urlsplitArrLen>3)
	{
		PageName=urlsplitArr[urlsplitArrLen-1];
	}
	PageName=PageName.replace(/page=(-*)(\d+)/i,"");
	if(PageName.indexOf('?')>=0)
	{
		if(PageName.endWith("&")||PageName.endWith("?"))
		{
			PageName=PageName+"page=";
		}
		else
		{
			PageName=PageName+"&page=";
		}
	}
	else
	{
		PageName=PageName+"?page=";
	}
	
	var dcmspager="<div class=pages>\n";
	
	dcmspager=dcmspager+"Total："+TotalRecord+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
	var startpager="<a class=pgNext href=\""+PageName+"1\">"+first+"</a>\n<a class=pgNext href=\""+PageName+(CurrentPage-1)+"\">"+prev+"</a>\n";
	if(CurrentPage==1)
	{
		startpager="<a class=\"pgnext pgempty\">"+first+"</li>\n<a class=\"pgnext pgempty\">"+prev+"</a>\n";
	}
	dcmspager=dcmspager+startpager;
	var beginI=1;
	if(CurrentPage>5&&TotalPage>9)
	{
		beginI=CurrentPage-4;
	}
	var loopi=0;
	for(var i=beginI;i<=TotalPage;i++)
 	{
		if(i==CurrentPage)
		{
		dcmspager=dcmspager+"<a class=\"pgcurrent\">"+i+"</a>";
		}
		else
  	{
			dcmspager=dcmspager+"<a href=\""+PageName+i+"\">"+i+"</a>";
		}
		loopi++;
		if(loopi==9) break;
	  }
	
	var endpager="<a class=pgNext href=\""+PageName+(CurrentPage+1)+"\">"+next+"</a>\n<a class=pgNext href=\""+PageName+TotalPage+"\">"+last+"</a>\n";

	if(CurrentPage>=TotalPage)
	{
		endpager="<a class=\"pgnext pgempty\">"+next+"</a>\n<a class=\"pgnext pgempty\">"+last+"</a>\n";
	}
	dcmspager=dcmspager+endpager;
	
	dcmspager=dcmspager+"Page:"+CurrentPage+"/"+TotalPage;
	
	
	dcmspager=dcmspager+"<select onchange='location.href=\""+PageName+"\"+this.value'>";
	for(var i=beginI;i<=TotalPage;i++)
	{
         if(i==CurrentPage)
		 {
     	 dcmspager=dcmspager+"<option value='"+i+"' selected=\"selected\">"+i+"</option>";
     	 }
     	 else
     	 {
     	   dcmspager=dcmspager+"<option value='"+i+"'>"+i+"</option>";
     	 }
	}
	
	dcmspager=dcmspager+"</select>";
	dcmspager=dcmspager+"</div>";
	get("dcms_pager").innerHTML=dcmspager;
}
//对于内容分页的处理，先在模板上创建一个对象id="content_page"
var htmlArr;
var len=1;
function renderContentPage()
{
	var urlsplitArr=window.location.href.split("/");
	var urlsplitArrLen=urlsplitArr.length;
	if(urlsplitArrLen>3)
	{
		PageName=urlsplitArr[urlsplitArrLen-1];
	}
	PageName=PageName.replace(/page=(-*)(\d+)/i,"");
	if(PageName.indexOf('?')>=0)
	{
		if(PageName.endWith("&")||PageName.endWith("?"))
		{
			PageName=PageName+"page=";
		}
		else
		{
			PageName=PageName+"&page=";
		}
	}
	else
	{
		PageName=PageName+"?page=";
	}
	
	var CurrentPage=1;
	if(isNaN(GetQueryString("page"))||(GetQueryString("page")=="")||(GetQueryString("page")==null))
	{
		CurrentPage=1;
	}
	else
	{
		CurrentPage=GetQueryString("page");
	}
	
	var html=get("content_page").innerHTML;
	//var reg=new RegExp("(^|&)"+name+"=([^&]*)(&|$)","i");
	//var r=window.location.search.substr(1).match(reg);
	
	var reg=new RegExp("<DIV style=\"PAGE-BREAK-AFTER: always\">([^.|.]*?)<SPAN style=\"DISPLAY: none\">&nbsp;</SPAN>([^.|.]*?)<hr style=\"HEIGHT: 4px\">([^.|.]*?)</DIV>","ig");
	
	html=html.replace(reg,"<div style='display:none;' id='pageBreack'></div>");
	htmlArr=html.split("<div style='display:none;' id='pageBreack'></div>");
	
	len=htmlArr.length;
	var pageStr="<div style='text-align:center;clear:both;'>";
	if(len>1)
	{
		for(var i=1;i<=parseInt(len);i++)
		{
			//var t=i-1;
			pageStr=pageStr+" <a href='"+PageName+i+"' style='padding:8px;'>"+i+"</a> "
		}
		get("content_page").innerHTML=htmlArr[parseInt(CurrentPage)-1]+pageStr+"</div>";
	}
}
function jump(index)
{
	var len=htmlArr.length;
	var pageStr="<div style='text-align:center;clear:both;'>";
	if(len>1)
	{
		for(var i=1;i<=parseInt(len);i++)
		{
			var t=i-1;
			pageStr=pageStr+" <a href='javascript:void(0);' style='padding:8px;' onclick='jump("+t+")'>"+i+"</a> "
		}
		get("content_page").innerHTML=htmlArr[parseInt(index)]+pageStr+"</div>";
	}
}