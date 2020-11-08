```sequence
participant user_k
participant S1a
participant S1b
participant S2
participant GR
participant S3
Note over S2: S2: create \n - CT-B-list (len = $n2) \n - CT-C-list (len = $n2) \n |
S2->GR: _\n  _ \n publish \n list of VAT-hashes \n list of corresp. CT-A-hashes \n list of unsorted CT-C-hashes
S2->S3: \n CT-B-list \n CT-C-list
S2->user_k: CT-B (to those who \n published a confirmation)
user_k-->S3 : CT-B (via tor)
S3->S1a : CT-C encrypted block 1 to AEA
S1a->user_k : CT-C encrypted block 1
S3->S1b : CT-C encrypted block 2 to AEA
S1b->user_k : CT-C encrypted block 2
Note over user_k: combine blocks \n decrypt CT-C
user_k-->GR: push commit with \n VAT, CT-A and CT-C
```
