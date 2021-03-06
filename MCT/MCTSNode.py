import numpy as np
import copy

class BattleshipsMonteCarloTreeSearchNode():

    def __init__(self, state, action=None, parent=None):
        self.state = copy.deepcopy(state)
        self.action = action
        self.parent = parent
        self.children = []
        self._number_of_visits = 0.
        self._results = 0.
        self._untried_actions = self.get_actions()

    def get_actions(self):
        actions = []
        for index, x in np.ndenumerate(self.state.board):
            if x == 0:
                actions.append(index)
        
        return actions
        

    def q(self):
        return self._results


    def n(self):
        return self._number_of_visits

    def uct(self):
        return self._results / self._number_of_visits

    def best_child(self, c_param=0.):
        best_child = self.children[0]

        for child in self.children:
            if child.uct() > best_child.uct():
                best_child = child

        return best_child

    def expand(self):
        rand_index = np.random.randint(len(self._untried_actions))
        action = self._untried_actions.pop(rand_index)
        # I think there is an error below: think about what next_state is meant to be and what move() returns
        next_state, _ = self.state.move(action) 
        child_node = BattleshipsMonteCarloTreeSearchNode(
            next_state, action=action, parent=self
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def is_fully_expanded(self):
        # This logic seems fine: returns true if there are no untried actions left for the node.
        return not self._untried_actions

    def rollout(self, move_limit=10):
        current_rollout_state = self.state
        hit_count = 0.
        guess_count = 0.
        while guess_count < move_limit:
            guess_count += 1
            if current_rollout_state.is_game_over():
                break
            possible_moves = self.get_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state, result = current_rollout_state.move(action)
            if result == True:
                hit_count += 1
            
        return hit_count / guess_count
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results += result
        if self.parent:
            self.parent.backpropagate(result)