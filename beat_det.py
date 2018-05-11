# -*- coding: utf-8 -*-
"""
Created on Thu May 10 22:25:57 2018

@author: Rudy
"""
import librosa
import copy
import measure

def onset_detection(filename="beats.wav"):
    y, sr = librosa.load('beats.wav')
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    onset_raw = librosa.onset.onset_detect(onset_envelope=oenv,backtrack=True)
#    plt.figure()
#    plt.subplot(3,1,1)
#    librosa.display.waveplot(y, sr=sr)
    onset_raw = librosa.frames_to_time(onset_raw)
#    print(onset_raw)

#    plt.vlines(onset_raw, 0, oenv.max(), label='Raw onsets')
    return onset_raw
    
#onset_detection()    

def pattern_recognition(onset_raw):
    
    max_sim = 0
    max_cut = 0
    max_a1a2 = 0
    for i in range(1, len(onset_raw)):
        new_onsets = copy.deepcopy(onset_raw)
        for j in range(len(onset_raw)-1):
            new_onsets[j] = new_onsets[j+1]-new_onsets[j]
        # now we split the onsets into two halves
        #DP to find similarities
        a1 = list(new_onsets[:i]) 
        a2 = list(new_onsets[i:])
        a2.append(a1[-1])
        
#        print(a1)
#        print(a2)
        f = []
        for i in range(len(a1)+1):
            f.append([])
            for j in range(len(a2)+1):
                f[i].append(0)
                
        for i in range(len(a1)):
            for j in range(len(a2)):
                if abs(a1[i]-a2[j]) < 0.06: f[i+1][j+1] = f[i][j]+1
                else:
                    f[i+1][j+1] = max(f[i][j+1], f[i+1][j])
#        print(f)
#        print(f[len(a1)][len(a2)])
#        print()
        if f[len(a1)][len(a2)] > max_sim:
            max_sim = f[len(a1)][len(a2)]
            max_cut = (len(a1), len(a2)-1)
            max_a1a2 = (a1, a2)
            
#    print("max_cut"+ str(max_cut))
#    print(max_a1a2)
#    return max_cut, max_a1a2
    return max_cut, onset_raw[:max_cut[0]], onset_raw[max_cut[0]:]

onset = onset_detection()
recog = pattern_recognition(onset)
print(recog)

def time_pattern_to_starts(recog, beats=4):
    onsets = list(recog[1])
#    print(onsets)
    time_len = onsets[-1]+(onsets[-1]-onsets[-2])
    rate = float(beats*measure.Unit.lpq)/time_len
    onsets = [int(onset*rate) for onset in onsets]
    return onsets

print(time_pattern_to_starts(recog))

#time_pattern_to_durations(recog)
#import matplotlib.pyplot as plt
#onset_env = librosa.onset.onset_strength(y, sr=sr,aggregate=np.median)
#hop_length = 512
#plt.figure(figsize=(8, 4))
#times = librosa.frames_to_time(np.arange(len(onset_env)),        sr=sr, hop_length=hop_length)
#plt.plot(times, librosa.util.normalize(onset_env),label='Onset strength')
#plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',            linestyle='--', label='Beats')
#plt.legend(frameon=True, framealpha=0.75)
## Limit the plot to a 15-second window
#plt.xlim(15, 30)
#plt.gca().xaxis.set_major_formatter(librosa.display.TimeFormatter())
#plt.tight_layout()