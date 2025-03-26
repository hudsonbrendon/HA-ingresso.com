![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

# Home Assistant ingresso.com
Custom component to get movie information in your city available at ingresso.com for the home assistant

## Install

### Installation via HACS

Have HACS installed, this will allow you to update easily.

Adding Ingresso to HACS can be using this button:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hudsonbrendon&repository=sensor.ingresso.com&category=integration)

If the button above doesn't work, add `https://github.com/hudsonbrendon/sensor.ingresso.com` as a custom repository of type Integration in HACS.

- Click Install on the `Ingresso` integration.
- Restart the Home Assistant.

### Manual installation

- Copy `ingresso` folder from [latest release](https://github.com/hudsonbrendon/sensor.ingresso.com/releases/latest) to your `<config dir>/custom_components/` directory.
- Restart the Home Assistant.

## Configuration

Adding Ingresso to your Home Assistant instance can be done via the UI using this button:

[![image](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=ingresso)

### Manual Configuration

If the button above doesn't work, you can also perform the following steps manually:

- Navigate to your Home Assistant instance.
- In the sidebar, click Settings.
- From the Setup menu, select: Devices & Services.
- In the lower right corner, click the Add integration button.
- In the list, search and select `Ingresso`.
- Follow the on-screen instructions to complete the setup.

## Get your city id

Access the url below with your UF see your city_id in the list of cities in your state.

https://api-content.ingresso.com/v0/states/YOUR-UF

UFs table:
| UF | Estate |
| --------- |:-----:|
| AC | Acre |
| AL | Alagoas |
| AP | Amapá |
| AM | Amazonas |
| BA | Bahia |
| CE | Ceará |
| DF | Distrito Federal |
| ES | Espírito Santo |
| GO | Goiás |
| MT | Mato Grosso |
| MA | Maranhão |
| MS | Mato Grosso do Sul |
| MG | Minas Gerais |
| PA | Pará |
| PB | Paraíba |
| PR | Paraná |
| PE | Pernambuco |
| PI | Piauí |
| RJ | Rio de Janeiro |
| RN | Rio Grande do Norte |
| RS | Rio Grande do Sul |
| RO | Rondônia |
| RR | Roraima |
| SC | Santa Catarina |
| SP | São Paulo |
| SE | Sergipe |
| TO | Tocantins |

Example:

https://api-content.ingresso.com/v0/states/SP

# Upcoming media card support

To view the movies from the configured cinema, we use the [upcoming-media-card](https://github.com/custom-cards/upcoming-media-card), install via hacs and add the configuration below (Remembering to replace sensor.cinepolis with your configured sensor) in a manual card:

```yaml
type: custom:upcoming-media-card
entity: sensor.cinepolis
title: Cinépolis
```

# Debugging

```yaml
logger:
  default: info
  logs:
    custom_components.ingresso: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
