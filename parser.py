import re

def load_replay_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    players = re.findall(r"<PlayerRecord>.*?</PlayerRecord>", content, re.DOTALL)
    return players[0], players[1]

def parse_new_unit_data(round_data):
    unit_map = {}
    for unit in re.findall(r"<NewUnitData>.*?</NewUnitData>", round_data, re.DOTALL):
        unit_id = int(re.search(r"<id>(\d+)</id>", unit).group(1))
        unit_index = int(re.search(r"<Index>(\d+)</Index>", unit).group(1))
        x = int(re.search(r"<x>(-?\d+)</x>", unit).group(1))
        y = int(re.search(r"<y>(-?\d+)</y>", unit).group(1))
        unit_map[unit_index] = {"unit_id": unit_id, "x": x, "y": y}
    return unit_map

def extract_round(round_number, player_data):
    match = re.search(
        rf"<PlayerRoundRecord>\s*<round>{round_number}</round>.*?</PlayerRoundRecord>",
        player_data,
        re.DOTALL
    )
    if not match:
        return {}, ""
    round_data = match.group(0)
    return parse_new_unit_data(round_data), round_data

def apply_actions_with_gift_detection(unit_map, round_data):
    pending_buys = {}

    for match in re.findall(r"<MatchActionData .*?</MatchActionData>", round_data, re.DOTALL):
        if 'PAD_MoveUnit' in match:
            for move in re.findall(r"<MoveUnitData>.*?</MoveUnitData>", match, re.DOTALL):
                unit_id = int(re.search(r"<unitID>(\d+)</unitID>", move).group(1))
                unit_index = int(re.search(r"<unitIndex>(\d+)</unitIndex>", move).group(1))
                x = int(re.search(r"<x>(-?\d+)</x>", move).group(1))
                y = int(re.search(r"<y>(-?\d+)</y>", move).group(1))
                px = int(re.search(r"<positionRecord>\s*<x>(-?\d+)</x>", move).group(1))
                py = int(re.search(r"<positionRecord>.*?<y>(-?\d+)</y>", move, re.DOTALL).group(1))

                if (px, py) in pending_buys:
                    unit_map[unit_index] = {"unit_id": pending_buys[(px, py)]["unit_id"], "x": x, "y": y}
                    del pending_buys[(px, py)]
                elif unit_index in unit_map:
                    unit_map[unit_index]["x"] = x
                    unit_map[unit_index]["y"] = y
                else:
                    unit_map[unit_index] = {"unit_id": unit_id, "x": x, "y": y}

        elif 'PAD_BuyUnit' in match:
            unit_id = int(re.search(r"<UID>(\d+)</UID>", match).group(1))
            x = int(re.search(r"<x>(-?\d+)</x>", match).group(1))
            y = int(re.search(r"<y>(-?\d+)</y>", match).group(1))
            pending_buys[(x, y)] = {"unit_id": unit_id}

        elif 'PAD_ReleaseCommanderSkill' in match and '<SkillIndex>0</SkillIndex>' in match:
            match_index = re.search(r"<UnitIndex>(\d+)</UnitIndex>", match)
            if match_index:
                sold_index = int(match_index.group(1))
                unit_map.pop(sold_index, None)

    for (x, y), data in pending_buys.items():
        unit_map[f"?_{x}_{y}"] = {"unit_id": data["unit_id"], "x": x, "y": y}

    return unit_map

def reconstruct_all_rounds(player1_data, player2_data):
    frames = []
    
    import re
    round_nums = sorted(set(map(int, re.findall(r"<PlayerRoundRecord>\s*<round>(\d+)</round>", player1_data))))
    for rnd in round_nums:
    
        p1_units, p1_round = extract_round(rnd, player1_data)
        p2_units, p2_round = extract_round(rnd, player2_data)
        if not p1_round or not p2_round:
            break
        p1_final = apply_actions_with_gift_detection(p1_units.copy(), p1_round)
        p2_final = apply_actions_with_gift_detection(p2_units.copy(), p2_round)
        frames.append((rnd, p1_final, p2_final))
    return frames
