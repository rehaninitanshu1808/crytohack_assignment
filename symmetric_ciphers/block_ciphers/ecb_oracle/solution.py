import subprocess
import json

def oracle(d):
    h = d.hex() if d else '00'
    r = subprocess.run(['curl', '-s', f'https://aes.cryptohack.org/ecb_oracle/encrypt/{h}/'], capture_output=True, text=True)
    return bytes.fromhex(json.loads(r.stdout)['ciphertext'])

flag = b''

for i in range(26):
    pad_len = (15 - i) % 16
    if len(flag) >= 15 and pad_len < 16:
        pad_len += 16
    
    pad = b'A' * pad_len
    target = oracle(pad)
    flag_i_position = pad_len + i
    target_blk_num = flag_i_position // 16
    target_blk = target[target_blk_num*16:(target_blk_num+1)*16]
    
    guess_position = len(pad) + len(flag)
    test_blk_num = guess_position // 16
    
    for g in range(256):
        test = pad + flag + bytes([g])
        test_ct = oracle(test)
        test_blk = test_ct[test_blk_num*16:(test_blk_num+1)*16]
        
        if test_blk == target_blk:
            flag += bytes([g])
            break
    
    if flag.endswith(b'}'):
        break

print(flag.decode("utf-8"))
