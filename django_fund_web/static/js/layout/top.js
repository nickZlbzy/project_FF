$(function(){
    //页面加载完成后执行内容
    initDimRadio()
    get_title_address("fund_tools")
    $("#select_1").bind("input propertychange",query_drop_title)
    $("#select_1").bind("blur",function(){
        $("#search-in-drop")[0].classList.remove("open");
    })

})



function get_title_address(sel_name){
    var typeName=$("#"+sel_name).attr("data-sel-name");
    $.ajax({
        type: "GET",
        url:"/sys/cate/query_box?selName=" + typeName,
        dataType: "json",
        async:false,
        success:function(data){
            console.log(data)
            if(data){

                creeateButtonSelect(sel_name,data)
            }
        }
    })
}


// 加载下拉菜单方法
function creeateButtonSelect(sel_name,text_url_data){
    // var str_select ="#"+sel_name+" ul"
    var ulContent = "";
    $.each(text_url_data,function(key,value){
        if(key.indexOf("风险测评")!=-1){
            ulContent += "<li class='st_a' onclick='check_eva_jump()'>"
          + key + "</li>"
        }else{
            ulContent += "<li class='st_a' onclick='window.open(\""+ value +"\",\"_self\")'>"
          + key + "</li>"
        }

    })
    $("#"+sel_name+" ul")[0].innerHTML=ulContent;
}

function initDimRadio(){
    var radios = document.getElementsByName("select_type")
    for(var i=0;i<radios.length;i++){
        radios[i].addEventListener("change",clickRadio);
        // radios[i].onclick = clickRadio;
    }
}

//模糊查询框点击事件
function clickRadio(){
    var parent = $(this).parent()

    parent.siblings().each(function(i,ele){
        ele.classList.remove("check_label");
        ele.children[0].setAttribute("checked",false)
    })
    parent[0].classList.add("check_label");
    this.setAttribute("checked",true);
    $("#select_1").val("");
    // var radios = document.getElementsByName("select_type")
    // for(var i=0;i<radios.length;i++){  console.log(radios[i])}
}

function query_drop_title(){
     //判断如果输入框有内容就发送请求
    if($("#select_1").val()){
        var drop_content=""
        $.ajax({
            type:"post",
            url:"/main/query_by_type",
            contentType: 'application/json;charset=utf-8',
            dataType:"json",
            async:true,
            data:JSON.stringify({"kind":$("input[name='select_type']:checked").val(),"value":$("#select_1").val()}),
            success:function(data){
                if(data!=undefined){

                    $.each(data,function(key,value){
                        drop_content+= "<li onclick='window.open(\""+ key +"\",\"_self\")'>" + value + "</li>"
                    })
                    $("#search-in-drop ul").html(drop_content);
                    $("#search-in-drop")[0].classList.add("open");

                    // $("#search-in-drop ul li").each(function(i,ele){
                    //     $(ele).bind("click",function(){
                    //         alert("敬请期待！")
                    //     })
                    //     console.log(ele)
                    // })

                    // $.each(data,function(key,value){
                    //     $("#"+key).bind("click",function(){
                    //         alert("1111")
                    //     })
                    // })

                }else{

                    $("#search-in-drop")[0].classList.remove("open");
                }

            }
         })

    }else{
        $("#search-in-drop")[0].classList.remove("open");
    }
}




function jump_fun(){
    alert("1111")
}
