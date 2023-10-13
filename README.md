# WeKws
# Code is here and run by the script
# Run：./run.sh
# You should download dataset by yourself
[**Roadmap**](https://github.com/wenet-e2e/wekws/issues/121)
| [**Paper**](https://arxiv.org/pdf/2210.16743.pdf)


Production First and Production Ready End-to-End Keyword Spotting Toolkit.

The goal of this toolkit it to...

Small footprint keyword spotting (KWS), or specifically wake-up word (WuW) detection is a typical and important module in internet of things (IoT) devices.  It provides a way for users to control IoT devices with a hands-free experience. A WuW detection system usually runs locally and persistently on IoT devices, which requires low consumptional power, less model parameters, low computational comlexity and to detect predefined keyword in a streaming way, i.e., requires low latency.


## Typical Scenario

We are going to support the following typical applications of wakeup word:

* Single wake-up word
* Multiple wake-up words
* Customizable wake-up word
* Personalized wake-up word, i.e. combination of wake-up word detection and voiceprint

## Installation

- Clone the repo
``` sh
git clone https://github.com/wenet-e2e/wekws.git
```

- Install Conda: please see https://docs.conda.io/en/latest/miniconda.html
- Create Conda env:

``` sh
conda create -n wekws python=3.8
conda activate wekws
pip install -r requirements.txt
conda install pytorch=1.10.0 torchaudio=0.10.0 cudatoolkit=11.1 -c pytorch -c conda-forge

## Reference

* Mining Effective Negative Training Samples for Keyword Spotting
  ([github]( https://github.com/jingyonghou/KWS_Max-pooling_RHE),
   [paper](https://www.microsoft.com/en-us/research/uploads/prod/2020/04/ICASSP2020_Max_pooling_KWS.pdf))
* Max-pooling Loss Training of Long Short-term Memory Networks for Small-footprint Keyword Spotting
  ([paper](https://arxiv.org/pdf/1705.02411.pdf))
* A depthwise separable convolutional neural network for keyword spotting on an embedded system
  ([github](https://github.com/PeterMS123/KWS-DS-CNN-for-embedded),
   [paper](https://asmp-eurasipjournals.springeropen.com/track/pdf/10.1186/s13636-020-00176-2.pdf))
* Hello Edge: Keyword Spotting on Microcontrollers
  ([github](https://github.com/ARM-software/ML-KWS-for-MCU),
   [paper](https://arxiv.org/pdf/1711.07128.pdf))
* An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling
  ([github](http://github.com/locuslab/TCN),
   [paper](https://arxiv.org/pdf/1803.01271.pdf))
