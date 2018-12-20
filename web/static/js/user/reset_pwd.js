;
var mod_pwd_ops = {
    init:function(){
        this.eventBind();
    },
    // 绑定触发事件
    eventBind:function(){
        // 触发点击事件
        $("#save").click(function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            // 获取值
            var old_password = $("#old_password").val();
            var new_password = $("#new_password").val();

            // 判断是否为空
            if( !old_password ){
                common_ops.alert( "请输入原密码~~" );
                return false;
            }
            // 判断是否为空和不少于6位数
            if( !new_password || new_password.length < 6 ){
                common_ops.alert( "请输入不少于6位的新密码~~" );
                return false;
            }

            // 完成点击之后添加class
            btn_target.addClass("disabled");

            // 定义返回值
            var data = {
                old_password: old_password,
                new_password: new_password
            };

            // 用ajax方式返回
            $.ajax({
                url:common_ops.buildUrl( "/user/reset-pwd" ),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });


        });
    }
};

// 页面生成时候加载
$(document).ready( function(){
    mod_pwd_ops.init();
} );