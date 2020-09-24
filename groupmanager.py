from hoshino import Service, priv, R
from hoshino.util import DailyNumberLimiter

import random
import re

from . import util

HELP = '''
注意本页指令可能由于风控在您的群不可用
[谁是龙王] 查看本群龙王
[龙王榜] 查看本群B话最多的人
以下指令需要机器人是管理员, 且被执行人是普通群员
[修改群名XXX] 群名修改为XXX
[修改名片XXX@某人] 修改某人的群名片为XXX
[来发口球360@某人] 禁言某人360秒, 可以修改为自己需要的时间
[解除口球@某人] 取消某人的禁言
[全员口球] 开启全员禁言
[取消全员禁言] 关闭全员禁言
[一带一路60@某人]神秘功能, 60可以修改为300以下的秒数
'''.strip()

sv = Service('group-manager', enable_on_default=True, help_=HELP, visible=True)

@sv.on_prefix('申请头衔')
async def special_title(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    title = ev.message.extract_plain_text()
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
    if sid is None:
        sid = uid
    await util.title_get(bot, ev, uid, sid, gid, title)

#go-cqhttp似乎暂时不支持收回专属头衔...
@sv.on_fullmatch(('删除头衔','清除头衔','收回头衔','回收头衔'))
async def del_special_title(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    title = None
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
    if sid is None:
        sid = uid
    await util.title_get(bot, ev, uid, sid, gid, title)

  
#单人禁言
@sv.on_prefix(('来发口球','塞口球','禁言一下'))
async def umm_ahh(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    time = ev.message.extract_plain_text().strip()
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            await util.gruop_silence(bot, ev, gid, True)
            return
    if sid is None:
        sid = uid
    await util.member_silence(bot, ev, uid, sid, gid, time, False)

#一带一路
@sv.on_prefix(('一带一路'))
async def umm_ahh_(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    time = ev.message.extract_plain_text().strip()
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            await bot.send(ev, '人干事？', at_sender=True)
            await util.member_silence(bot, ev, uid, uid, gid, 180, False)
            return
    if sid is None:
        sid = uid
    if eval(time) > 300:
        await bot.send(ev, f'时长不可大于300秒哟~', at_sender=True)
        return
    await util.member_silence(bot, ev, uid, sid, gid, time, True)
    await util.member_silence(bot, ev, uid, uid, gid, time, True)
    await bot.send(ev, f'[CQ:at,qq={uid}]成功一带一路[CQ:at,qq={sid}]{eval(time)}秒~')
        


@sv.on_prefix(('解除口球','取消口球','摘口球','脱口球','取消禁言','解除禁言'))
async def cancel_ban_member(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    sid = None
    time = '0'
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            await util.gruop_silence(bot, ev, gid, False)
            return
    if sid is None:
        await bot.send(ev, '请@需要摘口球的群员哦w')
        return
    await util.member_silence(bot, ev, uid, sid, gid, time, False)

@sv.on_fullmatch(('全员口球','全员禁言'))
async def ban_all(bot, ev):
    gid = ev.group_id
    status = True
    await util.gruop_silence(bot, ev, gid, status)

@sv.on_fullmatch(('取消全员口球','取消全员禁言','解除全员口球','解除全员禁言'))
async def cancel_ban_all(bot, ev):
    gid = ev.group_id
    status = False
    await util.gruop_silence(bot, ev, gid, status)
'''
@sv.on_prefix(('来张飞机票','踢出本群','移出本群','踢出此群','移出群聊'))
async def guoup_kick(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    sid = None
    is_reject = False
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
        elif m.type == 'at' and m.data['qq'] == 'all':
            await bot.send(ev, '人干事？', at_sender=True)
            return
    if sid is None:
        sid = uid
    await util.member_kick(bot, ev, uid, sid, gid, is_reject)
'''
@sv.on_prefix(('修改名片','修改群名片','设置名片','设置群名片'))
async def card_set(bot, ev):
    uid = ev.user_id
    sid = None
    gid = ev.group_id
    card_text = ev.message.extract_plain_text()
    for m in ev.message:
        if m.type == 'at' and m.data['qq'] != 'all':
            sid = int(m.data['qq'])
    if sid is None:
        sid = uid
    await util.card_edit(bot, ev, uid, sid, gid, card_text)
    
@sv.on_fullmatch(('谁是龙王','迫害龙王','龙王是谁'))
async def whois_dragon_king(bot, ev):
    gid = ev.group_id
    self_info = await util.self_member_info(bot, ev, gid)
    sid = self_info['user_id']
    honor_type = 'talkative'
    ta_info = await util.honor_info(bot, ev, gid, honor_type)
    if 'current_talkative' not in ta_info:
        await bot.send(ev, '本群没有开启龙王标志哦~')
        return
    dk = ta_info['current_talkative']['user_id']
    if sid == dk:
        pic = R.img('dk_is_me.jpg').cqcode
        await bot.send(ev,f'你们这群丢人玩意，龙王怎么又是我\n{pic}')
    else:
        action=random.choice(['龙王出来挨透','龙王出来喷水'])
        dk_avater = ta_info['current_talkative']['avatar'] + '640' + f'&t={dk}'
        await bot.send(ev, f'[CQ:at,qq={dk}]\n{action}\n[CQ:image,file={dk_avater}]')

@sv.on_prefix(('修改群名','设置群名'))
async def set_group_name(bot, ev):
    gid = ev.group_id
    name_text = ev.message.extract_plain_text()
    await util.group_name(bot, ev, gid, name_text)

@sv.on_message('group')
async def fuck_xxs(bot, ev):
    for m in ev.message:
        if m.type == 'json' and '"app":"com.tencent.autoreply"' in m.data['data']:
            await bot.delete_msg(message_id=ev.message_id)
            await bot.send(ev, '这是onse病毒码，会获取到你手机的xxs，然后发起攻击...以下省略6行需要全文背诵的金句')

@sv.on_fullmatch(('龙王榜','龙王排行','龙王排行榜', '龙王榜单'))
async def dragon_king_list(bot, ev):
    gid = ev.group_id
    ta_info = await util.honor_info(bot, ev, gid, 'talkative')
    dragon_king_list_info = ta_info['talkative_list']

    # 处理description和nickname关系
    dkdir = {}
    for item in dragon_king_list_info:
        user_id = item['user_id']
        nickname = item['nickname']
        description = item['description']
        temp = re.findall(r'\d+', description)
        
        # 累计获得龙王的次数
        dragon_king_days = int(temp[0])
        # 连续获得龙王
        dragon_king_days_continuous = int(temp[1])
        dkdir[nickname] = {
            'user_id': user_id,
            'days_max': dragon_king_days,
            'days_contin': dragon_king_days_continuous
        }
    # 瞎写的排序
    dkdir_sorted = sorted(dkdir.items(), key=lambda d: d[1]['days_max'], reverse=True)
    dkk = dkdir_sorted[0][1]['user_id']
    msg = f'本群获得龙王次数最多的是：\n{dkdir_sorted[0][0]}\n'
    dk_avater = f'http://q1.qlogo.cn/g?b=qq&nk={dkk}&s=5'
    msg += f'[CQ:image,file={dk_avater}]'
    msg += '\n本群龙王榜\n'
    i = 0
    for it in dkdir_sorted:
        _nickname = dkdir_sorted[i][0]
        _days_max = dkdir_sorted[i][1]['days_max']
        _days_contin = dkdir_sorted[i][1]['days_contin']
        msg += f'第{i+1}名：{_nickname}，共{_days_max}次，最长连续{_days_contin}天获得龙王\n'
        i = i+1
        # 只显示前五名
        if i >= 5:
            break
    await bot.send(ev, msg)
