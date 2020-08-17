$(function(){
 $('#nickname_modify').bind('click',function(){
        var value = $('#nickname').val();
        var reg = new RegExp(" ","g");
        nickname = value.replace(reg,"");
        $('#nickname').val(nickname);
        if(nickname && nickname.length>0)
            $('#ui-form').submit();
        else
            return false;

    });
    $('#user-btn1').bind('click',function(){
        $("#user-info").show();
        $("#list-order").hide();
        $("#user-btn2").addClass('select-color');
        $("#user-btn1").removeClass('select-color');
    });
    $('#user-btn2').bind('click',function(){
        $("#user-info").hide();
        $("#list-order").show();
        $("#user-btn1").addClass('select-color');
        $("#user-btn2").removeClass('select-color');

    })
});

function set_eva(ability,preference){
    var ability_id,preference_id;

    if(ability>19.2)
        ability_id="re_bear5";
    else if(ability>14.4)
        ability_id="re_bear4";
    else if(ability>9.6)
        ability_id="re_bear3";
    else if(ability>4.8)
        ability_id="re_bear2";
    else
        ability_id="re_bear1";

    if(preference>19.2)
        preference_id="re_prefer5";
    else if(preference>14.4)
        preference_id="re_prefer4";
    else if(preference>9.6)
        preference_id="re_prefer3";
    else if(preference>4.8)
        preference_id="re_prefer2";
    else
        preference_id="re_prefer1";
    $("#"+ability_id).addClass("select_level");
    $("#"+preference_id).addClass("select_level");

}

function buy_fund2(self){
    $.confirm({
        title: '确认',
        content: '即将跳转到支付页面',
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
    var amount = parseFloat(parent.children('.amount').text());
        // 测试功能暂定数量为100
    var order_code = parent.children('.order_code').text();
    var fund_code = parent.children('.fund_code').text();
    // var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // console.log(csrf)
    var post_data = {"fund_code":fund_code,"order_code":order_code,
        "amount":amount};

    $.ajax({
        url:"/payment/jump2/",
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