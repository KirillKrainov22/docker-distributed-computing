import os, time, redis

# Подключаемся к Redis
r = redis.Redis(host="redis", decode_responses=True)

# Ждём пока Redis поднимется
for _ in range(30):
    try:
        r.ping(); break
    except:
        time.sleep(1)

start = int(os.environ["RANGE_START"])
end   = int(os.environ["RANGE_END"])
chunk = int(os.environ["CHUNK_SIZE"])

# Сбрасываем старые данные и записываем новые
r.delete("results")
r.set("range_start", start)
r.set("range_end",   end)
r.set("chunk_size",  chunk)
r.set("current",     start)

print(f"Range set: {start} to {end}, chunk: {chunk}")
print("Consumers can start!")
