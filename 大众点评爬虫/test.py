import craw_ip
proxys = craw_ip.generalProxies()
with open('proxies.txt', 'a') as f:
    for proxy in proxys:
        f.write(proxy + '\n')