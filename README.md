# Proposing a Verifiable Anonymous Voting System Based on Encrypted Email and Git

`__version__ = "0.6.0"` (2020-11-23 13:49:00)

## Preliminary Notes

The following thoughts were triggered by the turbulences around the US presidential elections 2020, the ongoing protests in Belarus, allegations of election fraud in Tanzania and the discussion about voting on online party conventions in Germany. I am neither an expert in (online) voting systems nor in cybersecurity. Instead I am just a regular user of encrypted email and git and I am interested in how groups can manage the problem of decision-making without disintegrating.

As the above version number suggests the proposal has evolved since its initial publication mainly due to feedback. The following text is probably not trivial to understand. Visualization and text might complement each other.

The proposal does contain some flaws which I am aware of and probably some more. Nevertheless, it might be a starting point for something working.

---

**Important:** The assumptions/requirements below are obviously unrealistic (E.g. "Each user can use git and gpg"). They are stated this way to simplify the explanation of the voting protocol. I am confident that they can be relaxed w.r.t. to usability and robustness with a more elaborated approach and by implementing most of the user-activities in an (optional) open-source software frontend. However, the assumptions mainly serve to keep the discussion focussed to the backend mechanics.

---



## Motivation

(This section was included later in response to questions and criticism. It is not necessary to technically understand the rest.)

### Why Should the Free Software Community Think About Online Voting?

1. Currently high medial awareness due to US presidential elections and a significant amount of people who claim irregularities.
2. Good chance to point out the importance of transparency, credibility, signatures, encryption, and anonymity.
3. Good chance to raise awareness for established tools like *git*, *gpg* or *openPGP*.
4. Good possibility to point out an positively framed use case for online anonymity.
5. If digital voting will come, it must at least be based on Free and Open Source Software and community-approved concepts.
6. The usage of established tools (git, gpg, ...) increase the level of understandability (e.g. compared to blockchain-based approaches).


### General Arguments for Online Voting

1. Lower participation hurdle for voters
    - Nobody wants to wait for hours in a line outside.
    - Nobody wants to visit a voting station if there are attack warnings or other intimidation mechanisms.
2. Much Lower cost for holding a reliable election/voting (on almost any organizational level)
    - Allows the integration of more participative democratic elements (which is another complex topic, see below).
3. Trust problems with paper ballots
    - While in most public elections the local counting process can in principle be supervised by local voters, it remains intransparent how these results are aggregated at higher levels.
        - see severe issues with election result messaging software discovered by CCC ([PC-Wahl_Bericht](https://www.ccc.de/system/uploads/230/original/PC-Wahl_Bericht_CCC.pdf)).
    - Supervision of counting does not scale well.

### General Arguments against Online Voting

... and attempts for counter arguments

1. Possible attacks might scale very well (same effort for corrupting 10K votes as for 10 votes).
    - Countermeasures:
        - Independently controlled redundant systems (like for a block chain)
        - High degree of initial robustness: Even corrupting 10 votes should be very hard.
2. Private devices are mostly insecure (not up to date, malware, ...).
    - This is a general societal problem which is urgent to solve (not only for online voting).
    - Online voting could give big incentives for the public sector to provide enough resources to support users. Maintaining a secure digital device is currently much harder then it should be.
    - Additional Ideas:
        - Provide Linux live distribution which boots from a USB drive and has all necessary voting software installed.
        - Running voting software inside a virtual machine (assuming that it is hard to break into a VM from a malware-infected host).
        - Do not support phones and tablets as they are too malware prone.
            - Additional benefit: Raise awareness for this problem.
        - Provide (used) devices (PCs, notebooks) with Free Software for households that need one.
            - Additional benefit: This device could also be used for education.
3. Availability of cheap and legally safe online voting could raise the political pressure towards weakening parliaments in favor of plebiscites. This could lead to much more "populist" politics and increase the influence of unbalanced media and misinformation.
    - Unbalanced media and misinformation are general problems for (democratic) societies. An online voting procedure which is based on transparent processes and verifiability and not on the principle "Trust me, I tell the truth", could foster a more critical approach in media consumption and media production. It could raise the bar in what people believe and what not.
    - The decision about plebiscites (on which levels, for which kinds of issues, who can initiate and formulate them, ...) should be up to the sovereign anyway.
4. The fundamental insecurity of *the platform* (potential compromising of essential internet infrastructure by "[intelligence agencies](https://en.wikipedia.org/wiki/Intelligence_agency)" and other dangerous actors).
    - Severe concern! Citing from documents leaked by E. Snowden: *"activities such as […] e-voting […] beg to be mined"*
        - Source: https://www.evote-net.ch/index.html
    - Potential countermeasure: widespread usage of [open source hardware](https://en.wikipedia.org/wiki/Open-source_hardware)
        - Should be a political demand.
    - Argument: For votes in which not too much is at stake, this threat seems unrealistic. It would already be an improvement if online-voting were robust against other types of attacks (like corrupting one single server).


### Personal Conclusion of General Arguments

Voting is a delicate act. Digital voting bears many dangers (see assumptions below), but so does paper voting (see current and historical examples). In any case, I would prefer a Free and Open Source approach based on established and trusted tools and principles instead of someday using *facebook vote®*.


## Guiding principles

1. When it comes to voting there is no single trusted authority.
1. Only Free and Open Source Software can be trustable software.
1. Transparency prevents fraud and unjustified accusations of fraud.
1. Power and sensitive knowledge must be divided sufficiently among participating entities such that fraud is impossible without conspiration with other entities.
1. Each entity must have strong rational incentives to comply with the rules and to report any attempts of conspiration ("immune system").

## Assumptions and Requirements:

These assumptions serve to specify the environment on which the system operates. They are obviously unrealistic. This is to simplify the explanation of the system. Once the system is acknowledged to work under these assumptions, we can think about how to relax them.

### Environmental Assumptions

1. $N < 1000 users want (and are entitled) to vote.
4. There is a predefined time interval in which voting is allowed.
5. Each user has an official email address (say `user-$i@voting.org`) to which they have exclusive access to.
6. Each user can use git and gpg or openPGP
7. Every user has a pgp key-pair and the public key is known to everyone else and associated with this user.


### Assumptions about Entities and their Relations

9. There are five servers operated by independent actors that do not cooperate against the rules. In particular, they do not share unauthorized information among them nor with the public.
    - Server 1a (S1a)
    - Server 1b (S1b)
    - Server 2 (S2)
    - Server 3 (S3)
    - A public git repository for voting results (GR)
10. Every user has push-access to the `incoming`-branch.
10. S1a, S1b, S2 have push access to the branches `confirmed-pVAT1a`, `confirmed-pVAT1b`, and `confirmed-pVAT2`, respectively
12. The public key for each server is known to and trusted by all users. This can be ensured during voter registration.
11. The servers for the infrastructure and the devices on which the users vote are not corrupted and are secured against unauthorized access.


## Requirements

These are aspects which should be provided by the system:

1. Only entitled users are allowed to vote.
1. No user shall vote more than once.
1. The fact of whether a particular user voted can be public, the voting content shall be anonymous.
1. Every user must be able to formally confirm that their particular vote is represented correctly.
1. Only confirmed votes are counted.
1. One single entity with malicious intents should not be able to commit unnoticed fraud.



## How it works (regular case)

1. S1{a,b} generate $N partial voting authorization tokens (→ pVAT1a-list, pVAT1b-list).
1. S1{a,b} generates $N anonymous email addresses (AEAs) like `anonymous-$j@{a,b}-voting.org` and associates them randomly to the $N official user addresses via email forwarding (S1a and S1b each must run an indendent mail server). The association table is kept secret by S1{a,b}. Especially S2 is not allowed to know the associations.
1. S1{a,b} sends the list of all pVATs and all AEAs to S2.
1. S2 also generates $N pVATs. Then S2 creates triples by random combination ($pVAT1a, pVAT1b, $pVAT1c) and thereby forms a list of complete voting authorization token (VATs).
1. S2 also generates $N confirmation tokens of kind A (CT-A).
1. S2 associates randomly one VAT and one CT-A. This mapping is kept secret by S2, especially to S3.
1. S2 create a message containing:
    - one VAT
    - one CT-A
    - some random data (used as salt)
1. S2 encrypts this message with the public keys of **all** users. The encrypted message is split up into two blocks (block-A, block-B).
1. S2 Sends block-{A,B} to `anonymous-$j@{a,b}-voting.org`. Thus S1{a,b} sees only part of the encrypted data. Each email is signed with the official signature of S2.
1. User $k receives two encrypted emails, one via S1a, the other via S1b, each sent and signed by S2. They combine the blocks and decrypt it with their own private key. Thus the user obtains a VAT and a CT-A.
1. User $k clones the GR and makes an anonymous commit with a new text file (votes/$VAT) containing "$VOTING_CONTENT". The VAT ist unique and can be used as filename. The CT-A might be used later.
1. User $k pushes this commit over an anonymous connection (via tor) to the incoming branch of GR.
    - Alternatively, they could send a patch to GR via an encrypted anonymized email.
1. S{1a,1b,2} confirms that the commit contains a valid pVAT from its pVAT{1a,1b,2}-list and pushes it to the `confirmed-pVAT{1a,1b,2}` branch (one after another).
1. GR confirms that the other servers have confirmed the VAT and pushes the commit to the `main` branch.
1. User $k updates their version of the repo (`git pull`) and checks that their vote is correctly represented in the `main` branch.
1. After a random time delay (say 0.5 to 10 minutes) user $k commits a new text file (confirmations/$RANDOMNAME) containing: "My vote is correctly represented.", signs this commit with their private key, and pushes it to the `incoming`-branch. Due to the signature, this commit is non-anonymous. But it is unrelated to the actual voting.
1. GR formally checks this commit (spam prevention) and pushes it to the `main` branch.


![sequence diagram for the regular case (only showing up on github)](img/diagram_regular_case.svg "sequence diagram for the regular case")


### Result and Remarks

1. After the voting interval is over the GR contains $n1 votes, where $n1 <= $N and the difference is assumed to have voluntarily not voted. It also contains $n2 confirmations where  0 <= $n2 <= N. If all users acted as they should we have $n1 = $n2.
2. The CT-A is needed only for confirmation of VTA (see below).

## What could go wrong and what happens then?

This section collects attack scenarios and responses. It probably grows over time.

1. $n2 < $n1 (not all votes are confirmed):
    - Possible reasons: a) There could have been problems between voting and confirmation (device failure, ...) or b) The user actively decides not to confirm.
    - To ensure integrity of the voting, we only count confirmed votes. Challenge: filter out those VATs which are not confirmed without breaking anonymity.
        - S2 generates two more lists of confirmation tokens each list of length $n2: CT-B- and CT-C-list. The CT-A list was generated earlier and (as a whole) kept secret by S2. However, each user already has a personal CT-A from the first (anonymously received) email.
        - S2 publishes a list of all VAT-hashes, a list of all corresponding CT-A-hashes, and an unordered list of all CT-C hashes.
        - S2 sends both the CT-B- and CT-C-list to S3
        - S3 generates a random one-to-one mapping between CT-B and CT-C. This mapping is kept secret by S3.
        - S2 sends each of the $n2 users which did push a signed confirmation to GR an encrypted and signed email with a single CT-B.
        - User $k receives and decrypts the message with the CT-B
        - User $k receives an (encrypted to all users) message with a CT-C from S3 in exchange for (anonymously) sending a CT-B to S3.
        - User $k anonymously publishes their VAT, CT-A and CT-C in the repo.
        - Anybody can verify that this commit is valid by calculating the hashes and comparing them to the lists published and signed by S2. Invalid commits are removed from the repo by GR.
    - ![sequence diagram for anonymous VAT confirmation (only showing up on github)](img/diagram_VAT_confirmation.svg "sequence diagram for anonymous VAT confirmation")
2. $n2 > $n1 (more confirmations than votes)
    - Can be ignored. Just count all the votes.
3. GR could inject manipulated commits or refuse to accept specific commits.
    - There should be multiple and independently controlled instances of GR. Each user can push their commit to several repos and check the integrity of those against each other.


## Claims

1. Anonymity
    - Only the user knows their VAT because of random assignation, encrypted emails, and anonymous connections.
    - No single entity alone can break anonymity. Either S1{a|b} or S3 must conspire with S2 to do this. It would be easy to add more independent data-mixing layers to increase the number of necessary participants in the conspiration.
2. Trust
    - Any fraud against the users is detectable: Each single user can confirm that their vote is represented in the result.
    - The result cannot reasonably be disputed if the number of votes and valid confirmations matches. This can be checked by everyone.
3. Fast and Transparent Evaluation
    - Voting could be evaluated by anyone because the source data is publicly available in plain text. Evaluation software can be very easy.


## Criticism and Responses

- GPG was never audited and has bus factor 1
    - We could other software instead: [openpgp](https://www.openpgp.org/software/) or [sequoia-pgp](https://sequoia-pgp.org/).
- Tor is controlled via the exit nodes, many of which are operated by (foreingn) intelligence agencies.
    - The tor connections could be replaced by encrypted and anonymized emails. Like the VAT-distribution but the other way around.
    This makes the approach more complicated, though.
- In Git the order of merging matters this causes problems with many independet actors
    - Solution approach: <https://darcsbook.acmelabs.space/chapter01.html#why-darcs>

## Further Ideas

1. Specify a protocol on how to transparently file a complaint in an independent (and redundant) complaint repository (CR).
1. Specify a protocol for an inherent **immune system**: give infrastructure entities and users a high incentive to report any attempt to conspire
    - incentivize $A to falsely act as if they want to conspire with $B while having previously published an encrypted message. The key of which must be published at a given time.
    - These encrypted messages can obtain meaningful or random information. Many of them are automatically generated.
    - If $B does report this $A can prove its true intentions when publishing the key to its encrypted message.
    - If $B does not report this to CR but instead agrees to conspire, then $A can publish this agreement and identify $B as a potential conspirator.
    - There can be meta-levels to this.


## References (and commenting excerpts)

- [Why Electronic Voting Is Still A Bad Idea](https://www.youtube.com/watch?v=LkH2r-sNjQs), Tom Scott, 2020, youtube
    - Voting should be based on *trust* and *anonymity*.
    - In national elections there are probably high potential actors with huge budgets who want to influence the result to their favor.
    - Paper ballot version has matured over centuries → fair robustness against fraud attempts.
    - Potential fraud mechanisms do not scale very well (easy for 10 votes, hard for 10K votes).
    - Voting machines are badly maintained can be attacked (irrelevant to this approach).
    - Voting from private devices is even more dangerous (virus infection, botnets, ...).

- ["Analysis of an Election Software" (German)](https://www.ccc.de/system/uploads/230/original/PC-Wahl_Bericht_CCC.pdf)
    - In Germany there was widespread use of insecure software for communicating results of paper ballot voting to higher levels.

- [Logbuch:Netzpolitik: LNP356](https://logbuch-netzpolitik.de/lnp356-gesegneter-entscheidungswahn) (german)
    - In the last part of the audio (starting at 01:30:00h): interesting updates on the PC-Wahl story (see above).
    - Git is mentioned as a possibility to create transparency.


- [Successful "Man in the Middle"-Attack on the Swiss e-voting system](https://www.tagesanzeiger.ch/schweiz/standard/alle-evotingsysteme-der-schweiz-sind-unterwandert/story/31191771)
    - Demonstration only, no real harm was done.
    - Voters were redirected to a fake server by DNS spoofing. On that server their inputs could have been esily captured and manipulated.

- [Going from Bad to Worse: From Internet Voting to Blockchain Voting](https://people.csail.mit.edu/rivest/pubs/PSNR20.pdf)
    - Several persons brought this recent preprint to my attention.
    - Authors: Sunoo Park,  Michael Specter, Neha Narula,  [Ronald L. Rivest](https://en.wikipedia.org/wiki/Ron_Rivest) (cf. "RSA")
    - Very interesting: Section 4 (collection of critical questions which helps to analyse online-voting systems)




### What already exists (learned during feedback)

1. https://heliosvoting.org/
    - Free Software (Apache License)
    - Promises end-to-end verifiability
    - Seems to rely a central server
    - Last commit 2017
2. https://www.belenios.org/
    - Free Software (AGPL)
    - Promises end-to-end verifiability
    - Seems to rely a central server (?)
    - https://gitlab.inria.fr/belenios/belenios, last commit 2020
3. https://en.wikipedia.org/wiki/End-to-end_auditable_voting_systems
    - Extensive collection of E2E verifiable voting approaches. Too much to read for one day.
    - Still, the current approach might be simpler to implement because it uses only established tools.
