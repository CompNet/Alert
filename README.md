Alert
=======
*Abusive Language Detection in Online Conversations by Combining Content- and Graph-Based Features*

* Copyright 2018-20 Noé Cécillon

Alert is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. For source availability and license information see `LICENCE`

* Lab site: http://lia.univ-avignon.fr/
* GitHub repo: https://github.com/CompNet/Alert
* Contact: Noé Cécillon <noe.cecillon@univ-avignon.fr>

-----------------------------------------------------------------------


# Description
This software was designed to detect abusive messages in online conversations. It is a complete reimplementation and a much extended version of the software used in [[PLDL'17, PLDL'17a, PLDL'17b, PLDL'18, PLDL'19](#references)]. Two main approaches are implemented: a *content-based* approach and a *graph-based* approach, which can also be used jointly. This software was used in [[C'19, CLDL'19, CLDL'20, C'24](#references)] (cf. these publications for more details).


# Data
This software was applied to a corpus of chat messages written in French, whih unfortunately cannot be published due to legal matters [[PLDL'17, PLDL'17a, PLDL'17b, PLDL'18, PLDL'19, C'19, CLDL'19](#references)]. The conversational graphs extracted from these messages are publicly available on [Zenodo](https://doi.org/10.5281/zenodo.6815312), though, and can be used by this softwaree. It was also applied to some public data: a corpus of Wikipedia conversations annotated for 3 types of abuse [[CLDL'20](#references)], which is also available on [Zenodo](https://doi.org/10.5281/zenodo.6817093).


# Organization
Here are the folders composing the project:
* Folder `content-based`: contains the source code of the *content-based* approach.
    * Folder `Features`: contains the scripts to compute features.
    * `bad_words.txt`: the static list of french badwords used in [[CLDL'19](#references)].
    * `features.txt`: the list of all available features.
* Folder `graph-based`: contains the source code of the *graph-based* approach.
    * Folder `Features`: contains the scripts that compute the features.
* Folder `train-dev-test`: contains the train, development and test splits that we used in [[CLDL'20](#references)].


# Use
1. For the *content-based* approach, run the main script `content-based/main.py` with the following arguments:
    * `annotations`: Path to the file containing annotations such as *annotations_attack.csv* on [Zenodo](https://doi.org/10.5281/zenodo.6817093).
    * `messagesdir`: Path to the directory containing all conversation files.
    * `train`: Path to the file containing Ids of all messages in train split. Examples are available in `train-dev-test` folder.
    * `test`: Path to the file containing Ids of all messages in test split. Examples are available in `train-dev-test` folder.
    * `classifier`: The type of classifier to use. Only SVM is currently available.
    * `features`: Path to the file containing the subset of features to use. Use `features.txt` for the full feature set.
2. For *graph-based* approach, run the main script `graph-based/main.py` with the following arguments.
    * `annotations`: Path to the file containing annotations such as *annotations_attack.csv* on [Zenodo](https://doi.org/10.5281/zenodo.6817093).
    * `messagesdir`: Path to the directory containing all conversation files.
    * `train`: Path to the file containing Ids of all messages in train split. Examples are available in `train-dev-test` folder.
    * `test`: Path to the file containing Ids of all messages in test split. Examples are available in `train-dev-test` folder.
    * `classifier`: The type of classifier to use. Only SVM is currently available.
    * `window-size`: The size of window to use for the weight update.
    * `directed`: To use directed graphs.


# References
* **[PLDL'17]** É. Papegnies, V. Labatut, R. Dufour, and G. Linarès. *Detection of abusive messages in an on-line community*, 14ème Conférence en Recherche d'Information et Applications (CORIA), Marseille, FR, p.153–168, 2017. [doi: 10.24348/coria.2017.16](https://doi.org/10.24348/coria.2017.16) - [⟨hal-01505017⟩](https://hal.archives-ouvertes.fr/hal-01505017)
* **[PLDL'17a]** É. Papegnies, V. Labatut, R. Dufour, and G. Linarès. *Graph-based Features for Automatic Online Abuse Detection*, 5th International Conference on Statistical Language and Speech Processing (SLSP), Le Mans, FR, Lecture Notes in Artificial Intelligence, 10583:70-81, 2017. [doi: 10.1007/978-3-319-68456-7_6](https://doi.org/10.1007/978-3-319-68456-7_6) - [⟨hal-01571639⟩](https://hal.archives-ouvertes.fr/hal-01571639)
* **[PLDL'17b]** É. Papegnies, V. Labatut, R. Dufour, and G. Linarès. *Détection de messages abusifs au moyen de réseaux conversationnels*, 8ème Conférence sur les modèles et lánalyse de réseaux : approches mathématiques et informatiques (MARAMI), La Rochelle, FR, 2017. [⟨hal-01614279⟩](https://hal.archives-ouvertes.fr/hal-01614279)
* **[PLDL'18]** É. Papegnies, V. Labatut, R. Dufour, and G. Linarès. *Impact Of Content Features For Automatic Online Abuse Detection*, 18th International Conference on Computational Linguistics and Intelligent Text Processing (CICling 2017), Budapest, HU, Lecture Notes in Computer Science, 10762:153–168, 2018. [doi: 10.1007/978-3-319-77116-8_30](https://doi.org/10.1007/978-3-319-77116-8_30) - [⟨hal-01505502⟩](https://hal.archives-ouvertes.fr/hal-01505502)
* **[PLDL'19]** É. Papegnies, V. Labatut, R. Dufour, and G. Linarès. *Conversational Networks for Automatic Online Moderation*, IEEE Transactions on Computational Social Systems, 6(1):38–55, 2019. [doi: 10.1109/TCSS.2018.2887240](https://doi.org/10.1109/TCSS.2018.2887240) - [⟨hal-01999546⟩](https://hal.archives-ouvertes.fr/hal-01999546)
* **[C'19]** N. Cécillon. *Exploration de caractéristiques d’embeddings de graphes pour la détection de messages abusifs*, MSc Thesis, Avignon Université, Laboratoire Informatique d'Avignon (LIA), Avignon, FR, 2019. [⟨dumas-04073337⟩](https://dumas.ccsd.cnrs.fr/dumas-04073337)
* **[CLDL'19]** N. Cécillon, V. Labatut, R. Dufour & G. Linarès. *Abusive Language Detection in Online Conversations by Combining Content- and Graph-Based Features*, IAAA ICWSM International Workshop on Modeling and Mining Socia-Media Driven Complex Networks (Soc2Net), Munich, DE, Frontiers in Big Data 2:8, 2019. [doi: 10.3389/fdata.2019.00008](https://doi.org/10.3389/fdata.2019.00008) - [⟨hal-02130205⟩](https://hal.archives-ouvertes.fr/hal-02130205)
* **[CLDL'20]** N. Cécillon, V. Labatut, R. Dufour & G. Linarès. *WAC: A Corpus of Wikipedia Conversations for Online Abuse Detection*, 12th Language Resources and Evaluation Conference (LREC), Marseille, FR, p.1375–1383, 2020. [Conference version](http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.172.pdf) - [⟨hal-02497514⟩](https://hal.archives-ouvertes.fr/hal-02497514)
* **[C'24]** N. Cécillon. *Combining Graph and Text to Model Conversations: An Application to Online Abuse Detection*, PhD Thesis, Avignon Université, Laboratoire Informatique d'Avignon (LIA), Avignon, FR, 2024. [⟨tel-04441308⟩](https://hal.archives-ouvertes.fr/tel-04441308)
