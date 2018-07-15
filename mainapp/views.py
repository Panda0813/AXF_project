import hashlib
import random
import uuid

import os

import time
from PIL import Image, ImageDraw, ImageFont
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

from AXF_Project import settings
from mainapp.models import TopWheel, TopMenu, SwiperMenu, Shop, ShowStore, FoodTypes, Goods, User, Receive, Cart, Order, \
    OrderGoods


def home(req):
    print(SwiperMenu.objects.all())
    shopList = Shop.objects.all().order_by('position')
    shop1 = shopList[0]  #0
    shop2 = shopList[1:3]  #1,2
    shop3 = shopList[3:7]  #3,4,5,6
    shop4 = shopList[7:11]  #7,8,9,10
    return render(req,'home.html',{
        'title':'主页',
        'topWheels':TopWheel.objects.all(),   #查询所有要轮播的数据
        'topMenus':TopMenu.objects.all().order_by('position'),
        'menus': SwiperMenu.objects.all(),
        'shop1':shop1,'shop2':shop2,'shop3':shop3,'shop4':shop4,
        'mainList':ShowStore.objects.all(),
    })


def market(req,categoryid=0,childid=0,opt=0):
    leftSlider = FoodTypes.objects.all().order_by('typesort')
    goodList =None

    # 获取所有的子类型
    childTypes = []

    # '全部分类:0#进口水果:103534#国产水果:103533'
    cTypes = FoodTypes.objects.filter(typeid=categoryid).last().childtypenames
    cTypes = cTypes.split('#')
    for ctype in cTypes:
        ctype = ctype.split(':')
        childTypes.append({'name':ctype[0],'id':ctype[1]})


    if childid:
        goodList = Goods.objects.filter(categoryid=categoryid,childcid=childid)
    else:
        goodList = Goods.objects.filter(categoryid=categoryid)

    if opt == 1:
        goodList = goodList.order_by('-productnum')  #销量最高
    elif opt == 2:
        goodList = goodList.order_by('price')  #价格最低
    elif opt == 3:
        goodList = goodList.order_by('-price')  #价格最高


    return render(req,'market.html',{'title':'闪送超市',
                                     'leftSlider':leftSlider,
                                     'goodList':goodList,
                                     'childTypes':childTypes,
                                     'categoryid':str(categoryid),
                                     'childid':str(childid),
                                     'opt':opt})


def cart(req):
    #查询当前用户的默认收货地址
    user = User.objects.filter(token=req.COOKIES.get('token')).first()
    user_id = user.id
    address = user.receive_set.filter(isSelected=True).first()
    carts = Cart.objects.filter(user_id=user_id)
    sumprice = 0
    for cart in carts:
        if cart.isSelected:
            sumprice += cart.goods.price * cart.cnt

    return render(req,'cart.html',{'title':'购物车',
                                   'address':address,
                                   'carts':carts,
                                   'sumprice':sumprice})

def newToken(username):
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4())+username).encode())
    return md5.hexdigest()

def crypt(pwd,cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()

def mine(req):
    # username = req.session.get("username","未登录")
    # print(username)
    # if not req.COOKIES.get('token'):
    #     return redirect('/mine')

    return render(req,'mine.html',{
        'title':'我的',
        'user':User.objects.filter(token=req.COOKIES.get('token')).first(),
    })


def regist(req):
    if req.method == 'GET':
        return render(req,'regist.html',{'title':'用户注册'})

    user = User()
    user.account = req.POST.get('username')
    user.passwd = crypt(req.POST.get('passwd'))
    user.name = req.POST.get('name')
    user.phone = req.POST.get('phone')

    #设置用户的token
    user.token = newToken(user.account)
    user.save()

    # req.session['user_id'] = user.id
    # print(user.id)

    #将token设置到cookie中
    resp = redirect('/mine')
    resp.set_cookie('token',user.token)

    return resp

def vCode(req):
    img = Image.new(mode='RGB', size=(120, 30), color=(209, 241, 250))
    draw = ImageDraw.Draw(img, mode='RGB')
    chars = ''
    while len(chars) < 4:
        flag = random.randrange(3)
        num = chr(random.randint(48, 57)) if flag == 0 else chr(random.randint(65, 90)) if flag == 1 else chr(
            random.randint(97, 122))

        if len(chars) == 0 or chars.find(num) == -1:
            chars += num

    req.session['vcode'] = chars
    font = ImageFont.truetype(font='static/main/fonts/hktt.ttf', size=24)
    for char in chars:
        xy = (15 + chars.find(char) * 20, random.randrange(2, 8))  # 上下浮动2~8
        draw.text(xy=xy, text=char, fill=(39, 45, 255), font=font)

    # 干扰内容
    for i in range(35):
        xy = (random.randrange(120), random.randrange(30))
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        draw.point(xy=xy, fill=color)

    buffer = BytesIO()
    img.save(buffer, 'png')

    del draw
    del img

    return HttpResponse(buffer.getvalue(), content_type='image/png')

def login(req):
    if req.method == "GET":
        return render(req,'login.html',{'title':'用户登录'})

    iptcode = req.POST.get('verify')
    sessioncode = req.session.get('vcode')

    #登录信息
    account = req.POST.get('username')
    passwd = req.POST.get('passwd')

    if iptcode.lower() != sessioncode.lower():
        return render(req,'login.html',{'state':'fail',
                                        'name':account,'passwd':passwd})

    loginUser = User.objects.filter(account=account,passwd=crypt(passwd)).first()
    if loginUser:
        # 将用户id放入session中，用于购物车
        # req.session['user_id'] = loginUser.id
        # print(loginUser.id)

        del req.session['vcode']  #删除验证码
        loginUser.token = newToken(loginUser.account)
        loginUser.save()

        resp = redirect('/mine')
        #token存入cookie，用于登陆后的页面显示
        resp.set_cookie('token',loginUser.token)
        return resp
    else:
        # return HttpResponse('<h3>登录失败，请确认用户名或密码是否输入正确</h3>'
        #                     '<a href="/login">重新登录</a>')
        return render(req,'login.html',{
            'error_msg':'登录失败，请确认用户名或密码是否输入正确',
            'name': account,
        })

@csrf_exempt  #不做csrf_token的验证
def upload(req):
    msg = {}
    cookie_token = req.COOKIES.get('token')
    if not cookie_token:
        msg['state'] = 'fail'
        msg['msg'] = '请先登录'
        msg['code'] = '201'
    else:
        qs = User.objects.filter(token=cookie_token)
        if not qs.exists():
            msg['state'] = 'fail'
            msg['msg'] = '登录失效，请重新登录'
            msg['code'] = '202'
        else:
            #开始上传
            uploadFile = req.FILES.get('img')
            saveFileName = newFileName(uploadFile.content_type)
            saveFilePath = os.path.join(settings.MEDIA_ROOT,saveFileName)

            with open(saveFilePath,'wb') as f:
                for part in uploadFile.chunks():
                    f.write(part)
                    f.flush()
            imgpath = 'upload/'+saveFileName
            qs.update(imgpath=imgpath)

            msg['state'] = 'ok'
            msg['msg'] = '上传成功'
            msg['code'] = '200'
            msg['path'] = imgpath

    return JsonResponse(msg)

#生成新文件的名字
def newFileName(contentType):
    filename = crypt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName = '.png'

    return filename+extName


def logout(req):
    token = req.COOKIES.get('token')
    if token != '':
        user = User.objects.filter(token=token).first()
        user.token = ''
        user.save()
        resp = redirect('/mine')

        #删除会话中存储的信息
        resp.delete_cookie('token')
        # del req.session['user_id']

        return resp
    else:
        return redirect('/mine')


def selectCart(req,cart_id):
    # 0全选，9999取消全选
    if cart_id == 0 or cart_id == 9999:
        #全部更新
        user_id = User.objects.filter(token=req.COOKIES.get('token')).first().id
        carts = Cart.objects.filter(user_id=user_id)
        carts.update(isSelected=True if cart_id==0 else False)
        sumprice = 0
        if cart_id == 0:
            for cart in carts:
                sumprice += cart.cnt * cart.goods.price

        return JsonResponse({
            'price':sumprice,
            'status':200
        })

    data = {'status':200,'price':100}
    try:
        cart = Cart.objects.get(id=cart_id)
        print(cart)
        cart.isSelected = not cart.isSelected  #状态取反
        cart.save()
        data['price']=cart.goods.price * cart.cnt
        data['selected'] = cart.isSelected  #回传状态
    except:
        data['status']=300
        data['price']=0
    return JsonResponse(data)


def addCart(req,cart_id):
    #添加指定的cart_id的商品，如果cart_id不存在，要新添加cart信息
    data = {'status':200,'price':20}
    cart = Cart.objects.filter(id=cart_id)
    user = User.objects.filter(token=req.COOKIES.get('token')).first()
    if cart:
        goodsid = cart.first().goods_id
        cart = cart.first()
        if Goods.objects.filter(productid=goodsid).first().storenums > 0:
            Goods.objects.filter(productid=goodsid).update(storenums=F('storenums') - 1)
        else:
            data['status'] = 201  #库存不够不能再加
            return JsonResponse(data)
        cart.cnt += 1
        cart.save()
        data['price'] = cart.goods.price  #增加一次，可以只返回单价，在总价上减去一个单价就可以了
        return JsonResponse(data)

    #以商品id和用户id过滤信息
    else:
        cart = Cart.objects.filter(goods_id=cart_id,user_id=user.id)
        if cart:
            cart.update(cnt=F('cnt')+1)
            data['price'] = cart.goods.price
            return JsonResponse(data)

    cart = Cart()
    cart.cnt = 1
    cart.goods_id = cart_id

    #根据token拿到当前用户id
    user_id = user.id
    cart.user_id = user_id
    cart.save()

    data['price'] = cart.goods.price

    return JsonResponse(data)


def subCart(req,cart_id):
    #减去指定的cart_id的商品，减到0？
    data = {'status': 200, 'price': 20}
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        goodsid = cart.goods_id
        if cart.cnt > 1:
            cart.cnt -= 1
            Goods.objects.filter(productid=goodsid).update(storenums=F('storenums')+1)
            cart.save()
            data['price'] = cart.goods.price
        else:
            data['price'] = 0

    return JsonResponse(data)

#向购物车添加商品时减去库存
def subStores(req,id):
    data = {'status':'ok','storenums':1}
    goods = Goods.objects.filter(productid=id)
    if goods.first().storenums > 0:
        goods.update(storenums=F('storenums')-1)
        data['storenums'] = goods.first().storenums
    else:
        data['storenums'] = 0
    return JsonResponse(data)

def delcart(req,id):
    cart = Cart.objects.filter(id=id)
    cnt = cart.first().cnt  #拿到要删除的商品的数量，给之前减去的库存加回去
    #当客户不买这个商品以后，就把选择的数量有加回给库存
    Goods.objects.filter(productid=cart.first().goods_id).update(storenums=F('storenums')+cnt)
    cart.delete()  #删除要购买的此商品
    return JsonResponse({'status':'ok','msg':'删除成功!'})


#生成订单号
def createNo():
    no = '0029'+str(time.time()).replace('.','')[-8:]
    return no


def order(req,ordernum):
    user_id = User.objects.filter(token=req.COOKIES.get('token')).first().id
    if not user_id:
        return render(req,'login.html')
    if ordernum == '0':
        #创建订单
        order = Order()
        order.user_id = user_id

        #获取用户的默认收货地址
        order_address = User.objects.get(id=user_id).receive_set.all().filter(isSelected=True)
        #先判断用户是否有收获地址
        if not order_address:
            return JsonResponse({'status':'fail','msg':'请先填写收获地址'})

        order.order_address_id = order_address.first().id

        #设置订单号
        order.orderNum = createNo()

        #设置订单金额
        #1.查询当前用户购物车中所有被选中的商品
        carts = Cart.objects.filter(isSelected=True,user_id=user_id)

        if carts.count() == 0:  #如果没选择商品，就重定向到购物车
            return redirect('/cart')
        #2.统计订单总金额，将物品插入到订单明细中
        order.orderPrice = 0
        order.save()  #保存订单
        for cart in carts:
            order.orderPrice += cart.cnt * cart.goods.price

            ordergoods = OrderGoods()
            ordergoods.order_id = order.orderNum
            ordergoods.goods_id = cart.goods.pk  #pk是主键
            ordergoods.cnt = cart.cnt
            ordergoods.sumprice = cart.cnt * cart.goods.price
            ordergoods.save()

        order.save()  #更新订单总额

        #3.删除购物车中已购买的信息
        carts.delete()
    else:
        order = Order.objects.get(pk =ordernum)

    return render(req,'order.html',{'title':'我的订单',
                                    'order':order})


def pay(req,num,payType=0):
    try:
        order = Order.objects.get(pk=num)
        order.payType = payType
        user = User.objects.filter(token=req.COOKIES.get('token')).first()
        if not user:
            return render(req, 'login.html')

        if user.money < order.orderPrice:
            return JsonResponse({'status': 'fail', 'msg': '对不起，余额不足'})
        else:
            user.money -= order.orderPrice
            user.save()
            order.payState = 1  #已支付
            order.orderState = 1  #已派送
            order.save()

            #减去库存量
            #优化业务：添加到购物车之前判断商品库存量够不够
            #在超市中实现，当库存变为0，提示用户库存不够
            for item in order.ordergoods_set.all():
                goods = item.goods
                goods.productnum += item.cnt  #销量
                # goods.storenums -= item.cnt  #库存,去库存的部分在想购物车中添加时完成
                goods.save()

    except:
        return JsonResponse({'status': 'fail', 'msg': '支付失败'})


    return JsonResponse({'status':'ok','msg':'支付成功'})


def orderList(req,state):
    #state表示要查看的订单状态
    #0：所有订单，1：待付款，2：待收货，3：待评价，4：退款/售后
    user = User.objects.filter(token=req.COOKIES.get('token')).first()
    print(user.name)
    if not user:
        return render(req, 'login.html')

    userOreders = user.order_set
    if state == 1:
        orders = userOreders.filter(payState=0).order_by('-orderTime')  #未支付
    elif state == 2:
        orders = userOreders.filter(orderState__in=(0,1),payState=1).order_by('-orderTime')  #待派送或已派送并且已支付
    elif state == 3:
        orders = userOreders.filter(orderState__in=(2,3),payState=1).order_by('-orderTime')  #已到达，已签收且已支付
    elif state == 4:
        orders = userOreders.filter(Q(orderState__in=(4,5))|Q(payState=3)).order_by('-orderTime')  #未送达或拒收或已退款
    else:
        orders = userOreders.all().order_by('-orderTime')
    return render(req, 'orderlist.html', {'title': '订单页面', 'orders': orders,'state':state})


@csrf_exempt  #不做csrf_token的验证
def address(req,state,id):
    #state,0：查看所有，1：添加新地址，2：编辑，3：删除,4：设为默认(isSelected=1)
    #id为要操作的地址的id

    #判断用户是否登录
    user = User.objects.filter(token=req.COOKIES.get('token')).first()
    if not user:
        return render(req, 'login.html')

    if state == 1:
        receive = Receive()
        receive.name = req.POST.get('name')
        receive.phone = req.POST.get('phone')
        receive.address = req.POST.get('address')
        receive.user_id = user.id
        receive.save()
        return JsonResponse({'status':'ok','addressid':receive.id})
    elif state == 2:
        receive = Receive.objects.filter(id=id)
        name = req.POST.get('name')
        phone = req.POST.get('phone')
        address = req.POST.get('address')
        receive.update(name=name,phone=phone,address=address)
        return JsonResponse({'status': 'ok', 'addressid': receive.first().id})
    elif state == 3:
        Receive.objects.filter(id=id).delete()
        return JsonResponse({'status':'ok','msg':'信息删除成功!'})
    elif state == 4:
        lastSel = Receive.objects.filter(isSelected=True)  #拿到上一个被选为默认的地址
        lastid = ''
        if lastSel:
            lastid = lastSel.first().id
            lastSel.update(isSelected=False)  #将之前选为默认的地址取消默认
            Receive.objects.filter(id=id).update(isSelected=True)  #将要选择的设为默认
        else:
            Receive.objects.filter(id=id).update(isSelected=True)  # 将要选择的设为默认
        return JsonResponse({'status': 'ok', 'msg': '设置成功!','lastid':lastid})

    address = Receive.objects.filter(user_id=user.id)
    return render(req,'address.html',{'title':'收货地址','address':address})