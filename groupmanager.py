from hoshino import Service, priv

from . import util

sv = Service('group-manager', enable_on_default=True, visible=True)

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
    await util.member_silence(bot, ev, uid, sid, gid, time)

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
    await util.member_silence(bot, ev, uid, sid, gid, time)

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
'''
@sv.on_fullmatch(('谁是龙王','龙王是谁'))
async def whois_talkative(bot, ev):
    gid = ev.group_id
    honor_type = 'talkative'
    ta_info = await util.honor_info(bot, ev, gid, honor_type)
    print(ta_info)
'''