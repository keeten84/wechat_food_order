;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit();
        });

        // 删除
        $(".remove").click( function(){
            that.ops( "remove",$(this).attr("data") );
        } );

        // 恢复
        $(".recover").click( function(){
            that.ops( "recover",$(this).attr("data") );
        } );
    },
    ops:function( act,id ){
        var callback = {
            // 删除操作的时候需要点击ok
            'ok':function(){
                $.ajax({
                    url:common_ops.buildUrl( "/account/ops" ),
                    type:'POST',
                    data:{
                        act:act,
                        id:id
                    },
                    dataType:'json',
                    success:function( res ){
                        var callback = null;
                        if( res.code == 200 ){
                            callback = function(){
                                window.location.href = window.location.href;
                            }
                        }
                        common_ops.alert( res.msg,callback );
                    }
                });
            },
            // 取消按钮
            'cancel':null
        };
        common_ops.confirm( ( act == "remove" ? "确定删除？":"确定恢复？" ), callback );
    }

};

$(document).ready( function(){
    account_index_ops.init();
} );