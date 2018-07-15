$(function () {
    //给是否选择购买的span添加点击事件
    $('.ischose').click(function () {
        //获取当前element的第一个子控件
        var spanchild = $(this).children().first();
        id = spanchild.attr('id');  //取属性的方式拿到id值，传给后台拿到json对象
        console.log(id);
        if(spanchild.text().trim() == ''){
            spanchild.text('√');  //选择
            //所有商品被选择后，全选按钮就会被选择
        }else {
            //有一个商品没被选择，全选按钮都不能被选
            spanchild.text('');  //取消选择
        }

        checkall();

        //更新后台状态  $.getJSON(url,function(data){})
        $.getJSON('/select/' + id, function (data) {  //拿到json对象
            if(data.status == 200){
                //拿到总价格
                // console.log(data);
                var tp = $('.sumprice').text().trim();
                if(data.selected){
                    //选择
                    $('.sumprice').text(parseFloat(tp)+parseFloat(data.price));
                }else {
                    //取消选择
                    $('.sumprice').text(parseFloat(tp)-parseFloat(data.price));
                }
            }
        })
    });

    checkall();

    //全部选择或全部取消
    $('#allChose').click(function () {
        var span = $(this).children().first();
        id = 0;
        if(span.text().trim() == ''){
            span.text('√');  //全部选择
            $('.ischose :first-child').text('√');
            id = 0;
        }else {
            span.text('');  //全部取消
            $('.ischose :first-child').text('');
            id = 9999
        }
        $.getJSON('/select/' + id, function (data) {  //拿到json对象
            $('.sumprice').text(data.price);
            console.log(data)
        })
    });


    //增加减少商品数量
    $('.subShopping').click(function () {
        cnt = $(this).next();
        id = $(this).attr('id');
        console.log(id);
        if(parseInt(cnt.text()) > 1){
            cnt.text(parseInt(cnt.text())-1)
            //修改后台数据，更新总价格
        }
        $.getJSON('/subcart/'+id,function (data) {
            console.log(data.price);
            $('.sumprice').text(parseFloat($('.sumprice').text().trim())-parseFloat(data.price))
        })
    });
    $('.addShopping').click(function () {
        cnt = $(this).prev();
        id = $(this).attr('id');
        //修改后台数据，更新总价格
        $.getJSON('/addcart/'+id,function (data) {
            if(data.status == '201'){
                return
            }else {
                cnt.text(parseInt(cnt.text())+1);
                $('.sumprice').text(parseFloat($('.sumprice').text().trim())+parseFloat(data.price))
            }
        })
    });
    

    $('#toOrder').click(function () {
        // window.location.href = '/order/0'
        if($('.ischose').children().text().trim() ==''){
            $('#selectModal').modal({backdrop:'static', show:true});
        }else {
            var receives = $('.receive');
            for(var i=1;i<receives.length;i++){
                var receive = receives[i];
                if($(receive).text() == ''){
                    $('#delMsg').text('请先填写收获地址');
                    $('#deleteModal').modal({backdrop:'static',show:true});
                    $('#ok').text('添加地址');
                    $('#ok').click(function () {
                        window.open('/address/0/0',target='_self')  //添加地址
                    });
                    return
                }
            }
            window.open('/order/0',target='_self')
       }

    });

    //实现删除功能
    $('.delete').click(function () {
        id = $(this).attr('title');
        $('#delMsg').text('确定要删除此商品吗?');
        $('#deleteModal').modal({backdrop:'static', show:true});
        $('#ok').click(function () {
            $.getJSON('/delcart/' + id, function (data) {
                console.log(data);
                if (data.status == 'ok') {
                    $('#delMsg').text(data.msg);
                    console.log(data.msg);
                    $('.modal-footer').css('display','none');
                    setTimeout(function () {  //两秒后执行跳转
                        $('#deleteModal').modal('hide');
                        window.open('/cart', target = '_self')
                    }, 2000)
                }
            })
        })
    })

});


//实现取消产品，全选就会取消，全部都选了，全选就会选择
function checkall() {
    var choses = $('.ischose');
    for(var i=0;i<choses.length;i++){
        if($(choses[i]).children().first().text().trim() ==''){
            $('#allChose :first-child').text('');
            return
        }
    }
    $('#allChose :first-child').text('√')
}


