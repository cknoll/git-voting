# Proposing a Verifiable Anonymous Voting System Based on Email, GPG, Git and Tor

`__version__ = "0.1.2"`

## Preliminary Notes

As far as I know, there is currently no secure online voting system. The following thoughts were triggered by the turbulences around the US presidential elections 2020, the ongoing protests in Belarus and the discussion about voting on online party conventions in Germany. I am neither an expert in (online) voting systems nor in cyber security but instead just a regular user of email, gpg and git and interested in how groups can manage the problem of decision-making without desintegrating. The proposal does contain some flaws which I am aware of and probably many more. Nevertheless it might be a starting point for something working. The assumptions below are in part admittedly unrealistic (E.g. "Each user can use git and gnupg"). They are stated this way to simplify the explanation of the voting protocol. I am confident that they can be relaxed w.r.t. to usability and robustness with a more elaborated approach.

## Guiding principles

- There is no single trusted authority.
- Power and sensitive knowledge for each entity must be divided sufficiently such that each entity has rational incentives to comply with the rules.

## Assumptions:

1. $N users want (and are entitled) to vote.
2. No user shall vote more than once.
3. The fact whether they voted can be public, the voting content shall be anonymous.
4. There is a predefined time interval in which voting is allowed.
5. Each user has an official email address (say `user-$i@voting.org`) to which they have exclusive access to.
6. Each user can use git and gnupg.
7. Every user has a pgp key-pair and the public key is known to everyone else and associated to this user.
8. Every user has two key-pairs for asymmetric encryption
    - Key pair 1: public key known to everyone else and associated to the official email address of user
    - Key pair 2: public key not known to anyone (before voting)
9. There are three server operators which do not cooperate against the rules. In particular they do not share unauthorized information among them nor with the public.
    - Server 1 (S1)
    - Server 2 (S2)
    - A public git repository for voting results (GR) to which everyone as push-access to the incoming-branch.
10. S1 has push access to the main branch OF GR
11. The servers for the infrastructure and the device on which the users vote are not corrupted and are secured against unauthorized access.


## How it works

- S1 generates $N voting authorization tokens (VATs).
- S1 generate $N anonymous email addresses (AEAs) like `anonymous-$j@voting.org` and associated them randomly to the N official addresses via email forwarding. The association table is kept secret to S1.
- S1 sends the list of all VATs and AEAs to S2.
- S2 sends one random token to each e-mail address. Each email is encrypted with all $N public keys.
- User $k recieves an encrypted mail with one VAT and decrypts it with their own private key.
- User $k clones the GR and makes an anonymous commit with a new text file (votes/$RANDOMNAME) containing "$VAT: $VOTING_CONTENT".
- User $k pushes this commit over an anonymous connection (via Tor) to the incoming branch.
- S1 confirms that the commit contains a valid VAT and pushes it to the main branch
- User $k checks that their vote is correctly represented in the main branch.
- User $k commits a new text file (confirmations/$RANDOMNAME) containing: "My vote is correctly represented.", signs this commit with their private key. and pushes it to incoming.
- S1 formally checks this commit and pushes it to the main branch.

## Result

- After voting interval is over the GR contains $n votes and $n confirmations, where $n < $N and the difference is assumed to have voluntarily not voted.

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


