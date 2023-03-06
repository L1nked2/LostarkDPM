# LostarkDPM
------------
## 프로젝트 목적
* 스킬별 딜 비중을 구해내어 어떤 스킬이 가치가 더 높은지 정량적인 수치 제공, 멸화 투자 우선순위 제공
* 여러 상황과 조합식을 제공해 어떤 각인과 세팅이 유리한지 결과 제공
* 총 DPS, n초 DPS 등 여러 지표를 구해내어 직업 별 특성을 찾아내어 데미지 딜링 전략을 제시하고, 리스크에 맞는 지표를 가지고 있는지 확인

## 사용방법
---------
### Standard
python3를 설치 후 root 디렉토리에서 main.py를 실행합니다.
```
$ python3 main.py
```
result.csv와 result.txt를 확인하여 정보를 확인합니다.

세구빛은 적용되어있지 않으므로 1.15를 곱해주어야 실제 dps를 얻어낼 수 있습니다.

---------------------
### Advanced
* root 디렉토리에서 main_lk.py를 통해 특정 직업만 실행하는 것도 가능합니다.
* 원하는 캐릭터 정보 사용시 character_path에 원하는 캐릭터 세팅 json파일의 path를 입력합니다.
> main_lk.py
``` python
    character_path = './db/characters/character_scouter_evolutionary_legacy.json'
    character_configs = import_character(character_path)
```
-------
* 원하는 스킬 셋 사용시 character파일에서 skill_set 필드에 원하는 스킬셋 json을 입력합니다.
> character_scouter_evolutionary_legacy.json
``` json
{
  "character_settings": [
    {
      "class_name": "scouter",
      "upgrade": 25,
      "crit": 600,
      "specialization": 1600,
      "swiftness": 0,
      "engravings": ["Grudge_3", "Barricade_3", "Raid_Captain_3", "Cursed_Doll_3", "Keen_Blunt_Weapon_3", "Evolutionary_Legacy_1"],
      "options": ["Synergy_Crit_A", "Synergy_Damage_A", "갈망_3"],
      "artifact_set": ["환각_6_3"],
      "skill_set": "./db/skills/scouter_evolutionary_legacy_c1.json"
    }
  ]
}
```
----------
* 원하는 스킬 사이클 사용시 skill파일에서 main_cycle 필드에 우선 순위대로 스킬 사이클을 입력합니다.
* 각 서브사이클이 우선순위대로 사용되며, 서브사이클 내의 모든 스킬이 사용가능하다고 판단하면 사용합니다. 스킬 딜레이로 인해 쿨이 돌아오는 것도 감안하여 판단합니다.
> striker_death_blow.json
``` json
"class_name": "striker",
  "policy": {
    "mode": "fixed",
    "main_cycle": [
      ["폭쇄진", "번개의 속삭임", "폭쇄진_대폭발", "붕천퇴", "뇌호격"],
      ["격호각", "월섬각", "호왕출현"],
      ["붕천퇴", "운룡각", "격호각"],
      ["진천각"]
    ]
  },
```
-----------
* 스킬의 보석, 룬을 변경하는 것도 가능합니다. 각 skill의 jewel과 rune 필드에 원하는 정보를 입력하면 됩니다.
* 보석은 레벨 기준이며, 룬은 "이름_등급" 의 형태를 따릅니다.
> striker_death_blow.json
``` json
{
      "name": "뇌호격",
      "default_damage": 3809,
      "default_coefficient": 23.6,
      "base_damage_multiplier": 5.236,
      "skill_type": "Charge",
      "identity_type": "Esoteric",
      "cooldown": 18,
      "common_delay": 1.13,
      "type_specific_delay": 0.98,
      "jewel_cooldown_level": 10,
      "jewel_damage_level": 10,
      "head_attack": false,
      "back_attack": true,
      "triggered_actions": [],
      "key_strokes" : 1,
      "mana_cost": 0,
      "rune": "질풍_전설"
    },
```
------------
* 시뮬레이션 로그 확인 및 최대 시간 지정도 가능합니다. DpmSimulator Class에 원하는 argument를 넘겨주면 됩니다.
> main_lk.py
``` python
    # max_tick에 최대 틱수(기본적으로 100tick = 1s) 입력
    # verbose=1 또는 2로 지정시 추가적인 로그 확인 가능
    # 출력된 데미지는 방어력 적용 전으로, 0.4를 곱하면 실제 데미지
    for character_config in character_configs:
      character_dict = character_config.build_dict()
      simulator = DpmSimulator(character_dict, max_tick=9000, verbose=1)
```
------------
* 이외 다른 필드를 변경하는 것도 가능하나 의도치 않은 동작을 보일 수 있으므로 추천드리지 않습니다.

## 추후 계획
* 최적 각인, 유물셋, 보석, 스킬 사이클 발굴
* 사이클 인식 및 지딜, 폭딜 구분하여 딜링 난이도 정량화
