# SIC_Leap

###Sample.py

options:

--train
        
--test
        

Generate training data

`python2.7 Sample.py --train > paper.txt`

Real time testing gesture

`python2.7 Sample.py --test`

> Game entry point is at the end of the method `on_frame` of `SampleListener` (line.226)
> You should only play game at `--test` mode.

###data2Vec.py

Reorganize training data

arguments:
          `input data` `output data` 

`python2.7 data2Vec.py paper.txt dumppaper`

###train.py

Train/tune model

options:

--train

--tune

arguments:

`paper` `scissor` `stone` ... (input the dump files in this order)

`python2.7 train.py --train dumppaper dumpscissor dumpstone dumppaper01 dumpscissor01 dumpstone01 ...`

###NOTICE

1.Training model by train.py will replace the model as `model.pkl`
2.Tuning model will take long time while data set is large.
3.The default training data set size is set to 1300 for each dumpfile (define at `train.py` method `train_SVM` at line.68)

