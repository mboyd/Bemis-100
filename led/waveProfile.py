import wave

p = wave.WavePattern().__iter__()

while True:
    out = p.next()
