# AI Classification Standard (AICS)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/aics/badge/?version=latest)](https://4hum-ai.github.io/aics/)
[![Contributors](https://img.shields.io/github/contributors/4hum-ai/aics)](https://github.com/4hum-ai/aics/graphs/contributors)
[![Issues](https://img.shields.io/badge/github-issues-blue)](https://github.com/4hum-ai/aics/issues)

A comprehensive framework for classifying and evaluating artificial intelligence systems. AICS provides a structured approach to understanding the AI industry landscape, helping organizations navigate the complex world of artificial intelligence.

## 🌟 Features

- **Comprehensive Taxonomy**: Detailed classification of AI sectors and subsectors
- **Company Registry**: Curated database of Notable AI companies and their classifications
- **Open Standard**: Free to use and contribute to
- **Regular Updates**: Continuously evolving with the AI industry

## 📚 Framework Overview

AICS is built upon the OECD's AI framework while extending it with industry-specific classifications. Our taxonomy is organized into four main sectors:

1. **AI Infrastructure (INF)**: Core technologies enabling AI development
2. **AI Models & Platforms (MOD)**: Foundation models and deployment platforms
3. **AI Applications & Services (APP)**: End-user solutions across industries
4. **AI Governance & Ethics (GOV)**: Responsible AI development and deployment

For detailed information about our taxonomy and methodology, visit our [documentation](https://4hum-ai.github.io/aics/).

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Report Issues
Found a bug or have a suggestion? [Create an issue](https://github.com/4hum-ai/aics/issues) to let us know.

### Add Companies
To add a company to the registry:
1. Fork the repository
2. Create a new YAML file in the `registry` directory
3. Follow the [company template](registry/template.yaml)
4. Submit a pull request

### Improve Taxonomy
To suggest taxonomy improvements:
1. Fork the repository
2. Edit the [taxonomy file](taxonomy/versions/v1.0.yaml)
3. Submit a pull request with your changes

### Enhance Documentation
To improve documentation:
1. Fork the repository
2. Make your changes in the `docs` directory
3. Submit a pull request

### Generate Documentation
To generate documentation:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the script to generate documentation from folders
python tools/generate_docs.py

# Run the documentation server
mkdocs serve
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- This project builds upon the [OECD's AI framework](https://www.oecd.org/going-digital/ai/principles/), adapting and extending it for industry-specific classification needs.
- We thank all contributors who have helped shape and improve this standard.