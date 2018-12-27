# -*- coding: utf-8 -*-
from decimal import Decimal
from sqlalchemy import  or_
from application import app, db
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getDictFilterField
from common.libs.UrlManager import UrlManager
from common.models.food.Food import Food
from common.models.food.FoodCat import FoodCat
from common.libs.Helper import getCurrtentDate
from common.models.food.FoodStockChangeLog import FoodStockChangeLog

route_food = Blueprint('food_page', __name__)


@route_food.route("/index")
def index():
    resp_data = {}
    req = request.values
    cat_list = FoodCat.query.all()
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Food.query

    # 查询功能逻辑
    if 'mix_kw' in req:
        rule = or_(Food.name.ilike("%{0}%".format(req['mix_kw'])), Food.tags.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Food.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(Food.cat_id == int(req['cat_id']))

    # 分页显示功能
    page_params = {
        # 一共有多少数据需要展示
        'total': query.count(),
        # 分页的大小
        'page_size': app.config['PAGE_SIZE'],
        # 当前第几页
        'page': page,
        # 希望每一页展示多大
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }
    pages = iPagination(page_params)
    # 偏移量=（当前页数-1）* 每一页大小
    offset = (page - 1) * app.config['PAGE_SIZE']
    list = query.order_by(Food.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    cat_mapping = getDictFilterField(FoodCat, FoodCat.id, "id", [])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render("food/index.html", resp_data)


@route_food.route("/info")
def info():
    # 定义返回值
    resp_data = {}
    # 获取页面的值
    req = request.args
    # 获取到id
    id = int(req.get("id", 0))
    # 定义一个返回跳转路径
    reback_url = UrlManager.buildUrl("/food/index")
    # 如果没有id就返回
    if id < 1:
        return redirect(reback_url)
    # 根据id查询到菜品到数据
    info = Food.query.filter_by(id=id).first()
    # 如果没有查询到就返回菜品首页
    if not info:
        return redirect(reback_url)

    stock_change_list = FoodStockChangeLog.query.filter(FoodStockChangeLog.food_id == id) \
        .order_by(FoodStockChangeLog.id.desc()).all()

    resp_data['info'] = info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render("food/info.html", resp_data)


@route_food.route("/set", methods=['GET', 'POST'])
def set():
    # GET请求用于菜品列表展示用
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        info = Food.query.filter_by(id=id).first()
        if info and info.status != 1:
            return redirect(UrlManager.buildUrl("/food/index"))
        # 展示所有菜品分类信息
        cat_list = FoodCat.query.all()
        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("food/set.html", resp_data)


    # POST请求后台保存数据
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else ''
    main_image = req['main_image'] if 'main_image' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    stock = int(req['stock']) if 'stock' in req else ''
    tags = req['tags'] if 'tags' in req else ''


    if cat_id < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类~~"
        return jsonify(resp)

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称~~"
        return jsonify(resp)

    if not price or len(price) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    # 将价格的值转化为金额保留小数点
    price = Decimal(price).quantize(Decimal('0.00'))
    if price <= 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的售卖价格~~"
        return jsonify(resp)

    if main_image is None or len(main_image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图~~"
        return jsonify(resp)

    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入图书描述，并不能少于10个字符~~"
        return jsonify(resp)

    if stock < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的库存量~~"
        return jsonify(resp)

    if tags is None or len(tags) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入标签，便于搜索~~"
        return jsonify(resp)

    # 查询food信息
    food_info = Food.query.filter_by(id=id).first()
    before_stock = 0
    # 如果存在就做更新操作
    if food_info:
        model_food = food_info
        before_stock = model_food.stock
    # 不存在就添加
    else:
        model_food = Food()
        model_food.status = 1
        model_food.created_time = getCurrtentDate()

    model_food.cat_id = cat_id
    model_food.name = name
    model_food.price = price
    model_food.main_image = main_image
    model_food.summary = summary
    model_food.stock = stock
    model_food.tags = tags
    model_food.updated_time = getCurrtentDate()
    # 保存到数据库
    db.session.add(model_food)
    ret = db.session.commit()

    # 库存变更
    model_stock_change = FoodStockChangeLog()
    model_stock_change.food_id = model_food.id
    model_stock_change.unit = int(stock) - int(before_stock)
    model_stock_change.total_stock = stock
    model_stock_change.note = ''
    model_stock_change.created_time = getCurrtentDate()
    db.session.add(model_stock_change)
    db.session.commit()
    return jsonify(resp)


@route_food.route("/cat")
def cat():
    '''
    菜品分类列表展示
    :return:
    '''
    resp_data = {}
    req = request.values
    query = FoodCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == int(req['status']))

    list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
    resp_data['list'] = list
    resp_data['current'] = 'cat'
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("food/cat.html", resp_data)


@route_food.route("/cat-set", methods=['GET', 'POST'])
def catSet():
    '''
    添加菜品分类操作
    :return:
    '''
    if request.method == 'GET':
        resp_data = {}
        req = request.values
        id = int(req.get('id', 0))
        info = None
        if id:
            # 通过id去查询菜品数据
            info = FoodCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat'
        return ops_render("food/cat_set.html", resp_data)

    # POST请求
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    # 获取id，菜系名，权重
    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称~~"
        return jsonify(resp)

    # 通过id查询数据库时候有菜品数据存在
    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if food_cat_info:
        model_food_cat = food_cat_info
    else:
        model_food_cat = FoodCat()
        model_food_cat.created_time = getCurrtentDate()
        model_food_cat.name = name
        model_food_cat.weight = weight
        model_food_cat.updated_time = getCurrtentDate()
        db.session.add(model_food_cat)
        db.session.commit()
        return jsonify(resp)

    return ops_render("food/cat_set.html")


@route_food.route('/cat-ops', methods=['POST'])
def cat_ops():
    '''
    处理菜品分类列表删除逻辑
    :return:
    '''
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有错误，请重试"
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if not food_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定的分类不存在"
        return jsonify(resp)

    if act == 'remove':
        food_cat_info.status = 0
    elif act == 'recover':
        food_cat_info.status = 1

    food_cat_info.update_time = getCurrtentDate()
    db.session.add(food_cat_info)
    db.session.commit()

    return jsonify(resp)


@route_food.route("/ops",methods=["POST"])
def ops():
    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in [ 'remove','recover' ]:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    food_info = Food.query.filter_by( id = id ).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "指定美食不存在~~"
        return jsonify(resp)

    if act == "remove":
        food_info.status = 0
    elif act == "recover":
        food_info.status = 1

    food_info.updated_time = getCurrtentDate()
    db.session.add(food_info)
    db.session.commit()
    return jsonify( resp )

