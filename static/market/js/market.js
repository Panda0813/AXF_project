$(function () {
   $('#allType').click(function () {
       console.log('所有分类');
       $(this.lastElementChild).toggleClass('glyphicon glyphicon-chevron-up');
       $(this.lastElementChild).toggleClass('glyphicon glyphicon-chevron-down');
       $('#typeDiv').toggle();
       $('#sortDiv').css('display','none')
   });
   $('#goodsSort').click(function () {
       console.log('显示排序');
       //this,被点击的dom对象
       //toggleClass(classname)，有就删除，没有就添加
       $(this.lastElementChild).toggleClass('glyphicon glyphicon-chevron-up');
       $(this.lastElementChild).toggleClass('glyphicon glyphicon-chevron-down');
       $('#typeDiv').css('display', 'none');  //隐藏
       $('#sortDiv').toggle()  //循环显示
   });

   $('#typeDiv').click(function () {
       $('.last-child').removeClass('glyphicon glyphicon-chevron-down');
       $('.last-child').addClass('glyphicon glyphicon-chevron-up');
       $('#typeDiv').css('display', 'none');
       $('#sortDiv').css('display','none')
   });

   $('#sortDiv').click(function () {
       $('.last-child').removeClass('glyphicon glyphicon-chevron-down');
       $('.last-child').addClass('glyphicon glyphicon-chevron-up');
       $('#typeDiv').css('display', 'none');
       $('#sortDiv').css('display','none')
   });

    $('.add').click(function () {
        id = $(this).attr('title');  //拿到商品id
        stores = document.getElementById('store'+id);  //拿到当前库存量
        console.log($(stores).text().trim());
        $.getJSON('/substores/'+id,function (data) {  //请求后台减去库存
            console.log(data.storenums);
            if($(stores).text().trim() > 0){  //当页面显示的库存量大于0，就可以像购物车添加
                $(stores).text(data.storenums);
                $.getJSON('/addcart/'+id,function (data) {  //向购物车中添加
                console.log(data)
                })
            }else {
                $('#storeModal').modal({backdrop:'static', show:true});
            }
        })
    })

});

