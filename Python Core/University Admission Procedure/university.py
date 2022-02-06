class Applicant:
    def __init__(self, name, last_name, exams: list, special, priorities: list):
        self.full_name = f'{name} {last_name}'
        self.exams = exams
        self.special = special
        self.priorities = priorities
        self.score = 0

    def set_score(self, exams: list[int]):
        sum_ = 0
        for i in exams:
            sum_ += self.exams[i]
        self.score = sum_ / len(exams)

    def __gt__(self, other: 'Applicant') -> bool:
        if max(self.score, self.special) > max(other.score, other.special):
            return True
        elif max(self.score, self.special) == max(other.score, other.special) and self.full_name < other.full_name:
            return True
        return False

    def __repr__(self):
        return f'{self.full_name} {max(self.score, self.special)}'


class Applicants:
    def __init__(self):
        self.list = []

    def append(self, applicant: Applicant):
        self.list.append(applicant)

    def get_best_applicant(self, department: str, priority_num: int) -> Applicant or None:
        for applicant in self.list:
            if applicant.priorities[priority_num] == department:
                best_applicant = applicant
                break
        else:
            return None
        for applicant in self.list:
            applicant.set_score(department_and_exams[department])
            if applicant.priorities[priority_num] == department:
                if applicant > best_applicant:
                    best_applicant = applicant
        self.list.remove(best_applicant)
        return best_applicant

    def get_best_applicants(self, num, department, priority_num):
        result = []
        for i in range(num):
            applicant = self.get_best_applicant(department, priority_num)
            if not applicant:
                return result
            result.append(applicant)
        return result


def sort_applicants_list(applicants: list):
    for i in range(len(applicants) - 1):
        for j in range(len(applicants) - i - 1):
            if applicants[j] < applicants[j + 1]:
                applicants[j], applicants[j + 1] = applicants[j + 1], applicants[j]


if __name__ == '__main__':
    applicants_ = Applicants()
    with open('applicants.txt', 'r') as file:  # reading data about applicant from file
        lines = file.readlines()

    for line in lines:  # Parsing data from file, and creating Applicant objects
        name_, last_name_, *exams_, special_, dep1, dep2, dep3 = line.split()
        # exams_ : [physics, chemistry, math, computer science]
        priorities_ = [dep1, dep2, dep3]
        applicants_.append(Applicant(name_, last_name_, [float(ex) for ex in exams_], float(special_), priorities_))

    department_and_exams = {'Biotech': [0, 1], 'Chemistry': [1], 'Engineering': [2, 3],
                            'Mathematics': [2], 'Physics': [0, 2]}
    departments_and_applicants = {}

    N = int(input())
    for priority_ in range(3):  # Data processing
        for dep in department_and_exams.keys():
            number = N - len(departments_and_applicants.get(dep, ''))
            departments_and_applicants[dep] = departments_and_applicants.get(dep, []) + \
                applicants_.get_best_applicants(number, dep, priority_)
    for dep in departments_and_applicants:
        sort_applicants_list(departments_and_applicants[dep])

    for dep in departments_and_applicants:  # writing processed information to files
        with open(f'{dep.lower()}.txt', 'w') as file:
            print(*departments_and_applicants[dep], file=file, sep='\n', end='\n\n')
