#/usr/bin/env python
#coding=utf-8
import jieba
import sys
import numpy as np
import tensorflow as tf

from a1_dual_bilstm_cnn_predict_ensemble import predict_bilstm
#from a1_dual_bilstm_cnn_predict_ensemble_tempcnn import predict_bilstm as predict_bilstm_tempcnn

def process(inpath, outpath):
    # 1.1 model1: bilstm_char
    tokenize_style='char'
    ckpt_dir='dual_bilstm_char_checkpoint/'
    model_name='dual_bilstm'
    name_scope='bilstm_char'
    graph= tf.Graph().as_default()
    logits_bilstm_char,line_no_list,vocab_index2label=predict_bilstm(inpath,tokenize_style,ckpt_dir,model_name,name_scope,graph)

    # 1.2.model2:bilstm_word
    tokenize_style='word'
    ckpt_dir='dual_bilstm_word_checkpoint/'
    model_name='dual_bilstm'
    name_scope='bilstm_word'
    graph= tf.Graph().as_default()
    logits_bilstm_word,_,_ = predict_bilstm(inpath,tokenize_style,ckpt_dir,model_name,name_scope,graph)

    # 1.3.model2:bilstm_word
    tokenize_style='word'
    ckpt_dir='dual_cnn_word_checkpoint/'
    model_name='dual_cnn'
    name_scope='cnn_word'
    graph= tf.Graph().as_default()
    logits_cnn_word,line_no_list,vocab_index2label = predict_bilstm(inpath,tokenize_style,ckpt_dir,model_name,name_scope,graph)

    # 1.4.model2:bilstm_word
    tokenize_style='char'
    ckpt_dir='dual_cnn_char_checkpoint/' #dual_cnn_char_checkpoint
    model_name='dual_cnn'
    name_scope='cnn_char'
    graph= tf.Graph().as_default()
    logits_cnn_char,line_no_list,vocab_index2label = predict_bilstm(inpath,tokenize_style,ckpt_dir,model_name,name_scope,graph)

    # 2. get weighted logits
    logits=logits_bilstm_char+logits_bilstm_word+logits_cnn_word+logits_cnn_char #[test_data_size,num_classes]

    # 3. save predicted result to file system
    save_result_by_logit(logits, line_no_list,vocab_index2label,outpath)


def save_result_by_logit(logits, line_no_list, vocab_index2label, outpath):
    file_object = open(outpath, 'a')
    for index, logit in enumerate(logits):
        label_index=np.argmax(logit)
        label=vocab_index2label[label_index]
        file_object.write(line_no_list[index] + "\t" + label + "\n")
    file_object.close()

if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2])
