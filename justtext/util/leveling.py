from ..state import get_state

class LevelCalculator:
    def __init__(self, base_xp=100, exponent=1.5):
        self.base_xp = base_xp
        self.exponent = exponent
        self.state = get_state()
        self.state.total_xp = self.state.mining_xp + self.state.combat_xp

    def calculate_level(self, xp):
        level = 1
        while xp >= self.get_xp_required(level):
            level += 1

        return int(level - 1)
    
    def get_xp_required(self, level):
        return int(self.base_xp * (level**self.exponent))
    
    def get_xp_for_next_level(self, current_xp):
        return int(self.get_xp_required(self.calculate_level(current_xp) + 1) - current_xp)