#!/usr/bin/env python3

# Copyright He Wang
# Apache 2.0
""" This script prepares the XiaoT_XiaoT dataset.
"""

import os
import glob
import json

'''
audio文件夹里
    eval_far:       '*_0'       （共有四个通道，选择一个0）
    train & dev:    '*_0_*'

audio_bf文件夹里
   eval_far:        '*_bf'
   train & dev:     '*_bf_*'
'''
audio_dir = 'audio'
eval_filename = '*_0'
train_filename = '*_0_*'
signal = '0'    # 表示通道，或bf

def prepare_dataset(dataset):
    # 默认都取第一个通道 即 0 通道
    if dataset == 'eval':
        # far-field wavs
        positive_wavs = glob.glob(f"/home/hwang/2023internship/MISP2021_AVWWS/"
                                  f"positive/{audio_dir}/{dataset}/far/{eval_filename}.wav")
        negative_wavs = glob.glob(f"/home/hwang/2023internship/MISP2021_AVWWS/"
                                  f"negative/{audio_dir}/{dataset}/far/{eval_filename}.wav")
    else:
        # far-field wavs
        positive_wavs = glob.glob(f"/home/hwang/2023internship/MISP2021_AVWWS/"
                                  f"positive/{audio_dir}/{dataset}/far/{train_filename}.wav")
        negative_wavs = glob.glob(f"/home/hwang/2023internship/MISP2021_AVWWS/"
                                  f"negative/{audio_dir}/{dataset}/far/{train_filename}.wav")
        if dataset == 'train':
            # middle-field wavs
            positive_wavs += glob.glob(f'/home/hwang/2023internship/MISP2021_AVWWS/'
                                       f'positive/{audio_dir}/{dataset}/middle/{train_filename}_.wav')
            negative_wavs += glob.glob(f'/home/hwang/2023internship/MISP2021_AVWWS/'
                                       f'negative/{audio_dir}/{dataset}/middle/{train_filename}.wav')
            # near-field wavs
            positive_wavs += glob.glob(f'/home/hwang/2023internship/MISP2021_AVWWS/'
                                       f'positive/{audio_dir}/{dataset}/near/*.wav')
            negative_wavs += glob.glob(f'/home/hwang/2023internship/MISP2021_AVWWS/'
                                       f'negative/{audio_dir}/{dataset}/near/*.wav')

        positive_wavs = [item for item in positive_wavs if 'near' in item or item.split('/')[-1].split('_')[6] == signal]
        negative_wavs = [item for item in negative_wavs if 'near' in item or item.split('/')[-1].split('_')[6] == signal]
    print(f'Number of {dataset} positive wavs: {len(positive_wavs)}')
    print(f'Number of {dataset} negative wavs: {len(negative_wavs)}')
    return sorted(positive_wavs), sorted(negative_wavs)


if __name__ == '__main__':
    train_positive, train_negative = prepare_dataset('train')
    dev_positive, dev_negative = prepare_dataset('dev')
    eval_positive, eval_negative = prepare_dataset('eval')

    suffix = "ch0"
    os.system(f"mkdir -p data/train_{suffix}")
    os.system(f"mkdir -p data/dev_{suffix}")
    os.system(f"mkdir -p data/eval_{suffix}")

    # write train dataset files
    with open(f'data/train_{suffix}/wav.scp', 'w') as f:
        for wav in train_positive + train_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} {wav}\n")
    with open(f'data/train_{suffix}/text', 'w') as f:
        for wav in train_positive:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 1\n")
        for wav in train_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 0\n")

    # write dev dataset files
    with open(f'data/dev_{suffix}/wav.scp', 'w') as f:
        for wav in dev_positive + dev_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} {wav}\n")
    with open(f'data/dev_{suffix}/text', 'w') as f:
        for wav in dev_positive:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 1\n")
        for wav in dev_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 0\n")

    # write eval dataset files
    with open(f'data/eval_{suffix}/wav.scp', 'w') as f:
        for wav in eval_positive + eval_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} {wav}\n")
    with open(f'data/eval_{suffix}/text', 'w') as f:
        for wav in eval_positive:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 1\n")
        for wav in eval_negative:
            f.write(f"{os.path.basename(wav).replace('.wav', '')} 0\n")
