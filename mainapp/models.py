from django.db import models

class TopModel(models.Model):
    trackid = models.CharField(primary_key=True, max_length=50)
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

# Create your models here.
#轮播信息
class TopWheel(TopModel):
    class Meta:
        db_table = 'axf_wheel'  #指定表的名字

#导航信息
class TopMenu(TopModel):
    position = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_nav'

#必要菜单
class SwiperMenu(TopModel):
    class Meta:
        db_table = 'axf_mustbuy'

#商店信息
class Shop(TopModel):
    position = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_shop'

#热购的品牌信息
class ShowStore(models.Model):
    trackid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=300)
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    class Meta:
        db_table = 'axf_mainshow'

#品牌下的产品信息
class BrandProduct(models.Model):
    img = models.CharField(max_length=300)
    childcid = models.CharField(max_length=50)
    productid = models.CharField(max_length=50)
    longname = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    marketprice = models.CharField(max_length=20)
    showstore = models.ForeignKey(ShowStore,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'axf_brandproduct'

#左侧栏分类模型
class FoodTypes(models.Model):
    typeid = models.CharField(primary_key=True,max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()  #分类的顺序
    childtypenames = models.CharField(max_length=150)  #所有子类名称

    class Meta:
        db_table = 'axf_foodtypes'

class Goods(models.Model):
    productid = models.CharField(primary_key=True,max_length=10)
    productimg = models.CharField(max_length=300)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=100)
    isxf = models.BooleanField(default=1)
    pmdesc = models.IntegerField(default=1)
    specifics = models.CharField(max_length=100)
    price = models.DecimalField(default=0.0,max_digits=30,decimal_places=2)
    marketprice = models.DecimalField(default=0.0, max_digits=30, decimal_places=2)

    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=10)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'

class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)

class User(models.Model):
    account = models.CharField(max_length=50,unique=True)
    passwd = models.CharField(max_length=200)
    name = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=12)
    imgpath = models.CharField(max_length=100,default='')
    token = models.CharField(max_length=32,default='')
    state = models.BooleanField(default=True,verbose_name='用户状态')

    money = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    objects = UserManager()

    def delete(self, using=None, keep_parents=False):
        self.state = False
        self.save()
        return '已注销'

    class Meta:
        db_table = 'axf_user'

#收货信息的模型
class Receive(models.Model):
    name = models.CharField(max_length=30,verbose_name='收货人')
    phone = models.CharField(max_length=12,verbose_name='手机号')
    address = models.TextField(default='',verbose_name='收货地址')
    isSelected = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'axf_address'

#购物车模型
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #用户
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  #商品

    #数量
    cnt = models.IntegerField(default=1)

    #是否被选择
    isSelected = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'

#订单模型
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    #单号，唯一主键
    orderNum = models.CharField(primary_key=True,max_length=50,verbose_name='订单号')
    order_address = models.ForeignKey(Receive,on_delete=models.SET_NULL,null=True,verbose_name='收货地址')

    #订单总金额
    orderPrice = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    #支付状态
    pay_state = (
        (0,'待支付'),
        (1,'已支付'),
        (2,'正在支付'),
        (3,'已退款')
    )
    payState = models.IntegerField(choices=pay_state,default=0)

    pay_types = (
        (0,'余款'),
        (1, '支付宝'),
        (2, '微信'),
    )

    payType = models.IntegerField(choices=pay_types,default=0)

    @property
    def payTypeName(self):
        return self.pay_types[self.payType][1]

    #取到支付状态的内容
    @property
    def payStateName(self):
        return self.pay_state[self.payState][1]

    #订单派送状态
    order_state=(
        (0,'待派送'),
        (1, '已派送'),
        (2, '已到达'),
        (3, '已签收'),
        (4, '拒收'),
        (5, '未送达'),
    )

    orderState = models.IntegerField(choices=order_state,default=0)

    @property
    def orderStateName(self):
        return self.order_state[self.orderState][1]

    #下订单时间
    orderTime = models.DateTimeField(auto_now_add=True)

    #订单相关信息变更时间
    orderLastTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'

#订单商品明细
class OrderGoods(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.SET_NULL,null=True)
    cnt = models.IntegerField(default=1)
    sumprice = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='某个商品的总价')

    class Meta:
        db_table = 'axf_ordergoods'