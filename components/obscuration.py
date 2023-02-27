def obscure_hp(current_hp: int, max_hp: int):
    hp_percent = current_hp / max_hp
    if hp_percent >= 0.8:
        return "Fine"
    elif 0.8 > hp_percent > 0.5:
        return "Injured"
    elif 0.5 >= hp_percent >= 0.1:
        return "Wounded"
    elif 0.1 > hp_percent:
        return "Danger!"
    elif hp_percent == 0:
        return "Dead"
