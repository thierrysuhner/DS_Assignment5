Assignment 5 Report
---------------------

# Team Members
- Thierry Suhner
- Karla Ruggaber

# GitHub link to your (forked) repository

https://github.com/thierrysuhner/DS_Assignment5

# Task 1

Note: Some questions require you to take screenshots. In that case, please join the screenshots and indicate in your answer which image refer to which screenshot.

1. What happens when Raft starts? Explain the process of electing a leader in the first
term.

Ans: When Raft starts, firstly all servers start in the Follower state. To elect a leader in the first term, each Follower uses a randomized election timeout. This is not interrupted as there are yet no heartbeats as there is not yet a Leader. The first Follower whose timeout expires increments its current term (e.g. to Term 1), votes for itself and transitions to the Candidate state. The Candidate then sends RequestVote RPCs to all other servers (and resets its election timer). If the Candidate receives votes form the majority of the servers, it wins the election and becomes the Leader. The new Leader then immediately sends out heartbeats (AppendEntries RPCs) to maintain ints authority and prevent new elections.

2. Perform one request on the leader, wait until the leader is committed by all servers. Pause the simulation.
Then perform a new request on the leader. Take a screenshot, stop the leader and then resume the simulation.
Once, there is a new leader, perform a new request and then resume the previous leader. Once, this new request is committed by all servers, pause the simulation and take a screenshot. Explain what happened?

Ans: Initially, the first client request is successfully replicated and committed by the original Leader S1 (Term 1) to a majority of followers. The leader appends it to its log and all servers show the entry in the committed state (solid border). When the simulation is paused for the second request, S1 records this entry in its log. Since the Leader is stopped before it can replicate this entry to a majority, the entry remains uncommitted (dashed border) on S1 and is not seen in the logs of the Followers.
As the Leader is now stopped, the Followers no longer receive heartbeats, so they start a new election, where S2 is elected as the Leader for the new Term. S2 accepts the third request, appends it to its log and replicates it to a majority of Followers, so it is commited, all servers show the entry with solid borders. As the old leader is resumed, it then recognizes that its term is outdated and steps down to a Follower, the new leader S2 brings its log back in sync: The second entry before we paused the first time (uncommitted) will be discarded, it was never replicated. However, the new, committed entry from the new leader is replicated. This leads us to all servers containing the committed entry from the new leader S2 and the uncommitted entry from the old leader S1 being overwritten. This is according to Log Matching and Leader Completeness rules/properties of Raft, which guarantee that the new leader's log (S2) must eventually contain all committed entries. It shows what Raft does to keep logs consistent after a leader "crash".

**Screenshot Task 1, Question 2, Nr. 1**
![task1_q2_1.png](screenshots/task1_q2_1.png)

**Screenshot Task 1, Question 2, Nr. 2**
![task1_q2_2.png](screenshots/task1_q2_2.png)


3. Using the same visualization, stop the current leader and two additional servers. After a few increments, pause the simulation and take a screenshot. Then resume all servers and restart the simulation. After the leader election, pause the simulation and take a screenshot. How do you explain the behavior of the system during the above exercise?

Ans: When we stop the current leader and two additional servers, there are only two running nodes left. Because of the election process of Raft, it is then impossible for any of these two to become the leader. This is because the cluster has an original size of five, so the majority of 5 is 3, which is the amount of votes a node needs to be elected as a Leader. As the two nodes only vote for themselves and get the vote from the other one, they always just have 2/5, so no one of them can get a majority of votes. This results in the two nodes just repeatedly incrementing their current term and starting new elections after their randomized election timeout has run through, as all the elections fail. Then, after resuming all the nodes again the election process can again be successful, where one node gets a majority of votes and becomes the Leader. This will be one of the nodes that were left active before (in our case S1), as it already is in Candidate modes when the other 3 nodes are reactivated, so it sends out RequestVote RPCs immediately to the others who are in Follower state. Also, when the reactivated nodes receive these RPCs, their term is updated to the one of the Candidate (which is much higher now than their previous one).

**Screenshot Task 1, Question 3, Nr. 1**
![task1_q3_1.png](screenshots/task1_q3_1.png)

**Screenshot Task 1, Question 3, Nr. 2**
![task1_q3_2.png](screenshots/task1_q3_2.png)

# Task 2

1. Which server is the leader? Can there be multiple leaders? Justify your answer using the statuses from the different servers.
Ans: 

2. Perform a PUT operation for the key "a" on the leader. Check the status of the different nodes. What changes have occurred and why (if any)?

Ans:

3. Perform an APPEND operation for the key "a" on the leader. Check the status of the different nodes. What changes have occurred and why (if any)?

Ans: 

4. Perform a GET operation for the key "a" on the leader. Check the status of the different nodes. What changes have occured and why (if any)?

Ans:



# Task 3

1. Shut down the server that acts as a leader. Report the status changes that you get from the servers that remain active after shutting down the leader. What is the new leader (if any)?

Ans:

1. Perform a PUT operation for the key "a" on the new leader. Then, restart the previous leader, and indicate the changes in status for the three servers. Indicate the result of a GET operation for the key "a" to the previous leader.

Ans:

3. Has the PUT operation been replicated? Indicate which steps lead to a new election and which ones do not. Justify your answer using the statuses returned by the servers.

Ans:

4. Shut down two servers: first shut down a server that is not the leader, then shut down the leader. Report the status changes of the remaining server and explain what happened.

Ans:

5. Can you perform GET, PUT, or APPEND operations in this system state? Justify your answer.

Ans:

6. Restart the servers and note down the changes in status. Describe what happened.

Ans:

## Network Partition

For the first experiment, create a network partition with 2 servers (including the leader)
on the first partition and the 3 other servers on the other one. Indicate the changes that occur in the status of a server on the first partition and a server on the second partition. Reconnect the partitions and indicate what happens. What are the similarities and differences between the implementation of Raft used by your key/value service (based on the PySyncObj library) and the one shown in the Secret Lives of Data illustration from Task 1? How do you justify the differences?

Ans:

For the second experiment, create a network partition with 3 servers (including the
leader) on the first partition and the 2 other servers on the other one. Indicate the changes that occur in the status of a server on the first partition and a server on the second partition. Reconnect the partitions and indicate what happens. How does the implementation of Raft used by your key/value service (based on the PySyncObj library) compare to the one shown in the Secret Lives of Data illustration from Task 1?

Ans: 


# Task 4

1. Raft uses a leader election algorithm based on randomized timeouts and majority voting, but other leader election algorithms exist. One of them is the bully algorithm, which is described in Section 5.4.1 of the Distributed Systems book by van Steen and Tanenbaum. Imagine you update the PySyncObject library to use the bully algorithm for Raft (as described in the Distributed Systems book) instead of randomized timeouts and majority voting. What would happen in the first network partition from Task 3?

Ans: 

2. Why is it that Raft cannot handle Byzantine failure? Explain in your own words.

Ans: 
