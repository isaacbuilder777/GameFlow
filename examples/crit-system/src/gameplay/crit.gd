class_name CritResolver
extends RefCounted

signal crit_rolled(result: CritResult)

const MAX_CRIT_CHANCE := 0.5

static func roll(character: Character, weapon: WeaponResource, rng: RandomNumberGenerator) -> CritResult:
	var chance := clampf(weapon.crit_base + character.luck * 0.01, 0.0, MAX_CRIT_CHANCE)
	var is_crit := rng.randf() < chance
	var multiplier := weapon.crit_multiplier if is_crit else 1.0
	return CritResult.new(is_crit, multiplier, chance)


class CritResult extends RefCounted:
	var is_crit: bool
	var damage_multiplier: float
	var rolled_chance: float

	func _init(is_crit_: bool, damage_multiplier_: float, rolled_chance_: float) -> void:
		is_crit = is_crit_
		damage_multiplier = damage_multiplier_
		rolled_chance = rolled_chance_
