$(function () {
    $('#payBtn > button').click(function () {
        // $('#myModal').on('hide.bs.modal',function () {
        //
        // });
        $('#payMsg').text('正在使用 '+$(this).text()+' 支付...');
         // 弹出模态框，但不能点击内容以外关闭
        $('#myModal').modal({backdrop:'static', show:true});

        ordernum = $(this).parent().attr('title');
        payType = $(this).attr('title');
        setTimeout(function () {
            $.getJSON('/pay/' + ordernum + '/' + payType, function (data) {
                if (data.status == 'ok') {
                    $('#payMsg').text(data.msg);
                    setTimeout(function () {
                        $('#myModal').modal('hide');
                        window.open('/cart', target = '_self')  //返回目标界面
                    }, 1500)
                }else if(data.status == 'fail'){
                    $('#payMsg').text(data.msg);
                    setTimeout(function () {
                        $('#myModal').modal('hide');
                        window.open('/order/'+ordernum, target = '_self')  //返回目标界面
                    }, 1500)
                }
            })
        },1500)
    });


    $('#back').click(function () {
        window.history.back();
    })
});