#  2PC protocol implementation

Two phase commit protocol between one Transaction coordinator and two participant nodes.

# Process
The TC first sends a ‘prepare’ message to all the participant nodes in the system to which the participant nodes reply with yes or no. If the participant nodes do not receive the message within the timeout period or if the participant node is not ready, it will reply no and the transaction will be aborted. If the TC receive ‘yes’ votes from all the participant nodes, it sends ‘commit’ message to all the participants. The participants commit the transaction and will send the final acknowledgement to the TC. The TC closes the connection after receiving all ack messages from the nodes.

## Running the Program

1. Open a terminal in the all the machines.
2. Execute the required programs.
   $python coordinator.py \
   or \
   $python participant#.py \
3. The TC and participants send and recieve messages and finally decide whether to commit or abort a transaction.


