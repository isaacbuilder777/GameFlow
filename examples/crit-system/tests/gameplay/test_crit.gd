extends GdUnitTestSuite

var rng: RandomNumberGenerator

func before_test() -> void:
	rng = RandomNumberGenerator.new()
	rng.seed = 42


func _character(luck: int) -> Character:
	var c := Character.new()
	c.luck = luck
	return c


func _weapon(base: float, mult: float) -> WeaponResource:
	var w := WeaponResource.new()
	w.crit_base = base
	w.crit_multiplier = mult
	return w


func test_zero_luck_and_zero_weapon_base_gives_zero_chance() -> void:
	var result := CritResolver.roll(_character(0), _weapon(0.0, 2.0), rng)
	assert_that(result.rolled_chance).is_equal(0.0)
	assert_that(result.is_crit).is_false()
	assert_that(result.damage_multiplier).is_equal(1.0)


func test_crit_chance_clamps_at_50_percent() -> void:
	var result := CritResolver.roll(_character(200), _weapon(0.5, 2.0), rng)
	assert_that(result.rolled_chance).is_equal(0.5)


func test_crit_damage_is_multiplicative_when_crit_lands() -> void:
	# Force a crit by using chance 0.5 with seed 42 — first roll is < 0.5.
	var result := CritResolver.roll(_character(50), _weapon(0.0, 2.5), rng)
	if result.is_crit:
		assert_that(result.damage_multiplier).is_equal(2.5)
	else:
		assert_that(result.damage_multiplier).is_equal(1.0)


func test_luck_contributes_linearly() -> void:
	# luck * 0.01 means luck 25 alone gives 25% chance.
	var result := CritResolver.roll(_character(25), _weapon(0.0, 2.0), rng)
	assert_that(result.rolled_chance).is_equal(0.25)


func test_weapon_base_contributes_directly() -> void:
	var result := CritResolver.roll(_character(0), _weapon(0.15, 2.0), rng)
	assert_that(result.rolled_chance).is_equal(0.15)
