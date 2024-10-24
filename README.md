# 自动科技评价学 Auto Science and Technology Evaluation
> 目前只有一个小例子

# 路径

1. 生成树；
   1. 
2. 加权得分；

## LLM-KG

[[2210.11298\] Tele-Knowledge Pre-training for Fault Analysis (arxiv.org)](https://arxiv.org/abs/2210.11298)

> To achieve this, we fifirst address the issue from multi
>
> source and multi-modal data (e.g., multi-directional machine
>
> data, textual documents, and semi-structured KG), which can
>
> distract the model from effificient learning. To remedy this,
>
> we refer to the **prompt engineering** techniques [16]–[18] for
>
> modality unifification and provide relevant **template hints** to
>
> the model for modalities unifification.
>
> 参考提示词工程来进行模态统一



> Thirdly, we are aware of different training target among
>
> the tele-corpus, machine data and the knowledge triples.
>
> **Thus we adopt a multi-stage training mode for multi-level**
>
> **knowledge acquisition**: *(i)* **TeleBERT**: in stage one we follow
>
> ELECTRA [25] pre-training paradigm and data augmentation
>
> method SimCSE [26] for large-scale (about 20 million) textual
>
> tele-corpus pre-training; *(ii)* **KTeleBERT**: In stage two, we
>
> extract those causal sentences which contain relevant causal
>
> keywords to re-train TeleBERT together with the numeric
>
> related machine data, where a knowledge embedding training
>
> objective and multi-task learning method are introduced for
>
> explicit knowledge integration.
>
> 采用多阶段训练模式进行多层次知识获取



> With our pre-trained model, we apply the model-generated
>
> service vectors to enhance three tasks of fault analysis: root
>
> cause analysis (RCA), event association prediction (EAP),
>
> and fault chain tracing (FCT). The experimental results show
>
> that our TeleBERT and KTeleBERT successfully improve the
>
> performance of these three tasks.



[Do Pre-trained Models Benefit Knowledge Graph Completion？ A Reliable Evaluation and a Reasonable Approach](./docs/Do Pre-trained Models Benefit Knowledge Graph Completion？ A Reliable Evaluation and a Reasonable Approach.pdf)

> For these unknown triples, we conduct human annotation to check if they are valid.
>
> We conduct experiments on two KGC datasets sampled from **Wikidata** and **Freebase**, and reevaluate the KGE-based and PLM-based KGC models under OWA instead of CWA.



[通俗易懂解释知识图谱（Knowledge Graph）_知识图谱本体和实体的区别-CSDN博客](https://blog.csdn.net/Cocktail_py/article/details/119907693)



[[2404.14741\] Generate-on-Graph: Treat LLM as both Agent and KG in Incomplete Knowledge Graph Question Answering (arxiv.org)](https://arxiv.org/abs/2404.14741)

[LLM+KG@VLDB’24 Workshop Summary (arxiv.org)](https://arxiv.org/html/2410.01978v1#bib.bib3)

[Semantic-enhanced Programmable Graph (openkg.cn)](https://spg.openkg.cn/en-US)

[开放图谱 – 开放知识图谱 (openkg.cn)](http://openkg.cn/datasets-type/)

# QUESTION

1. 抓哪些数据？
2. 如何生成树。


> <Achievements, Contributors, Institutions>

还有一个点：

主要的知识是英文的，但是科技评价学最终要整理成中文内容

