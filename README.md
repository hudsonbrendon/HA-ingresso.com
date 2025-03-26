# Ingresso.com Integration for Home Assistant

This custom integration allows you to track movie listings from [Ingresso.com](https://www.ingresso.com/) in your Home Assistant instance. Keep up with the latest movies showing in theaters near you!

## Features

- Show current movie listings for a selected theater
- Display movie details including title, synopsis, director, cast, and more
- Configurable via the Home Assistant UI
- Search by city and theater
- Movie posters display in Lovelace UI

## Installation

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
