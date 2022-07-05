"""
data example
{
  "name": "차지 스팅거",
  "level": 12,
  "tripod": "222",
  "tripod_level": "555",
  "attributes": {
    "Charge": true,
    "Lance": true,
    "Head": true,
    "Cooldown": 30
  },
  "default_damage": [2997],
  "default_coeff": [18.593],
  "actual_damage": [],
  "actual_coeff": [],
  "delay": [{ "delay": 1.0, "type": "Common" }, { "delay": 1.0, "type": "Charge" }],
  "triggered_buffs": [],
  "rune": { "category": "질풍", "level": "영웅" },
  "jewel": {
    "cooldown": 7,
    "damage": 7
  }
}
"""
class Skill:
    def __init__(self, data, character, **kwargs):
        self.data = data
        self.character = character
    
    def print_skill_info(self):
        print(f"Name: {self.data['name']}")