import os, sys

rules_dir = r'E:\dev\clash-rules'

# ---- Classified domains to add ----

# proxy.txt: Plex infrastructure + misc foreign services
proxy_adds = sorted(set([
    'DOMAIN-SUFFIX,plex.tv',
    'DOMAIN-SUFFIX,analytics.plex.tv',
    'DOMAIN-SUFFIX,app.plex.tv',
    'DOMAIN-SUFFIX,clients.plex.tv',
    'DOMAIN-SUFFIX,community.plex.tv',
    'DOMAIN-SUFFIX,discover.provider.plex.tv',
    'DOMAIN-SUFFIX,epg.provider.plex.tv',
    'DOMAIN-SUFFIX,features.plex.tv',
    'DOMAIN-SUFFIX,metadata.provider.plex.tv',
    'DOMAIN-SUFFIX,oauth2.plex.tv',
    'DOMAIN-SUFFIX,pubsub.plex.tv',
    'DOMAIN-SUFFIX,status.plex.tv',
    'DOMAIN-SUFFIX,support.plex.tv',
    'DOMAIN-SUFFIX,together.plex.tv',
    'DOMAIN-SUFFIX,vod.provider.plex.tv',
    'DOMAIN-SUFFIX,www.plex.tv',
    'DOMAIN-SUFFIX,chat-ws.x.com',
    'DOMAIN-SUFFIX,nrs.hooked.fm',
    'DOMAIN-SUFFIX,xpaywalletcdn-prod.azureedge.net',
]))

# direct.txt: Microsoft/Windows + Chinese CDN + Tencent/WeChat + misc
direct_adds = sorted(set([
    # Microsoft/Windows
    'DOMAIN-SUFFIX,arc.msn.com',
    'DOMAIN-SUFFIX,assets.activity.windows.com',
    'DOMAIN-SUFFIX,crl.microsoft.com',
    'DOMAIN-SUFFIX,ctldl.windowsupdate.com',
    'DOMAIN-SUFFIX,displaycatalog.mp.microsoft.com',
    'DOMAIN-SUFFIX,ecn.dev.virtualearth.net',
    'DOMAIN-SUFFIX,edge-enterprise.microsoft.com',
    'DOMAIN-SUFFIX,fe3cr.delivery.mp.microsoft.com',
    'DOMAIN-SUFFIX,go.microsoft.com',
    'DOMAIN-SUFFIX,login.live.com',
    'DOMAIN-SUFFIX,msedge.extensions.microsoft.com',
    'DOMAIN-SUFFIX,ocsp.digicert.com',
    'DOMAIN-SUFFIX,oneclient.sfx.ms',
    'DOMAIN-SUFFIX,settings-win.data.microsoft.com',
    'DOMAIN-SUFFIX,slscr.update.microsoft.com',
    'DOMAIN-SUFFIX,store-images.s-microsoft.com',
    'DOMAIN-SUFFIX,tile-service.weather.microsoft.com',
    'DOMAIN-SUFFIX,update.microsoft.com',
    'DOMAIN-SUFFIX,windows.msn.com',
    'DOMAIN-SUFFIX,windowsupdate.com',
    'DOMAIN-SUFFIX,api.onedrive.com',
    'DOMAIN-SUFFIX,api.cognitive.microsoft.com',
    'DOMAIN-SUFFIX,aks-prod-japaneast.access-point.cloudmessaging.edge.microsoft.com',
    'DOMAIN-SUFFIX,array809.prod.do.dsp.mp.microsoft.com',
    # Chinese CDN / static
    'DOMAIN-SUFFIX,2026.ip138.com',
    'DOMAIN-SUFFIX,a.sinaimg.cn',
    'DOMAIN-SUFFIX,bot-resource-1251316161.file.myqcloud.com',
    'DOMAIN-SUFFIX,cstaticdun.126.net',
    'DOMAIN-SUFFIX,d.alicdn.com',
    'DOMAIN-SUFFIX,d.sinaimg.cn',
    'DOMAIN-SUFFIX,f.video.weibocdn.com',
    'DOMAIN-SUFFIX,face.t.sinajs.cn',
    'DOMAIN-SUFFIX,ntp.aliyun.com',
    'DOMAIN-SUFFIX,r1.res.126.net',
    'DOMAIN-SUFFIX,sam68.secdn.com',
    'DOMAIN-SUFFIX,www.ipip.net',
    # Tencent/WeChat
    'DOMAIN-SUFFIX,act.weixin.qq.com',
    'DOMAIN-SUFFIX,aegis.qq.com',
    'DOMAIN-SUFFIX,apm.zhihu.com',
    'DOMAIN-SUFFIX,bot.q.qq.com',
    'DOMAIN-SUFFIX,dldir1.qq.com',
    'DOMAIN-SUFFIX,dldir2.qq.com',
    'DOMAIN-SUFFIX,ding.wenote.cn',
    'DOMAIN-SUFFIX,docs.qq.com',
    'DOMAIN-SUFFIX,dyn.wps.cn',
    'DOMAIN-SUFFIX,help.wps.com',
    'DOMAIN-SUFFIX,img.whalenote.cn',
    'DOMAIN-SUFFIX,log.whalenote.cn',
    'DOMAIN-SUFFIX,long.weixin.qq.com',
    'DOMAIN-SUFFIX,short.weixin.qq.com',
    'DOMAIN-SUFFIX,support.weixinbridge.com',
    'DOMAIN-SUFFIX,t.cal.qq.com',
    'DOMAIN-SUFFIX,update.whalenote.cn',
    'DOMAIN-SUFFIX,wps-advice-activity.wps.com',
    'DOMAIN-SUFFIX,wps-live-cloud.wps.com',
    'DOMAIN-SUFFIX,k.wps.com',
    # Other direct (Chinese services)
    'DOMAIN-SUFFIX,galaxy.bjcathay.com',
    'DOMAIN-SUFFIX,gateway.bjcathay.com',
    'DOMAIN-SUFFIX,pingfe.huya.com',
    'DOMAIN-SUFFIX,s2s.mine.cn',
    'DOMAIN-SUFFIX,api.ipify.org',
    'DOMAIN-SUFFIX,ipv4.icanhazip.com',
    'DOMAIN-SUFFIX,c.pki.goog',
]))

# apple.txt: missing Apple domains
apple_adds = sorted(set([
    'DOMAIN-SUFFIX,buy.music.apple.com',
]))


def dedup_append(filepath, new_lines, comment_before=None):
    if not os.path.exists(filepath):
        print(f'  FILE NOT FOUND: {filepath}')
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    existing = set()
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            existing.add(stripped)

    to_add = [l for l in new_lines if l not in existing]

    if not to_add:
        print(f'  {os.path.basename(filepath)}: nothing new to add')
        return

    print(f'  {os.path.basename(filepath)}: adding {len(to_add)} new rules')

    lines = content.split('\n')
    # Find the insertion point and insert new rules before first real rule
    insert_at = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('#') or line.strip() == '':
            insert_at = i + 1
        else:
            break

    insert_block = ''
    if comment_before:
        insert_block = '\n' + comment_before + '\n'
    insert_block += '\n'.join(to_add) + '\n'

    lines.insert(insert_at, insert_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'  -> {len(to_add)} rules added')


print('Updating proxy.txt...')
dedup_append(os.path.join(rules_dir, 'proxy.txt'), proxy_adds,
             comment_before='# Plex')

print()
print('Updating direct.txt...')
dedup_append(os.path.join(rules_dir, 'direct.txt'), direct_adds,
             comment_before='# Microsoft / Windows update')

print()
print('Updating apple.txt...')
dedup_append(os.path.join(rules_dir, 'apple.txt'), apple_adds,
             comment_before='# Apple direct domain additions')

print()
print('Done!')