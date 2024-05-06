from copy import deepcopy

class Solver:
    def __init__(self, num_vars, num_clauses) -> None:
        self.num_vars = num_vars
        self.num_clauses = num_clauses

    def solve(self, formula):
        assignments = []
        return self.recursion(formula, assignments)
        
    def recursion(self, formula, assignments):
        if len(formula) == 0:
            return True, assignments
        else:
            pure_literals = self.find_pure_literals(formula)
            for pure in pure_literals:
                formula, assignments = self.remove_pure_literal(formula, pure, assignments)
            if len(formula) == 0:
                return True, assignments
            for clause in formula:
                if len(clause) == 1:
                    formula, assignments = self.remove_unit_clause(formula, clause[0], assignments)
                    if not formula:
                        return False, None
                    elif len(formula) == 0:
                        return True, assignments
                    return self.recursion(formula, assignments)
            
            literal = formula[0][0]
            formula_copy = deepcopy(formula)
            assignments_til_now = deepcopy(assignments)
            formula_copy, assignments_copy = self.remove_unit_clause(formula_copy, literal, assignments)
            success, assignments_ret = self.recursion(formula_copy, assignments_copy)
            if success:
                return success, assignments_ret
            else:
                formula_copy2 = deepcopy(formula)
                formula_copy2, assignments_copy2 = self.remove_unit_clause(formula_copy2, -literal, assignments_til_now)
                return self.recursion(formula_copy2, assignments_copy2)

    def find_pure_literals(self, formula):
        literals = {}
        for clause in formula:
            for literal in clause:
                if literal in literals:
                    literals[literal] += 1
                else:
                    literals[literal] = 1
        pure_literals = []
        for literal in literals:
            if -literal not in literals:
                pure_literals.append(literal)
        return pure_literals
    
    def remove_pure_literal(self, formula, pure, assignments):
        assignments.append(pure)
        copy_formula = formula.copy()
        for clause in copy_formula:
            if pure in clause:
                formula.remove(clause)
        return formula, assignments
    
    def remove_unit_clause(self, formula, unit, assignments):
        assignments.append(unit)
        copy_formula = formula.copy()
        for clause in copy_formula:
            if unit in clause:
                formula.remove(clause)
            if -unit in clause:
                clause.remove(-unit)
                if len(clause) == 0:
                    return False, assignments
        return formula, assignments

def read_input(path):
    num_vars = 0
    num_clauses = 0
    clauses = []

    with open(path, 'r') as file:
        for line in file:
            if line.startswith('c'):  # Skip comments
                continue
            elif line.startswith('p'):  # Problem line
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
            else:  # Clause line
                clause = [int(x) for x in line.split() if x != '0']
                clauses.append(clause)
            
    return num_vars, num_clauses, clauses

def write_output(path, solution):
    with open(path, 'w') as file:
        file.write(' '.join([str(x) for x in solution]))

def check_solution(assignments, path_to_solution):
    with open(path_to_solution, 'r') as file:
        solution = [int(x) for x in file.readline().split()]
    sorted_assignments = sorted(assignments)
    sorted_solution = sorted(solution)
    print(sorted_assignments)
    print(sorted_solution)
    return sorted_assignments == sorted_solution

if __name__ == "__main__":
    filename = "sudoku_mini"
    num_vars, num_clauses, formula = read_input("..\\examples\\"+filename+".txt")
    solver = Solver(num_vars, num_clauses)
    success, assignments = solver.solve(formula)
    print(success)
    # print(assignments)
    # print(check_solution(assignments, "..\\examples\\"+filename+"_solution.txt"))
    write_output("..\\examples\\"+filename+"_output.txt", assignments)