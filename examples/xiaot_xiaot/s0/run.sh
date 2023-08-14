#!/bin/bash
# Copyright 2021  Binbin Zhang(binbzha@qq.com)

. ./path.sh

stage=0
stop_stage=4
num_keywords=2  # 1

train_set=train_ch0
dev_set=dev_ch0
eval_set=eval_ch0

config=conf/ds_tcn_ce_3.yaml
norm_mean=true
norm_var=true
gpus="0,1,2,3"
nj=48

checkpoint=
dir=exp/kws_train_$(basename "${config}" .yaml)

num_average=15
score_checkpoint=$dir/avg_${num_average}.pt

. tools/parse_options.sh || exit 1;
window_shift=50

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
  echo "Preparing datasets..."
  mkdir -p dict
  echo "<filler> -1" > dict/words.txt
  echo "XiaoT_XiaoT 0" >> dict/words.txt
  python3 local/prepare_datasets.py
fi


if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
  echo "Compute CMVN and Format datasets"
  tools/compute_cmvn_stats.py --num_workers ${nj} --train_config $config \
    --in_scp data/${train_set}/wav.scp \
    --out_cmvn data/${train_set}/global_cmvn

  for x in ${train_set} ${dev_set} ${eval_set}; do
    tools/wav_to_duration.sh --nj ${nj} data/$x/wav.scp data/$x/wav.dur
    tools/make_list.py data/$x/wav.scp data/$x/text \
      data/$x/wav.dur data/$x/data.list
  done
fi


if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
  echo "Start training ..."
  mkdir -p $dir
  cmvn_opts=
  $norm_mean && cmvn_opts="--cmvn_file data/${train_set}/global_cmvn"
  $norm_var && cmvn_opts="$cmvn_opts --norm_var"
  num_gpus=$(echo $gpus | awk -F ',' '{print NF}')
  torchrun --standalone --nnodes=1 --nproc_per_node=$num_gpus \
    wekws/bin/train.py --gpus $gpus \
      --config $config \
      --train_data data/${train_set}/data.list \
      --cv_data data/${dev_set}/data.list \
      --model_dir $dir \
      --num_workers 16 \
      --num_keywords $num_keywords \
      --min_duration 50 \
      --seed 666 \
      $cmvn_opts \
      ${checkpoint:+--checkpoint $checkpoint}
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
  echo "Do model average, Compute FRR/FAR ..."
  python3 wekws/bin/average_model.py \
    --dst_model $score_checkpoint \
    --src_path $dir  \
    --num ${num_average} \
    --val_best

  result_dir=$dir/${eval_set}_$(basename $score_checkpoint)
  mkdir -p $result_dir
  python3 wekws/bin/score.py \
    --config $dir/config.yaml \
    --test_data data/${eval_set}/data.list \
    --batch_size 256 \
    --checkpoint $score_checkpoint \
    --score_file $result_dir/score.txt  \
    --num_workers 8

  # shellcheck disable=SC2043
  for keyword in 1 ; do # keyword 0
    python3 wekws/bin/compute_det.py \
      --keyword $keyword \
      --test_data data/${eval_set}/data.list \
      --window_shift $window_shift \
      --step 0.0001 \
      --score_file $result_dir/score.txt \
      --stats_file $result_dir/stats.${keyword}.txt
  done
fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    result_dir=$dir/${eval_set}_$(basename $score_checkpoint)
    python3 wekws/bin/plot_det_curve.py \
    --keywords_dict dict/words.txt \
    --stats_dir $result_dir \
    --figure_file $result_dir/det.png \
    --x_axis 'FAR' \
    --xlim 100 \
    --x_step 10 \
    --ylim 100 \
    --y_step 10
fi
