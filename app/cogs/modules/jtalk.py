import subprocess

def jtalk(t):
    file_path = "open_jtalk.wav"
    open_jtalk = ['open_jtalk']
    mech = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m','/usr/share/hts-voice/mei_normal.htsvoice']
    speed = ['-r','1.0']
    outwav = ['-ow', file_path]
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd, stdin = subprocess.PIPE)
    c.stdin.write(t.encode('utf-8'))
    c.stdin.close()
    c.wait()
    return file_path