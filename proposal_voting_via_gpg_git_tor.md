# Proposing a Verifiable Anonymous Voting System Based on Email, GPG, Git and Tor

`__version__ = "0.2.0"` (expecting detailed critical feedback at 2020-11-06 15:00 UTC)

## Preliminary Notes

As far as I know, there is currently no secure online voting system. The following thoughts were triggered by the turbulences around the US presidential elections 2020, the ongoing protests in Belarus and the discussion about voting on online party conventions in Germany. I am neither an expert in (online) voting systems nor in cyber security but instead just a regular user of email, gpg and git and interested in how groups can manage the problem of decision-making without desintegrating. The proposal does contain some flaws which I am aware of and probably many more. Nevertheless it might be a starting point for something working. The assumptions below are in part admittedly unrealistic (E.g. "Each user can use git and gnupg"). They are stated this way to simplify the explanation of the voting protocol. I am confident that they can be relaxed w.r.t. to usability and robustness with a more elaborated approach.

## Guiding principles

- There is no single trusted authority.
- Only Free and Open Source Software can be trustable software.
- Transparency prevents frauds and unjustified accusations of fraud.
- Power and sensitive knowledge for each entity must be divided sufficiently such that each entity has rational incentives to comply with the rules.

## Assumptions:

1. $N users want (and are entitled) to vote.
1. $N < 100.
2. No user shall vote more than once.
3. The fact whether they voted can be public, the voting content shall be anonymous.
4. There is a predefined time interval in which voting is allowed.
5. Each user has an official email address (say `user-$i@voting.org`) to which they have exclusive access to.
6. Each user can use git and gnupg.
7. Every user has a pgp key-pair and the public key is known to everyone else and associated to this user.
9. There are four server operators which do not cooperate against the rules. In particular they do not share unauthorized information among them nor with the public.
    - Server 1 (S1)
    - Server 2 (S2)
    - Server 3 (S3)
    - A public git repository for voting results (GR) to which everyone as push-access to the incoming-branch.
10. S1 has push access to the branch `pVAT1-confirmed`. S2 has push access to the main branch of GR.
12. The public key for each server is known to and trusted by all users.
11. The servers for the infrastructure and the device on which the users vote are not corrupted and are secured against unauthorized access.


## How it works (regular case)

1. S1 generates $N partial voting authorization tokens (pVATs).
1. S1 generate $N anonymous email addresses (AEAs) like `anonymous-$j@voting.org` and associates them randomly to the N official addresses via email forwarding (S1 must run a mail server). The association table is kept secret by S1. Especially S2 is not allowed to know the associations.
1. S1 sends the list of all pVATs and all AEAs to S2.
1. S2 also generates $N pVATs. Then S2 combines randomly each pVAT from S1 with one pVAT from S2 and thereby forms a complete voting authorization token (VAT).
1. S2 also generates $N confirmation tokens of kind A (CT-A).
1. S2 associates randomly one VAT and one CT-A. This mapping is kept secret by S2, especially to S3.
1. S2 sends one VAT-CT-A-pair to each anonymous e-mail address. Because the final recipient is unknown to S2, each email is encrypted with **all** $N public keys. Each email is signed with the official signature of S2.
1. User $k recieves exactly one encrypted mail with one VAT-CT-A-pair signed by S2. They decrypt it with their own private key.
1. User $k clones the GR and makes an anonymous commit with a new text file (votes/$RANDOMNAME) containing "$VAT: $VOTING_CONTENT". The CT-A might be used later.
1. User $k pushes this commit over an anonymous connection (via Tor) to the incoming branch of GR.
1. S1 confirms that the commit contains a valid pVAT from its pVAT1-list and pushes it to the `pVAT1-confirmed` branch.
1. S2 confirms that the commit contains a valid pVAT from its pVAT2-list and pushes it to the `main` branch.
1. User $k updates their version of the repo (`git pull`) and checks that their vote is correctly represented in the `main` branch.
1. After a random time delay (say 0.5 to 10 minutes) user $k commits a new text file (confirmations/$RANDOMNAME) containing: "My vote is correctly represented.", signs this commit with their private key, and pushes it to incoming. This commit is non-anonymous.
1. S2 formally checks this commit (spam prevention) and pushes it to the main branch.

## Result and Remarks (regular case)

1. After the voting interval is over the GR contains $n1 votes, where $n1 <= $N and the difference is assumed to have voluntarily not voted. It also contains $n2 confirmations where  0 <= $n2 <= N. If all users acted as they should we have $n1 = $n2.

## What could go wrong and what happens then?

This section collects attack scenarios and responses.

1. $n2 < $n1 (not all votes are confirmed):
    - Possible reasons: a) Their could have been problems between voting and confirmation (device failure, ...) or b) The user actively decides not to confirm.
    - To ensure integrity of the voting we only count confirmed votes. We thus filter out those VATs which are not confirmed without breaking anonymity.
        - We use the CT-A and S3 as a "mixer". To be detailed.
2. $n2 > $n1 (more confirmations than votes)
    - Can be ignored. Just count the votes.
3. More to come ...


## Claims

- Anonymity
    - Only the user knows their VAT because of random assignation, encrypted emails, and anonymous connections.
- Any fraud is detectable:
    - S1 operator could use VATs by their own to generate votes but their would not be any signed confirmation for them.
    - S1 could force-push to the repo but could not generate valid signatures.
- Fast and Transparent Evaluation
    - Voting could be evaluated by anyone because the source data is publicly available.

## Final Remarks

The sketched approach could be improved significantly by implementing most of the user-activities in an open-source software frontend to increase usability. More division of power and knowledge and redundant versions of infrastructural entities (S1, S2 and GR) could increase robustness against vandalism and attacks.


