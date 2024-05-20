# inventory-routing-problem

The inventory-routing problem (IRP) integrates two well-studied problems, namely, inventory management and vehicle routing. We consider an inventory routing problem in discrete time where a supplier has to serve a set of customers over a multi period horizon. A capacity constraint for the inventory is given for each customer, and the service cannot cause any stockout situation. A single vehicle with a given capacity is available. The transportation cost is proportional to the distance traveled, whereas the inventory holding cost is proportional to the level of the inventory at the customers and at the supplier. The objective is the minimization of the sum of the inventory and transportation costs. 
The IRP is concerned with the repeated distribution of a single product from a single facility to a set of n customers (i.e., retailers) over a given planning horizon of length T. Customer i consumes the product at a given rate u_i (volume per day) and has the capability to maintain a local inventory of the product up to a maximum of C_i. The inventory at customer i is I_i at time 0. A single vehicle with capacity Q is available for distribution of the product. The objective is to minimize the distribution costs during the planning period without causing stockout at any of the customers.
So, three decisions have to be made:

1. When to serve a customer?
2. How much to deliver to a customer when it is served?
3. Which delivery routes to use?
   
It should be mentioned that IRP differs from traditional vehicle routing problems because it is based on customer’s usage instead of customers’ orders. Moreover, we consider two different replenishment policies that impose rules on the quantity that can be delivered in each delivery to a customer: the order-up-to-level (OU) and the maximum-level (ML) policies. In the OU policy each delivery must fill the inventory to its maximum capacity, effectively linking two of the decisions: once one decides to visit a customer, the quantity to be delivered is simply the difference between its maximum capacity and its current inventory level. In the ML policy, any quantity can be delivered as long as the maximum capacity is not exceeded. The ML policy clearly encompasses the OU one and is more flexible, but also more difficult to solve given the extra set of decision variables.

Problem Description

We consider a distribution network where a product is shipped from a common supplier, denoted by 0, to a set M={1,2,…,n} of customers over a time horizon of H periods. At each discrete time t∈T={1,…,H} a quantity r_0t is produced at the supplier, and a quantity r_it is consumed at customer i∈M. Starting inventory level B_0 at the supplier is given. Each customer i has a maximum capacity U_i and a given starting inventory I_i0≤U_i. If customer i is visited at time t, then the quantity x_it shipped to the customer depends on the replenishment policy. We consider two different replenishment policies:

	In the order-up-to-level (OU) policy, if customer i is served at time t, the quantity x_it is the difference between U_i and the current inventory level I_it of i.
	In the maximum-level (ML) policy, the quantity x_it can take any nonnegative value that does not violate the capacity U_i . 

 
The inventory holding cost is charged both at the supplier and at the customers. Inventory holding costs at the customers are taken into account in real inventory routing problems whenever the supplier agrees with the customers to require the payment of the products only when the products are sold by the customers. This is one of the incentives used by suppliers to move toward inventory routing systems.
Denoting by h_0 the unit inventory cost at the supplier and by B_t the inventory level at the supplier at time t, the total inventory cost at the supplier is ∑_(t∈T')▒〖h_0 B_t 〗 where T^'=T∪{H+1}. The time H+1 is included in the computation of the inventory cost to take into account the consequences of the operations performed at time H. Denoting by h_i  the unit inventory cost of customer i, the total inventory cost over the time horizon is ∑_(t∈T')▒〖h_i I_it 〗.

Shipments from the supplier to the customers can be performed at each time t by a vehicle of capacity C. The transportation cost c_ij from i to j is known, and c_ij=c_ji. Therefore, letting y_ij^t be a binary variable equal to 1 if j immediately follows I in the route traveled at time t and 0 otherwise, the total transportation cost is ∑_(i∈M')▒∑_(j∈M')▒∑_(t∈T)▒c_ij  y_ij^t where M^'=M∪{0}.
The objective of the considered IRP is to determine a feasible solution with minimum total cost. If the initial inventory of each customer is 0 and H = 1, the problem becomes a TSP and, thus, is NP-hard. To be feasible, a solution should not have any stockout at the supplier and at the customers (i.e., B_t≥0 and I_it≥0), the level of the inventory of each customer i should not be greater than its maximum level U_i , and the total quantity delivered at any given time should not exceed the vehicle capacity C.

