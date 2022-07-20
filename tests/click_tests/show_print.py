import click

@click.command()
@click.argument('location')
def main(location):
    weather = current_weather(location)
    click.echo("echo")
    print(f"The weather in {location} right now: {weather}.")


def current_weather(location):
    return "Sunny"


if __name__ == '__main__':
    main()

