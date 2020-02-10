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
                        + "<td><a onclick=\"alert('敬请期待!')\">"+ ele.f_code +"</a></td>"
                        + "<td>"+ ele.f_name +"</td>"
                        + "<td>"+ ele.type_name +"</td>"
                        + "<td>"+ ele.three_year_level +"</td>"
                        + "<td>"+ ele.five_year_level +"</td>"
                        + "<td>2020-01-08</td>"
                        + "<td>"+ ele.unit_price +"</td>"
                        + "<td>"+ ele.day_change +"</td>"
                        + "<td>"+ ele.interest +"</td>"
                        + "</tr>"
    })
    $("#fund-tbody").html(fund_content)

}
//加载分页栏方法
function create_pagination(page){
     pagingContent = ""
     if(page.prev_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.prev_num + ")' "
             + "<span aria-hidden='true'>&laquo;</span></a></li>"
     }else{
         pagingContent += '<li><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
     }
     $.each(page.page_range,function(i,ele) {
         if(ele == page.number){
            pagingContent += '<li class="active"><a>'+ ele +'</a></li>'
         }else{
             pagingContent += '<li><a href="#t-filter-form" '
                + 'onclick="query_fund_fun('+ ele +')">'+ ele +'</a></li>'
         }
     })
     if(page.next_num){
         pagingContent += "<li><a href='#t-filter-form'  aria-label='Previous' "
             + "onclick='query_fund_fun(" + page.next_num + ")' "
             + "<span aria-hidden='true'>&raquo;</span></a></li>"
     }else{
         pagingContent += '<li><a aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'
     }

    $("#fund_pagination").html(pagingContent);s
}