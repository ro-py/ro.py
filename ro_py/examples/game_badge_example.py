from ro_py import Game

universe_id = 1605107130

print(f"Loading game {universe_id}...")
game = Game(universe_id)
print("Loaded game.")

print(f"Name: {game.name}")

print("Loading badges...")
badges = game.badges
print("Loaded badges.")
print(f"Badge count: {len(badges)}")
for badge in badges:
    badge_tab = " "*(32-len(badge.name))
    badge_stats = badge.statistics
    print(f"{badge.name}{badge_tab}"
          f"Rarity: {badge_stats.win_rate_percentage}% "
          f"Won Yesterday: {badge_stats.past_date_awarded_count} "
          f"Won Ever: {badge_stats.awarded_count}")
