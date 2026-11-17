<p align="center">
  <img src="custom_components/ingresso/brand/logo@2x.png" alt="Ingresso.com" height="128">
</p>

# Ingresso.com Integration for Home Assistant

[![Tests](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/tests.yml/badge.svg)](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/tests.yml)
[![Hassfest](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/hassfest.yml/badge.svg)](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/hassfest.yml)
[![HACS](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/validate.yml/badge.svg)](https://github.com/hudsonbrendon/HA-ingresso.com/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/hudsonbrendon/HA-ingresso.com?sort=semver)](https://github.com/hudsonbrendon/HA-ingresso.com/releases)
[![Downloads](https://img.shields.io/github/downloads/hudsonbrendon/HA-ingresso.com/total)](https://github.com/hudsonbrendon/HA-ingresso.com/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.2.4%2B-18BCF2?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/hudsonbrendon/HA-ingresso.com)](LICENSE)

This custom integration allows you to track movie listings from [Ingresso.com](https://www.ingresso.com/) in your Home Assistant instance. Keep up with the latest movies showing in theaters near you!

## Features

- Show current movie listings for a selected theater
- Display movie details including title, synopsis, director, cast, and more
- Configurable via the Home Assistant UI
- Search by city and theater
- Movie posters display in Lovelace UI

## Installation

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hudsonbrendon&repository=HA-ingresso.com&category=integration)
[![Add integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ingresso)

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Add this repository to HACS as a custom repository:
   - Go to HACS > Integrations
   - Click the three dots in the upper right corner and select "Custom repositories"
   - Enter `https://github.com/hudsonbrendon/HA-ingresso.com` in the repository field
   - Select "Integration" as the category
   - Click "Add"
3. Search for "Ingresso.com" in the HACS store and install it
4. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/hudsonbrendon/HA-ingresso.com)
2. Unpack the release and copy the `custom_components/ingresso` directory into the `custom_components` directory of your Home Assistant installation
3. Restart Home Assistant

## Configuration

1. Go to Home Assistant Settings > Devices & Services
2. Click the "+ Add Integration" button
3. Search for "Ingresso.com" and select it
4. Follow the configuration steps:
   - Select your city
   - Select your preferred theater
5. The integration will start fetching movie listings for your selected theater

## Lovelace Card Examples

You can display the movie listings using various Lovelace cards. Here's an example using the [upcoming-media-card](https://github.com/custom-cards/upcoming-media-card):

```yaml
type: custom:upcoming-media-card
entity: sensor.my_sensor
title: Movies
max: 10
```

## Updating

### HACS

1. Open HACS > Integrations
2. Find the Ingresso.com integration and click on it
3. Click "Update" if an update is available
4. Restart Home Assistant

### Manual

1. Download the latest release
2. Replace the contents of the `custom_components/ingresso` directory
3. Restart Home Assistant

## Support

If you have any issues or feature requests, please [open an issue](https://github.com/hudsonbrendon/HA-ingresso.com/issues) on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to [Ingresso.com](https://www.ingresso.com/) for providing the movie data
- Thanks to the Home Assistant community for their support and contributions
