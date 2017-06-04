#minimax with dispatch function
def mini(state):

	childs = succesor(state)
	
	best = 9999999
	mini_node = None
	for child in childs:
		if (value = minimax_rec(child, "max")) < best :
			best = value
			mini_node = child
	return mini_node

def maxi(state):

	childs = succesor(state)
	
	best = -9999999
	maxi_node = None
	for child in childs:
		if (value = minimax_rec(child, "min")) > best :
			best = value
			maxi_node = child
	return maxi_node


def minimax_rec(state, agent):

	if state is terminal:
		return eval_value(state), state

	if agent is "min":
		return mini(state)
	if agent is "max":
		return maxi(state)

# Without dispatch function
# def  minimax_rec(node, agent):

# 	childs = succesor(node)

#	if childs is None:
#		return eval_value(node)
#
#	if agent is "min":
#		mini = 9999999
#		mini_node = None
#		for child in childs:
#			if (value = minimax(child, "max")) < mini :
#				mini = value
#				mini_node = child
#		return mini_node
#
#	if agent is "max":
#		maxi = -9999999
#		maxi_node = None
#		for child in childs:
#			if (value = minimax(child, "mini")) > maxi :
#				maxi = value
#				maxi_node = child
#		return maxi_node


#-------------Alpha-Beta-Prunning------------------#

def alpha_f(state, alpha, beta):

	childs = succesor(state)
	
	for child in childs:
		value = alpha_beta(child, "min")
		if value >= beta:
			return value, state
		if value > alpha
			alpha = value
	return alpha, state

def beta_f(state, alpha, beta):

	childs = succesor(state)
	
	for child in childs:
		value = alpha_beta(child, "min")
		if value <= alpha:
			return value, state
		if value < beta
			beta = value
	return beta, state

#Function calling alpha_beta should initialize alpha-beta
#	alpha = -999999
#	beta  = +999999

def alpha_beta(state, agent, alpha, beta:

	if state is terminal:
		return eval_value(state), state

	if agent is "min":
		return beta_f(state, alpha, beta)
	if agent is "max":
		return alpha_f(state, alpha, beta)


