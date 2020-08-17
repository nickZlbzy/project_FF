$(function(){
    //页面加载完成后执行
    $('#jump_login_a').bind("click",function(){
            window.open("/user/login","_self");
    });

    $(".tags").bind("click",function(){
            window.open("http://www.baidu.com/","_blank");
    });
    // 绑定默认路径
    bind_default();
    // 加载导航条
    create_top_bar("top_navigation_bar");
    // 绑定头部分类查询事件
    $("#select_1").bind("input propertychange",query_drop_title);
    $("#search_drop_list").bind("mouseleave",function(){
        $("#search_drop_list >ul")[0].innerHTML = "";
        $("#search_drop_list").hide();
    });
    $("#search_drop_list").bind("click",function(){
        $("#search_drop_list >ul")[0].innerHTML = "";
        $("#search_drop_list").hide();
    });

})

function bind_default(){
    $('#jump_index_page').bind("click",function(){
         window.open("/","_self");
    });
    $('#fund_tools_btn').bind("click",function(){
         window.open("/filter/ffpage","_self");
    });
    $('#jump_etfs_page').bind("click",function(){
        alert("敬请期待!")
    });

    $('#jump_forum_home').bind("click",function(){
        alert("敬请期待!")
    });
    $('#jump_article_home').bind("click",function(){
        window.open("/article/info/art_page","_self");
    })
     $('#jump_course_home').bind("click",function(){
        window.open("/article/course/index/0","_self");
    })
    // $('#fund_tools ul>li:nth-child(2)').bind("click",function(){
    //     alert("敬请期待!")
    // })
}

function create_top_bar(sel_name){
    /**
     * sel_name 页面组件id
     * @type {jQuery}
     */
    var moduleName=$("#"+sel_name).attr("data-module-name");
    $.ajax({
        type: "GET",
        url:"/sys/cate/query_drop_bar?moName=" + moduleName,
        dataType: "json",
        async:false,
        success:function(data){
            if(data){
                var index = 0;
                var content = "";
                $.each(data,function(k,v){
                    $("#jump_"+k).bind("click",function(){
                        window.open(v.url,"_self");
                    });
                    if(v.childs){
                        content += '<div class="nav_list_title" id="div_'+ k +'">'
                                +  '<ul class="drop_down_list" style="margin-left:'+ index*12 +'vw">'
                        $.each(v.childs,function(i,ele){
                            content += '<li class="dd_a" onclick="jump_to(\''+ele.url+'\')">'+ele.title+'</li>'
                        })
                        content += '</ul></div>'
                        $("#jump_"+k).html(v.title+'<div class="bar_triangle"><div class="bar_triangle_in"></div></div>');
                    }else{
                        $("#jump_"+k).text(v.title);
                    }
                    $("#jump_"+k).mouseover(function(){
                        $(".nav_text").removeClass("sta_status");
                        this.classList.add("sta_status");
                        $("#drop_down_nav_content > div").hide();
                        $("#div_"+k).show();
                    });
                    index++;
                });
                $("#drop_down_nav_content").html(content);
                //当鼠标离开，隐藏导航栏
                $("#top_navigation_bar").on("mouseleave",function(){
                    $("#drop_down_nav_content > div").hide();
                    $(".nav_text").removeClass("sta_status");
                });
            }
        }
    })
}

// 登出
function logout(){
    $.ajax({
        type:"get",
        url:"/user/logout",
        dataType:"json",
        success:function(res){
            if(res){
                alert("已注销.")
                location.reload()
            }
        }
    })
}

//模糊查询框点击事件
function changeSelect(){
    // var parent = $(this).parent();
    // parent.siblings().removeClass("check_label");
    // parent.siblings().each(function(i,ele){
    //     ele.children[0].setAttribute("checked",false)
    // })
    // parent[0].classList.add("check_label");
    // this.setAttribute("checked",true);
    // $("#select_1").val("");
    // var radios = document.getElementsByName("select_type")
    // for(var i=0;i<radios.length;i++){  console.log(radios[i])}
}

function query_drop_title(){
     //判断如果输入框有内容就发送请求
    var in_val=$("#select_1").val();
    if(!in_val){
        $("#search_drop_list").hide();
        return;
    }
    var drop_content="";
    $.ajax({
        type:"post",
        url:"/sys/cate/query_title_by_kind",
        contentType: 'application/json;charset=utf-8',
        dataType:"json",
        async:true,
        // data:{"kind":$("input[name='select_type']:checked").val(),"value":$("#select_1").val()},
        data:JSON.stringify({"kind":$("input[name='select_type']:checked").val(),"value":$("#select_1").val()}),
        headers: {
            "X-CSRFToken": getCsrfFromCookie("csrftoken")
        },
        success:function(data) {
            if (!data) {
                $("#search_drop_list").hide();
                return;
            }
            $.each(data, function (key, value) {
                drop_content += "<li onclick='jump_to(\"" + key + "\")'>" + value + "</li>"
            });
            $("#search_drop_list").show();
            $("#search_drop_list >ul")[0].innerHTML = drop_content;
        }
    })
}

//页面跳转
function jump_to(url){
   window.open(url,"_self");
}


// 加载下拉菜单方法
// function createButtonSelect(sel_name,text_url_data){
//     // var str_select ="#"+sel_name+" ul"
//     var ulContent = "";
//     $.each(text_url_data,function(key,value){
//         if(key.indexOf("风险测评")!=-1){
//             ulContent += "<li class='st_a' onclick='check_eva_jump()'>"
//           + key + "</li>"
//         }else{
//             ulContent += "<li class='st_a' onclick='window.open(\""+ value +"\",\"_self\")'>"
//           + key + "</li>"
//         }
//
//     })
//     $("#"+sel_name+" ul")[0].innerHTML=ulContent;
// }

// function initDimRadio(){
    // $('[name="select_type"]').bind("change",clickRadio);
    // var radios = document.getElementsByName("select_type")
    // for(var i=0;i<radios.length;i++){
    //     radios[i].addEventListener("change",clickRadio);
    //     // radios[i].onclick = clickRadio;
    // }
// }