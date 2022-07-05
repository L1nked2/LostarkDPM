BASE_BUFF_TABLE = {
  'Raid_Captain_3': {
    'type': 'stat',
    'body': [('damage_mutiplier', 'movement_speed', lambda x,y: x * max(1, (1+(y-1)*0.45)))]
  }
}