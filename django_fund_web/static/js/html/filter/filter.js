function init_query_box(){
    query_company_fun()

}
function query_company_fun(){
     $.ajax({
        type: "GET",
        dataType: "json",
        url: "/filter/queryBox/company",
        data: "",
        async:false,
        success: function(res){

          if(res.code==1){
              var content = ""
              $.each(res.data,function(key,value){
                content += "<option value='" + key + "'>"+ value +"</option>"
              })
              $("#sel_company").append(content)
          }
        }
     })

}

function query_fund_fun(ser_num){
    //    var jsonString = JSON.stringify(selData);
    //dataType可以指定 html、json、jsonp、script或者text。
    var selData = $('#fund_sel_from').serializeArray();
    var ser_index = 1
    if(ser_num && typeof(ser_num)!="object"){  // “object”类型为点击事件
        selData.push({name:"ser_num",value:ser_num})
    }

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/filter/queryFund",
        data: selData,
        async:true,
        success: function(res){
            $("#fund_query_btn").removeAttr("disabled")

             if(res.code==1){
                table_list_fun(res.data)
                // 生成分页部分
                create_pagination(res.data[0])
             }
        }
         ,error: function(e){

        },
        beforeSend:function(){
            $("#fund_query_btn").attr("disabled","disabled")
        }
    });
}

function table_list_fun(data){
    var fund_content = ""
    $.each(data[1],function(i,ele){
        fund_content += "<tr><td>"+ ((data[0].number-1)*data[0].page_size+1+parseInt(i)) +"</td>"
                        + "<td><a onclick='buy_fund(this)' style='cursor: pointer;' >"+ ele.f_code +"</a></td>"
                        + "<td>"+ ele.f_name +"</td>"
                        + "<td>"+ ele.type_name +"</td>"
                        + "<td>"+ ele.three_year_level +"</td>"
                        + "<td>"+ ele.five_year_level +"</td>"
                        + "<td>"+ ele.update_time + "</td>"
                        + "<td class='price'>"+ ele.unit_price +"</td>"
                        + "<td>"+ ele.day_change +"</td>"
                        + "<td>"+ ele.interest +"</td>"
                        + "</tr>"
    })
    $("#fund-tbody").html(fund_content)

}
//加载分页栏方法  (bug未解决)
function create_pagination(page){
     // console.log(page.page_range)
    console.log(page)
     pagingContent = ""
     if(page.prev_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.prev_num + ")' "
             + "<span aria-hidden='true'>&laquo;</span></a></li>"
     }else{
         pagingContent += '<li><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
     }
     if(page.prev_range_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.prev_range_num + ")' "
             + "<span aria-hidden='true'>..</span></a></li>"
     }

     $.each(page.page_range,function(i,ele) {
         if(ele == page.number){
             pagingContent += '<li class="active"><a href="#t-filter-form" '
            + 'onclick="query_fund_fun('+ ele +')">'+ ele +'</a></li>'
         }else{
             pagingContent += '<li><a href="#t-filter-form" '
            + 'onclick="query_fund_fun('+ ele +')">'+ ele +'</a></li>'
         }



     })

     if(page.next_range_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.next_range_num + ")' "
             + "<span aria-hidden='true'>..</span></a></li>"
     }

     if(page.next_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.next_num + ")' "
             + "<span aria-hidden='true'>&raquo;</span></a></li>"
     }else{
         pagingContent += '<li><a aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'
     }

    $("#fund_pagination").html(pagingContent);
}




function buy_fund(self){
    $.confirm({
        title: '确认',
        content: '确认购买基金吗？',
        type: 'red',
        icon: 'glyphicon glyphicon-question-sign',
        buttons: {
            ok: {
                text: '确认',
                btnClass: 'btn-primary',
                action: function() {
                    aliPayment(self)
                }
            },
            cancel: {
                text: '取消',
                btnClass: 'btn-primary'
            }
        }
    });
}

function aliPayment(self){

    var parent = $(self).parent().parent();
    var price = parseFloat(parent.children('.price').text());
        // 测试功能暂定数量为100
    var count =  100;
    var amount = parseInt(price*count);
    var fund_code = self.innerText;
    // var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // console.log(csrf)
    var post_data = {"fund_code":fund_code,"price":price,"count":count,
        "amount":amount};

    $.ajax({
        url:"/payment/jump/",
        type:"post",
        dataType:"json",
        headers: {
            "X-CSRFToken": getCsrfFromCookie("csrftoken")
        },
        // contentType:"application/json",
        data:JSON.stringify(post_data),
        success:function(data){
            if(data.code==200)
                window.location = data.pay_url;
            else
                alert(data.msg)
        }
    })

}

