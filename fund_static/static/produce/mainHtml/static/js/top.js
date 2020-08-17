var arr_fund_tools = ["基金筛选器","基金龙虎榜(RQFII)","基金公司"]
$(function(){   
        //页面加载完成后执行内容
        initDimRadio()
        initButtonSelect()       
   
})
   

//初始化导航栏下拉菜单
function initButtonSelect(){
    var toolsObj = document.getElementById("fund_tools");
    ulContent = "";
    for(var i = 0;i<arr_fund_tools.length;i++){
        ulContent += "<li class='st_a' onclick='jump_fun(this)'>" + arr_fund_tools[i] + "</li>"
    }   
    toolsObj.children[2].innerHTML=ulContent;
}

function initDimRadio(){
    var radios = document.getElementsByName("select_type")            
    for(var i=0;i<radios.length;i++){                   
        radios[i].addEventListener("change",clickRadio)
        // radios[i].onclick = clickRadio;               
    }
}   

//模糊查询框点击事件
function clickRadio(){      
  
   
    parent = this.parentNode;                    
    var allLabels = parent.parentNode.children;
    for(var j=0;j<allLabels.length;j++){
        allLabels[j].classList.remove("check_label");                 
        allLabels[j].children[0].setAttribute("checked",false) 
    }   
    parent.classList.add("check_label");            
    this.setAttribute("checked",true);
    $("#select_1").val("");
    // var radios = document.getElementsByName("select_type")             
    // for(var i=0;i<radios.length;i++){  console.log(radios[i])}
} 


function jump_fun(){        
    
}
