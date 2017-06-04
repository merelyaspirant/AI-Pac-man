#include <stdio.h>
struct Node
{
	char name[5];
	struct Node *lchild, *rchild;
	float value;
	int type;
};

float alpha_beta(struct Node *node, float alpha,
		float beta, unsigned int depth, int *action);

float max(struct Node *node, float alpha,
	float beta, unsigned int depth, int *action)
{
	struct Node *child;
	float value;
	float best_for_this_node;
	int act = 0; //act = 0 => LEFT && act = 1 => RIGHT
	
	best_for_this_node = -999999.0;
	for (act = 0; act < 2; act ++) {
		if (act == 0) {
			if (!(child = node->lchild)) {
//				printf (" node %s, chid %s\n", node->name, child->name);
				continue;
			}
		} else {
			if (!(child = node->rchild)) {
//				printf (" right node %s, chid %s\n", node->name, child->name);
				continue;
			}
		}

		value = alpha_beta(child, alpha, beta, depth, action);
		if (value > beta) {
			*action = act;
			return value;
		}
		if (value > best_for_this_node) {
			*action = act;
			 best_for_this_node = value;
		}
		if (value > alpha) {
			alpha = value;
		}
	}
	
	return best_for_this_node;
}
		
float min(struct Node *node, float alpha,
	float beta, unsigned int depth, int *action)
{
	struct Node *child;
	float value;
	float best_for_this_node;
	int act = 0; //act = 0 => LEFT && act = 1 => RIGHT
	
	best_for_this_node = +999999.0;
	for (act = 0; act < 2; act++) {

		if (act == 0) {
			if (!(child = node->lchild))
				continue;
		} else {
			if (!(child = node->rchild))
				continue;
		}
		value = alpha_beta(child, alpha, beta, depth, action);
		if (!strcmp("b2", node->name))
			printf ("value %f alpha %f \n", value, alpha);
		
		if (value < alpha) {
			*action = act;
			return value;
		}
		if (value < best_for_this_node) {
			*action = act;
			best_for_this_node = value;
		}
		if (value < beta) {
			beta = value;
		}

	}
	return best_for_this_node;
}

float alpha_beta(struct Node *node, float alpha,
		float beta, unsigned int depth, int *action)
{
	depth -= 1;

	printf ("node explored alpha beta %s %p %p  %f %f \n", node->name, node->lchild, node->rchild, alpha, beta);
	if ((!node->lchild && !node->rchild) || depth < 0)
		return node->value;

	if (!node->type) //0 is min, 1 is max
		return min(node, alpha, beta, depth, action);
	else
		return max(node, alpha, beta, depth, action);
}
struct Node nodes[] = {
{"a", &nodes[1], &nodes[2], 0, 1},
{"b1", &nodes[3], NULL, 0, 0},
{"b2", &nodes[5], &nodes[6], 0, 0},
{"cx", &nodes[4], NULL, 0, 1},
{"dx", NULL, NULL, 4.01, 0},
{"c3", &nodes[7], &nodes[8], 0, 1},
{"c4", &nodes[9], &nodes[10], 0, 1},
{"d5", NULL, NULL, 4, 0},
{"d6", NULL, NULL, -7, 0},
{"d7", NULL, NULL, 0, 0},
{"d8", NULL, NULL, 5, 0}
}; 

int main()
{
	float alpha = -999999.0;
	float beta  = +999999.0;
	unsigned int depth = 1;
	int action = -1;

	printf ("value %f action %d\n",
		alpha_beta(nodes, alpha, beta, depth, &action), action);
	return 0;
}
