```sequence
participant user_k
participant S1a
participant S1b
participant S2
participant GR
participant S3
Note over S1a: create \n - random  mail fwd \n (AEA-list1) \n - pVAT-list-1a
S1a->S2: (AEA-list1a) \n pVAT-list-1a
Note over S1b: S1b: create \n - random  mail fwd \n (AEA-list2) \n - pVAT-list-1b
S1b->S2: \n (AEA-list1b) \n pVAT-list-1b
Note over S2: S2: create \n - pVAT-list2 \n - VAT-list \n (from all pVATs) \n - CT-A-list
S2->S1a: \n VAT + CT-A (encrypted) \n (block1) to AEA
S1a->user_k: \n VAT + CT-A (encrypted) \n (block1) (fwd)
S2->S1b: \n VAT + CT-A (encrypted) \n (block1) to AEA
S1b->user_k: \n VAT + CT-A (encrypted) \n (block1) (fwd)
Note over user_k: - combine blocks \n - decrypt VAT + CT-A
user_k-->GR: push vote-commit \n to incoming branch via tor
S1a->GR: confirm valid pVAT-1a (via push)
S1b->GR: \n confirm valid pVAT-1b (via push)
S2->GR: \n confirm valid pVAT-2 (via push)
Note over GR: vote commit \n is now in \n main branch
user_k->GR: \n push confirmation-commit \n (signed with official key) \n to incomming
Note over GR: GR: \n formally check commit \n (prevent spam) \n push to main main branch
Note over S3: not needed \n in regular case
```
