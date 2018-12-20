;
var user_edit_ops = {
    init:function(){
        this.eventBind();
    },
    // 绑定事件
    eventBind:function(){
        // 绑定点击对象
        $(".user_edit_wrap .save").click(function(){
            // 触发事件，点击提交后不要重复点击
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            // 获取nickname输入的值
            var nickname_target = $(".user_edit_wrap input[name=nickname]");
            var nickname = nickname_target.val();
            // 获取email输入的值
            var email_target = $(".user_edit_wrap input[name=email]");
            var email = email_target.val();
            // 判断输入是否正确，输入错误弹出tip提示
            if( !nickname || nickname.length < 2 ){
                common_ops.tip( "请输入符合规范的姓名~~",nickname_target );
                return false;
            }
            // 对邮箱进行判断
            if( !email || email.length < 2 ){
                common_ops.tip( "请输入符合规范的邮箱~~",nickname_target );
                return false;
            }

            btn_target.addClass("disabled");

            // 定义返回值
            var data = {
                nickname: nickname,
                email: email
            };


            $.ajax({
                url:common_ops.buildUrl( "/user/edit" ),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            // 当200时候刷新当前页面
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });


        });
    }
};

$(document).ready( function(){
    user_edit_ops.init();
} );