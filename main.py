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
        guild_obj = None
        if players[name]["guild"]:
            guild_obj = Guild.objects.get_or_create(
                name=players[name]["guild"]["name"],
                description=players[name]["guild"]["description"]
            )[0]
        else:
            guild_obj = Guild.objects.get_or_create(
                name="unknown",
                description=""
            )[0]
        Player.objects.create(
            nickname=name,
            email=players[name]["email"],
            bio=players[name]["bio"],
            race=Race.objects.get_or_create(
                name=players[name]["race"]["name"],
                description=players[name]["race"]["description"],
            )[0],
            guild=guild_obj
        )
        for skill in players[name]["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill["name"],
                bonus=skill["bonus"],
                race=Race.objects.get_or_create(
                    name=players[name]["race"]["name"],
                    description=players[name]["race"]["description"],
                )[0]
            )
        Guild.objects.filter(
            name="unknown"
        ).delete()


if __name__ == "__main__":
    main()
