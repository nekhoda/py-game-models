import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    Race.objects.all().delete()
    Skill.objects.all().delete()
    Guild.objects.all().delete()
    Player.objects.all().delete()
    with open("players.json", "r") as file:
        players = json.load(file)
    for name in players:
        players_race = Race.objects.get_or_create(
                name=players[name]["race"]["name"],
                description=players[name]["race"]["description"],
            )[0]
        Player.objects.create(
            nickname=name,
            email=players[name]["email"],
            bio=players[name]["bio"],
            race=players_race,
            guild=Guild.objects.get_or_create(
                name=players[name]["guild"]["name"] if players[name]["guild"] else "unknown",
                description=players[name]["guild"]["description"] if players[name]["guild"] else ""
            )[0]
        )
        for skill in players[name]["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                bonus=skill["bonus"],
                race=players_race
            )
        Guild.objects.filter(
            name="unknown"
        ).delete()


if __name__ == "__main__":
    main()
