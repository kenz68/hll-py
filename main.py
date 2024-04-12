from loglog.loglog import LogLog

if __name__ == '__main__':
    ll = LogLog(2000000, 0.05)
    for i in range(10):
        ll.add(str(i))

    print(ll.get_number_estimate())