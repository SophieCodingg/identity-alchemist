# Identity Alchemist

![Identity Alchemist Logo](logo.svg)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Data Security](#data-security)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

Identity Alchemist is a sophisticated tool designed for generating, managing, and analyzing synthetic personal data. This system is invaluable for developers, researchers, and businesses that require realistic fake identities for testing, simulations, and data analysis, especially in scenarios where using real personal information is restricted due to privacy regulations.

## Features

- **Identity Generation**: Create realistic synthetic identities with various attributes including name, gender, age, nationality, and more.
- **Machine Learning Integration**: Utilizes a Random Forest classifier to predict a person's country based on other characteristics.
- **Data Validation**: Ensures the integrity and realism of generated data through various validation checks.
- **Encryption and Decryption**: Secures sensitive identity information using strong encryption methods.
- **Data Analysis**: Provides tools for analyzing generated identities, including age distribution, gender ratios, and common names.
- **Import/Export Functionality**: Supports data import and export in multiple formats (CSV, JSON, SQL).
- **Synthetic ID Card Generation**: Creates simulated identification cards based on the generated identity information. (Future update)

## Requirements

- Python 3.x
- Required libraries:
  - numpy
  - scikit-learn
  - Faker
  - cryptography

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/identity-alchemist.git
   cd identity-alchemist
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main program file:

```
python identity_alchemist.py
```

Follow the on-screen menu to:
1. Generate synthetic identities
2. Train the machine learning model
3. Generate enhanced identities
4. Save identities to a file
5. Generate synthetic ID cards
6. Validate identities
7. Encrypt/decrypt identities
8. Analyze identity data
9. Export/import identities

## System Architecture

Identity Alchemist consists of several key components:

- `IdentityGenerator`: Creates individual synthetic identities.
- `MachineLearningModel`: Trains and uses a Random Forest classifier for country prediction.
- `DataValidator`: Ensures the validity of generated data.
- `IdentityEncryptor`: Handles encryption and decryption of identity information.
- `IdentityAnalyzer`: Provides statistical analysis of generated identities.
- `IdentityExporter` and `IdentityImporter`: Handle data import/export in various formats.

## Data Security

The system implements robust security measures:
- All generated identities can be encrypted using the Fernet symmetric encryption scheme.
- Encrypted data can only be decrypted using the system's encryption key.
- The system does not store or transmit real personal data.

## Contributing

Contributions to Identity Alchemist are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

Identity Alchemist is designed for legitimate testing, development, and research purposes only. Users are responsible for ensuring that their use of this tool complies with all applicable laws and regulations. The creators and contributors of this project are not responsible for any misuse or illegal application of this system.

---

For any questions or support, please open an issue on the GitHub repository.
