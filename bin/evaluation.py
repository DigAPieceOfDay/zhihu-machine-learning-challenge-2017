#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 7/24/17 3:38 PM
# @Author  : Jianpeng Hou
# @Email   : houjp1992@gmail.com


import math
import heapq
from bin.utils import LogUtil


def F_by_fuck_zhihu_eng(preds, labels):
    topk = 5
    top5_labels = list()

    for i, ps in enumerate(preds):
        top5 = enumerate(ps)
        top5 = sorted(top5, key=lambda s:s[1], reverse=True)
        top5_ids = [x[0] for x in top5[:5]]

        label_ids = list()
        for kv in enumerate(labels[i]):
            if 1 == kv[1]:
                label_ids.append(kv[0])

        top5_labels.append([top5_ids, label_ids])

    right_label_num = 0
    right_label_at_pos_num = [0 for i in range(50)]
    sample_num = 0
    all_marked_label_num = 0

    for predict_labels, marked_labels in top5_labels:
        sample_num += 1
        marked_label_set = set(marked_labels)
        all_marked_label_num += len(marked_label_set)

        for pos, label in zip(range(0, min(len(predict_labels), topk)), predict_labels):
            if label in marked_label_set:
                right_label_num += 1
                right_label_at_pos_num[pos] += 1

    precision = 0.0

    for pos, right_num in zip(range(0, topk), right_label_at_pos_num):
        precision += (right_num / float(sample_num)) / math.log(2.0 + pos)
    recall = float(right_label_num) / all_marked_label_num

    LogUtil.log('INFO', 'precision=%s, recall=%s, f=%s' % (str(precision),
                                                           str(recall),
                                                           str((precision * recall) / (precision + recall))))


def F(preds, labels):
    topk = 5

    right_label_num = 0
    right_label_at_pos_num = [0] * 5
    sample_num = 0
    all_marked_label_num = 0

    for i, ps in enumerate(preds):
        sample_num += 1
        top5_ids = [x[0] for x in heapq.nlargest(5, enumerate(ps), key=lambda p: p[1])]

        label_ids = list()
        for kv in enumerate(labels[i]):
            if 1 == kv[1]:
                label_ids.append(kv[0])

        marked_label_set = set(label_ids)
        all_marked_label_num += len(marked_label_set)

        for pos, label in enumerate(top5_ids):
            if label in marked_label_set:
                right_label_num += 1
                right_label_at_pos_num[pos] += 1

    precision = 0.0

    for pos, right_num in zip(range(0, topk), right_label_at_pos_num):
        precision += (right_num / float(sample_num)) / math.log(2.0 + pos)
    recall = float(right_label_num) / all_marked_label_num

    LogUtil.log('INFO', 'precision=%s, recall=%s, f=%s' % (str(precision),
                                                           str(recall),
                                                           str((precision * recall) / (precision + recall))))


def F_by_ids(ids, labels):
    topk = 5

    right_label_num = 0
    right_label_at_pos_num = [0] * 5
    sample_num = 0
    all_marked_label_num = 0

    for i, top5_ids in enumerate(ids):
        top5_ids = top5_ids[:5]
        sample_num += 1

        label_ids = list()
        for kv in enumerate(labels[i]):
            if 1 == kv[1]:
                label_ids.append(kv[0])

        marked_label_set = set(label_ids)
        all_marked_label_num += len(marked_label_set)

        for pos, label in enumerate(top5_ids):
            if label in marked_label_set:
                right_label_num += 1
                right_label_at_pos_num[pos] += 1

    precision = 0.0

    for pos, right_num in zip(range(0, topk), right_label_at_pos_num):
        precision += (right_num / float(sample_num)) / math.log(2.0 + pos)
    recall = float(right_label_num) / all_marked_label_num

    f = (precision * recall) / (precision + recall)

    LogUtil.log('INFO', 'precision=%s, recall=%s, f=%s' % (str(precision),
                                                           str(recall),
                                                           str(f)))
    return f