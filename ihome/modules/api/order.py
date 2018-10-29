import datetime

from ihome import db
from ihome.models import House, Order
from ihome.utils.common import login_required
from ihome.utils.response_code import RET
from . import api_blu
from flask import request, g, jsonify, current_app


# 预订房间
@api_blu.route('/orders', methods=['POST'])
@login_required
def add_order():
    """
    下单
    1. 获取参数
    2. 校验参数
    3. 查询指定房屋是否存在
    4. 判断当前房屋的房主是否是登录用户
    5. 查询当前预订时间是否存在冲突
    6. 生成订单模型，进行下单
    7. 返回下单结果
    :return:
    """
    # 获取到当前用户的id
    user_id = g.user_id
    # 1. 获取到传入的参数
    params = request.get_json()
    house_id = params.get('house_id')
    start_date_str = params.get('start_date')
    end_date_str = params.get('end_date')

    # 2. 校验参数
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        assert start_date < end_date, Exception("开始日期大于结束日期")
        # 计算入住天数
        days = (end_date - start_date).days
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3. 查询指定房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 4. 判断当前房屋的房主是否是当前用户，如果当前用户是房东，不能预订
    if house.user_id == user_id:
        return jsonify(errno=RET.ROLEERR, errmsg="不能预订自已的房屋")

    # 5. 查询该房屋是否有冲突的订单
    try:
        filters = [Order.house_id == house_id, Order.begin_date < end_date, Order.end_date > start_date]
        count = Order.query.filter(*filters).count()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if count > 0:
        return jsonify(errno=RET.DATAERR, errmsg="该房屋已被预订")

    # 6. 生成订单模型，进行下单
    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = days * house.price

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="生成订单失败")
    # 7. 返回下单结果
    return jsonify(errno=RET.OK, errmsg="OK", data={"order_id": order.id})