"""
黄历模块
提供每日黄历查询功能，包含宜忌、冲煞、胎神、五行纳音、吉神凶煞等传统历法信息
依赖：lunar_python 库
"""
from lunar_python import Solar


def get_daily_almanac(year: int, month: int, day: int) -> dict:
    """
    获取每日黄历信息

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        完整黄历信息字典，字段与 AlmanacResponse 模型对应
    """
    s = Solar.fromYmd(year, month, day)  # 创建公历对象
    l = s.getLunar()  # 转农历

    return {
        # -- 日期基础
        "solar_date": f"{year}-{month:02d}-{day:02d}",  # 公历日期(2025-10-01)
        "lunar_date": l.toString(),  # 农历日期(乙巳年八月初九)
        # -- 宜忌
        "yi": l.getDayYi(),             # 宜(今日适宜事项列表)
        "ji": l.getDayJi(),             # 忌(今日不宜事项列表)
        # -- 冲煞
        "chong_gan": l.getChongGan(),     # 冲天干
        "chong_zhi": l.getChong(),         # 冲地支
        "chong_shengxiao": l.getChongShengXiao(),  # 冲生肖
        "chong_desc": l.getChongDesc(),  # 冲描述((丁酉)鸡)
        "sha": l.getSha(),              # 煞方(东/南/西/北)
        # -- 胎神
        "taishen": l.getDayPositionTai(),  # 胎神占方
        # -- 五行
        "wuxing_nayin": l.getDayNaYin(),   # 五行纳音
        # -- 彭祖百忌
        "pengzu": f"{l.getPengZuGan()} {l.getPengZuZhi()}",  # 彭祖百忌(天干忌 地支忌)
        # -- 吉神凶煞
        "jishen": l.getDayJiShen(),     # 吉神(列表)
        "xiongsha": l.getDayXiongSha(),  # 凶煞(列表)
        # -- 值星
        "zhixing": l.getZhiXing(),       # 建除十二值星(建/除/满/平/定/执/破/危/成/收/开/闭)
        # -- 天神
        "tianshen": l.getDayTianShen(),   # 值日天神
        "tianshen_type": l.getDayTianShenType(),  # 天神类型
        # -- 方位
        "position_cai": l.getDayPositionCaiDesc(),     # 财神方位
        "position_xi": l.getDayPositionXiDesc(),       # 喜神方位
        "position_fu": l.getDayPositionFuDesc(),       # 福神方位
        "position_yanggui": l.getDayPositionYangGuiDesc(),  # 阳贵方位
        "position_yingui": l.getDayPositionYinGuiDesc(),  # 阴贵方位
        # -- 其他
        "liuyao": l.getLiuYao(),         # 六曜(大安/留连/速喜/赤口/小吉/空亡)
        "wuhou": l.getWuHou(),           # 七十二候
        "xiu": l.getXiu(),               # 二十八星宿名称
        "xiu_luck": l.getXiuLuck(),      # 星宿吉凶
    }
