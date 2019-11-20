import hashlib
m = hashlib.md5()

s = "lingyunyi"
s = s.encode(encoding='utf-8')
m.update(s)
str_md5 = m.hexdigest()

print(str_md5)