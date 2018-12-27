# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from sqlalchemy import or_

from application import app, db
from common.libs.Helper import ops_render, iPagination
from common.models.member.Member import Member
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrtentDate

route_member = Blueprint('member_page', __name__)


@route_member.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query

    # 查询逻辑
    if 'mix_kw' in req:
        # ilike方式为忽略大小写
        rule = or_(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

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
    list = query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("member/index.html", resp_data)


@route_member.route("/info")
def info():
    resp_data = {}
    req = request.args  # args智能用于GET请求
    id = int(req.get('id', 0))
    redirect_url = UrlManager.buildUrl('/member/index')

    if id < 1:
        return redirect(redirect_url)

    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(redirect_url)

    resp_data['info'] = info
    resp_data['current'] = 'index'
    return ops_render("member/info.html", resp_data)


@route_member.route("/set", methods=['GET', 'POST'])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int( req.get( "id",0 ) )
        redirect_url = UrlManager.buildUrl("/member/index")
        # 没有id跳转到member首页
        if id < 1:
            return redirect(redirect_url)
        # 没有用户信息跳转到member首页
        info = Member.query.filter_by(id=id).first()
        if not info:
            return redirect(redirect_url)
        # status不等于1跳转到member首页
        if info.status != 1:
            return redirect(redirect_url)

        resp_data['info'] = info
        resp_data['current'] = 'index'
        return ops_render( "member/set.html",resp_data )

    resp = { 'code':200,'msg':'操作成功~~','data':{} }
    req = request.values
    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    member_info.nickname = nickname
    member_info.updated_time = getCurrtentDate()
    db.session.add( member_info )
    db.session.commit()
    return jsonify( resp )



@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html")


@route_member.route("/ops",methods=['POST'])
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

    member_info = Member.query.filter_by( id = id ).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    if act == "remove":
        member_info.status = 0
    elif act == "recover":
        member_info.status = 1

    member_info.updated_time = getCurrtentDate()
    db.session.add(member_info)
    db.session.commit()
    return jsonify( resp )

