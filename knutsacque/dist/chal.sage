import secrets

F.<i,j,k> = QuaternionAlgebra(-1, -1)
A = []
B = [1, i, j, k]

msg_bin = b"irisctf{redacted_redacted_redacted_}"
assert len(msg_bin) % 4 == 0
msg = [F(sum(Integer(msg_bin[idx+bi])*b for bi, b in enumerate(B))) for idx in range(0, len(msg_bin), len(B))]
targ = 2^64

for _ in range(len(msg)):
    a = F(sum(secrets.randbelow(targ)*b for b in B))
    A.append(a)

sm = F(0)
for idx in range(len(msg)):
    sm += msg[idx] * A[idx]

print("A =", A)
print("s =", sm)
