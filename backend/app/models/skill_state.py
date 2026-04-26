class SkillState:
    def __init__(self, clusters):
        self.state = {}

        for cluster_name, skills, score in clusters:
            self.state[cluster_name] = {
                "skills": skills,
                "questions_asked": [],
                "answers": [],
                "level": None,
                "score": 0
            }

    def add_interaction(self, cluster, question, answer):
        self.state[cluster]["questions_asked"].append(question)
        self.state[cluster]["answers"].append(answer)

    def update_score(self, cluster, score, level):
        self.state[cluster]["score"] = score
        self.state[cluster]["level"] = level

    def get_cluster_state(self, cluster):
        return self.state[cluster]