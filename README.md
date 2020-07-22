Alert
=======
*Abusive Language Detection in Online Conversations by Combining Content- and Graph-Based Features*

* Copyright 2018-20 Noé Cécillon & Vincent Labatut

Alert is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. For source availability and license information see `licence.txt`

* Lab site: http://lia.univ-avignon.fr/
* GitHub repo: https://github.com/CompNet/Alert
* Contact: Nejat Arinik <noe.cecillon@univ-avignon.fr>

-----------------------------------------------------------------------

# Description
This software was designed to detect abusive messages in online conversations. Two approaches are implemented : a *content-based* approach and a *graph-based* approach. See reference [Soc2Net'19] for more details.

# Data
This software was applied to a corpus of Wikipedia conversations annotated for 3 types of abuse. The data and annotations are available on [FigShare](https://figshare.com/articles/Wikipedia_Abusive_Conversations/11299118).

# Organization
Here are the folders composing the project:
* Folder `content-based`: contains the source code of the *content-based* approach.
    * Folder `Features`: contains the scripts to compute features.
    * `bad_words.txt`: the static list of french badwords used in [Soc2Net'19].
    * `features.txt`: the list of all available features.
* Folder `graph-based`: contains the source code of the *graph-based* approach.
    * Folder `Features`: contains the scripts to compute features.
* Folder `train-dev-test`: contains the train, development and test splits that we used in [LREC'20].


# Use
1. For *content-based* approach, run the main script `content-based/main.py` with the following arguments.
    * `annotations`: Path to the file containing annotations such as *annotations_attack.csv* on [FigShare](https://figshare.com/articles/Wikipedia_Abusive_Conversations/11299118).
    * `messagesdir`: Path to the directory containing all conversation files.
    * `train`: Path to the file containing Ids of all messages in train split. Examples are available in `train-dev-test` folder.
    * `test`: Path to the file containing Ids of all messages in test split. Examples are available in `train-dev-test` folder.
    * `classifier`: The type of classifier to use. Only SVM is currently available.
    * `features`: Path to the file containing the subset of features to use. Use `features.txt` for the full feature set.
2. For *graph-based* approach, run the main script `graph-based/main.py` with the following arguments.
    * `annotations`: Path to the file containing annotations such as *annotations_attack.csv* on [FigShare](https://figshare.com/articles/Wikipedia_Abusive_Conversations/11299118).
    * `messagesdir`: Path to the directory containing all conversation files.
    * `train`: Path to the file containing Ids of all messages in train split. Examples are available in `train-dev-test` folder.
    * `test`: Path to the file containing Ids of all messages in test split. Examples are available in `train-dev-test` folder.
    * `classifier`: The type of classifier to use. Only SVM is currently available.
    * `window-size`: The size of window to use for the weight update.
    * `directed`: To use directed graphs.



# References
* **[Soc2Net'19]** N. Cécillon, V. Labatut, R. Dufour & G. Linarès. *Abusive Language Detection in Online Conversations by Combining Content- and Graph-Based Features*, 2019. [doi: 10.3389/fdata.2019.00008](https://doi.org/10.3389/fdata.2019.00008) - [⟨hal-02130205](https://hal.archives-ouvertes.fr/hal-02130205)
* **[LREC'20]** N. Cécillon, V. Labatut, R. Dufour & G. Linarès. *WAC: A Corpus of Wikipedia Conversations for Online Abuse Detection*, 2020. [⟨hal-02497514](https://hal.archives-ouvertes.fr/hal-02497514)