# sudo conda activate biosyntax
export BIOBERT_DIR=./biobert_v1.1_pubmed
echo $BIOBERT_DIR
export NER_DIR=./srl_data
export OUTPUT_DIR=./srl_output_syntax
rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
nohup /opt/conda/bin/python run_srl_syntax.py --do_train=True --do_eval=True --do_predict=True --vocab_file=$BIOBERT_DIR/vocab.txt --bert_config_file=$BIOBERT_DIR/bert_config.json --init_checkpoint=$BIOBERT_DIR/model.ckpt-1000000 --num_train_epochs=10.0 --data_dir=$NER_DIR --output_dir=$OUTPUT_DIR > nohup_syntax.out &

