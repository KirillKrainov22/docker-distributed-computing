import os, time, math, redis, socket

def count_primes(lo, hi):
    count = 0
    for n in range(max(2, lo), hi):
        if all(n % d != 0 for d in range(2, int(math.isqrt(n)) + 1)):
            count += 1
    return count
    
r = redis.Redis(host="redis", decode_responses=True)

# Уникальный ID для этого consumer-а
cid = socket.gethostname()
# Ждём пока producer запишет данные в Redis
for _ in range(60):
    try:
        if r.exists("range_end"):
            break
    except:
        pass
    time.sleep(1)

range_end  = int(r.get("range_end"))
chunk_size = int(r.get("chunk_size"))
print(f"{cid} started, end={range_end}")

while True:
    # Атомарно берём следующий чанк
    end_pos   = r.incrby("current", chunk_size)
    start_pos = end_pos - chunk_size

    if start_pos >= range_end:
        break  # Работа закончена — выходим

    hi = min(end_pos, range_end)
    t0 = time.time()
    primes = count_primes(start_pos, hi)
    elapsed = time.time() - t0

    print(f"{cid} [{start_pos}, {hi}) done: {primes} primes in {elapsed:.2f}s")
    r.rpush("results", f"{cid} [{start_pos},{hi}) {primes} primes {elapsed:.2f}s")

print(f"{cid} all done, exiting")
